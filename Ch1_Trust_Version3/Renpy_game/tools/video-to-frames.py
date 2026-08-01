# -*- coding: utf-8 -*-
r"""影片 → 去背序列 PNG 工具（Seedance 後處理）

從生成的 mp4 均勻抽 N 幀，將接近白色的背景轉為透明，輸出可直接給
Ren'Py Animation 使用的序列 PNG。

用法範例（PowerShell，在 Renpy_game 目錄下）：

  python tools\video-to-frames.py --video tools\output\seedance\dog-wag-test.mp4 `
      --frames 8 --name dog-wag --out tools\output\seedance\dog-wag

去背方式：從四角 flood fill 侵蝕近白色區域（只清外圍背景，
不會挖掉狗身上的淺色毛）。--tolerance 越大吃掉越多背景。

需求：ffmpeg（抽幀）、Pillow（去背）。
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image


def ffprobe_frame_count(video):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-count_frames", "-show_entries", "stream=nb_read_frames",
         "-of", "default=nw=1:nk=1", video],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return int(out)


def extract_frames(video, indices, tmp_dir):
    """用 ffmpeg select 過濾器一次抽出指定幀序號。"""
    expr = "+".join(f"eq(n\\,{i})" for i in indices)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", video,
         "-vf", f"select='{expr}'", "-vsync", "vfr",
         os.path.join(tmp_dir, "f-%03d.png")],
        check=True,
    )
    files = sorted(os.listdir(tmp_dir))
    if len(files) != len(indices):
        sys.exit(f"[錯誤] 預期抽出 {len(indices)} 幀，實際 {len(files)} 幀")
    return [os.path.join(tmp_dir, f) for f in files]


def remove_white_bg(img, tolerance):
    """從四角 flood fill，把連通的近白背景設為透明。"""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    threshold = 255 - tolerance

    def is_bg(p):
        r, g, b = p[0], p[1], p[2]
        return r >= threshold and g >= threshold and b >= threshold

    visited = bytearray(w * h)
    # 從整圈邊框像素出發，避免被前景（如狗腳）擋住而漏掉夾縫區域
    stack = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)] + \
            [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        idx = y * w + x
        if visited[idx]:
            continue
        visited[idx] = 1
        p = px[x, y]
        if not is_bg(p):
            continue
        px[x, y] = (p[0], p[1], p[2], 0)
        stack.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    return img


def main():
    p = argparse.ArgumentParser(description="影片抽幀 + 去背 → 序列 PNG")
    p.add_argument("--video", required=True, help="輸入 mp4 路徑")
    p.add_argument("--frames", type=int, default=8, help="要抽的幀數（預設 8）")
    p.add_argument("--name", default="frame", help="輸出檔名前綴（如 dog-wag → dog-wag-01.png）")
    p.add_argument("--out", required=True, help="輸出資料夾")
    p.add_argument("--tolerance", type=int, default=28,
                   help="白背判定容差 0~255（預設 28；背景有淡灰漸層時調大）")
    p.add_argument("--skip-tail", type=int, default=1,
                   help="略過結尾幀數（預設 1；循環動畫尾幀=首幀，避免重複）")
    p.add_argument("--no-alpha", action="store_true", help="不去背，直接輸出原幀")
    args = p.parse_args()

    if not os.path.exists(args.video):
        sys.exit(f"[錯誤] 找不到影片：{args.video}")
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        sys.exit("[錯誤] 需要 ffmpeg/ffprobe，請先安裝並加入 PATH")

    total = ffprobe_frame_count(args.video)
    usable = max(total - args.skip_tail, args.frames)
    indices = [round(i * (usable - 1) / (args.frames - 1)) for i in range(args.frames)] \
        if args.frames > 1 else [0]
    indices = sorted(set(min(i, total - 1) for i in indices))
    print(f"[抽幀] 影片共 {total} 幀，抽取序號：{indices}")

    os.makedirs(args.out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        raw_files = extract_frames(args.video, indices, tmp_dir)
        for i, path in enumerate(raw_files, start=1):
            img = Image.open(path)
            if not args.no_alpha:
                img = remove_white_bg(img, args.tolerance)
            out_path = os.path.join(args.out, f"{args.name}-{i:02d}.png")
            img.save(out_path)
            print(f"[輸出] {out_path}")

    print(f"[完成] {len(indices)} 幀已輸出到 {args.out}")
    print("[提示] Ren'Py 用法：Animation 依序列出各幀，或用 ATL：")
    print(f'  image {args.name}:')
    for i in range(1, len(indices) + 1):
        print(f'      "{args.name}-{i:02d}.png"')
        print("      pause 0.12")
    print("      repeat")


if __name__ == "__main__":
    main()
