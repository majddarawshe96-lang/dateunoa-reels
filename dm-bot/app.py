"""dateunoa comment-to-DM bot.

Someone comments a story reel's keyword (e.g. "TEXT") on Instagram (or the Facebook page);
Meta sends a webhook here; the bot finds that keyword's DM in the episode index
(content/stories/dm_index.json in the public dateunoa-reels repo, updated automatically every
time a new episode is made) and sends it as a private reply, plus a short public reply under
the comment.

Environment (set as Replit Secrets):
  VERIFY_TOKEN        any random string; the same value goes in the Meta webhook settings
  APP_SECRET          the Meta app secret (to verify webhook signatures)
  IG_ACCESS_TOKEN     Instagram user access token (Business Login for Instagram, long-lived)
  IG_USER_ID          optional; your Instagram professional account id (used to ignore your own comments)
  FB_PAGE_ID, FB_PAGE_TOKEN   optional; enables the same on the Facebook page
  DM_INDEX_URL        optional; defaults to the repo's dm_index.json on GitHub
  GRAPH_VERSION       optional; default v23.0
  ADMIN_KEY           optional; protects /status
  DRY_RUN=1           optional; log what would be sent without sending
"""
import hashlib
import hmac
import json
import logging
import os
import random
import re
import threading
import time

import requests
from flask import Flask, abort, jsonify, request

log = logging.getLogger("dm-bot")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DM_INDEX_URL = os.environ.get(
    "DM_INDEX_URL",
    "https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/content/stories/dm_index.json")
GRAPH_VERSION = os.environ.get("GRAPH_VERSION", "v23.0")
STATE_FILE = os.environ.get("STATE_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json"))
PUBLIC_REPLIES = ["Sent! Check your DMs 🤍", "Just sent it to your DMs 🤍", "Check your inbox 💌",
                  "Sent 🤍 check your messages", "It's in your DMs now 🤍"]
INDEX_TTL = 300  # seconds

app = Flask(__name__)
_lock = threading.Lock()
_index = {"data": {}, "at": 0.0}


# ------------------------------------------------------------------ state (tokens, sent ids, counters)
def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(st):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f)
    os.replace(tmp, STATE_FILE)


def ig_token():
    return load_state().get("ig_token") or os.environ.get("IG_ACCESS_TOKEN", "")


def already_handled(comment_id):
    """Mark a comment as handled; returns True if it was handled before (Meta can retry webhooks)."""
    with _lock:
        st = load_state()
        done = st.setdefault("handled", [])
        if comment_id in done:
            return True
        done.append(comment_id)
        st["handled"] = done[-5000:]
        save_state(st)
        return False


def bump(key):
    with _lock:
        st = load_state()
        c = st.setdefault("counts", {})
        c[key] = c.get(key, 0) + 1
        save_state(st)


# ------------------------------------------------------------------ the DM index
def dm_index(force=False):
    """{"TEXT": {"dm": "...", "episode": "ep02"}, ...} fetched from GitHub, cached for 5 minutes."""
    if force or time.time() - _index["at"] > INDEX_TTL:
        try:
            r = requests.get(DM_INDEX_URL, timeout=10)
            r.raise_for_status()
            data = r.json()
            _index["data"] = {k.upper(): v for k, v in data.get("keywords", {}).items()}
            _index["at"] = time.time()
        except Exception as e:  # keep serving the last good copy
            log.warning("could not refresh dm index: %s", e)
    return _index["data"]


def match_keyword(text, index):
    """The keyword must appear as its own word (any case): 'TEXT', 'text pls', 'Text!' match; 'context' doesn't."""
    if not text:
        return None
    words = set(re.findall(r"[A-Za-z0-9]+", text.upper()))
    for kw in index:
        if kw in words:
            return kw
    return None


# ------------------------------------------------------------------ Graph API calls
def graph_post(host, path, token, payload):
    if os.environ.get("DRY_RUN") == "1":
        log.info("DRY_RUN %s%s %s", host, path, json.dumps(payload)[:300])
        return {"dry_run": True}
    r = requests.post(f"https://{host}/{GRAPH_VERSION}/{path}", json=payload,
                      headers={"Authorization": f"Bearer {token}"}, timeout=15)
    if r.status_code >= 400:
        raise RuntimeError(f"{r.status_code} {r.text[:300]}")
    return r.json()


def send_instagram(comment_id, dm_text):
    tok = ig_token()
    graph_post("graph.instagram.com", "me/messages", tok,
               {"recipient": {"comment_id": comment_id}, "message": {"text": dm_text}})
    try:
        graph_post("graph.instagram.com", f"{comment_id}/replies", tok, {"message": random.choice(PUBLIC_REPLIES)})
    except Exception as e:  # the DM is what matters
        log.warning("public reply failed for %s: %s", comment_id, e)


def send_facebook(comment_id, dm_text):
    page, tok = os.environ.get("FB_PAGE_ID"), os.environ.get("FB_PAGE_TOKEN")
    if not (page and tok):
        return
    graph_post("graph.facebook.com", f"{page}/messages", tok,
               {"recipient": {"comment_id": comment_id}, "message": {"text": dm_text}})
    try:
        graph_post("graph.facebook.com", f"{comment_id}/comments", tok, {"message": random.choice(PUBLIC_REPLIES)})
    except Exception as e:
        log.warning("public reply failed for %s: %s", comment_id, e)


# ------------------------------------------------------------------ webhook handling
def comments_from(payload):
    """Yield (network, comment_id, text, author_id, owner_id) for every new comment in a webhook payload."""
    obj = payload.get("object")
    for entry in payload.get("entry", []):
        owner = str(entry.get("id", ""))
        for ch in entry.get("changes", []):
            v = ch.get("value", {})
            if obj == "instagram" and ch.get("field") == "comments":
                if v.get("parent_id"):  # replies to comments (including our own public replies)
                    continue
                yield "instagram", v.get("id"), v.get("text", ""), str(v.get("from", {}).get("id", "")), owner
            elif obj == "page" and ch.get("field") == "feed" and v.get("item") == "comment" and v.get("verb") == "add":
                if v.get("parent_id") and v.get("parent_id") != v.get("post_id"):
                    continue
                yield "facebook", v.get("comment_id"), v.get("message", ""), str(v.get("from", {}).get("id", "")), owner


def handle(payload):
    index = dm_index()
    own = {os.environ.get("IG_USER_ID", ""), os.environ.get("FB_PAGE_ID", "")} - {""}
    for net, cid, text, author, owner in comments_from(payload):
        if not cid or author in own or author == owner:
            continue
        kw = match_keyword(text, index)
        if not kw:
            continue
        if already_handled(cid):
            continue
        try:
            (send_instagram if net == "instagram" else send_facebook)(cid, index[kw]["dm"])
            bump(f"{net}:{kw}")
            log.info("sent %s DM for %s to comment %s", net, kw, cid)
        except Exception as e:
            bump(f"error:{net}")
            log.error("failed %s DM for %s (comment %s): %s", net, kw, cid, e)


def valid_signature(raw, header):
    secret = os.environ.get("APP_SECRET", "")
    if not secret:
        return False
    expected = "sha256=" + hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header or "")


@app.get("/webhook")
def verify():
    if (request.args.get("hub.mode") == "subscribe"
            and request.args.get("hub.verify_token") == os.environ.get("VERIFY_TOKEN")):
        return request.args.get("hub.challenge", ""), 200
    abort(403)


@app.post("/webhook")
def webhook():
    raw = request.get_data()
    if not valid_signature(raw, request.headers.get("X-Hub-Signature-256")):
        abort(401)
    payload = json.loads(raw or b"{}")
    # answer Meta immediately, do the work in the background
    threading.Thread(target=handle, args=(payload,), daemon=True).start()
    return "ok", 200


@app.get("/")
def health():
    return "dateunoa dm-bot running", 200


@app.get("/status")
def status():
    key = os.environ.get("ADMIN_KEY")
    if key and request.args.get("key") != key:
        abort(403)
    st = load_state()
    return jsonify({"keywords": sorted(dm_index(force=True)), "counts": st.get("counts", {}),
                    "token_refreshed_at": st.get("token_refreshed_at"), "dry_run": os.environ.get("DRY_RUN") == "1"})


# ------------------------------------------------------------------ keep the Instagram token alive
def refresh_token_forever():
    """Long-lived Instagram tokens last 60 days; refresh every 20 days."""
    while True:
        st = load_state()
        if time.time() - st.get("token_refreshed_at", 0) > 20 * 86400 and ig_token():
            try:
                r = requests.get("https://graph.instagram.com/refresh_access_token",
                                 params={"grant_type": "ig_refresh_token", "access_token": ig_token()}, timeout=15)
                r.raise_for_status()
                with _lock:
                    st = load_state()
                    st["ig_token"] = r.json()["access_token"]
                    st["token_refreshed_at"] = time.time()
                    save_state(st)
                log.info("instagram token refreshed")
            except Exception as e:
                log.error("token refresh failed: %s", e)
        time.sleep(6 * 3600)


if __name__ == "__main__":
    threading.Thread(target=refresh_token_forever, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
