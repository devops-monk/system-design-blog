#!/usr/bin/env python3
"""Social share cards.

The article covers are 1600x640 WebP. Neither of those is right for a share
card: LinkedIn has never reliably rendered WebP, and 2.5:1 gets cropped by
every network that expects the 1.91:1 OpenGraph ratio.

So each cover is scaled to 1200x480 and centred on a 1200x630 canvas. The
bands above and below are filled with a blurred, over-scaled copy of the
cover rather than a flat colour — the covers carry a gradient, so a flat
fill leaves a visible seam. Nothing is cropped, the ratio is what the
networks want, and the output is JPEG, which every network reads.

    python3 tools/gen_social.py
"""
import os
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "static/images/articles")
OUT = os.path.join(ROOT, "static/images/social")

W, H = 1200, 630


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for name in sorted(os.listdir(SRC)):
        if not name.endswith(".webp"):
            continue
        cover = Image.open(os.path.join(SRC, name)).convert("RGB")
        scaled = cover.resize((W, round(cover.height * W / cover.width)),
                              Image.LANCZOS)
        # Backdrop: the cover blown up to fill the frame, then blurred out.
        fill = cover.resize((round(cover.width * H / cover.height), H),
                            Image.LANCZOS)
        left = (fill.width - W) // 2
        canvas = fill.crop((left, 0, left + W, H)).filter(
            ImageFilter.GaussianBlur(36))
        canvas.paste(scaled, (0, (H - scaled.height) // 2))
        dest = os.path.join(OUT, name[:-5] + ".jpg")
        canvas.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
        n += 1
    print(f"wrote {n} cards to static/images/social/")


if __name__ == "__main__":
    main()
