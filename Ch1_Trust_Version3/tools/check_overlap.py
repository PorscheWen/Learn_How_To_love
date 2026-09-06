"""靜態重疊檢查：立繪橫向重疊與字幕框遮蓋比例（tester §6.3）。

與 script.rpy transforms／DOG_POSE_SCALE 同步；重產資產後請先跑
`python tools/recalibrate_sprites.py` 再視需要微調本檔。
"""
from PIL import Image

SCREEN_W, SCREEN_H = 1280, 720
TEXTBOX = 108  # gui.textbox_height, yalign 1.0
CHAR_REF, DOG_REF = 1280.0, 1536.0

POSE_SCALE = {
    "dog-anxious": 1.575,
    "dog-s04-anxious": 0.551,
    "dog-back-sleep": 0.427,
    "dog-behind-legs": 0.535,
    "dog-check-sleep": 0.452,
    "dog-door-edge": 0.434,
    "dog-door-sleep": 0.42,
    "dog-ear-flat": 0.695,
    "dog-ear-perk": 0.414,
    "dog-chin-hover": 0.558,
    "dog-head-turn": 0.369,
    "dog-forehead-nudge": 0.543,
    "dog-guard-door": 0.438,
    "dog-halfstep": 0.687,
    "dog-kitchen-door": 0.577,
    "dog-leash-wait": 0.556,
    "dog-parallel": 0.524,
    "dog-refuse-stranger": 0.656,
    "dog-shoe-sleep": 0.414,
    "dog-sniff-wire": 0.71,
    "dog-stair-watch": 0.615,
    "dog-street-tense": 0.808,
}
CHAR_T = {
    "char_center": (0.50, 0.86, 0.384),
    "char_right": (0.74, 0.86, 0.36),
    "char_left": (0.26, 0.86, 0.36),
    "char_right_walk": (0.74, 0.86, 0.32),
}
DOG_T = {
    "dog_far": (0.58, 0.86, 0.208),
    "dog_mid": (0.50, 0.86, 0.24),
    "dog_near": (0.42, 0.86, 0.272),
    "dog_far_pair": (0.50, 0.86, 0.176),
    "dog_mid_pair": (0.56, 0.86, 0.184),
    "dog_near_pair": (0.60, 0.86, 0.192),
    "dog_nudge": (0.68, 0.86, 0.224),
    "dog_entrance_far": (0.50, 0.87, 0.192),
    "dog_entrance_mid": (0.54, 0.87, 0.216),
    "dog_far_walk": (0.30, 0.86, 0.192),
    "dog_mid_walk": (0.40, 0.86, 0.216),
    "dog_near_walk": (0.50, 0.86, 0.24),
}


def rect(name, transform, is_dog):
    folder = "dog" if is_dog else "char"
    img = Image.open(f"assets/{folder}/{name}.png").convert("RGBA")
    w, h = img.size
    ab = img.split()[3].getbbox()
    xa, ypos, zoom = (DOG_T if is_dog else CHAR_T)[transform]
    ref = DOG_REF * POSE_SCALE.get(name, 1.0) if is_dog else CHAR_REF
    total = (ref / h) * zoom
    dw, dh = w * total, h * total
    # Ren'Py xalign：displayable 中心對齊螢幕 xalign
    x0 = xa * SCREEN_W - dw / 2
    y0 = ypos * SCREEN_H - dh
    ox0, oy0 = x0 + ab[0] * total, y0 + ab[1] * total
    ow, oh = (ab[2] - ab[0]) * total, (ab[3] - ab[1]) * total
    return name, transform, ox0, oy0, ow, oh


def report(label, a, b):
    ax0, _, aw, _ = a[2:]
    bx0, _, bw, _ = b[2:]
    ox = max(0.0, min(ax0 + aw, bx0 + bw) - max(ax0, bx0))
    pct = ox / min(aw, bw) * 100 if min(aw, bw) else 0
    print(
        f"{label}: {a[0]}({a[1]}) x=[{ax0:.0f},{ax0 + aw:.0f}] vs "
        f"{b[0]}({b[1]}) x=[{bx0:.0f},{bx0 + bw:.0f}] "
        f"overlap={ox:.0f}px ({pct:.0f}%)"
    )


def textbox_cover(r):
    _, _, _, y0, _, h = r
    top = SCREEN_H - TEXTBOX
    cover = max(0.0, (y0 + h) - top) / h * 100 if h else 0
    print(
        f"textbox: {r[0]}({r[1]}) height={h:.0f}px "
        f"y=[{y0:.0f},{y0 + h:.0f}] covered={cover:.0f}%"
    )


PAIRS = [
    ("S02 相遇", ("char-yuan-commute", "char_right", 0), ("dog-s04-anxious", "dog_far", 1)),
    ("S02 靠近", ("char-yuan-commute", "char_right", 0), ("dog-halfstep", "dog_mid", 1)),
    ("S06 躲腿後", ("char-yuan-commute", "char_right", 0), ("dog-behind-legs", "dog_near_pair", 1)),
    ("S06 頂額單圖", ("dog-forehead-nudge", "dog_nudge", 1), ("dog-forehead-nudge", "dog_nudge", 1)),
    ("S08 出發", ("char-yuan-leash", "char_right_walk", 0), ("dog-leash-wait", "dog_far_walk", 1)),
    ("S08 高信任", ("char-yuan-leash", "char_right_walk", 0), ("dog-leash-wait", "dog_near_walk", 1)),
    ("S09 拒絕", ("char-yuan-leash", "char_right", 0), ("dog-refuse-stranger", "dog_near_pair", 1)),
    ("S09 交接遠", ("char-yuan-leash", "char_right", 0), ("dog-street-tense", "dog_mid_pair", 1)),
    ("S09 玄關", ("char-yuan-leash", "char_right", 0), ("dog-leash-wait", "dog_entrance_far", 1)),
    ("S06 兩人", ("char-neighbor", "char_left", 0), ("char-yuan-commute", "char_right", 0)),
    ("S09 兩人", ("char-coworker", "char_left", 0), ("char-yuan-leash", "char_right", 0)),
    ("S01 店員", ("char-clerk", "char_left", 0), ("char-yuan-commute", "char_right", 0)),
    ("S05 耳機", ("char-yuan-headphones", "char_right", 0), ("dog-sniff-wire", "dog_mid", 1)),
    ("S06 擋人", ("char-yuan-block", "char_right", 0), ("dog-behind-legs", "dog_near_pair", 1)),
]

DOG_SOLO = [
    ("dog-s04-anxious", "dog_far"), ("dog-anxious", "dog_far"), ("dog-halfstep", "dog_mid"),
    ("dog-parallel", "dog_mid"), ("dog-kitchen-door", "dog_mid"),
    ("dog-shoe-sleep", "dog_near"), ("dog-back-sleep", "dog_near"),
    ("dog-check-sleep", "dog_mid"), ("dog-door-edge", "dog_far"),
    ("dog-door-sleep", "dog_far"), ("dog-guard-door", "dog_near"),
    ("dog-leash-wait", "dog_far_walk"), ("dog-behind-legs", "dog_near_pair"),
    ("dog-sniff-wire", "dog_mid"), ("dog-stair-watch", "dog_far"),
    ("dog-street-tense", "dog_far_walk"), ("dog-ear-flat", "dog_far"),
    ("dog-refuse-stranger", "dog_near_pair"), ("dog-forehead-nudge", "dog_nudge"),
]

for label, a_spec, b_spec in PAIRS:
    if a_spec == b_spec:
        r = rect(*a_spec)
        print(f"{label}: solo {r[0]}({r[1]}) x=[{r[2]:.0f},{r[2]+r[4]:.0f}]")
        textbox_cover(r)
        continue
    report(label, rect(*a_spec), rect(*b_spec))
print()
for name, transform in DOG_SOLO:
    textbox_cover(rect(name, transform, 1))
