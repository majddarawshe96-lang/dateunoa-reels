"""Render @masculinepack long-form carousels (X-style slides) and build the Buffer batch.

Usage: python3 masculinepack/make_carousels.py masculinepack/content/carousels_week1.py [--render] [--plan out/mpc]
  --render: reels/masculinepack/carousels/<date>/slide_NN.jpg (1080x1350 JPEG; Instagram needs JPEG)
  --plan D: D/batch.json for Buffer execute_mutation (Instagram carousel posts at 12:30)
"""
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from make_mp_post import AV, AVATAR, BG, GREY, HANDLE, BOLD, MARGIN, NAME, HANDLE_TXT, WHITE, wrap  # noqa: E402

W, H = 1080, 1350
CHANNEL = "6adfaee72f1f5ed648de3f9b"
RAW = "https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/masculinepack/carousels/"
TZ = ZoneInfo("Asia/Jerusalem")
SLOT = "12:30"
TAGS = ["#masculinity #masculineenergy #selfimprovement #discipline #mensadvice",
        "#stoicism #selfmastery #menmotivation #mindset #highvalueman",
        "#datingadviceformen #masculineframe #selfrespect #brotherhood #growth"]
FONT = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
HOOKFONT = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
GOLD = (212, 168, 75)


def wrap_no_orphans(d, text, font, width):
    out = []
    for para in text.split("\n"):
        ls = wrap(d, para, font, width) if para else [""]
        if len(ls) > 1 and len(ls[-1].split()) == 1 and len(ls[-2].split()) > 2:
            prev = ls[-2].split()
            ls[-2], ls[-1] = " ".join(prev[:-1]), prev[-1] + " " + ls[-1]
        out += ls
    return out


def slide(text, cover=False, hook=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    width = W - 2 * MARGIN
    sizes = (66, 60, 54) if hook else ((62, 56, 50) if len(text) < 70 and "\n\n" not in text else (54, 50, 46, 42))
    for size in sizes:  # shrink long slides to fit
        font = ImageFont.truetype(HOOKFONT if hook else FONT, size)
        lines = wrap_no_orphans(d, text, font, width)
        lh, bh = int(size * 1.38), int(size * 0.72)
        body_h = sum(bh if not ln else lh for ln in lines)
        extra = 330 if cover else 0
        if AVATAR + 52 + body_h + extra < H - 200:
            break
    block = AVATAR + 52 + body_h + extra
    y = (H - block) // 2
    img.paste(AV, (MARGIN, y), AV)
    tx = MARGIN + AVATAR + 28
    d.text((tx, y + 14), NAME, font=BOLD, fill=WHITE)
    d.text((tx, y + 66), HANDLE_TXT, font=HANDLE, fill=GREY)
    ty = y + AVATAR + 52
    for ln in lines:
        if not ln:
            ty += bh
            continue
        d.text((MARGIN, ty), ln, font=font, fill=GOLD if (cover and ln.isupper()) else WHITE)
        ty += lh
    if cover:
        c = Image.open(HERE / "promo_cover.jpg").convert("RGB").resize((200, 300), Image.LANCZOS)
        img.paste(c, (MARGIN, ty + 20))
    return img


def load(p):
    spec = importlib.util.spec_from_file_location("c", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def render(m):
    for day, slides, _ in m.CAROUSELS:
        out = ROOT / "reels" / "masculinepack" / "carousels" / day
        out.mkdir(parents=True, exist_ok=True)
        allslides = slides + [m.CTA_SLIDE]
        for k, s in enumerate(allslides, 1):
            slide(s, cover=(k == len(allslides)), hook=(k == 1)).save(out / f"slide_{k:02d}.jpg", quality=93)
        print(day, len(allslides), "slides")


def plan(m, outdir):
    decl, parts, var = [], [], {}
    for i, (day, slides, body) in enumerate(m.CAROUSELS):
        n = len(slides) + 1
        hook = slides[0].replace("\n", " ")
        text = (f"{hook} 👇 (swipe)\n\n{body}\n\n📌 Save this. 👥 Send it to a brother who needs it.\n"
                f"📕 The Iron Code: 12 laws + the 30-Day Iron Protocol. Link in bio.\n\n{TAGS[i % len(TAGS)]}")
        assets = [{"image": {"url": f"{RAW}{day}/slide_{k:02d}.jpg",
                             "metadata": {"altText": (slides + [m.CTA_SLIDE])[k - 1].replace("\n", " ")[:250]}}}
                  for k in range(1, n + 1)]
        due = datetime.fromisoformat(f"{day}T{SLOT}:00").replace(tzinfo=TZ).isoformat()
        decl.append(f"$i{i}:CreatePostInput!")
        parts.append(f"p{i}:createPost(input:$i{i}){{__typename ...on MutationError{{message}}}}")
        var[f"i{i}"] = {"channelId": CHANNEL, "mode": "customScheduled", "dueAt": due, "schedulingType": "automatic",
                        "text": text, "assets": assets, "metadata": {"instagram": {"type": "post", "shouldShareToFeed": True}}}
    outdir.mkdir(parents=True, exist_ok=True)
    json.dump({"mutation": f"mutation MPC({','.join(decl)}){{{' '.join(parts)}}}", "variables": var},
              open(outdir / "batch.json", "w"), ensure_ascii=False)
    print(len(var), "carousels planned")


if __name__ == "__main__":
    a = sys.argv[1:]
    m = load(a[0])
    if "--render" in a:
        render(m)
    if "--plan" in a:
        plan(m, Path(a[a.index("--plan") + 1]))
