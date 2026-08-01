# -*- coding: utf-8 -*-
"""把動畫幀依 --pad 幾何反向裁回原圖區域，使其與靜態 PNG 完全同框。

背景：seedance-generate.py --pad 會把原圖置中墊到 4:3／3:4 白畫布（margin 0.1），
抽幀後畫布幾何改變（底部留白變大），yanchor 1.0 貼底錨點下狗會浮空。
本腳本將每幀裁回「原圖在畫布中的區域」再放大回原圖尺寸，
之後 DOG_POSE_SCALE 直接沿用靜態圖原值即可。

pad 幾何（margin=0.1, usable=0.8）：
  橫式原圖 1536x1024 → 畫布 1920x1440 → 720p 影片 1112x834（縮 0.579167）
    原圖區域（幀座標）= (111, 120)-(1001, 714) → resize 回 1536x1024
  直式原圖 1024x1536 → 畫布 1440x1920 → 影片 834x1112（縮 0.579167）
    原圖區域（幀座標）= (120, 111)-(714, 1001) → resize 回 1024x1536
"""
import os
import shutil
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(BASE, "..", "..", "..", "..", "assets", "dog"))
BACKUP = os.path.join(BASE, "prenorm-backup")

# pose -> (crop box, 原圖尺寸)
LANDSCAPE = ((111, 120, 1001, 714), (1536, 1024))
PORTRAIT = ((120, 111, 714, 1001), (1024, 1536))
PLAN = {
    "door-sleep": LANDSCAPE,
    "back-sleep": LANDSCAPE,
    "check-sleep": LANDSCAPE,
    "door-edge": LANDSCAPE,
    "guard-door": LANDSCAPE,
    "sniff-wire": PORTRAIT,
    "drink-bowl": PORTRAIT,
    "farewell": PORTRAIT,
}

for pose, (box, size) in PLAN.items():
    src_dir = os.path.join(ASSETS, pose)
    bak_dir = os.path.join(BACKUP, pose)
    os.makedirs(bak_dir, exist_ok=True)
    for i in range(1, 6):
        name = f"dog-{pose}-{i:02d}.png"
        path = os.path.join(src_dir, name)
        shutil.copy2(path, os.path.join(bak_dir, name))
        img = Image.open(path).convert("RGBA")
        out = img.crop(box).resize(size, Image.LANCZOS)
        out.save(path)
        print(f"{pose}/{name}: {img.size} -> crop{box} -> {size}")
