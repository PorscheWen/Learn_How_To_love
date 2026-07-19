#!/usr/bin/env python3`n"""OPTIONAL backup via FLUX 2 Pro. Primary: Cursor GenerateImage + remove_ai_bg.py (agents/image.md).`n`nGenerate Version3 S03/S04 backgrounds and dog poses with FLUX 2 Pro."""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance


HERMES_ROOT = Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "hermes-agent"
sys.path.insert(0, str(HERMES_ROOT))
os.environ["FAL_IMAGE_MODEL"] = "fal-ai/flux-2-pro"

from tools.image_generation_tool import image_generate_tool  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
OUT_BG = ROOT / "assets" / "bg"
OUT_DOG = ROOT / "assets" / "dog"

STYLE = (
    "Impressionistic oil painting. Thick visible brushstrokes, painterly impasto "
    "texture, soft blended edges, subtle canvas tooth. Warm amber light contrasting "
    "cool deep indigo shadows. Cozy nostalgic quiet everyday Taiwanese atmosphere. "
    "Soft atmospheric depth, storybook concept-art feel. Not a photograph, not "
    "anime cel shading, not hard black outlines, not chibi, not flat vector."
)

DOG_LOCK = (
    "SAME PUPPY IDENTITY LOCK (Option B wiry, must match dog-ref-canonical.png): "
    "one continuous character, about 2 months old Taiwanese scruffy wiry mixed-breed "
    "puppy, not purebred. Short stubby legs, slightly thin body, ribs may be faintly "
    "visible. Wiry short-to-medium messy coat. Honey golden-tan fur, darker brown ear "
    "tips and ear edges and back ridge, cream chest, cream muzzle area, lighter paws. "
    "Soft semi-floppy ears, round warm dark-brown eyes, small black nose, slightly "
    "angular scruffy street-puppy face. Not fluffy, not a round plush face, not a "
    "show dog, not a corgi, poodle, shiba or husky."
)

JOBS = [
    {
        "directory": OUT_BG,
        "name": "bg-stairwell-night.png",
        "aspect": "landscape",
        "prompt": (
            f"{STYLE} Empty ground-floor stairwell of an older Taiwanese apartment "
            "building at night, wide 16:9 visual novel background. Gray concrete "
            "stairs turning upward, brushed metal elevator doors clearly visible, "
            "a humming fluorescent tube, a neighboring apartment door with a very "
            "thin line of warm light beneath it. Open floor space near the stair "
            "corner for an old coat and a shallow water dish. Quiet temporary-border "
            "mood. No people, no dogs, no animals, no text, no logo, no readable "
            "signs, no trust HUD."
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-stair-watch-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Full body puppy pressed close beside an imaginary "
            "wall, body curled low but awake, head turned toward an elevator direction, "
            "ears slightly back, eyes vigilant, tail wrapped low beside a hind leg. "
            "The pose must clearly show wary watching and a changed resting position. "
            "Centered on a perfectly flat solid chroma green #00FF00 background, no "
            "floor, no shadow, no scenery, no props, no text, no logo. Entire puppy "
            "inside frame with clear green margin."
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-door-sleep-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Full body puppy asleep on its side on an imaginary "
            "door mat, back facing outward while face and nose point toward an "
            "imaginary closed apartment door, paws tucked unevenly, exhausted but "
            "still guarding the doorway, ears relaxed yet one ear faintly alert, tail "
            "curled close. Centered on a perfectly flat solid chroma green #00FF00 "
            "background, no actual mat, no door, no floor, no shadow, no scenery, no "
            "props, no text, no logo. Entire puppy inside frame with clear green margin."
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-parallel-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Full body puppy resting calmly on belly at a cautious "
            "two-step distance, chin fully touching the ground, front paws forward, "
            "ears loosened, warm eyes half-open watching a person off-frame, tail lying "
            "quietly beside the body. Relaxed but still keeping an escape route. "
            "Centered on a perfectly flat solid chroma green #00FF00 background, no "
            "floor, no shadow, no scenery, no props, no text, no logo. Entire puppy "
            "inside frame with clear green margin."
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-kitchen-door-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Full body puppy standing with both front paws aligned "
            "at an imaginary threshold, body leaning forward with cautious curiosity "
            "but refusing to cross, head slightly tilted, ears half-raised, eyes "
            "following a person off-frame, tail low with a tiny relaxed curve. The "
            "stopping-at-the-doorway action must read clearly. Centered on a perfectly "
            "flat solid chroma green #00FF00 background, no actual doorway, no floor, "
            "no shadow, no scenery, no props, no text, no logo. Entire puppy inside "
            "frame with clear green margin."
        ),
    },
]


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "lhtl-flux-v3/1.0"})
    with urllib.request.urlopen(request, timeout=240) as response:
        destination.write_bytes(response.read())


def make_living_day() -> None:
    """Preserve the living-room furniture while grading the night base to daytime."""
    source = OUT_BG / "bg-living-night.png"
    destination = OUT_BG / "bg-living-day.png"
    if (
        destination.exists()
        and destination.stat().st_size > 100_000
        and "--force-day" not in sys.argv
    ):
        print(f"SKIP {destination.name} (exists)", flush=True)
        return
    image = Image.open(source).convert("RGB")
    image = ImageEnhance.Brightness(image).enhance(1.34)
    image = ImageEnhance.Color(image).enhance(0.82)
    cool_day = Image.new("RGB", image.size, (211, 222, 219))
    image = Image.blend(image, cool_day, 0.13)

    # The living family must keep its furniture and camera angle. Replace only
    # the blue night values inside the known window opening with a pale daytime
    # wash, while keeping the dark mullions readable.
    pixels = image.load()
    width, height = image.size
    for y in range(0, int(height * 0.78)):
        for x in range(int(width * 0.31), int(width * 0.78)):
            r, g, b = pixels[x, y]
            value = max(r, g, b)
            if value < 48:
                continue
            target = (176, 207, 218) if y < height * 0.55 else (190, 204, 205)
            amount = 0.56 if b >= r * 1.04 else 0.32
            pixels[x, y] = tuple(
                int(channel * (1.0 - amount) + day * amount)
                for channel, day in zip((r, g, b), target)
            )

    image = ImageEnhance.Contrast(image).enhance(0.92)
    image.save(destination, quality=96)
    print(f"OK {source.name} -> {destination.name}", flush=True)


def main() -> int:
    make_living_day()
    if "--day-only" in sys.argv:
        return 0
    completed = 0
    for job in JOBS:
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

    print(f"Done {completed}/{len(JOBS)} generated assets", flush=True)
    return 0 if completed == len(JOBS) else 1


if __name__ == "__main__":
    raise SystemExit(main())
