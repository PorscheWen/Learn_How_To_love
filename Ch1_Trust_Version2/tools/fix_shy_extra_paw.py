"""Remove duplicate pink paw-pad cluster on viewer's right (extra left hind)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "assets" / "raw" / "shy-backs-goodish.png"
out = ROOT / "assets" / "dog" / "dog-shy.png"


def main() -> None:
    im = Image.open(src).convert("RGBA")
    arr = np.array(im)
    h, w = arr.shape[:2]
    rgb = arr[:, :, :3].astype(np.float32)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    pink = (r > 140) & (r > g + 10) & (r > b + 25) & (g > 80) & (b > 60) & (r < 240)
    pink[:, : w // 2] = False
    pink[: int(h * 0.35), :] = False
    pink[int(h * 0.85) :, :] = False

    ys, xs = np.where(pink)
    print(f"pink pixels right={len(xs)}")
    if len(xs) < 10:
        im.save(out)
        print("too few pink pixels; copied as-is")
        return

    pts = np.column_stack([xs.astype(np.float64), ys.astype(np.float64)])
    # 2-means without sklearn
    c0 = pts[0].copy()
    c1 = pts[len(pts) // 2].copy()
    for _ in range(20):
        d0 = np.linalg.norm(pts - c0, axis=1)
        d1 = np.linalg.norm(pts - c1, axis=1)
        lab = (d1 < d0).astype(np.int32)
        if lab.sum() == 0 or lab.sum() == len(lab):
            break
        c0 = pts[lab == 0].mean(axis=0)
        c1 = pts[lab == 1].mean(axis=0)

    # remove inward cluster (smaller x = closer to torso)
    remove = 0 if c0[0] < c1[0] else 1
    print(f"centers x=({c0[0]:.1f},{c1[0]:.1f}) remove={remove}")
    sel = pts[lab == remove]

    mask = np.zeros((h, w), dtype=np.uint8)
    for x, y in sel:
        x, y = int(x), int(y)
        mask[max(0, y - 3) : y + 4, max(0, x - 3) : x + 4] = 255
    mimg = Image.fromarray(mask).filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(3))
    mask_b = np.array(mimg) > 40

    out_arr = arr.copy()
    yy, xx = np.where(mask_b)
    for y, x in zip(yy, xx):
        sy = max(0, y - 20)
        sx = min(w - 1, max(0, x - 10))
        # prefer non-pink sample
        for _ in range(8):
            if not pink[sy, sx]:
                break
            sy = max(0, sy - 3)
            sx = max(0, sx - 2)
        out_arr[y, x, :3] = arr[sy, sx, :3]

    Image.fromarray(out_arr).save(out)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
