"""Render @masculinepack reels for a content file and build the Buffer batch.

Usage: python3 masculinepack/run_week.py masculinepack/content/week1.py [--render] [--plan out/mp]
  --render  writes reels/masculinepack/<date>/mp_0N.mp4 and reels/masculinepack/promo/<id>.mp4
  --plan D  writes D/plan.json and D/batch_NN.json (Buffer execute_mutation payloads, 21 posts max per batch)
Hosted at https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/masculinepack/...
"""
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from make_mp_post import BG, WHITE, wrap, reel  # noqa: E402
import make_mp_post  # noqa: E402

CHANNEL = "6adfaee72f1f5ed648de3f9b"  # Instagram masculinepack (Buffer)
SLOTS = ["09:30", "15:00", "21:15"]
RAW = "https://raw.githubusercontent.com/majddarawshe96-lang/dateunoa-reels/main/reels/masculinepack/"
TZ = ZoneInfo("Asia/Jerusalem")
TAGS = [
    "#masculinity #masculineenergy #selfimprovement #discipline #mindset",
    "#menmotivation #stoicism #selfmastery #menshealth #grindset",
    "#masculine #highvalueman #menscoaching #dailymotivation #selfdiscipline",
    "#mensmentalhealth #brotherhood #stoic #selfgrowth #disciplineequalsfreedom",
]
CTA = "📌 Save this. 👥 Send it to a brother who needs it.\n📕 The Iron Code: 12 laws + the 30-Day Iron Protocol. Link in bio."
GOLD = (212, 168, 75)


def load(p):
    spec = importlib.util.spec_from_file_location("content", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def promo_frame(text, out_png):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 64)
    small = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 38)
    lines = wrap(d, text, f, W - 180)
    y = 210
    for ln in lines:
        if not ln:
            y += 34
            continue
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=WHITE)
        y += 84
    cover = Image.open(HERE / "promo_cover.jpg").convert("RGB").resize((620, 930), Image.LANCZOS)
    cy = max(y + 70, 760)
    cy = min(cy, H - 930 - 230)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([(W - 620) // 2 + 20, cy + 30, (W + 620) // 2 + 20, cy + 960], fill=(0, 0, 0, 210))
    img = Image.alpha_composite(img.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(28))).convert("RGB")
    img.paste(cover, ((W - 620) // 2, cy))
    d = ImageDraw.Draw(img)
    foot = "12 LAWS  ·  30-DAY PROTOCOL  ·  LINK IN BIO"
    d.text(((W - d.textlength(foot, font=small)) / 2, cy + 930 + 70), foot, font=small, fill=GOLD)
    img.save(out_png)


def track(mood, k):
    files = sorted((HERE / "music" / mood).glob(f"{mood}_*.m4a"))
    return files[k % len(files)]


def render(m):
    out = ROOT / "out" / "masculinepack"
    out.mkdir(parents=True, exist_ok=True)
    counter = {}
    for day, posts in m.DAYS.items():
        dst = ROOT / "reels" / "masculinepack" / day
        dst.mkdir(parents=True, exist_ok=True)
        for i, (kind, q, mood, _) in enumerate(posts, 1):
            k = counter.get(mood, 0)
            counter[mood] = k + 1
            if kind == "q":
                dur = reel(q, track(mood, k), dst / f"mp_{i:02d}.mp4", out / f"{day}_{i}.png")
                make_mp_post.card(q, 1080, 1350).save(out / f"{day}_{i}_post.png")
                print(day, i, mood, f"{dur:.1f}s")
            else:
                pdir = ROOT / "reels" / "masculinepack" / "promo"
                pdir.mkdir(parents=True, exist_ok=True)
                target = pdir / f"{q}.mp4"
                if not target.exists():
                    png = out / f"promo_{q}.png"
                    promo_frame(m.PROMOS[q], png)
                    _ = make_mp_post
                    import subprocess
                    subprocess.run([
                        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(png),
                        "-i", str(track(mood, k)), "-t", "10",
                        "-vf", "scale=2160:3840,zoompan=z='1+0.00022*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=300:s=1080x1920:fps=30,fade=t=in:st=0:d=0.3,format=yuv420p",
                        "-af", "afade=t=in:d=0.2,afade=t=out:st=9:d=1",
                        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                        "-shortest", "-movflags", "+faststart", str(target)], check=True)
                print(day, i, "promo", q)


def plan(m, outdir):
    items, n = [], 0
    for day, posts in m.DAYS.items():
        for i, (kind, q, mood, body) in enumerate(posts, 1):
            url = f"{RAW}{day}/mp_{i:02d}.mp4" if kind == "q" else f"{RAW}promo/{q}.mp4"
            tail = CTA if kind == "q" else "👉 Link in bio."
            text = f"{body}\n\n{tail}\n\n{TAGS[n % len(TAGS)]}"
            due = datetime.fromisoformat(f"{day}T{SLOTS[i - 1]}:00").replace(tzinfo=TZ).isoformat()
            items.append({"day": day, "slot": SLOTS[i - 1], "dueAt": due, "video": url, "text": text})
            n += 1
    outdir.mkdir(parents=True, exist_ok=True)
    json.dump(items, open(outdir / "plan.json", "w"), ensure_ascii=False, indent=1)
    decl, parts, var = [], [], {}
    for i, x in enumerate(items):
        decl.append(f"$i{i}:CreatePostInput!")
        parts.append(f"p{i}:createPost(input:$i{i}){{__typename ...on MutationError{{message}}}}")
        var[f"i{i}"] = {"channelId": CHANNEL, "mode": "customScheduled", "dueAt": x["dueAt"], "schedulingType": "automatic",
                        "text": x["text"], "assets": [{"video": {"url": x["video"]}}],
                        "metadata": {"instagram": {"type": "reel", "shouldShareToFeed": True}}}
    json.dump({"mutation": f"mutation MP({','.join(decl)}){{{' '.join(parts)}}}", "variables": var},
              open(outdir / "batch_00.json", "w"), ensure_ascii=False)
    print(len(items), "posts planned")


if __name__ == "__main__":
    a = sys.argv[1:]
    m = load(a[0])
    if "--render" in a:
        render(m)
    if "--plan" in a:
        plan(m, Path(a[a.index("--plan") + 1]))
