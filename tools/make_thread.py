"""Render @dateunoa "thread" carousels (each slide = one X-post screenshot) and plan their Buffer posts.

Usage: python3 tools/make_thread.py content/threads/<YYYY-MM-DD>.py [--render] [--plan out/threads]
  content file: THREADS = {"<date>": [ {"pillar": "M", "hook": "...", "slides": ["...", ...]}, ... (2 per day) ]}
  --render: reels/threads/<date>/t<N>_<KK>.jpg (1080x1350 JPEG; Instagram carousels need JPEG).
            A last CTA slide (the 3 ebooks) is added to every thread automatically.
  --plan D: D/<date>.json = list of posts (Instagram + Facebook) ready for Buffer create_post.
Slots: thread 1 at 10:30, thread 2 at 19:30 (between the reel slots).
"""
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from captions import BOOK, COLLECTION, CTA, LONG, TAGS  # noqa: E402
from make_post import circle, wrap  # noqa: E402

W, H = 1080, 1350
FD = "/usr/share/fonts/opentype/inter/"
BOLD = ImageFont.truetype(FD + "Inter-Bold.otf", 40)
SMALL = ImageFont.truetype(FD + "Inter-Regular.otf", 36)
BG, WHITE, GREY, LINE = (0, 0, 0), (231, 233, 234), (113, 118, 123), (47, 51, 54)
MARGIN, AVATAR = 90, 110
AV = circle(ROOT / "tools" / "avatar.jpg", AVATAR)
SLOTS = ["10:30", "19:30"]
TZ = ZoneInfo("Asia/Jerusalem")
RAW = "https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/threads/"
CH = {"instagram": "6ac7b0a16a5c39ccb651ff2c", "facebook": "6ada5f7b778b240e2f9111b7"}
CTA_SLIDE = ("If this thread felt personal:\n\n3 short dating ebooks\n"
             "• What Do I Text Back?\n• What Do Men Want?\n• What Do Women Want?\n\nAll 3 at the link in our profile.")


def lines_for(d, text, font, width):
    out = []
    for para in text.split("\n"):
        ls = wrap(d, para, font, width) if para else [""]
        if len(ls) > 1 and len(ls[-1].split()) == 1 and len(ls[-2].split()) > 2:  # no orphan words
            prev = ls[-2].split()
            ls[-2], ls[-1] = " ".join(prev[:-1]), prev[-1] + " " + ls[-1]
        out += ls
    return out


def slide(text, k, n, first=False):  # noqa: C901
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    width = W - 2 * MARGIN
    sizes = (68, 62, 56) if first else (60, 56, 52, 48, 44)
    for size in sizes:  # shrink long slides until they fit
        font = ImageFont.truetype(FD + ("Inter-SemiBold.otf" if first else "Inter-Regular.otf"), size)
        lines = lines_for(d, text, font, width)
        lh, bh = int(size * 1.36), int(size * 0.7)
        body_h = sum(bh if not ln else lh for ln in lines)
        if AVATAR + 52 + body_h < H - 260:
            break
    y = (H - (AVATAR + 52 + body_h)) // 2
    if k > 1:  # thread connector from the previous post
        d.line((MARGIN + AVATAR // 2, 0, MARGIN + AVATAR // 2, y - 14), fill=LINE, width=4)
    img.paste(AV, (MARGIN, y), AV)
    tx = MARGIN + AVATAR + 28
    d.text((tx, y + 14), "dateunoa", font=BOLD, fill=WHITE)
    d.text((tx, y + 64), "@dateunoa", font=SMALL, fill=GREY)
    cnt = f"{k}/{n}"
    d.text((W - MARGIN - d.textlength(cnt, font=SMALL), y + 36), cnt, font=SMALL, fill=GREY)
    ty = y + AVATAR + 52
    for ln in lines:
        if not ln:
            ty += bh
            continue
        d.text((MARGIN, ty), ln, font=font, fill=WHITE)
        ty += lh
    if first:
        d.text((MARGIN, ty + 30), "Swipe for the thread  →", font=SMALL, fill=GREY)
    return img


def load(p):
    spec = importlib.util.spec_from_file_location("c", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def render(m):
    for day, threads in m.THREADS.items():
        out = ROOT / "reels" / "threads" / day
        out.mkdir(parents=True, exist_ok=True)
        for t, th in enumerate(threads, 1):
            sl = th["slides"] + [CTA_SLIDE]
            for k, s in enumerate(sl, 1):
                slide(s, k, len(sl), first=(k == 1)).save(out / f"t{t}_{k:02d}.jpg", quality=92)
            print(day, f"thread {t}:", len(sl), "slides")


def caption(th, net, n):
    book = BOOK[th["pillar"]]
    tags = TAGS[book][n % len(TAGS[book])]
    tags = tags if net == "instagram" else tags[:3]
    lead = th["hook"] if book == "ALL" else f"{th['hook']}\n\n{LONG[book]}"
    return f"{lead}\n\n{COLLECTION}\n\n{CTA[net]}\n\n{' '.join(tags)}"


def plan(m, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    for day, threads in m.THREADS.items():
        posts = []
        for t, th in enumerate(threads, 1):
            sl = th["slides"] + [CTA_SLIDE]
            assets = [{"image": {"url": f"{RAW}{day}/t{t}_{k:02d}.jpg",
                                 "metadata": {"altText": s.replace("\n", " ")[:250]}}} for k, s in enumerate(sl, 1)]
            due = datetime.fromisoformat(f"{day}T{SLOTS[t - 1]}:00").replace(tzinfo=TZ).isoformat()
            for net in ("instagram", "facebook"):
                meta = ({"instagram": {"type": "post", "shouldShareToFeed": True}} if net == "instagram"
                        else {"facebook": {"type": "post"}})
                posts.append({"channelId": CH[net], "net": net, "mode": "customScheduled", "dueAt": due,
                              "schedulingType": "automatic", "text": caption(th, net, t), "assets": assets,
                              "metadata": meta})
        json.dump(posts, open(outdir / f"{day}.json", "w"), ensure_ascii=False, indent=1)
        print(day, len(posts), "posts planned")


if __name__ == "__main__":
    a = sys.argv[1:]
    mod = load(a[0])
    if "--render" in a:
        render(mod)
    if "--plan" in a:
        plan(mod, Path(a[a.index("--plan") + 1]))
