#!/usr/bin/env python3
"""Generate pet-shop NPC sprites: shop aunt + checkout clerk.

Outputs (portrait, rembg in-place):
  assets/char/char-shop-aunt.png
  assets/char/char-shop-cashier.png

Requires FAL_KEY via Hermes image_generation_tool (hermes login).
Force regenerate: set FLUX_FORCE=1
"""
from __future__ import annotations

import base64
import io
import json
import os
import sys
import urllib.request
from pathlib import Path

HERMES_ROOT = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "hermes-agent"
sys.path.insert(0, str(HERMES_ROOT))
os.environ["FAL_IMAGE_MODEL"] = "fal-ai/flux-2-pro"

from tools.image_generation_tool import image_generate_tool  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_CHAR = ROOT / "assets" / "char"
REN_CHAR = ROOT / "Renpy_game" / "game" / "assets" / "char"

CHAR_STYLE = (
    "Impressionistic oil painting character illustration. Thick visible brushstrokes, "
    "painterly impasto texture, soft blended edges, subtle canvas tooth. Warm amber "
    "and golden interior light. Believable proportions, soft facial features. "
    "Cozy nostalgic quiet everyday Taiwanese atmosphere. Soft atmospheric depth, "
    "storybook visual-novel sprite feel. Not a photograph, not DSLR realism, not "
    "anime cel shading, not hard black outlines, not chibi, not flat vector. "
    "No text, no logo, no readable nametag."
)

# 寵物店阿姨：迎賓／推薦用品（Day3 貨架）
AUNT_PROMPT = (
    f"{CHAR_STYLE} "
    "Single Taiwanese middle-aged pet shop auntie (阿姨), about 48–52 years old, "
    "warm plump face, short permed dark hair with a few gray strands, kind but "
    "slightly pushy enthusiastic smile, face clearly visible. "
    "Wearing a soft mustard-yellow shop apron over a simple oatmeal blouse and "
    "muted brown pants; no brand logos. "
    "Standing three-quarter pose, one hand gesturing toward imaginary product "
    "shelves, welcoming energetic body language suitable for a visual novel sprite. "
    "Centered full body from head to shoes, plain soft cream paper background for cutout. "
    "No dog, no customer, no cash register."
)

# 結帳妹妹：櫃檯問名字（Day2 取名）
CASHIER_PROMPT = (
    f"{CHAR_STYLE} "
    "Single young Taiwanese pet shop checkout clerk (結帳妹妹), about 22 years old, "
    "shoulder-length straight dark hair with a neat side clip, gentle polite smile, "
    "face clearly visible, soft warm skin. "
    "Wearing a light sage-green shop apron over a simple white t-shirt and jeans; "
    "no brand logos. "
    "Standing behind an implied counter height, hands resting as if at a checkout, "
    "friendly quiet energy (not loud). Three-quarter portrait / upper-to-full body "
    "sprite, centered, feet or lower legs visible. "
    "Plain soft cream paper background for cutout. No dog, no customer, no readable "
    "receipt or screen text."
)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "lhtl-flux/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def gen(prompt: str, dest: Path, *, aspect: str = "portrait") -> bool:
    if dest.is_file() and dest.stat().st_size > 50_000 and not os.environ.get("FLUX_FORCE"):
        print(f"SKIP {dest.name} (exists {dest.stat().st_size} bytes)", flush=True)
        return True
    print(f"\n=== Generating {dest.name} ===", flush=True)
    raw = image_generate_tool(prompt=prompt, aspect_ratio=aspect)
    data = json.loads(raw)
    if not data.get("success") or not data.get("image"):
        print(f"FAIL {dest.name}: {data}", flush=True)
        return False
    url = data["image"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    if url.startswith("data:"):
        dest.write_bytes(base64.b64decode(url.split(",", 1)[1]))
    else:
        download(url, dest)
    print(f"OK {dest} ({dest.stat().st_size} bytes)", flush=True)
    return True


def rembg_inplace(path: Path) -> None:
    from rembg import remove
    from PIL import Image

    out = remove(path.read_bytes())
    img = Image.open(io.BytesIO(out)).convert("RGBA")
    img.save(path, "PNG")
    print(f"REMBG OK {path.name} {img.size}", flush=True)


def sync_renpy(src: Path) -> None:
    REN_CHAR.mkdir(parents=True, exist_ok=True)
    dest = REN_CHAR / src.name
    dest.write_bytes(src.read_bytes())
    print(f"SYNC {dest}", flush=True)


def main() -> int:
    OUT_CHAR.mkdir(parents=True, exist_ok=True)
    jobs = [
        (AUNT_PROMPT, OUT_CHAR / "char-shop-aunt.png"),
        (CASHIER_PROMPT, OUT_CHAR / "char-shop-cashier.png"),
    ]
    ok = 0
    for prompt, dest in jobs:
        if gen(prompt, dest, aspect="portrait"):
            rembg_inplace(dest)
            sync_renpy(dest)
            ok += 1
    print(f"\nDone: {ok}/{len(jobs)}", flush=True)
    return 0 if ok == len(jobs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
