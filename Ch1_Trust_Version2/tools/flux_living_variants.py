#!/usr/bin/env python3
"""Generate living light variants from bg-living-night (FLUX 2 Pro edit).

See agents/image_bg.md — same place, only change day/night lighting.
"""
from __future__ import annotations

import base64
import io
import json
import os
import sys
from pathlib import Path

HERMES_ROOT = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "hermes-agent"
sys.path.insert(0, str(HERMES_ROOT))
os.environ["FAL_IMAGE_MODEL"] = "fal-ai/flux-2-pro"

from tools.image_generation_tool import image_generate_tool  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_BG = ROOT / "assets" / "bg"
BASE = OUT_BG / "bg-living-night.png"

KEEP = (
    "Keep the EXACT same Taiwanese apartment living room as the reference: "
    "navy sofa left with cream lamp, framed picture, large sliding glass balcony "
    "doors center with black railing and city skyline, tall wooden bookshelf right, "
    "Monstera in terracotta, small wooden stool, cream rug on dark wood floor, "
    "leafy plant left. Same impressionistic oil painting, thick brushstrokes. "
    "No people, no dogs, no animals, no text, no logo."
)

JOBS = [
    {
        "name": "bg-living-day.png",
        "prompt": (
            f"{KEEP} "
            "Change ONLY lighting to DAYTIME / brighter: soft natural daylight "
            "through the balcony doors, softer shadows, warm cheerful afternoon "
            "mood instead of night lamp chiaroscuro. City outside can be soft "
            "daytime haze. Optionally one empty cardboard box with plain cream "
            "towel near the rug (NO bird nest). Wide 16:9."
        ),
    },
]


def ref_data_uri(path: Path, max_side: int = 1280) -> str:
    from PIL import Image

    im = Image.open(path).convert("RGB")
    im.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def save_image_payload(payload: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if payload.startswith("data:"):
        dest.write_bytes(base64.b64decode(payload.split(",", 1)[1]))
        return
    import urllib.request

    req = urllib.request.Request(payload, headers={"User-Agent": "lhtl-flux/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        dest.write_bytes(resp.read())


def main() -> int:
    if not BASE.is_file():
        print(f"Missing baseline: {BASE}", flush=True)
        return 1
    print(f"Baseline: {BASE.name}", flush=True)
    uri = ref_data_uri(BASE)
    ok = 0
    for job in JOBS:
        name = job["name"]
        if (OUT_BG / name).is_file() and not os.environ.get("FLUX_FORCE"):
            print(f"SKIP {name} (exists; set FLUX_FORCE=1 to overwrite)", flush=True)
            ok += 1
            continue
        print(f"\n=== {BASE.name} → {name} ===", flush=True)
        raw = image_generate_tool(
            prompt=job["prompt"],
            aspect_ratio="landscape",
            image_url=uri,
        )
        data = json.loads(raw)
        if not data.get("success") or not data.get("image"):
            print(f"FAIL {name}: {data}", flush=True)
            continue
        dest = OUT_BG / name
        save_image_payload(data["image"], dest)
        print(f"OK {dest} ({dest.stat().st_size} bytes)", flush=True)
        ok += 1
    print(f"\nDone: {ok}/{len(JOBS)}", flush=True)
    return 0 if ok == len(JOBS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
