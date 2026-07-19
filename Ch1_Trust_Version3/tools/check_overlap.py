"""靜態重疊檢查：立繪橫向重疊與字幕框遮蓋比例（tester §6.3）。"""
from PIL import Image

SCREEN_W, SCREEN_H = 1280, 720
TEXTBOX = 108  # gui.textbox_height, yalign 1.0
CHAR_REF, DOG_REF = 1280.0, 1536.0

POSE_SCALE = {
    "dog-halfstep": 0.46, "dog-stair-watch": 0.46, "dog-leash-wait": 0.49,
    "dog-kitchen-door": 0.49, "dog-guard-door": 0.52, "dog-sniff-wire": 0.52,
    "dog-parallel": 0.40, "dog-shoe-sleep": 0.41, "dog-back-sleep": 0.39,
    "dog-check-sleep": 0.35, "dog-door-edge": 0.36, "dog-door-sleep": 0.37,
}
CHAR_T = {
    "char_center": (0.50, 1.02, 0.52), "char_right": (0.82, 1.02, 0.50),
    "char_left": (0.18, 1.02, 0.50), "char_right_walk": (0.90, 1.02, 0.42),
}
DOG_T = {
    "dog_far": (0.72, 1.03, 0.26), "dog_mid": (0.66, 1.04, 0.30),
    "dog_near": (0.58, 1.05, 0.34),
    "dog_far_pair": (0.62, 1.06, 0.22), "dog_mid_pair": (0.55, 1.07, 0.24),
    "dog_near_pair": (0.49, 1.08, 0.26),
    "dog_far_walk": (0.20, 1.06, 0.24), "dog_mid_walk": (0.36, 1.07, 0.27),
    "dog_near_walk": (0.52, 1.08, 0.30),
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
    x0 = xa * (SCREEN_W - dw)
    y0 = ypos * SCREEN_H - dh
    ox0, oy0 = x0 + ab[0] * total, y0 + ab[1] * total
    ow, oh = (ab[2] - ab[0]) * total, (ab[3] - ab[1]) * total
    return name, transform, ox0, oy0, ow, oh


def report(label, a, b):
    ax0, _, aw, _ = a[2:]
    bx0, _, bw, _ = b[2:]
    ox = max(0.0, min(ax0 + aw, bx0 + bw) - max(ax0, bx0))
    pct = ox / min(aw, bw) * 100
    print(
        f"{label}: {a[0]}({a[1]}) x=[{ax0:.0f},{ax0 + aw:.0f}] vs "
        f"{b[0]}({b[1]}) x=[{bx0:.0f},{bx0 + bw:.0f}] "
        f"overlap={ox:.0f}px ({pct:.0f}%)"
    )


def textbox_cover(r):
    _, _, _, y0, _, h = r
    top = SCREEN_H - TEXTBOX
    cover = max(0.0, (y0 + h) - top) / h * 100
    print(
        f"textbox: {r[0]}({r[1]}) height={h:.0f}px "
        f"y=[{y0:.0f},{y0 + h:.0f}] covered={cover:.0f}%"
    )


PAIRS = [
    ("S02 相遇", ("char-yuan-commute", "char_right", 0), ("dog-anxious", "dog_far", 1)),
    ("S02 靠近", ("char-yuan-commute", "char_right", 0), ("dog-halfstep", "dog_mid", 1)),
    ("S06 躲腿後", ("char-yuan-commute", "char_right", 0), ("dog-behind-legs", "dog_near_pair", 1)),
    ("S06 頂額", ("char-yuan-commute", "char_right", 0), ("dog-forehead-nudge", "dog_near_pair", 1)),
    ("S08 出發", ("char-yuan-leash", "char_right_walk", 0), ("dog-leash-wait", "dog_far_walk", 1)),
    ("S08 高信任", ("char-yuan-leash", "char_right_walk", 0), ("dog-leash-wait", "dog_near_walk", 1)),
    ("S09 拒絕", ("char-yuan-leash", "char_right", 0), ("dog-refuse-stranger", "dog_near", 1)),
    ("S09 交接遠", ("char-yuan-leash", "char_right", 0), ("dog-street-tense", "dog_far", 1)),
    ("S09 玄關", ("char-yuan-leash", "char_right", 0), ("dog-leash-wait", "dog_far", 1)),
    ("S06 兩人", ("char-neighbor", "char_left", 0), ("char-yuan-commute", "char_right", 0)),
    ("S09 兩人", ("char-coworker", "char_left", 0), ("char-yuan-leash", "char_right", 0)),
]

DOG_SOLO = [
    ("dog-anxious", "dog_far"), ("dog-halfstep", "dog_mid"),
    ("dog-parallel", "dog_mid"), ("dog-kitchen-door", "dog_mid"),
    ("dog-shoe-sleep", "dog_near"), ("dog-back-sleep", "dog_near"),
    ("dog-check-sleep", "dog_mid"), ("dog-door-edge", "dog_far"),
    ("dog-door-sleep", "dog_far"), ("dog-guard-door", "dog_near"),
    ("dog-leash-wait", "dog_far_walk"), ("dog-behind-legs", "dog_near_pair"),
    ("dog-sniff-wire", "dog_mid"), ("dog-stair-watch", "dog_far"),
    ("dog-street-tense", "dog_far_walk"), ("dog-ear-flat", "dog_far"),
]

for label, a_spec, b_spec in PAIRS:
    report(label, rect(*a_spec), rect(*b_spec))
print()
for name, transform in DOG_SOLO:
    textbox_cover(rect(name, transform, 1))
