"""@masculinepack 30-day plan: 6 reels (automatic, music baked in) + 6 carousels (Buffer reminders, owner adds IG music).

Usage: python3 masculinepack/month.py [--render-reels] [--render-slides] [--plan out/month]
Days: 2026-10-27 .. 2026-11-25. Reels at REEL_SLOTS, carousels at CAR_SLOTS (Asia/Jerusalem).
Week 1 (Oct 27 - Nov 2) already has 3 reels (09:30, 15:00, 21:15) and 1 carousel (12:30, re-created here as a reminder).
New files: reels/mp/<MMDD>/r<HHMM>.mp4, reels/mp/<MMDD>/c<HHMM>/<N>.jpg
"""
import importlib.util
import json
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from make_mp_post import reel, card  # noqa: E402
from make_carousels import slide  # noqa: E402
import run_week  # noqa: E402

TZ = ZoneInfo("Asia/Jerusalem")
CHANNEL = "6adfaee72f1f5ed648de3f9b"
RAW = "https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/"
REEL_SLOTS = ["07:30", "09:30", "12:00", "15:00", "18:15", "21:15"]
CAR_SLOTS = ["08:30", "11:00", "12:30", "14:00", "17:00", "20:00"]
START = date(2026, 10, 27)
DAYS = [START + timedelta(d) for d in range(30)]
WEEK1_END = date(2026, 11, 2)
WEEK1_PROMO_DAYS = {date(2026, 10, 28), date(2026, 10, 30), date(2026, 11, 1)}
CTA = "📌 Save this. 👥 Send it to a brother who needs it.\n📕 The Iron Code: 12 laws + the 30-Day Iron Protocol. Link in bio."
TAGS = run_week.TAGS + [
    "#masculinity #stoicmindset #selfimprovementformen #menswellness #masculinemindset",
    "#discipline #menmotivation #gymmotivation #selfdevelopment #mensadvice",
]
CTA_SLIDES = [
    "School never taught you this:\n\nDiscipline. Frame. Confidence.\nWomen. Money. Purpose.\n\nThe Iron Code puts it all in one place: 12 laws and a 30-day protocol to make them who you are.\n\nLINK IN BIO.",
    "Want the full system?\n\nThe Iron Code: 12 laws, 46 exercises and the 30-Day Iron Protocol for men who are done drifting.\n\nLINK IN BIO.",
    "If this hit you, the book will hit harder.\n\nThe Iron Code. 12 laws of discipline, frame and purpose for the modern man.\n\nLINK IN BIO.",
]


def L(f, name):
    s = importlib.util.spec_from_file_location("x", HERE / "content" / f)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return getattr(m, name)


QUOTES = L("month_reels_a.py", "QUOTES_A") + L("month_reels_b.py", "QUOTES_B") + L("month_reels_c.py", "QUOTES_C")
CARS = L("month_car_a.py", "CAR_A") + L("month_car_b.py", "CAR_B") + L("month_car_c.py", "CAR_C") + L("month_car_d.py", "CAR_D")
PROMO_TEXT = dict(L("week1.py", "PROMOS"), **L("month_reels_c.py", "PROMOS_EXTRA"))
PROMO_BODY = L("month_reels_c.py", "PROMO_BODY")
WEEK1_CARS = L("carousels_week1.py", "CAROUSELS")
# Two week-1 posts went live early (published by hand on Oct 26): refill their slots with new content.
EXTRA_CAR = ("The silent rules of a self-respecting man:", [
    "He doesn't beg for time, attention or loyalty.",
    "He leaves the table when respect is no longer served.",
    "He keeps his problems private and his goals quiet.",
    "He never argues with people committed to misunderstanding him.",
    "He treats his body like it's the only one he'll get.",
    "He keeps his word, even when nobody would know.",
], "No speeches. No announcements. Just a standard he lives by every day. Which rule do you already live by?")
EXTRA_QUOTE = ("A man who knows his worth\ndoesn't need to argue\nabout it.", "stoic",
    "When you know who you are, other people's opinions turn into background noise. Stay calm. Stay building.")


def dd(d):
    return d.strftime("%m%d")


def due(d, hhmm):
    return datetime.fromisoformat(f"{d.isoformat()}T{hhmm}:00").replace(tzinfo=TZ).isoformat()


def schedule():
    """Every new post in time order: dicts with kind reel/promo/car/car_w1."""
    qi = ci = 0
    promo_cycle = ["p4", "p5", "p6", "p1", "p2", "p3"]
    pi = 0
    posts = []
    for d in DAYS:
        week1 = d <= WEEK1_END
        free_r = ["07:30", "12:00", "18:15"] if week1 else REEL_SLOTS
        if d == date(2026, 10, 29):
            q, mood, body = EXTRA_QUOTE
            posts.append({"kind": "reel", "day": d, "slot": "09:30", "quote": q, "mood": mood, "body": body})
        for hhmm in free_r:
            if hhmm == "12:00" and (not week1 or d not in WEEK1_PROMO_DAYS):
                pid = promo_cycle[pi % len(promo_cycle)]
                pi += 1
                posts.append({"kind": "promo", "day": d, "slot": hhmm, "promo": pid})
            else:
                q, mood, body = QUOTES[qi]
                qi += 1
                posts.append({"kind": "reel", "day": d, "slot": hhmm, "quote": q, "mood": mood, "body": body})
        for hhmm in CAR_SLOTS:
            if d == date(2026, 10, 27) and hhmm == "12:30":
                hook, slides, body = EXTRA_CAR
                posts.append({"kind": "car", "day": d, "slot": hhmm, "hook": hook, "slides": slides, "body": body, "ci": 0})
            elif week1 and hhmm == "12:30":
                w = next(c for c in WEEK1_CARS if c[0] == d.isoformat())
                posts.append({"kind": "car_w1", "day": d, "slot": hhmm, "hook": w[1][0], "n": len(w[1]) + 1, "body": w[2]})
            else:
                hook, slides, body = CARS[ci]
                ci += 1
                posts.append({"kind": "car", "day": d, "slot": hhmm, "hook": hook, "slides": slides, "body": body, "ci": ci})
    assert qi == len(QUOTES) and ci == len(CARS), (qi, len(QUOTES), ci, len(CARS))
    assert len(posts) == 339 + 1, len(posts)
    return sorted(posts, key=lambda p: due(p["day"], p["slot"]))


def path_reel(p):
    return f"mp/{dd(p['day'])}/r{p['slot'].replace(':', '')}.mp4"


def path_car(p, k):
    return f"mp/{dd(p['day'])}/c{p['slot'].replace(':', '')}/{k}.jpg"


def render_reels(posts, only_days=None):
    counter = {}
    tmp = ROOT / "out" / "mp_frames"
    tmp.mkdir(parents=True, exist_ok=True)
    for p in posts:
        if p["kind"] != "reel":
            continue
        k = counter.get(p["mood"], 0)
        counter[p["mood"]] = k + 1
        if only_days and p["day"] not in only_days:
            continue
        out = ROOT / "reels" / path_reel(p)
        if out.exists():
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        files = sorted((HERE / "music" / p["mood"]).glob(f"{p['mood']}_*.m4a"))
        reel(p["quote"], files[(k + 2) % len(files)], out, tmp / "frame.png")
    # promo videos p4-p6
    pdir = ROOT / "reels" / "masculinepack" / "promo"
    for pid in ("p4", "p5", "p6"):
        target = pdir / f"{pid}.mp4"
        if target.exists():
            continue
        png = tmp / f"promo_{pid}.png"
        run_week.promo_frame(PROMO_TEXT[pid], png)
        track = sorted((HERE / "music" / "epic").glob("epic_*.m4a"))[int(pid[1]) % 5]
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(png), "-i", str(track), "-t", "10",
            "-vf", "scale=2160:3840,zoompan=z='1+0.00022*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=300:s=1080x1920:fps=30,fade=t=in:st=0:d=0.3,format=yuv420p",
            "-af", "afade=t=in:d=0.2,afade=t=out:st=9:d=1", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(target)], check=True)


def render_slides(posts):
    for p in posts:
        if p["kind"] != "car":
            continue
        body = p["slides"]
        if all("\n\n" not in b and not b[:2].strip(".").isdigit() for b in body):
            body = [f"{i}. {b}" for i, b in enumerate(body, 1)]
        allslides = [p["hook"]] + body + [CTA_SLIDES[p["ci"] % len(CTA_SLIDES)]]
        for k, s in enumerate(allslides, 1):
            out = ROOT / "reels" / path_car(p, k)
            if out.exists():
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            slide(s, cover=(k == len(allslides)), hook=(k == 1)).save(out, quality=92)


def post_input(p, i):
    tags = TAGS[i % len(TAGS)]
    if p["kind"] in ("reel", "promo"):
        if p["kind"] == "reel":
            url, text = RAW + path_reel(p), f"{p['body']}\n\n{CTA}\n\n{tags}"
        else:
            url, text = f"{RAW}masculinepack/promo/{p['promo']}.mp4", f"{PROMO_BODY[p['promo']]}\n\n👉 Link in bio.\n\n{tags}"
        return {"channelId": CHANNEL, "mode": "customScheduled", "dueAt": due(p["day"], p["slot"]), "schedulingType": "automatic",
                "text": text, "assets": [{"video": {"url": url}}],
                "metadata": {"instagram": {"type": "reel", "shouldShareToFeed": True}}}
    if p["kind"] == "car":
        n = len(p["slides"]) + 2
        urls = [RAW + path_car(p, k) for k in range(1, n + 1)]
    else:
        n = p["n"]
        urls = [f"{RAW}masculinepack/carousels/{p['day'].isoformat()}/slide_{k:02d}.jpg" for k in range(1, n + 1)]
    hook = p["hook"].replace("\n", " ")
    text = f"{hook} 👇 (swipe)\n\n{p['body']}\n\n{CTA}\n\n{tags}"
    return {"channelId": CHANNEL, "mode": "customScheduled", "dueAt": due(p["day"], p["slot"]), "schedulingType": "notification",
            "text": text, "assets": [{"image": {"url": u}} for u in urls],
            "metadata": {"instagram": {"type": "post", "shouldShareToFeed": True}}}


def plan(posts, outdir, size=30):
    outdir.mkdir(parents=True, exist_ok=True)
    inputs = [post_input(p, i) for i, p in enumerate(posts)]
    json.dump([{"day": p["day"].isoformat(), "slot": p["slot"], "kind": p["kind"]} for p in posts],
              open(outdir / "index.json", "w"), indent=0)
    for b in range(0, len(inputs), size):
        chunk = inputs[b:b + size]
        decl = ",".join(f"$i{i}:CreatePostInput!" for i in range(len(chunk)))
        parts = " ".join(f"p{i}:createPost(input:$i{i}){{__typename ...on MutationError{{message}}}}" for i in range(len(chunk)))
        json.dump({"mutation": f"mutation M({decl}){{{parts}}}", "variables": {f"i{i}": x for i, x in enumerate(chunk)}},
                  open(outdir / f"batch_{b // size:02d}.json", "w"), ensure_ascii=False, separators=(",", ":"))
    print(len(inputs), "posts,", (len(inputs) + size - 1) // size, "batches")


if __name__ == "__main__":
    a = sys.argv[1:]
    posts = schedule()
    print(len(posts), "new posts:", {k: sum(1 for p in posts if p["kind"] == k) for k in ("reel", "promo", "car", "car_w1")})
    if "--render-reels" in a:
        render_reels(posts)
    if "--render-slides" in a:
        render_slides(posts)
    if "--plan" in a:
        plan(posts, Path(a[a.index("--plan") + 1]))
