# -*- coding: utf-8 -*-
"""Verify ending gallery + secret photos + hidden content are readable."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = (ROOT / ".." / "assets").resolve()
GAME = ROOT / "game"

GALLERY_FILES = [
    "gallery/secret-lap-sleep.png",
    "gallery/secret-forehead-nudge.png",
    "gallery/secret-behind-legs.png",
    "gallery/secret-shoe-sleep.png",
    "gallery/secret-nose-touch.png",
    "gallery/secret-water-bowl.png",
    "gallery/ending-a-back.png",
    "gallery/ending-b-learning.png",
    "gallery/ending-c-handover.png",
    "gallery/ending-d-thin-ice.png",
]

IMAGE_DEFS = [
    "image gallery secret_lap_sleep",
    "image gallery secret_forehead_nudge",
    "image gallery secret_behind_legs",
    "image gallery secret_shoe_sleep",
    "image gallery secret_nose_touch",
    "image gallery secret_water_bowl",
    "image gallery ending_a_back",
    "image gallery ending_b_learning",
    "image gallery ending_c_handover",
    "image gallery ending_d_thin_ice",
]

SECRET_IDS = (
    "lap_sleep",
    "forehead_nudge",
    "behind_legs",
    "shoe_sleep",
    "nose_touch",
    "water_bowl",
)

HIDDEN_IDS = (
    [f"dog_diary_{x}" for x in "abcd"]
    + [f"character_aftercare_{x}" for x in "abcd"]
    + [f"friend_perspective_{x}" for x in "abcd"]
    + ["ch2_trust_foundation_hint"]
)


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def main() -> int:
    if not ASSETS.is_dir():
        fail(f"assets missing: {ASSETS}")

    options = (GAME / "options.rpy").read_text(encoding="utf-8")
    if "config.searchpath.append" not in options or "assets" not in options:
        fail("options.rpy must append Version3/assets to searchpath")
    ok("options.rpy searchpath -> Version3/assets")

    for rel in GALLERY_FILES:
        path = ASSETS.joinpath(*rel.split("/"))
        if not path.is_file():
            fail(f"missing {rel}")
        if path.stat().st_size < 1000:
            fail(f"too small {rel}")
        with path.open("rb") as fh:
            sig = fh.read(8)
        if sig[:4] != b"\x89PNG":
            fail(f"not PNG {rel}")
        ok(f"loadable {rel} ({path.stat().st_size} bytes)")

    script = (GAME / "script.rpy").read_text(encoding="utf-8")
    for needle in IMAGE_DEFS:
        if needle not in script:
            fail(f"missing image def: {needle}")
    if "image gallery secret_back_to_back" in script:
        fail("secret_back_to_back should be removed from image defs")
    ok("script.rpy gallery image definitions")

    screens = (GAME / "screens.rpy").read_text(encoding="utf-8")
    for needle in (
        'screen ending_gallery():',
        'screen hidden_content_gallery():',
        'screen hidden_content_reader',
        'screen ending_still_view',
        'screen secret_photo_view',
        'ShowMenu("ending_gallery")',
        'ShowMenu("hidden_content_gallery")',
        "open_gallery_image",
    ):
        if needle not in screens:
            fail(f"screens.rpy missing {needle}")
    if "胸口同睡" in screens or "open_memo_chest" in screens:
        fail("screens still reference chest/back-to-back memorial")
    ok("screens.rpy ending/hidden menu wiring")

    hc = (GAME / "hidden_content.rpy").read_text(encoding="utf-8")
    for cid in HIDDEN_IDS:
        if f'"{cid}"' not in hc:
            fail(f"hidden_content missing {cid}")
    if hc.count('"body":') < 12:
        fail("hidden_content should have >=12 body entries")
    for pid in SECRET_IDS:
        if f'"{pid}"' not in hc:
            fail(f"SECRET_PHOTO_META missing {pid}")
    if '"back_to_back"' in hc:
        fail("back_to_back still in hidden_content SECRET_PHOTO")
    ok(f"hidden_content.rpy entries ({len(HIDDEN_IDS)} ids + {len(SECRET_IDS)} photos)")

    if 'unlock_secret_photo("lap_sleep")' not in script and "unlock_secret_photo(_pid)" not in script:
        fail("ending A must unlock secret photos")
    if 'unlock_secret_photo("back_to_back")' in script:
        fail("back_to_back unlock should be removed")
    if 'process_ending_unlock' not in script:
        fail("missing process_ending_unlock")
    ok("unlock wiring present")

    print("[OK] gallery images + ending gallery + hidden content readable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
