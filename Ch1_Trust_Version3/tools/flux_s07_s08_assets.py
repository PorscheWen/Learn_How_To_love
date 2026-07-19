#!/usr/bin/env python3`n"""OPTIONAL backup via FLUX 2 Pro. Primary: Cursor GenerateImage + remove_ai_bg.py (agents/image.md).`n`nGenerate Version3 S07/S08 assets with FLUX 2 Pro through Nous Portal."""
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
OUT_CHAR = ROOT / "assets" / "char"
OUT_DOG = ROOT / "assets" / "dog"

STYLE = (
    "Impressionistic oil painting, thick visible brushstrokes, painterly impasto "
    "texture, soft blended edges, subtle canvas tooth, warm natural Taiwanese light, "
    "quiet everyday atmosphere, storybook concept-art feel. Not photography, anime, "
    "cel shading, hard black outlines, chibi, or flat vector."
)

DOG_LOCK = (
    "SAME PUPPY IDENTITY LOCK (Option B wiry, matching dog-ref-canonical.png): one "
    "continuous character, about 2 months old Taiwanese scruffy wiry mixed-breed puppy, "
    "short stubby legs and slightly thin body, wiry short-to-medium messy honey "
    "golden-tan coat, darker brown ear tips and back ridge, cream chest and muzzle, "
    "lighter paws, soft semi-floppy ears, round warm dark-brown eyes, small black nose, "
    "slightly angular street-puppy face. Not fluffy or purebred."
)

YUAN_LOCK = (
    "Same Yuan character: 26-year-old Taiwanese office worker woman, long natural "
    "dark-brown to black hair, warm skin, ordinary slender build, gentle realistic "
    "features, oatmeal blouse and muted gray-brown pants, no logo."
)

CHROMA = (
    "Centered full body on a perfectly flat solid chroma green #00FF00 background, "
    "no floor, cast shadow, scenery, writing, logo, or interface. Entire subject "
    "inside frame with a wide green margin."
)

JOBS = [
    {
        "directory": OUT_DOG,
        "name": "dog-guard-door-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated puppy lying lengthwise across an imaginary "
            "door threshold, chest down and front paws forward, head awake and turned "
            "toward the room, one ear listening behind, worried but gentle watchful "
            f"expression, tail resting low. Puppy only. {CHROMA}"
        ),
    },
    {
        "directory": OUT_BG,
        "name": "bg-alley-day.png",
        "aspect": "landscape",
        "prompt": (
            f"{STYLE} Wide 16:9 daytime visual-novel background of a quiet older "
            "Taiwanese residential alley meeting a small street corner. Low apartment "
            "facades, tiled walls, potted plants, a roadside tree casting soft shade, "
            "utility poles and a clear turning point several meters ahead. Unoccupied "
            "vacant architectural study with a completely clear walking path and no "
            "focal subject. No readable signs, lettering, logos, or interface."
        ),
    },
    {
        "directory": OUT_CHAR,
        "name": "char-yuan-leash-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {YUAN_LOCK} Full-body side-on gentle crouching pose for a visual "
            "novel sprite, one hand loosely holding the handle of a plain thin brown "
            "leash that exits the frame, the other hand relaxed near her knee, shoulders "
            "lowered, patient neutral expression, practical flat shoes, no animal. "
            f"{CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-street-tense-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated frightened puppy recoiling from a sudden "
            "street noise: belly extremely low near the ground, spine curved backward, "
            "all four paws spread and braced against being pulled forward, shoulders "
            "tight, BOTH ears pinned flat, tail tightly tucked between the hind legs, "
            "wide wary eyes. A simple muted harness with a taut thin lead exiting frame "
            f"behind it, puppy only, no person. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-leash-wait-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated tired puppy paused during a first walk, "
            "standing with weight slightly back but choosing to look forward, ears "
            "half-lowered, breathing calmer, one front paw preparing a small voluntary "
            "step. A simple muted harness with a slack thin lead exiting frame, puppy "
            f"only, no person. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-shoe-sleep-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated exhausted puppy curled asleep with cheek and "
            "shoulder gently touching one plain oatmeal-gray woman's flat shoe placed "
            "beside it, eyes closed, ears loose, body finally relaxed, tail near paws. "
            "The single empty shoe is the only prop; no foot or person. {CHROMA}"
        ),
    },
]


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "lhtl-flux-v3/1.0"})
    with urllib.request.urlopen(request, timeout=240) as response:
        destination.write_bytes(response.read())


def main() -> int:
    selected = {arg for arg in sys.argv[1:] if arg.endswith(".png")}
    jobs = [job for job in JOBS if not selected or job["name"] in selected]
    completed = 0

    for job in jobs:
        destination = job["directory"] / job["name"]
        if (
            destination.exists()
            and destination.stat().st_size > 100_000
            and not os.environ.get("FLUX_FORCE")
        ):
            print(f"SKIP {destination.name} (exists)", flush=True)
            completed += 1
            continue

        print(f"Generating {destination.name} with FLUX 2 Pro", flush=True)
        result = json.loads(
            image_generate_tool(
                prompt=job["prompt"],
                aspect_ratio=job["aspect"],
            )
        )
        if not result.get("success") or not result.get("image"):
            print(f"FAIL {destination.name}: {result}", flush=True)
            continue

        download(result["image"], destination)
        print(f"OK {destination.name} ({destination.stat().st_size} bytes)", flush=True)
        completed += 1

    print(f"Done {completed}/{len(jobs)} generated assets", flush=True)
    return 0 if completed == len(jobs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
