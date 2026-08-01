#!/usr/bin/env python3
"""Fill missing Version2 assets (treestreet-day, clinic-day, char-sit-floor).

Day7 日間路程：bg-treestreet-day.png（樹蔭人行道）
Also：bg-clinic-day.png、char-sit-floor.png（char 需 rembg）

Requires FAL_KEY via Hermes image_generation_tool.
"""
from __future__ import annotations

import base64
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
OUT_CHAR = ROOT / "assets" / "char"

STYLE = (
    "Impressionistic oil painting. Thick visible brushstrokes, painterly impasto "
    "texture, soft blended edges, subtle canvas tooth. Cozy nostalgic quiet "
    "everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art "
    "feel. Not a photograph, not DSLR realism, not anime cel shading, not hard "
    "black outlines, not chibi, not flat vector. No people, no dogs, no animals, "
    "no text, no logo, no readable signs. Wide 16:9 empty environment background."
)

TREE_PROMPT = (
    f"{STYLE} "
    "Empty Taiwanese residential sidewalk under TREE SHADE on a bright day. "
    "Overhanging green tree canopy casting soft dappled light on concrete pavement. "
    "Quiet neighborhood street edge, low walls, distant scooters soft focus. "
    "Warm daylight filtered through leaves — cool green shade with golden sun flecks. "
    "Tree-lined walkway (樹蔭人行道), peaceful morning walk to the clinic. "
    "No people, no dogs, no cars in foreground."
)

CLINIC_PROMPT = (
    f"{STYLE} "
    "Empty small Taiwanese veterinary clinic waiting room INTERIOR, daytime. "
    "Reception counter, soft chairs, plant, posters with blank text, pale walls, "
    "daylight from frosted window. Quiet calm clinic atmosphere. "
    "STRICTLY NO exterior street, NO open doorway to outside."
)

CHAR_PROMPT = (
    "Impressionistic oil painting character illustration, soft brushstrokes. "
    "Young Taiwanese woman sitting on apartment floor, gentle tired expression, "
    "casual home clothes, warm indoor light. Full body / seated pose suitable "
    "for visual novel sprite. Soft edges, no hard black outlines, not anime cel, "
    "not photoreal. Plain soft background for easy background removal. "
    "No dog, no text, no logo."
)


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "lhtl-flux/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def gen(prompt: str, dest: Path) -> bool:
    if dest.is_file() and dest.stat().st_size > 100_000 and not os.environ.get("FLUX_FORCE"):
        print(f"SKIP {dest.name} (exists {dest.stat().st_size} bytes)", flush=True)
        return True
    print(f"\n=== Generating {dest.name} ===", flush=True)
    raw = image_generate_tool(prompt=prompt, aspect_ratio="landscape")
    data = json.loads(raw)
    if not data.get("success") or not data.get("image"):
        print(f"FAIL {dest.name}: {data}", flush=True)
        return False
    url = data["image"]
    if url.startswith("data:"):
        dest.write_bytes(base64.b64decode(url.split(",", 1)[1]))
    else:
        download(url, dest)
    print(f"OK {dest} ({dest.stat().st_size} bytes)", flush=True)
    return True


def main() -> int:
    OUT_BG.mkdir(parents=True, exist_ok=True)
    OUT_CHAR.mkdir(parents=True, exist_ok=True)
    ok = 0
    total = 3
    if gen(TREE_PROMPT, OUT_BG / "bg-treestreet-day.png"):
        ok += 1
    if gen(CLINIC_PROMPT, OUT_BG / "bg-clinic-day.png"):
        ok += 1
    if gen(CHAR_PROMPT, OUT_CHAR / "char-sit-floor.png"):
        ok += 1
        print("Note: run rembg / remove_sprite_bg.py on char-sit-floor.png", flush=True)
    print(f"\nDone: {ok}/{total}", flush=True)
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
