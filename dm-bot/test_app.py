"""Tests for the dm-bot. Run: cd dm-bot && python -m pytest -q"""
import hashlib
import hmac
import json
import os
import tempfile

import pytest

os.environ["STATE_FILE"] = tempfile.mktemp(suffix=".json")
os.environ["APP_SECRET"] = "secret"
os.environ["VERIFY_TOKEN"] = "verify-me"
os.environ["IG_ACCESS_TOKEN"] = "tok"
os.environ["IG_USER_ID"] = "999"
os.environ["FB_PAGE_ID"] = "555"
os.environ["FB_PAGE_TOKEN"] = "ptok"

import app as bot  # noqa: E402

INDEX = {"TEXT": {"dm": "Here's what she sent", "episode": "ep02"}, "ASK": {"dm": "His exact words", "episode": "ep04"}}


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    if os.path.exists(os.environ["STATE_FILE"]):
        os.remove(os.environ["STATE_FILE"])
    monkeypatch.setattr(bot, "dm_index", lambda force=False: INDEX)
    sent = []
    monkeypatch.setattr(bot, "graph_post", lambda host, path, tok, payload: sent.append((host, path, tok, payload)) or {})
    return sent


def ig_payload(cid, text, author="123", parent=None):
    v = {"id": cid, "text": text, "from": {"id": author, "username": "someone"}, "media": {"id": "m1"}}
    if parent:
        v["parent_id"] = parent
    return {"object": "instagram", "entry": [{"id": "999", "changes": [{"field": "comments", "value": v}]}]}


def fb_payload(cid, text, author="321"):
    v = {"item": "comment", "verb": "add", "comment_id": cid, "post_id": "555_1", "parent_id": "555_1",
         "message": text, "from": {"id": author}}
    return {"object": "page", "entry": [{"id": "555", "changes": [{"field": "feed", "value": v}]}]}


@pytest.mark.parametrize("text,kw", [("TEXT", "TEXT"), ("text pls 🙏", "TEXT"), ("Text!", "TEXT"), ("ask", "ASK"),
                                     ("context matters", None), ("wow", None), ("", None)])
def test_match_keyword(text, kw):
    assert bot.match_keyword(text, INDEX) == kw


def test_instagram_comment_gets_dm_and_public_reply(setup):
    bot.handle(ig_payload("c1", "TEXT"))
    assert setup[0] == ("graph.instagram.com", "me/messages", "tok",
                        {"recipient": {"comment_id": "c1"}, "message": {"text": "Here's what she sent"}})
    assert setup[1][1] == "c1/replies"


def test_same_comment_only_once(setup):
    bot.handle(ig_payload("c2", "text"))
    bot.handle(ig_payload("c2", "text"))
    assert sum(1 for s in setup if s[1] == "me/messages") == 1


def test_ignores_own_comments_replies_and_other_words(setup):
    bot.handle(ig_payload("c3", "TEXT", author="999"))
    bot.handle(ig_payload("c4", "TEXT", parent="c1"))
    bot.handle(ig_payload("c5", "love this"))
    assert setup == []


def test_facebook_comment(setup):
    bot.handle(fb_payload("fc1", "ASK"))
    assert setup[0] == ("graph.facebook.com", "555/messages", "ptok",
                        {"recipient": {"comment_id": "fc1"}, "message": {"text": "His exact words"}})


def test_webhook_signature_and_verify():
    c = bot.app.test_client()
    assert c.get("/webhook?hub.mode=subscribe&hub.verify_token=verify-me&hub.challenge=42").data == b"42"
    assert c.get("/webhook?hub.mode=subscribe&hub.verify_token=wrong&hub.challenge=42").status_code == 403
    body = json.dumps({"object": "instagram", "entry": []}).encode()
    assert c.post("/webhook", data=body).status_code == 401
    sig = "sha256=" + hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert c.post("/webhook", data=body, headers={"X-Hub-Signature-256": sig}).status_code == 200
