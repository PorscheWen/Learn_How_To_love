# -*- coding: utf-8 -*-
"""第二批後處理：依動作特性挑幀＋亮度校正到原圖 → 正式資產目錄

挑幀策略：
- sniff-wire：幀 2,4,5,6,8 = 鼻碰線→抬起→再碰線 完整週期（順播 loop）
- drink-bowl：連續幀 2~6（ping-pong）
- farewell：依內容框寬度排序（尾巴掃地位置）3,7,4,6,2（ping-pong）
- guard-door：連續幀 2~6（ping-pong）
"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "assets", "dog"))

# pose -> 來源幀序（輸出依此順序重編 01~05）
PLAN = {
    "sniff-wire": [2, 4, 5, 6, 8],
    "drink-bowl": [2, 3, 4, 5, 6],
    "farewell": [3, 7, 4, 6, 2],
    "guard-door": [2, 3, 4, 5, 6],
}


def mean_lum(img):
    px = img.load()
    tot = 0.0
    n = 0
    for y in range(0, img.height, 4):
        for x in range(0, img.width, 4):
            r, g, b, a = px[x, y]
            if a > 0:
                tot += 0.299 * r + 0.587 * g + 0.114 * b
                n += 1
    return tot / max(n, 1)


def apply_gain(img, gain):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a > 0:
                px[x, y] = (min(int(r * gain), 255), min(int(g * gain), 255),
                            min(int(b * gain), 255), a)
    return img


for pose, order in PLAN.items():
    src = os.path.join(BASE, pose + "-frames")
    dst = os.path.join(ASSETS, pose)
    os.makedirs(dst, exist_ok=True)

    # 幀 01 = 原圖，作為亮度基準
    ref = Image.open(os.path.join(src, f"dog-{pose}-01.png")).convert("RGBA")
    target_lum = mean_lum(ref)

    for out_i, src_i in enumerate(order, start=1):
        img = Image.open(os.path.join(src, f"dog-{pose}-{src_i:02d}.png")).convert("RGBA")
        gain = target_lum / mean_lum(img)
        img = apply_gain(img, gain)
        out = os.path.join(dst, f"dog-{pose}-{out_i:02d}.png")
        img.save(out)
        print(f"{pose}: 幀{src_i:02d} gain={gain:.3f} -> {out}")
