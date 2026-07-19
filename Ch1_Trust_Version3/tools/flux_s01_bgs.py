#!/usr/bin/env python3`n"""OPTIONAL backup via FLUX 2 Pro. Primary: Cursor GenerateImage + remove_ai_bg.py (agents/image.md).`n`nGenerate Version3 S01 missing night BGs via Hermes FAL (flux-2-pro)."""
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
    "texture, soft blended edges, subtle canvas tooth. Warm amber and golden "
    "interior light contrasting cool deep indigo navy night exterior. "
    "Complementary blue-and-gold / teal-and-orange palette. Cozy nostalgic quiet "
    "everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art "
    "feel. Not a photograph, not DSLR realism, not anime cel shading, not hard "
    "black outlines, not chibi, not flat vector. No people, no dogs, no animals, "
    "no text, no logo, no readable signs, no trust HUD. Wide 16:9 empty "
    "environment background for indie visual novel."
)

JOBS = [
    {
        "name": "bg-office-night.png",
        "prompt": (
            f"{STYLE} "
            "Empty Taiwanese open-plan office at late night. A few dark desks with "
            "glowing computer monitors casting cool white-blue light, one monitor "
            "still on with a soft presentation slide glow. Ceiling fluorescent "
            "strips half-dimmed. Empty swivel chairs, distant glass partitions, "
            "quiet overtime loneliness. Cool indigo wash with tiny warm desk-lamp "
            "accents. No readable text on screens."
        ),
    },
    {
        "name": "bg-convenience-night.png",
        "prompt": (
            f"{STYLE} "
            "Empty Taiwanese convenience store interior at night. Microwave area, "
            "refrigerated drink coolers with soft cyan-white glow, high stools near "
            "a counter, snack shelves with blank packaging, warm overhead store "
            "lighting. Quiet after-work atmosphere. Strictly no readable brand "
            "names, no logos, no people, no dogs."
        ),
    },
]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "lhtl-flux-v3/1.0"})
    with urllib.request.urlopen(req, timeout=180) as resp:
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
        print(f"Downloading {url}", flush=True)
        download(url, dest)
        print(f"OK {name} -> {dest} ({dest.stat().st_size} bytes)", flush=True)
        ok += 1
    print(f"\nDone {ok}/{len(JOBS)}", flush=True)
    return 0 if ok == len(JOBS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
