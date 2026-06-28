"""Remove background from dog mood sprites (in-place overwrite with alpha PNG)."""
from pathlib import Path

try:
    from rembg import remove
    from PIL import Image
    USE_REMBG = True
except ImportError:
    from PIL import Image
    USE_REMBG = False


def remove_bg_pillow(img: Image.Image) -> Image.Image:
    """Fallback: key out white/cream paper and near-black backdrops."""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            spread = max(r, g, b) - min(r, g, b)
            if lum < 28 and spread < 35:
                px[x, y] = (r, g, b, 0)
            elif lum > 210 and spread < 45:
                px[x, y] = (r, g, b, 0)
            elif lum > 185 and spread < 30:
                px[x, y] = (r, g, b, max(0, int(255 - (lum - 185) * 6)))
    return img


def process(path: Path) -> None:
    raw = path.read_bytes()
    if USE_REMBG:
        out = remove(raw)
        img = Image.open(__import__("io").BytesIO(out)).convert("RGBA")
    else:
        img = remove_bg_pillow(Image.open(path))
    img.save(path, "PNG")
    print(f"OK {path.name}")


def main() -> None:
    base = Path(__file__).resolve().parent.parent / "assets"
    targets = sorted(base.glob("dog/dog-*.png")) + sorted(base.glob("scene/scene-*.png"))
    for p in targets:
        process(p)
    print(f"Done ({len(targets)} files, {'rembg' if USE_REMBG else 'pillow fallback'})")


if __name__ == "__main__":
    main()
