#!/usr/bin/env python3
"""Remove background from dog/character sprites (RGBA). Does not touch bg/ backgrounds."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image
from rembg import remove

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "Ch1_Trust_Version2" / "assets" if (ROOT / "Ch1_Trust_Version2").exists() else ROOT / "assets"


def rembg_file(src: Path, dst: Path | None = None) -> Path:
    dst = dst or src
    raw = src.read_bytes()
    out = remove(raw)
    img = Image.open(__import__("io").BytesIO(out)).convert("RGBA")
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "PNG")
    print(f"OK {src} → {dst} ({img.size[0]}x{img.size[1]})")
    return dst


def main() -> int:
    p = argparse.ArgumentParser(description="Rembg for Version2 dog/char sprites")
    p.add_argument("paths", nargs="+", help="PNG paths or pose names under assets/dog/Week0/")
    p.add_argument("--inplace", action="store_true", help="Overwrite source (default)")
    p.add_argument(
        "--from-raw",
        action="store_true",
        help="Read assets/raw/{name}.png, write final under dog/ or char/",
    )
    args = p.parse_args()

    for item in args.paths:
        path = Path(item)
        if not path.suffix:
            # pose name → dog/dog-{name}.png（不分 week）
            path = ASSETS / "dog" / f"dog-{item}.png"
        if not path.is_file():
            # try relative to assets
            alt = ASSETS / item
            if alt.is_file():
                path = alt
            else:
                print(f"MISSING {item}", file=sys.stderr)
                return 1
        rembg_file(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
