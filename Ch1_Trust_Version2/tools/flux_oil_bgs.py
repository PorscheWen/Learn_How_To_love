#!/usr/bin/env python3
"""Generate Version2 oil-painting BG baselines via Hermes FAL (flux-2-pro).

Naming: bg-{place}-{light}.png — see agents/image_bg.md
Living day/night variants: use flux_living_variants.py from bg-living-night.
"""
from __future__ import annotations

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
OUT_BG = ROOT / "assets" / "bg"

STYLE = (
    "Impressionistic oil painting. Thick visible brushstrokes, painterly impasto "
    "texture, soft blended edges, subtle canvas tooth. Cozy nostalgic quiet "
    "everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art "
    "feel. Not a photograph, not DSLR realism, not anime cel shading, not hard "
    "black outlines, not chibi, not flat vector. No people, no dogs, no animals, "
    "no text, no logo, no readable signs. Wide 16:9 empty environment background."
)

JOBS = [
    {
        "name": "bg-street-night.png",
        "prompt": (
            f"{STYLE} "
            "Empty Taiwanese alley at rainy night. Wet asphalt with soft "
            "orange-gold reflections from a warm street lamp. Low buildings, "
            "scooter soft focus, mossy wall hint. Alone at curb: empty damp "
            "cardboard shipping box (NO puppy, NO bird nest, maybe plain towel). "
            "Cool indigo night wash with burnt-sienna lamp accent."
        ),
    },
    {
        "name": "bg-living-night.png",
        "prompt": (
            f"{STYLE} "
            "Empty Taiwanese small apartment living room at night. Left: dark sofa "
            "under warm classic table lamp, framed picture, leafy plant. Center: "
            "large glass sliding doors to balcony with black railing, distant city "
            "skyline under textured cloudy indigo night sky. Right: wooden bookshelf, "
            "Monstera, small stool. Cream rug reflecting golden lamp light."
        ),
    },
    {
        "name": "bg-entrance-night.png",
        "prompt": (
            f"{STYLE} "
            "Empty Taiwanese apartment balcony entrance at twilight. Tiled balcony, "
            "leafy plant left, shoes near entrance right. Open wooden door pouring "
            "warm gold interior light; coat and tote on pegs; trailing ivy. Railing "
            "overlooking apartment buildings with lit windows under deep blue dusk."
        ),
    },
    {
        "name": "bg-petshop-day.png",
        "prompt": (
            f"{STYLE} "
            "Empty BRIGHT sunny pet boutique INTERIOR — cheerful daylight, honey wood. "
            "Rustic wooden SERVICE COUNTER and tall SHELVES with colorful pet food bags "
            "(blank packaging), treat jars, leashes, bowls, wicker toys. Bright window "
            "with sheer curtains. STRICTLY NO entrance, NO open doorway, NO exterior."
        ),
    },
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "lhtl-flux/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> int:
    OUT_BG.mkdir(parents=True, exist_ok=True)
    ok = 0
    for job in JOBS:
        name = job["name"]
        dest = OUT_BG / name
        if dest.is_file() and dest.stat().st_size > 100_000 and not os.environ.get("FLUX_FORCE"):
            print(f"SKIP {name} (exists {dest.stat().st_size} bytes)", flush=True)
            ok += 1
            continue
        print(f"\n=== Generating {name} (flux-2-pro) ===", flush=True)
        raw = image_generate_tool(prompt=job["prompt"], aspect_ratio="landscape")
        data = json.loads(raw)
        if not data.get("success") or not data.get("image"):
            print(f"FAIL {name}: {data}", flush=True)
            continue
        url = data["image"]
        if url.startswith("data:"):
            import base64

            dest.write_bytes(base64.b64decode(url.split(",", 1)[1]))
        else:
            download(url, dest)
        print(f"OK {dest} ({dest.stat().st_size} bytes)", flush=True)
        ok += 1
    print(f"\nDone: {ok}/{len(JOBS)}", flush=True)
    print("Living day variant: python tools/flux_living_variants.py", flush=True)
    return 0 if ok == len(JOBS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
