"""Promo reels for the dateunoa Collection (book covers / inside pages + offer).

Usage: python3 tools/make_promo.py <out_dir>
Writes promo_<name>.mp4 (1080x1920, 9 s, slow push-in, original music) for every entry in PROMOS.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
A = HERE / "promo_assets"
MUSIC = HERE / "music"
INTER = "/usr/share/fonts/opentype/inter/"
LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
LORA_I = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
GOLD = (226, 196, 135)
GOLD_D = (176, 141, 76)
IVORY = (243, 234, 214)
W, H = 1080, 1920


def font(path, size):
    return ImageFont.truetype(path, size)


def bg():
    im = Image.new("RGB", (W, H), (8, 7, 5))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse((-200, 300, W + 200, 1500), fill=(48, 38, 22))
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    return Image.blend(im, glow, 0.9)


def centered(d, y, text, f, fill, spacing=10):
    for line in text.split("\n"):
        w = d.textlength(line, font=f)
        d.text(((W - w) / 2, y), line, font=f, fill=fill)
        y += f.size + spacing
    return y


def tracked(d, y, text, f, fill, track=6):
    total = sum(d.textlength(c, font=f) + track for c in text) - track
    x = (W - total) / 2
    for c in text:
        d.text((x, y), c, font=f, fill=fill)
        x += d.textlength(c, font=f) + track
    return y + f.size


def shadowed(base, img, xy, radius=28):
    sh = Image.new("RGBA", (img.width + 120, img.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((60, 70, 60 + img.width, 70 + img.height), fill=(0, 0, 0, 200))
    sh = sh.filter(ImageFilter.GaussianBlur(radius))
    base.paste(sh, (xy[0] - 60, xy[1] - 60), sh)
    base.paste(img, xy)
    ImageDraw.Draw(base).rectangle((xy[0] - 1, xy[1] - 1, xy[0] + img.width, xy[1] + img.height), outline=GOLD_D, width=2)


def cta(d, y, price, sub):
    y = centered(d, y, price, font(LORA, 64), IVORY)
    y = centered(d, y + 6, sub, font(LORA_I, 36), (205, 187, 149))
    bw, bh = 520, 92
    x0 = (W - bw) // 2
    d.rounded_rectangle((x0, y + 34, x0 + bw, y + 34 + bh), radius=46, fill=GOLD)
    f = font(INTER + "Inter-SemiBold.otf", 30)
    t = "LINK IN BIO"
    tracked(d, y + 34 + (bh - 30) // 2 - 4, t, f, (12, 10, 7), 5)


def cover_promo(cover, kicker, bullets, price, sub):
    im = bg()
    d = ImageDraw.Draw(im)
    tracked(d, 120, kicker, font(INTER + "Inter-Medium.otf", 30), GOLD, 7)
    c = Image.open(A / cover).convert("RGB")
    cw = 640
    c = c.resize((cw, int(c.height * cw / c.width)), Image.LANCZOS)
    shadowed(im, c, ((W - cw) // 2, 210))
    y = 210 + c.height + 70
    for b in bullets:
        y = centered(d, y, "✦  " + b if False else b, font(LORA, 40), IVORY, 8) + 6
    cta(d, y + 30, price, sub)
    return im


def page_promo(page, title, line, price, sub):
    im = bg()
    d = ImageDraw.Draw(im)
    tracked(d, 120, "INSIDE THE BOOK", font(INTER + "Inter-Medium.otf", 30), GOLD, 7)
    centered(d, 180, title, font(LORA, 58), IVORY)
    p = Image.open(A / page).convert("RGB")
    pw = 700
    p = p.resize((pw, int(p.height * pw / p.width)), Image.LANCZOS)
    shadowed(im, p, ((W - pw) // 2, 360))
    y = 360 + p.height + 50
    y = centered(d, y, line, font(LORA_I, 38), (205, 187, 149))
    cta(d, y + 20, price, sub)
    return im


def bundle_promo():
    im = bg()
    d = ImageDraw.Draw(im)
    tracked(d, 120, "THE DATEUNOA COLLECTION", font(INTER + "Inter-Medium.otf", 30), GOLD, 7)
    centered(d, 180, "3 ebooks.\nBuy 2, get 1 free.", font(LORA, 66), IVORY, 14)
    cw = 420
    m = Image.open(A / "men_cover.png").convert("RGB")
    w_ = Image.open(A / "women_cover.png").convert("RGB")
    m = m.resize((cw, int(m.height * cw / m.width)), Image.LANCZOS)
    w_ = w_.resize((cw, int(w_.height * cw / w_.width)), Image.LANCZOS)
    # third book: text card
    t = Image.new("RGB", (cw, m.height), (14, 12, 9))
    td = ImageDraw.Draw(t)
    td.rectangle((18, 18, cw - 18, m.height - 18), outline=GOLD_D, width=2)
    yy = m.height // 2 - 120
    for ln in ("What Do I", "Text Back?"):
        f = font(LORA, 54)
        td.text(((cw - td.textlength(ln, font=f)) / 2, yy), ln, font=f, fill=GOLD)
        yy += 66
    f = font(LORA_I, 26)
    for ln in ("the exact words for", "slow replies & mixed signals"):
        td.text(((cw - td.textlength(ln, font=f)) / 2, yy + 30), ln, font=f, fill=(205, 187, 149))
        yy += 36
    top = 400
    shadowed(im, m, (30, top + 90))
    shadowed(im, w_, (W - cw - 30, top + 90))
    shadowed(im, t, (W // 2 - cw // 2, top))
    y = top + 90 + m.height + 60
    d.text((0, 0), "")
    y = centered(d, y, "What Do I Text Back? · What Do Men Want?\nWhat Do Women Want?", font(LORA, 34), IVORY, 8)
    cta(d, y + 30, "$56 for all 3", "instead of $84 · instant download")
    return im


def textback_promo():
    im = bg()
    d = ImageDraw.Draw(im)
    tracked(d, 260, "THE TEXTING GUIDE", font(INTER + "Inter-Medium.otf", 30), GOLD, 7)
    y = centered(d, 340, "What Do I\nText Back?", font(LORA, 120), GOLD, 10)
    y = centered(d, y + 40, "The exact words for slow replies,\nmixed signals, ghosting & boundaries.\nWithout looking needy.", font(LORA_I, 42), IVORY, 14)
    y += 60
    for b in ("“haha” → what to send", "Read at 2am → what to send", "“we should hang out sometime” → what to send"):
        y = centered(d, y, b, font(INTER + "Inter-Regular.otf", 36), (205, 187, 149), 6) + 18
    cta(d, y + 40, "$28", "or all 3 ebooks for $56")
    return im


PROMOS = {
    "men_cover": lambda: cover_promo("men_cover.png", "NEW EBOOK",
                                     ["What he's really looking for.", "How real interest looks.", "What makes him stay."],
                                     "$28", "or all 3 ebooks for $56"),
    "women_cover": lambda: cover_promo("women_cover.png", "NEW EBOOK",
                                       ["What makes her feel safe.", "What makes her choose you.", "The exact texts to send."],
                                       "$28", "or all 3 ebooks for $56"),
    "men_page": lambda: page_promo("men_page.png", "What his texts\nreally mean", "Stop decoding. Start knowing.", "What Do Men Want?", "$28 · or all 3 for $56"),
    "men_page2": lambda: page_promo("men_page2.png", "Into you, or keeping\nyou as an option?", "Chapter 6 answers it.", "What Do Men Want?", "$28 · or all 3 for $56"),
    "women_page": lambda: page_promo("women_page.png", "The texting rules\nwomen wish men knew", "Chapter 7, plus 30 ready texts.", "What Do Women Want?", "$28 · or all 3 for $56"),
    "women_page2": lambda: page_promo("women_page2.png", "Confident or\narrogant?", "She notices the difference instantly.", "What Do Women Want?", "$28 · or all 3 for $56"),
    "bundle": bundle_promo,
    "textback": textback_promo,
}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    tracks = sorted(MUSIC.glob("music_*.m4a"))
    for k, (name, fn) in enumerate(PROMOS.items()):
        frame = out / f"promo_{name}.png"
        fn().save(frame)
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(frame),
            "-i", str(tracks[k % len(tracks)]), "-t", "9",
            "-vf", "scale=2160:3840,zoompan=z='1+0.00016*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=270:s=1080x1920:fps=30,fade=t=in:st=0:d=0.4,format=yuv420p",
            "-af", "afade=t=in:d=0.5,afade=t=out:st=8:d=1",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
            "-shortest", "-movflags", "+faststart", str(out / f"promo_{name}.mp4"),
        ], check=True)
        print("wrote", name)


if __name__ == "__main__":
    main()
