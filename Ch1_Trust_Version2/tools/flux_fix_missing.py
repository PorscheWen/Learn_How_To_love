- Day7 日間路程：`bg-treestreet-day.png`（樹蔭人行道，img2img／生圖）
- bg-clinic-day.png  (clinic waiting interior)
- char-sit-floor.png (woman sitting on floor; rembg after)
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
OUT_CHAR = ROOT / "assets" / "char"
STREET_NIGHT = OUT_BG / "bg-street-night.png"

STYLE_BG = (
    "Impressionistic oil painting. Thick visible brushstrokes, painterly impasto "
    "texture, soft blended edges, subtle canvas tooth. Cozy nostalgic quiet "
    "everyday Taiwanese atmosphere. Soft atmospheric depth, storybook concept-art "
    "feel. Not a photograph, not DSLR realism, not anime cel shading, not hard "
    "black outlines, not chibi, not flat vector. No people, no dogs, no animals, "
    "no text, no logo, no readable signs. Wide 16:9 empty environment background."
)

CHAR_STYLE = (
    "Impressionistic oil painting. Thick visible brushstrokes, soft blended edges. "
    "26-year-old Taiwanese office worker woman Xiaoqing, long natural dark hair, "
    "warm skin, simple oatmeal gray-brown clothes, tired gentle expression, face visible. "
    "Believable proportions. Clean solid soft cream background for cutout. "
    "Not a photograph, not anime idol face, not chibi. No text, no logo."
)


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
    with urllib.request.urlopen(req, timeout=180) as resp:
        dest.write_bytes(resp.read())


def gen(prompt: str, dest: Path, *, image_url: str | None = None, aspect: str = "landscape") -> bool:
    if dest.is_file() and dest.stat().st_size > 50_000 and not os.environ.get("FLUX_FORCE"):
        print(f"SKIP {dest.name} (exists {dest.stat().st_size} bytes)", flush=True)
        return True
    print(f"\n=== Generating {dest.name} ===", flush=True)
    kwargs = {"prompt": prompt, "aspect_ratio": aspect}
    if image_url:
        kwargs["image_url"] = image_url
    raw = image_generate_tool(**kwargs)
    data = json.loads(raw)
    if not data.get("success") or not data.get("image"):
        print(f"FAIL {dest.name}: {data}", flush=True)
        return False
    save_image_payload(data["image"], dest)
    print(f"OK {dest} ({dest.stat().st_size} bytes)", flush=True)
    return True


def rembg_inplace(path: Path) -> None:
    from rembg import remove
    from PIL import Image

    out = remove(path.read_bytes())
    img = Image.open(io.BytesIO(out)).convert("RGBA")
    img.save(path, "PNG")
    print(f"REMBG OK {path.name} {img.size}", flush=True)


def main() -> int:
    ok = 0
    total = 3

    # 1) tree-shaded sidewalk (day)
    tree_prompt = (
        f"{STYLE_BG} "
        "Empty Taiwanese urban sidewalk in daytime under dense tree shade. "
        "Leafy green canopy filtering soft dappled light onto concrete walkway. "
        "Quiet residential street edge, soft blur of buildings beyond trees. "
        "Cool peaceful shade, no people, no dogs."
    )
    if gen(tree_prompt, OUT_BG / "bg-treestreet-day.png"):
        ok += 1

    # 2) clinic day interior
    clinic_prompt = (
        f"{STYLE_BG} "
        "Empty small Taiwanese veterinary CLINIC WAITING ROOM interior in daytime. "
        "Soft daylight through frosted window. Simple reception counter (blank, no text), "
        "two empty waiting chairs, pale green wall, linoleum floor, quiet calm mood. "
        "No people, no dogs, no animals, no posters with readable text, no logo. "
        "Warm muted teal and cream palette, soft oil brushstrokes."
    )
    if gen(clinic_prompt, OUT_BG / "bg-clinic-day.png"):
        ok += 1

    # 3) char sit floor
    char_prompt = (
        f"{CHAR_STYLE} "
        "Full-body portrait of Xiaoqing sitting on the floor, knees drawn up loosely, "
        "one hand resting near an empty cardboard box with a plain towel (NO bird nest). "
        "Tired caring expression looking gently toward the box. Soft cream flat background "
        "for easy cutout. Centered, feet visible."
    )
    char_dest = OUT_CHAR / "char-sit-floor.png"
    if gen(char_prompt, char_dest, aspect="portrait"):
        try:
            rembg_inplace(char_dest)
        except Exception as e:
            print(f"REMBG WARN: {e}", flush=True)
        ok += 1

    print(f"\nDone: {ok}/{total}", flush=True)
    return 0 if ok == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
