#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""掃描狗／人立繪 pose scale：透明留白、zoom、連續 show 鏡頭跳變。"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
IMG = GAME / "images"
SCRIPT = (GAME / "script.rpy").read_text(encoding="utf-8")

DOG_REF_H = 1536.0
CHAR_REF_H = 1536.0  # char_sprite 同公式


@dataclass
class SpriteRow:
    rel: str
    kind: str  # dog | char
    scale: float
    canvas: tuple[int, int]
    bbox: tuple[int, int, int, int] | None
    top_pad_ratio: float
    bottom_pad_ratio: float
    zoom: float
    vis_w: float
    vis_h: float
    content_vis_h: float


def parse_scales() -> dict[str, tuple[str, float]]:
    """path -> (kind, scale)"""
    out: dict[str, tuple[str, float]] = {}
    block = SCRIPT.split("DOG_POSE_SCALE = {", 1)[1].split("\n    }", 1)[0]
    for m in re.finditer(r'"((?:dog)/[^"]+\.png)"\s*:\s*([\d.]+)', block):
        out[m.group(1)] = ("dog", float(m.group(2)))
    block = SCRIPT.split("CHAR_POSE_SCALE = {", 1)[1].split("\n    }", 1)[0]
    for m in re.finditer(r'"((?:char)/[^"]+\.png)"\s*:\s*([\d.]+)', block):
        out[m.group(1)] = ("char", float(m.group(2)))
    for m in re.finditer(
        r'image dog (\w+)\s*=\s*dog_sprite\(\s*\n?\s*"([^"]+)"[^)]*?(?:,\s*([\d.]+)\s*)?\)',
        SCRIPT,
        re.S,
    ):
        path = m.group(2)
        if m.group(3):
            out[path] = ("dog", float(m.group(3)))
    for m in re.finditer(
        r'image (\w+(?: \w+)*)\s*=\s*char_sprite\(\s*\n?\s*"([^"]+)"[^)]*?(?:,\s*([\d.]+)\s*)?\)',
        SCRIPT,
        re.S,
    ):
        path = m.group(2)
        if m.group(3):
            out[path] = ("char", float(m.group(3)))
    return out


def image_path(rel: str) -> Path | None:
    p = GAME / rel
    if p.is_file():
        return p
    p = IMG / rel.replace("dog/", "dog/").replace("char/", "char/")
    alt = IMG / Path(rel).name
    if (IMG / "dog" / Path(rel).name).is_file():
        return IMG / "dog" / Path(rel).name
    if (IMG / "char" / Path(rel).name).is_file():
        return IMG / "char" / Path(rel).name
    return None


def analyze(rel: str, kind: str, scale: float) -> SpriteRow | None:
    path = GAME / rel if (GAME / rel).is_file() else IMG / rel
    if not path.is_file():
        path = IMG / "dog" / Path(rel).name if kind == "dog" else IMG / "char" / Path(rel).name
    if not path.is_file():
        return None
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    bb = im.getbbox()
    ref = DOG_REF_H if kind == "dog" else CHAR_REF_H
    zoom = ref * scale / float(h)
    if not bb:
        return SpriteRow(rel, kind, scale, (w, h), None, 1.0, 1.0, zoom, w * zoom, h * zoom, 0.0)
    top_pad = bb[1] / h
    bottom_pad = (h - bb[3]) / h
    content_h = bb[3] - bb[1]
    return SpriteRow(
        rel,
        kind,
        scale,
        (w, h),
        bb,
        top_pad,
        bottom_pad,
        zoom,
        w * zoom,
        h * zoom,
        content_h * zoom,
    )


def parse_image_to_path() -> dict[str, str]:
    """show name -> png rel path (first arg of dog_sprite)."""
    m: dict[str, str] = {}
    for im in re.finditer(
        r'^image dog ([\w ]+?)\s*=\s*dog_sprite\(\s*\n?\s*"([^"]+)"',
        SCRIPT,
        re.M,
    ):
        m[im.group(1).strip()] = im.group(2)
    for im in re.finditer(
        r'^image (\w+(?: \w+)*)\s*=\s*char_sprite\(\s*\n?\s*"([^"]+)"',
        SCRIPT,
        re.M,
    ):
        m[im.group(1).strip()] = im.group(2)
    return m


def consecutive_show_blocks() -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in SCRIPT.splitlines():
        s = line.strip()
        if s.startswith("show dog ") or s.startswith("show yuan ") or s.startswith("show neighbor "):
            name = s.split(" at ", 1)[0].replace("show ", "").strip()
            current.append(name)
            continue
        if s.startswith("label ") or s.startswith("menu:") or s.startswith("scene "):
            if len(current) >= 2:
                blocks.append(current)
            current = []
            continue
        if current and (s.startswith("hide ") or s.startswith("jump ") or s.startswith("call ")):
            if len(current) >= 2:
                blocks.append(current)
            current = []
    if len(current) >= 2:
        blocks.append(current)
    return blocks


def main() -> int:
    scales = parse_scales()
    rows: list[SpriteRow] = []
    print("=== 逐檔摘要（dog_sprite / CHAR_POSE_SCALE 登記路徑）===\n")
    print(
        f"{'path':<42} {'canvas':>10} {'scale':>6} {'zoom':>7} "
        f"{'visW':>6} {'visH':>6} {'cntH':>6} {'top%':>6} {'bot%':>6}"
    )
    for rel in sorted(scales.keys()):
        kind, scale = scales[rel]
        row = analyze(rel, kind, scale)
        if row is None:
            print(f"[MISSING] {rel}")
            continue
        rows.append(row)
        print(
            f"{row.rel:<42} {row.canvas[0]}×{row.canvas[1]:>4} {row.scale:>6.3f} {row.zoom:>7.4f} "
            f"{row.vis_w:>6.0f} {row.vis_h:>6.0f} {row.content_vis_h:>6.0f} "
            f"{row.top_pad_ratio * 100:>5.1f} {row.bottom_pad_ratio * 100:>5.1f}"
        )

    print("\n=== 底部透明 >5%（易 yanchor 浮空）===\n")
    floaters = [r for r in rows if r.bottom_pad_ratio > 0.05]
    for r in sorted(floaters, key=lambda x: -x.bottom_pad_ratio):
        print(
            f"  {r.rel}: bottom {r.bottom_pad_ratio * 100:.1f}% canvas {r.canvas[0]}×{r.canvas[1]}"
        )

    img_map = parse_image_to_path()
    print("\n=== 連續 show 鏡頭：可見高/content 跳變 >20% ===\n")
    issues = 0
    for block in consecutive_show_blocks():
        metrics: list[tuple[str, float, float]] = []
        for name in block:
            path = img_map.get(name)
            if not path or path not in scales:
                continue
            kind, scale = scales[path]
            row = analyze(path, kind, scale)
            if row:
                metrics.append((name, row.content_vis_h, row.vis_w))
        for i in range(1, len(metrics)):
            prev_n, prev_h, prev_w = metrics[i - 1]
            cur_n, cur_h, cur_w = metrics[i]
            if prev_h <= 0:
                continue
            dh = abs(cur_h - prev_h) / prev_h
            dw = abs(cur_w - prev_w) / prev_w if prev_w else 0
            if dh > 0.20 or dw > 0.20:
                issues += 1
                print(
                    f"  {' → '.join(block[max(0, i - 1): i + 1])}: "
                    f"contentH {prev_h:.0f}→{cur_h:.0f} ({dh * 100:.0f}%), "
                    f"visW {prev_w:.0f}→{cur_w:.0f} ({dw * 100:.0f}%)"
                )
    if not issues:
        print("  （無超過 20% 的連續跳變）")

    print(f"\n[OK] scanned {len(rows)} sprites; floaters={len(floaters)}; seq_issues={issues}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
