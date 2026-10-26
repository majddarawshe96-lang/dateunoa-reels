"""Render @masculinepack X-style quote cards and reels.

card(quote, w, h) -> PIL image (dark navy, wolf avatar, "Masculine Pack" + "@masculinepack", white text)
reel(quote, track, out_mp4): 1080x1920 reel with a slow push-in and the music baked in.
Reel length grows with the quote so it can be read: 8-13 s.
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = "/usr/share/fonts/opentype/inter/"
BOLD = ImageFont.truetype(FONT_DIR + "Inter-Bold.otf", 42)
HANDLE = ImageFont.truetype(FONT_DIR + "Inter-Regular.otf", 36)
BODY = ImageFont.truetype(FONT_DIR + "Inter-Regular.otf", 54)
BG = (12, 21, 36)          # dark navy, like the niche's "X dim mode" screenshots
WHITE = (236, 238, 240)
GREY = (125, 136, 150)
MARGIN = 92
AVATAR = 112
NAME, HANDLE_TXT = "Masculine Pack", "@masculinepack"


def wrap(d, text, font, width):
    lines = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            test = (line + " " + w).strip()
            if d.textlength(test, font=font) <= width:
                line = test
            else:
                lines.append(line)
                line = w
        lines.append(line)
    return lines


def circle(path, size):
    im = Image.open(path).convert("RGB")
    big = size * 4
    im = im.resize((big, big), Image.LANCZOS)
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, big, big), fill=255)
    im.putalpha(mask)
    return im.resize((size, size), Image.LANCZOS)


AV = circle(HERE / "avatar.png", AVATAR)


def card(quote, w, h):
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    lines = wrap(d, quote, BODY, w - 2 * MARGIN)
    line_h, blank_h = 74, 40
    body_h = sum(blank_h if not ln else line_h for ln in lines)
    block_h = AVATAR + 52 + body_h
    y = (h - block_h) // 2
    img.paste(AV, (MARGIN, y), AV)
    tx = MARGIN + AVATAR + 28
    d.text((tx, y + 14), NAME, font=BOLD, fill=WHITE)
    d.text((tx, y + 66), HANDLE_TXT, font=HANDLE, fill=GREY)
    ty = y + AVATAR + 52
    for ln in lines:
        if not ln:
            ty += blank_h
            continue
        d.text((MARGIN, ty), ln, font=BODY, fill=WHITE)
        ty += line_h
    return img


def duration(quote):
    return max(8.0, min(13.0, 4.5 + 0.28 * len(quote.split())))


def reel(quote, track, out_mp4, frame_png):
    card(quote, 1080, 1920).save(frame_png)
    dur = duration(quote)
    frames = int(dur * 30)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(frame_png),
        "-i", str(track), "-t", f"{dur:.2f}",
        "-vf", f"scale=2160:3840,zoompan=z='1+0.00016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30,fade=t=in:st=0:d=0.3,format=yuv420p",
        "-af", f"afade=t=in:d=0.2,afade=t=out:st={dur - 1:.2f}:d=1",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(out_mp4),
    ], check=True)
    return dur
