"""Recalibrate dog pose scales + audit sprite overlaps after asset regen."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DOG_DIR = ROOT / "assets" / "dog"
CHAR_DIR = ROOT / "assets" / "char"
OUT = ROOT / "Renpy_game" / "tools" / "overlap-previews"
OUT.mkdir(parents=True, exist_ok=True)

SCREEN_W, SCREEN_H = 1280, 720
TEXTBOX = 108
CHAR_REF, DOG_REF = 1280.0, 1536.0
NEAR = 0.272  # dog_near after full-chapter ×0.8 baseline

# Target on-screen content height (px) at dog_near after recalibration.
# (Same visual targets as pre-×0.8; scale formula uses NEAR.)
TARGETS = {
    "dog-halfstep": 185,
    "dog-stair-watch": 160,
    "dog-kitchen-door": 160,
    "dog-leash-wait": 160,
    "dog-ear-flat": 152,
    "dog-street-tense": 148,
    "dog-sniff-wire": 144,
    "dog-sniff-bento": 175,
    "dog-coat-sniff": 140,
    "dog-chin-floor": 124,
    "dog-drink-bowl": 140,
    "dog-nose-fingertip": 148,
    "dog-harness-bite": 148,
    "dog-paper-bag-sniff": 144,
    "dog-refuse-stranger": 128,
    "dog-behind-legs": 132,
    "dog-forehead-nudge": 152,
    "dog-anxious": 136,
    "dog-parallel": 124,
    "dog-door-sleep": 120,
    "dog-guard-door": 128,
    "dog-shoe-sleep": 120,
    "dog-back-sleep": 120,
    "dog-check-sleep": 120,
    "dog-door-edge": 120,
}

# Tuned transforms (xalign, ypos, zoom) — feet above textbox; ×0.8 baseline.
CHAR_T = {
    "char_center": (0.50, 0.86, 0.384),
    "char_right": (0.74, 0.86, 0.36),
    "char_left": (0.26, 0.86, 0.36),
    "char_right_walk": (0.74, 0.86, 0.32),
    "char_sofa": (0.78, 0.86, 0.304),
}
DOG_T = {
    "dog_far": (0.58, 0.86, 0.208),
    "dog_mid": (0.50, 0.86, 0.24),
    "dog_near": (0.42, 0.86, 0.272),
    "dog_sofa_mid": (0.42, 0.86, 0.224),
    "dog_sofa_near": (0.38, 0.86, 0.24),
    "dog_sick_mid": (0.36, 0.86, 0.224),
    "dog_sick_far": (0.32, 0.86, 0.192),
    # Person on right (~0.74): dog between stranger (~0.26) and person
    "dog_far_pair": (0.50, 0.86, 0.176),
    "dog_mid_pair": (0.56, 0.86, 0.184),
    "dog_near_pair": (0.60, 0.86, 0.192),
    "dog_entrance_far": (0.50, 0.87, 0.192),
    "dog_entrance_mid": (0.54, 0.87, 0.216),
    "dog_far_walk": (0.30, 0.86, 0.192),
    "dog_mid_walk": (0.40, 0.86, 0.216),
    "dog_near_walk": (0.50, 0.86, 0.24),
}


def content_box(path: Path):
    im = Image.open(path).convert("RGBA")
    bb = im.split()[3].getbbox()
    return im, bb


def calc_scales() -> dict[str, float]:
    scales: dict[str, float] = {}
    print("=== DOG_POSE_SCALE (recalibrated) ===")
    for path in sorted(DOG_DIR.glob("dog-*.png")):
        stem = path.stem
        if stem == "dog-ref-canonical" or "bak" in stem:
            continue
        im, bb = content_box(path)
        if not bb:
            continue
        w, h = im.size
        ch = bb[3] - bb[1]
        target = TARGETS.get(stem, 180)
        scale = target * h / (ch * DOG_REF * NEAR)
        scales[stem] = round(scale, 3)
        zoom = (DOG_REF * scale) / h
        ch_screen = ch * zoom * NEAR
        print(
            f"  {stem:24} fill={ch/h:.2f} scale={scales[stem]:.3f} "
            f"-> near~{ch_screen:.0f}px"
        )
    return scales


def place(name: str, transform: str, is_dog: bool, scales: dict[str, float]):
    folder = DOG_DIR if is_dog else CHAR_DIR
    path = folder / f"{name}.png"
    im, bb = content_box(path)
    w, h = im.size
    xa, ypos, zoom = (DOG_T if is_dog else CHAR_T)[transform]
    if is_dog:
        ref = DOG_REF * scales.get(name, 1.0)
    else:
        ref = CHAR_REF
    total = (ref / h) * zoom
    dw, dh = w * total, h * total
    # Ren'Py xalign with yanchor 1.0: xpos = xalign * (screen_w - width) roughly
    # Actually for Transform xalign: the anchor point x is at xalign * screen
    # with default xanchor 0.5 for xalign... In Ren'Py, xalign sets both xpos and xanchor.
    # xalign 0.5 means center of displayable at 50% of screen.
    # So left = xa * SCREEN_W - dw/2
    x0 = xa * SCREEN_W - dw / 2
    y0 = ypos * SCREEN_H - dh  # yanchor 1.0
    ox0 = x0 + bb[0] * total
    oy0 = y0 + bb[1] * total
    ow = (bb[2] - bb[0]) * total
    oh = (bb[3] - bb[1]) * total
    return {
        "name": name,
        "transform": transform,
        "im": im,
        "total": total,
        "x0": x0,
        "y0": y0,
        "ox0": ox0,
        "oy0": oy0,
        "ow": ow,
        "oh": oh,
        "dw": dw,
        "dh": dh,
    }


def overlap_x(a, b) -> tuple[float, float]:
    ox = max(0.0, min(a["ox0"] + a["ow"], b["ox0"] + b["ow"]) - max(a["ox0"], b["ox0"]))
    pct = ox / min(a["ow"], b["ow"]) * 100 if min(a["ow"], b["ow"]) else 0
    return ox, pct


def textbox_cover(r) -> float:
    top = SCREEN_H - TEXTBOX
    return max(0.0, (r["oy0"] + r["oh"]) - top) / r["oh"] * 100 if r["oh"] else 0


def compose(label: str, layers: list, bg_color=(40, 36, 32)):
    canvas = Image.new("RGB", (SCREEN_W, SCREEN_H), bg_color)
    draw = ImageDraw.Draw(canvas, "RGBA")
    # fake textbox
    draw.rectangle(
        [(0, SCREEN_H - TEXTBOX), (SCREEN_W, SCREEN_H)],
        fill=(243, 233, 217, 230),
    )
    for r in layers:
        sprite = r["im"].resize(
            (max(1, int(r["dw"])), max(1, int(r["dh"]))), Image.Resampling.LANCZOS
        )
        canvas.paste(sprite, (int(r["x0"]), int(r["y0"])), sprite)
    safe = label.replace(" ", "_").replace("/", "-")
    out = OUT / f"{safe}.jpg"
    canvas.convert("RGB").save(out, quality=85)
    return out


def main() -> int:
    scales = calc_scales()
    print()

    pairs = [
        ("S02_meet", ("char-yuan-commute", "char_right", False), ("dog-anxious", "dog_far", True)),
        ("S02_close", ("char-yuan-squat-side", "char_right", False), ("dog-halfstep", "dog_mid", True)),
        ("S02_bento", ("char-yuan-squat-side", "char_right", False), ("dog-sniff-bento", "dog_mid", True)),
        ("S04_sofa", ("char-yuan-sofa", "char_sofa", False), ("dog-parallel", "dog_sofa_mid", True)),
        ("S04_chin", ("char-yuan-sofa", "char_sofa", False), ("dog-chin-floor", "dog_sofa_near", True)),
        ("S05_headphones", ("char-yuan-headphones-off", "char_right", False), ("dog-sniff-wire", "dog_mid", True)),
        ("S07_sick", ("char-yuan-sick-bed", "char_right", False), ("dog-guard-door", "dog_sick_mid", True)),
        ("S07_nose", ("char-yuan-sick-bed", "char_right", False), ("dog-nose-fingertip", "dog_near", True)),
        ("S08_harness", ("char-yuan-leash", "char_right", False), ("dog-harness-bite", "dog_entrance_mid", True)),
        ("S08_drink", ("char-yuan-leash", "char_right", False), ("dog-drink-bowl", "dog_entrance_mid", True)),
        ("S09_bag", ("char-yuan-leash", "char_right", False), ("dog-paper-bag-sniff", "dog_entrance_far", True)),
        ("S06_pair_chars", ("char-neighbor", "char_left", False), ("char-yuan-commute", "char_right", False)),
        ("S06_behind", ("char-yuan-commute", "char_right", False), ("dog-behind-legs", "dog_near_pair", True)),
        ("S06_nudge", ("char-yuan-commute", "char_right", False), ("dog-forehead-nudge", "dog_near_pair", True)),
        ("S08_walk", ("char-yuan-leash", "char_right_walk", False), ("dog-leash-wait", "dog_far_walk", True)),
        ("S08_near", ("char-yuan-leash", "char_right_walk", False), ("dog-leash-wait", "dog_near_walk", True)),
        ("S09_chars", ("char-coworker", "char_left", False), ("char-yuan-leash", "char_right", False)),
        ("S09_refuse", ("char-yuan-leash", "char_right", False), ("dog-refuse-stranger", "dog_near_pair", True)),
        ("S09_entrance", ("char-yuan-leash", "char_right", False), ("dog-leash-wait", "dog_entrance_far", True)),
        ("S01_clerk", ("char-clerk", "char_left", False), ("char-yuan-commute", "char_right", False)),
        ("S06_block", ("char-yuan-block", "char_right", False), ("dog-behind-legs", "dog_near_pair", True)),
    ]

    print("=== PAIR OVERLAP ===")
    issues = []
    for label, a_spec, b_spec in pairs:
        a = place(*a_spec, scales)
        b = place(*b_spec, scales)
        ox, pct = overlap_x(a, b)
        ca, cb = textbox_cover(a), textbox_cover(b)
        status = "OK"
        # Char-char: allow small gap; char-dog near_pair may intentionally overlap legs a bit
        if "pair_chars" in label or "chars" in label or "clerk" in label:
            if pct > 8:
                status = "WARN"
                issues.append((label, pct, "char-char overlap"))
        elif "behind" in label or "nudge" in label or "refuse" in label or "block" in label:
            # Intentional near-leg contact; warn only if glued (>55%) or detached (<3%)
            if pct > 55:
                status = "WARN"
                issues.append((label, pct, "pair dog too much on person"))
            elif pct < 3:
                status = "WARN"
                issues.append((label, pct, "pair dog too far from person"))
        else:
            if pct > 25:
                status = "WARN"
                issues.append((label, pct, "general overlap"))
        if ca > 18 or cb > 22:
            status = "WARN"
            issues.append((label, max(ca, cb), "textbox cover"))
        print(
            f"  {label:16} overlap={ox:.0f}px ({pct:.0f}%) "
            f"tb={ca:.0f}%/{cb:.0f}% [{status}]"
        )
        compose(label, [a, b])

    print()
    print("=== DOG SOLO TEXTBOX ===")
    solos = [
        ("dog-anxious", "dog_far"),
        ("dog-halfstep", "dog_mid"),
        ("dog-parallel", "dog_mid"),
        ("dog-kitchen-door", "dog_mid"),
        ("dog-shoe-sleep", "dog_near"),
        ("dog-back-sleep", "dog_near"),
        ("dog-check-sleep", "dog_mid"),
        ("dog-door-edge", "dog_far"),
        ("dog-door-sleep", "dog_far"),
        ("dog-guard-door", "dog_near"),
        ("dog-leash-wait", "dog_far_walk"),
        ("dog-behind-legs", "dog_near_pair"),
        ("dog-sniff-wire", "dog_mid"),
        ("dog-stair-watch", "dog_far"),
        ("dog-street-tense", "dog_far_walk"),
        ("dog-ear-flat", "dog_far"),
        ("dog-refuse-stranger", "dog_near_pair"),
        ("dog-forehead-nudge", "dog_near_pair"),
    ]
    for name, tr in solos:
        r = place(name, tr, True, scales)
        cov = textbox_cover(r)
        mark = "WARN" if cov > 22 else "OK"
        print(f"  {name:24} {tr:16} h={r['oh']:.0f} cover={cov:.0f}% [{mark}]")
        if cov > 22:
            issues.append((name, cov, "solo textbox"))

    print()
    print("=== SCALE DICT FOR script.rpy ===")
    print("DOG_POSE_SCALE = {")
    for stem, scale in sorted(scales.items()):
        print(f'        "dog/{stem}.png": {scale},')
    print("    }")

    print()
    if issues:
        print(f"ISSUES ({len(issues)}):")
        for item in issues:
            print(" ", item)
    else:
        print("No WARN issues under thresholds.")
    print(f"Previews -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
