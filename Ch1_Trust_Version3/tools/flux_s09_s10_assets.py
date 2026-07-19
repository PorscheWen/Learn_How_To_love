#!/usr/bin/env python3
"""OPTIONAL backup: generate S09/S10 assets with FLUX 2 Pro.

Primary pipeline is Cursor GenerateImage + remove_ai_bg.py (see agents/image.md).
Run this only when Cursor cannot generate, or the user explicitly asks for FLUX.
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

COWORKER_LOCK = (
    "One 28-year-old Taiwanese woman office worker, shoulder-length natural dark hair, "
    "warm skin, realistic ordinary features, muted lavender-gray cardigan over a cream "
    "top, dark straight pants and practical flats, calm sincere expression, no logo."
)

CHROMA = (
    "Centered full body on a perfectly flat solid chroma green #00FF00 background, "
    "no floor, cast shadow, scenery, writing, logo, or interface. Entire subject "
    "inside frame with a wide green margin."
)

JOBS = [
    {
        "directory": OUT_BG,
        "name": "bg-cafe-day.png",
        "aspect": "landscape",
        "prompt": (
            f"{STYLE} Wide 16:9 daytime visual-novel background of the entrance of a "
            "small quiet Taiwanese neighborhood cafe, viewed from the sidewalk. Warm "
            "wood-framed glass door, pale tiled exterior, one simple planter, subtle "
            "interior counter shapes through glass, ample clear foreground for two "
            "character sprites. STRICTLY EMPTY architectural scene: no people, dogs, "
            "animals, readable signs, lettering, logos, or interface."
        ),
    },
    {
        "directory": OUT_CHAR,
        "name": "char-coworker-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {COWORKER_LOCK} Full-body visual-novel sprite standing at a slight "
            "angle, shoulders relaxed, one empty hand held low and open without reaching, "
            f"empathetic but not overly cheerful. Woman only, no animal or props. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-refuse-stranger-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated puppy pressed close beside an implied familiar "
            "person's shoe but show NO person and NO shoe: body low and leaning sideways, "
            "shoulders tense, ears pinned back, tail low, eyes fixed warily toward an "
            "off-frame stranger, mouth closed as if making a tiny warning rumble. A "
            f"simple muted harness and slack thin leash. Puppy only. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-back-sleep-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated deeply relaxed puppy asleep on its side with "
            "its BACK facing the viewer, body gently curved, vulnerable belly side and "
            "loose hind legs visible, ears completely relaxed, breathing peacefully, "
            f"tail resting naturally. Puppy only, no person, furniture, or props. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-check-sleep-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated puppy lying close and almost asleep, body "
            "relaxed on its belly but head lifted slightly to glance back and confirm "
            "someone is still there, one ear loose and one listening, cautious comfort "
            f"rather than fear. Puppy only, no person, furniture, or props. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-door-edge-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Isolated puppy sleeping lightly beside an implied door "
            "edge: body curled but oriented toward an escape route, paws tucked tightly, "
            "ears not fully relaxed, eyes barely closed, tail close to body, emotionally "
            f"distant but not abused. Puppy only, no visible door or room. {CHROMA}"
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
