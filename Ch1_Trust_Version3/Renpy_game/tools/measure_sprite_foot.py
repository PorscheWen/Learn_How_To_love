# -*- coding: utf-8 -*-
r"""量立繪「腳底列」與留白，產生 scale.rpy SPRITE_FOOT 用的列。

用法（在 Renpy_game 下）：
  python tools\measure_sprite_foot.py char/char-yuan-cafe.png dog/dog-cafe-tense.png
  python tools\measure_sprite_foot.py --anim dog/cafe-sniff/dog-cafe-sniff-%02d.png 5

foot ＝ alpha>16 的最下面一列 + 1（Transform crop 高度；裁掉腳下透明列後 yanchor 1.0＝腳底）。
動畫幀取各幀最大值，避免某幀腳被裁掉。只讀檔、不改檔。
"""
import sys
from pathlib import Path
from PIL import Image
import numpy as np

ASSETS = Path(__file__).resolve().parents[2] / "assets"
ALPHA = 16


def measure(rel):
    im = Image.open(ASSETS / rel).convert("RGBA")
    a = np.array(im)[..., 3]
    ys, xs = np.where(a > ALPHA)
    w, h = im.size
    top, bot = int(ys.min()), int(ys.max())
    return dict(rel=rel, w=w, h=h, top=top, foot=bot + 1, content=bot - top + 1, padB=h - 1 - bot)


def row(m, note=""):
    return '        "%s": %d,  # %dx%d 內容高 %d 底留白 %d%s' % (m["rel"], m["foot"], m["w"], m["h"], m["content"], m["padB"], note)


def main(argv):
    out = []
    i = 0
    while i < len(argv):
        if argv[i] == "--anim":
            pat, n = argv[i + 1], int(argv[i + 2]); i += 3
            ms = [measure(pat % k) for k in range(1, n + 1)]
            foot = max(m["foot"] for m in ms)
            for m in ms:
                m["foot"] = foot
                out.append(row(m, "（動畫取各幀最大）"))
        else:
            out.append(row(measure(argv[i]))); i += 1
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
