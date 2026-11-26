"""Thumbnail, video 3. Figures: $74B = $73,990M FDIC-guaranteed GE Capital debt at Mar 31, 2009 (facts.md row 14)."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import engine as E
from engine import *
from thumbs import base, glow_text, save
import scenes as S

def thumb(out):
    img, d = base()
    # darker, moodier background
    img = Image.blend(img, Image.new("RGB", img.size, (4, 6, 10)), 0.35); d = ImageDraw.Draw(img)
    # factory with glowing vault (left)
    lay = Image.new("RGB", img.size, (0, 0, 0)); ld = ImageDraw.Draw(lay)
    S.factory(d, 60, 520, 1050, 1.0, lit=1.0, vault=1.0, t=0.4)
    # warm glow behind vault
    gl = Image.new("L", img.size, 0); gd = ImageDraw.Draw(gl)
    cx, cy = 60 + 0.62 * 1050, 520 + 0.24 * 1050
    gd.ellipse([cx - 330, cy - 330, cx + 330, cy + 330], fill=110)
    gl = gl.filter(ImageFilter.GaussianBlur(90))
    img.paste(Image.new("RGB", img.size, (245, 170, 50)), (0, 0), gl.point(lambda v: int(v * 0.7)))
    d = ImageDraw.Draw(img)
    d.line([0, 520 + 0.45 * 1050, 1920, 520 + 0.45 * 1050], fill=(60, 70, 92), width=4)
    glow_text(img, "$74B", 1880, 120, 300, RED, align="r")
    glow_text(img, "GUARANTEED", 1880, 450, 140, INK, align="r", blur=12)
    d = ImageDraw.Draw(img)
    f = font("black", 74); s = "THE BANK INSIDE GE"
    tw = d.textlength(s, font=f)
    d.rounded_rectangle([1880 - tw - 40, 650, 1880, 760], radius=10, fill=GOLD)
    d.text((1880 - tw - 20, 662), s, font=f, fill=(12, 14, 20))
    save(img, out)

if __name__ == "__main__":
    thumb(sys.argv[1])
