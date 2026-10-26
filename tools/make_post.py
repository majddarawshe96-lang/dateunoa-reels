"""Generate X-style quote posts for @dateunoa.

Usage: python3 make_post.py [--music DIR] [--start K] <avatar> <out_dir> <name> "<quote 1>" "<quote 2>" ...
Makes, per quote: post_N.png (1080x1350 feed post) and reel_N.mp4 (1080x1920, 8s).
--tracks a.m4a,b.m4a,...: one music file per quote (mood-matched, chosen by tools/render_day.py).
--music DIR: mix an original music bed from DIR/music_XX.m4a (rotates through the tracks,
             starting at track K) and add a slow push-in so the reel has motion.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/opentype/inter/"
BOLD = ImageFont.truetype(FONT_DIR + "Inter-Bold.otf", 40)
HANDLE = ImageFont.truetype(FONT_DIR + "Inter-Regular.otf", 36)
BODY = ImageFont.truetype(FONT_DIR + "Inter-Regular.otf", 56)

BG = (0, 0, 0)
WHITE = (231, 233, 234)
GREY = (113, 118, 123)
MARGIN = 90
AVATAR = 110


def wrap(draw, text, font, width):
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            test = (line + " " + w).strip()
            if draw.textlength(test, font=font) <= width:
                line = test
            else:
                lines.append(line)
                line = w
        lines.append(line)
    return lines


def circle(avatar_path, size):
    im = Image.open(avatar_path).convert("RGB")
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2,
                  (im.width + s) // 2, (im.height + s) // 2))
    big = size * 4
    im = im.resize((big, big), Image.LANCZOS)
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big, big), fill=255)
    im.putalpha(mask)
    return im.resize((size, size), Image.LANCZOS)


def card(avatar, name, handle, quote, w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    lines = wrap(d, quote, BODY, w - 2 * MARGIN)
    line_h = 76
    block_h = AVATAR + 50 + len(lines) * line_h
    y = (h - block_h) // 2

    img.paste(avatar, (MARGIN, y), avatar)
    tx = MARGIN + AVATAR + 28
    d.text((tx, y + 14), name, font=BOLD, fill=WHITE)
    d.text((tx, y + 64), handle, font=HANDLE, fill=GREY)

    ty = y + AVATAR + 50
    for ln in lines:
        d.text((MARGIN, ty), ln, font=BODY, fill=WHITE)
        ty += line_h
    return img


def main():
    args = sys.argv[1:]
    music_dir, start, explicit = None, 0, None
    while args and args[0].startswith("--"):
        flag = args.pop(0)
        if flag == "--music":
            music_dir = Path(args.pop(0))
        elif flag == "--start":
            start = int(args.pop(0))
        elif flag == "--tracks":  # one music file per quote, comma-separated (from tools/render_day.py)
            explicit = [Path(x) for x in args.pop(0).split(",")]
    avatar_path, out_dir, name, *quotes = args
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    avatar = circle(avatar_path, AVATAR)
    tracks = sorted(music_dir.glob("music_*.m4a")) if music_dir else []
    for i, q in enumerate(quotes, 1):
        card(avatar, name, "@dateunoa", q, 1080, 1350).save(out / f"post_{i}.png")
        frame = out / f"reel_{i}.png"
        card(avatar, name, "@dateunoa", q, 1080, 1920).save(frame)
        if explicit or tracks:
            track = explicit[i - 1] if explicit else tracks[(start + i - 1) % len(tracks)]
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(frame),
                "-i", str(track), "-t", "8",
                "-vf", "scale=2160:3840,zoompan=z='1+0.00018*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=240:s=1080x1920:fps=30,fade=t=in:st=0:d=0.4,format=yuv420p",
                "-af", "afade=t=in:d=0.5,afade=t=out:st=7:d=1",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
                str(out / f"reel_{i}.mp4"),
            ], check=True)
        else:
            subprocess.run([
                "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(frame),
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                "-t", "8", "-vf", "fade=t=in:st=0:d=0.4,format=yuv420p", "-r", "30",
                "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-c:a", "aac", "-shortest", "-movflags", "+faststart",
                str(out / f"reel_{i}.mp4"),
            ], check=True)


if __name__ == "__main__":
    main()
