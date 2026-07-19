#!/usr/bin/env python3`n"""OPTIONAL backup via FLUX 2 Pro. Primary: Cursor GenerateImage + remove_ai_bg.py (agents/image.md).`n`nGenerate Version3 S05/S06 final assets with FLUX 2 Pro after Nous login."""
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
    "Impressionistic oil painting. Thick visible brushstrokes, painterly impasto "
    "texture, soft blended edges, subtle canvas tooth. Warm natural Taiwanese "
    "apartment light, quiet everyday atmosphere, soft atmospheric depth, storybook "
    "concept-art feel. Not a photograph, not anime cel shading, not hard black "
    "outlines, not chibi, not flat vector."
)

DOG_LOCK = (
    "SAME PUPPY IDENTITY LOCK (Option B wiry, must match dog-ref-canonical.png): "
    "one continuous character, about 2 months old Taiwanese scruffy wiry mixed-breed "
    "puppy, not purebred. Short stubby legs, slightly thin body. Wiry short-to-medium "
    "messy coat. Honey golden-tan fur, darker brown ear tips, ear edges and back ridge; "
    "cream chest, cream muzzle and lighter paws. Soft semi-floppy ears, round warm "
    "dark-brown eyes, small black nose, slightly angular street-puppy face. Not fluffy, "
    "not a round plush face, not a corgi, poodle, shiba or husky."
)

YUAN_LOCK = (
    "Same Yuan character: 26-year-old Taiwanese office worker woman, long natural "
    "dark-brown to black hair, warm skin, ordinary slender build, gentle realistic "
    "features, oatmeal blouse and muted gray-brown pants, no logo. Must resemble "
    "char-yuan-commute.png and char-yuan-headphones.png."
)

CHROMA = (
    "Centered full body on a perfectly flat solid chroma green #00FF00 background. "
    "No floor, no cast shadow, no scenery, no props unless explicitly requested, "
    "no text, no logo, no trust meter. Entire subject inside frame with green margin."
)

JOBS = [
    {
        "directory": OUT_DOG,
        "name": "dog-ear-flat-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} ISOLATED PUPPY ONLY. Puppy startled by a sharp human "
            "voice: belly lowered close to the ground, body visibly shrinking backward, "
            "all four paws braced, BOTH ears pressed completely flat against the head, "
            "tail tucked tightly under the body, eyes looking up with wary confusion, "
            "mouth closed. Absolutely no room, no furniture, no human, no hand, no leg, "
            f"no foot, no other animal. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-sniff-wire-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} Puppy cautiously leaning forward to sniff the loose "
            "end of a plain dark headphone cable, nose almost touching it, one front "
            "paw lifted, ears half-raised with careful curiosity, tail low but relaxed. "
            "The cable is the only prop and has no device or logo. {CHROMA}"
        ),
    },
    {
        "directory": OUT_BG,
        "name": "bg-corridor-day.png",
        "aspect": "landscape",
        "prompt": (
            f"{STYLE} Empty daytime corridor of an older Taiwanese apartment building, "
            "wide 16:9 visual novel background. A row of apartment doors, warm window "
            "light, muted tile floor, elevator doors at the far end, generous open space "
            "near one doorway. Unoccupied, vacant architectural study with a completely "
            "clear floor and no focal subject. Clean understated composition, blank door "
            "plates, no readable writing, no logo, no interface."
        ),
    },
    {
        "directory": OUT_CHAR,
        "name": "char-neighbor-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} Friendly but slightly overfamiliar Taiwanese woman neighbor in "
            "her early thirties, casual muted sage cardigan and cream shirt, practical "
            "pants, natural dark shoulder-length hair. Full-body standing pose, one "
            "hand initially reaching forward with curious warmth, not villainous, "
            "believable everyday proportions. {CHROMA}"
        ),
    },
    {
        "directory": OUT_CHAR,
        "name": "char-yuan-block-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {YUAN_LOCK} Full-body protective side-on pose: Yuan steps one "
            "half-step forward with one open hand gently lowered between an unseen "
            "visitor and a puppy behind her leg. Calm neutral face, polite but firm, "
            "shoulders relaxed, not aggressive, no dog included. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-behind-legs-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} ISOLATED PUPPY ONLY. Puppy seeking protection beside "
            "an OFF-CANVAS person: body angled diagonally as if partly tucked behind "
            "something outside the frame, head peeking sideways cautiously, ears lowered, "
            "eyes watching an approaching stranger, tail low, shoulders slightly tense. "
            "Absolutely no human, no hand, no leg, no foot, no person-shaped object, no "
            f"furniture, no room, no other animal. {CHROMA}"
        ),
    },
    {
        "directory": OUT_DOG,
        "name": "dog-forehead-nudge-green.png",
        "aspect": "portrait",
        "prompt": (
            f"{STYLE} {DOG_LOCK} ISOLATED PUPPY ONLY. Puppy taking one small step "
            "forward, head lowered and forehead gently extended toward a target that is "
            "completely outside the frame, eyes softly half closed, ears loose, mouth "
            "relaxed, tail low with a tiny warm curve. The grateful nudge gesture must "
            "read from the neck and body angle alone. Absolutely no human, no hand, no "
            f"leg, no foot, no person-shaped object, no room, no other animal. {CHROMA}"
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
    completed = 0
    jobs = [job for job in JOBS if not selected or job["name"] in selected]
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
