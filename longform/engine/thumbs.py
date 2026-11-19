"""Thumbnail helpers (1280x720 JPG). glow_text() + engine background give the house look.
Write thumb() for each new video: ONE striking image + 2-5 words, numbers only from the fact table, no logos, no real people.
Usage: python3 thumbs.py out.jpg"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
import engine as E
from engine import *

def base():
    E.init()
    img = E.background(0)
    return img, ImageDraw.Draw(img)

def glow_text(img, s, x, y, size, color, w="black", align="l", blur=18):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    f = font(w, size); tw = ld.textlength(s, font=f)
    xx = x - tw / 2 if align == "c" else x - tw if align == "r" else x
    ld.text((xx, y), s, font=f, fill=color + (255,))
    g = lay.filter(ImageFilter.GaussianBlur(blur))
    img.paste(Image.new("RGB", img.size, color), (0, 0), g.split()[3].point(lambda v: int(v * 0.55)))
    img.paste(lay, (0, 0), lay)

def save(img, out):
    img.resize((1280, 720), Image.LANCZOS).save(out, quality=90)
    assert os.path.getsize(out) < 2_000_000, "thumbnail must be under 2 MB"

# Example from video 1 (paper document on the left, big glowing figure + word on the right):
def thumb_example(out):
    img, d = base()
    pap = Image.new("RGBA", (900, 1100), (0, 0, 0, 0)); pd = ImageDraw.Draw(pap)
    pd.rounded_rectangle([0, 0, 899, 1099], radius=10, fill=PAPER + (255,))
    pd.text((60, 60), "COMPANIES HOUSE", font=font("serifb", 36), fill=(90, 90, 96))
    pd.text((60, 120), "LANTANA TRADE LLP", font=font("serifb", 66), fill=PAPER_INK)
    pd.rectangle([40, 330, 860, 470], fill=(250, 215, 90))
    pd.text((70, 350), "NET ASSETS", font=font("serifb", 70), fill=PAPER_INK)
    pd.text((600, 350), "0.00", font=font("serifb", 80), fill=(170, 30, 36))
    for i in range(10): pd.rounded_rectangle([60, 560 + i * 48, 60 + 780 - (i * 37) % 300, 576 + i * 48], radius=6, fill=(190, 184, 172))
    pap = pap.resize((720, 880), Image.LANCZOS).rotate(6, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", pap.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 160), (0, 0), pap.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(20))
    img.paste(sh, (90, 120), sh); img.paste(pap, (60, 80), pap)
    glow_text(img, "$480M", 1880, 280, 260, RED, align="r")
    glow_text(img, "MOVED", 1880, 590, 200, INK, align="r")
    save(img, out)

if __name__ == "__main__":
    thumb_example(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ytw/deliver/thumb_example.jpg")
