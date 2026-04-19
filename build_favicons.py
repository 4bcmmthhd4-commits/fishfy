#!/usr/bin/env python3
"""Build tab-favicon PNGs from favicon.png (high-quality stepped downscale)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "favicon.png"


def downscale(src: Image.Image, target: int) -> Image.Image:
    img = src.convert("RGBA")
    while max(img.size) > target:
        nw = max(img.width // 2, target)
        nh = max(img.height // 2, target)
        if nw == img.width and nh == img.height:
            break
        img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    if img.size != (target, target):
        img = img.resize((target, target), Image.Resampling.LANCZOS)
    if target <= 48:
        img = img.filter(ImageFilter.UnsharpMask(radius=0.35, percent=55, threshold=2))
    return img


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"Missing {SRC.name} in {ROOT}")
    source = Image.open(SRC)
    for size in (16, 32, 48, 64):
        out = downscale(source, size)
        path = ROOT / f"favicon-{size}.png"
        out.save(path, format="PNG", optimize=True)
        print(path.name, out.size)
    apple = downscale(source, 180)
    apple.save(ROOT / "apple-touch-icon.png", format="PNG", optimize=True)
    print("apple-touch-icon.png", apple.size)
    # Einzelbild-.ico für ältere Clients / feste /favicon.ico-Anfragen (Multi-Res-ICO: Pillow SAVE_ALL).
    Image.open(ROOT / "favicon-32.png").convert("RGBA").save(ROOT / "favicon.ico", format="ICO")
    print("favicon.ico (32×32 embedded)")


if __name__ == "__main__":
    main()
