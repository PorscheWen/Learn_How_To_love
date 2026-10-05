# -*- coding: utf-8 -*-
"""Loop C 對景／頭距：門框量人狗、兩眼距量同場換 pose。

不產 PNG（除非 --preview）。偵測失敗只 HINT。
"""
from __future__ import annotations

import math
import re
from collections import deque
from pathlib import Path
from typing import Any

DOG_REF = 1536.0
CHAR_REF = 1280.0
SCREEN_H = 720.0
PUPPY_RATIO = 0.12 / 0.31
FEET_Y = 0.80
HINT_PCT = 10.0
FAIL_PCT = 18.0
PNG_SPAN_LO, PNG_SPAN_HI = 0.82, 1.22
# 低頭／橫躺／巷口牽繩族：畫法或畫布與母尺不同，禁止用兩眼距／頭框改已鎖 scale。
SKIP_EYE_SPAN = {
    "drink_bowl",
    "shoe_sleep",
    "harness_bite",
    "s08_tense",
    "s08_explore",
    "s08_startle",
    "s08_resist",
    # 紙袋那張：眼睛偵測常只抓到 1 眼、頭框吃進紙袋（2026-10-03 S09 實測建議 1.10→0.695 是假警報）
    "paper_bag",
    "paper_bag_s09",
}

DEPTH_SKIP = {"kitchen", "stairwell"}
CU_SKIP = {"living_wire", "entrance_nudge", "bedroom_nose", "nudge"}

MOTHER_POSE = {
    "living": "parallel",
    "entrance": "leash_wait",
    "alley": "leash_wait",
    "bedroom": "guard_door",
    "backdoor": "s04_anxious",
    "corridor": "s06_retreat",
}

BG_PLACE = {
    "entrance_day": "entrance",
    "entrance_night": "entrance",
    "living_day": "living",
    "living_night": "living",
    "living_dusk": "living",
    "alley_day": "alley",
    "alley_night": "alley",
    "kitchen_day": "kitchen",
    "kitchen_night": "kitchen",
    "bedroom_night": "bedroom",
    "backdoor_night": "backdoor",
    "stairwell_day": "stairwell",
    "stairwell_night": "stairwell",
    "gate_night": "gate",
    "street_night": "street",
    "office_night": "office",
    "cafe_day": "cafe",
    "clinic_night": "clinic",
    "convenience_night": "convenience",
}

# 720p 門／窗（油彩自動抓不穩，鎖定實測）
ANCHORS = {
    "entrance": {"kind": "door", "fit": "大門", "top": 58, "bot": 488},
    "gate": {"kind": "door", "fit": "鐵門", "top": 142, "bot": 516},
    "living": {"kind": "window", "fit": "落地窗（遠牆）", "top": 55, "bot": 445},
    "alley": {"kind": "foreground", "fit": "巷口前景（中景木門不同平面）"},
    "backdoor": {"kind": "door", "fit": "卸貨門", "top": 80, "bot": 536},
}

SHOW_AT_RE = re.compile(r"^\s*show dog (\w+)(?:\s+at\s+(\w+))?")
SHOW_YUAN_AT_RE = re.compile(r"^\s*show yuan (\w+)(?:\s+at\s+(\w+))?")
SCENE_RE = re.compile(r"^\s*scene bg (\w+)")
SCALE_ROW_RE = re.compile(
    r'"(\w+)":\s*\{\s*"char":\s*(None|[0-9.]+),\s*"dog":\s*'
    r'(None|_puppy\([0-9.]+\)|[0-9.]+),\s*"fit":\s*"([^"]*)"'
)
POSE_SCALE_RE = re.compile(r'"(dog/[^"]+)":\s*([0-9.]+)')
CHAR_SCALE_RE = re.compile(r'"(char/[^"]+)":\s*([0-9.]+)')
TRANSFORM_RE = re.compile(r"^transform (\w+):(.*?)(?=^transform |\Z)", re.M | re.S)
IMAGE_YUAN_RE = re.compile(
    r'^image yuan (\w+) = char_sprite\(\s*"([^"]+)"', re.M
)
# 2026-10-03 透視場（scale.rpy PERSP／PV_PT）：zoom 由腳底 y 算，不讀 SCALE 固定值
PERSP_RE = re.compile(r'"(\w+)":\s*\{"horizon":\s*(\d+),\s*"cam_h":\s*([0-9.]+)')
PV_PT_RE = re.compile(r'"(\w+)":\s*\(\s*"(\w+)",\s*(\d+),\s*(\d+)\s*\)')
KEY_RE = re.compile(r'\bkey\s*=\s*"([^"]+)"')


def _const(text: str, name: str, default: float) -> float:
    m = re.search(rf"^\s*{name}\s*=\s*([0-9.]+)", text, re.M)
    return float(m.group(1)) if m else default


def parse_persp(text: str) -> dict[str, tuple[int, float]]:
    return {m.group(1): (int(m.group(2)), float(m.group(3))) for m in PERSP_RE.finditer(text)}


def parse_pv_pt(text: str) -> dict[str, tuple[str, int, int]]:
    return {m.group(1): (m.group(2), int(m.group(3)), int(m.group(4))) for m in PV_PT_RE.finditer(text)}


def pv_points_used(body: str, rpy: str, pv: dict[str, tuple[str, int, int]]) -> set[str]:
    names = set(re.findall(r'"(\w+)"', body)) & set(pv)
    tf = {m.group(1): m.group(2) for m in TRANSFORM_RE.finditer(rpy)}
    for _kind, _name, at in walk_shows(body):
        if at and at in tf:
            names |= set(re.findall(r'"(\w+)"', tf[at][:600])) & set(pv)
    return names


def _eval_dog(raw: str) -> float | None:
    if raw == "None":
        return None
    m = re.match(r"_puppy\(([0-9.]+)\)", raw)
    if m:
        return round(float(m.group(1)) * PUPPY_RATIO, 3)
    return float(raw)


def parse_s08_alley(text: str) -> dict[str, float] | None:
    """scale.rpy S08_ALLEY 的 horizon／char_k／dog_ratio／size_y（缺任一項 → None）。"""
    m = re.search(r"S08_ALLEY\s*=\s*\{(.*?)\n\s*\}", text, re.S)
    if not m:
        return None
    out: dict[str, float] = {}
    for k in ("horizon", "char_k", "dog_ratio", "size_y"):
        km = re.search(r'"%s":\s*([0-9.]+)' % k, m.group(1))
        if not km:
            return None
        out[k] = float(km.group(1)) if "." in km.group(1) else int(km.group(1))
    return out


def parse_scale_rpy(text: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for m in SCALE_ROW_RE.finditer(text):
        place, char_s, dog_s, fit = m.group(1), m.group(2), m.group(3), m.group(4)
        out[place] = {
            "char": None if char_s == "None" else float(char_s),
            "dog": _eval_dog(dog_s),
            "fit": fit,
        }
    return out


def _strip_foot_table(script: str) -> str:
    # scale.rpy SPRITE_FOOT 也是 "dog/…": 數字 的格式（腳底列），不是 pose 尺
    return re.sub(r"SPRITE_FOOT\s*=\s*\{.*?\n\s*\}", "", script, flags=re.S)


def parse_pose_scales(script: str) -> dict[str, float]:
    return {k: float(v) for k, v in POSE_SCALE_RE.findall(_strip_foot_table(script))}


def parse_char_scales(script: str) -> dict[str, float]:
    return {k: float(v) for k, v in CHAR_SCALE_RE.findall(_strip_foot_table(script))}


def parse_transforms(rpy: str) -> tuple[dict[str, str], dict[str, str]]:
    dog_at: dict[str, str] = {}
    char_at: dict[str, str] = {}
    for m in TRANSFORM_RE.finditer(rpy):
        name, body = m.group(1), m.group(2)
        head = "\n".join(body.splitlines()[:24])
        dm = re.search(r'(?:sc_dog|s02_dog)\("(\w+)"', head)
        cm = re.search(r'(?:sc_char|s02_char)\("(\w+)"', head)
        if dm:
            dog_at[name] = dm.group(1)
        if cm:
            char_at[name] = cm.group(1)
    return dog_at, char_at


def parse_yuan_paths(rpy: str) -> dict[str, str]:
    out = dict(IMAGE_YUAN_RE.findall(rpy))
    # key="路徑#別名" → 用別名查 CHAR_POSE_SCALE（resolve_png 會去掉 #別名）
    for m in re.finditer(r"^image yuan (\w+) = char_sprite\(", rpy, re.M):
        chunk = rpy[m.end() : m.end() + 400].split("\nimage ", 1)[0].split("\n#", 1)[0]
        k = KEY_RE.search(chunk)
        if k:
            out[m.group(1)] = k.group(1)
    return out


def walk_shows(body: str) -> list[tuple[str, str, str | None]]:
    """(kind, name, at) in order; kind is bg／dog／yuan."""
    rows: list[tuple[str, str, str | None]] = []
    for line in body.splitlines():
        sm = SCENE_RE.match(line)
        if sm:
            rows.append(("bg", sm.group(1), None))
            continue
        dm = SHOW_AT_RE.match(line)
        if dm:
            rows.append(("dog", dm.group(1), dm.group(2)))
            continue
        ym = SHOW_YUAN_AT_RE.match(line)
        if ym:
            rows.append(("yuan", ym.group(1), ym.group(2)))
    return rows


def group_by_place(
    body: str, dog_at: dict[str, str]
) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    bg_place = None
    for kind, name, at in walk_shows(body):
        if kind == "bg":
            bg_place = BG_PLACE.get(name)
            continue
        if kind != "dog":
            continue
        place = dog_at.get(at or "") or bg_place
        if not place:
            continue
        grouped.setdefault(place, [])
        if name not in grouped[place]:
            grouped[place].append(name)
    return grouped


def first_yuan_in_place(
    body: str, char_at: dict[str, str], place: str
) -> str | None:
    bg_place = None
    for kind, name, at in walk_shows(body):
        if kind == "bg":
            bg_place = BG_PLACE.get(name)
            continue
        if kind != "yuan":
            continue
        p = char_at.get(at or "") or bg_place
        if p == place:
            return name
    return None


def resolve_png(rel: str, assets: Path, game: Path) -> Path | None:
    rel = rel.replace("\\", "/").split("#", 1)[0]
    for root in (assets, game, game / "images"):
        path = root / rel
        if path.exists():
            return path
    return None


def _cluster(points, min_size=3, max_size=55):
    s = set(points)
    seen = set()
    out = []
    for start in points:
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        blob = [start]
        while q:
            x, y = q.popleft()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n in s and n not in seen:
                    seen.add(n)
                    q.append(n)
                    blob.append(n)
        if min_size <= len(blob) <= max_size:
            out.append(blob)
    return out


def _bb(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def _ring(px, x, y, r, sw, sh):
    dark = amber = n = 0
    for deg in range(0, 360, 15):
        a = math.radians(deg)
        xx = int(round(x + r * math.cos(a)))
        yy = int(round(y + r * math.sin(a)))
        if not (0 <= xx < sw and 0 <= yy < sh):
            continue
        rr, g, b, al = px[xx, yy]
        if al < 50:
            continue
        n += 1
        if rr < 60 and g < 50:
            dark += 1
        elif rr > 100 and rr > g >= 35 and (rr - b) > 28:
            amber += 1
    return n, dark, amber


def _fur_bbox(px, box, sw, sh):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(sw, x1), min(sh, y1)
    pts = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if a < 50:
                continue
            if abs(r - g) < 14 and abs(g - b) < 14 and r < 150:
                continue
            pts.append((x, y))
    if not pts:
        return x0, y0, x1, y1
    return _bb(pts)


def measure_head(path: Path) -> dict[str, Any] | None:
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    f = 1.0
    small = im
    if w > 280:
        f = w / 280.0
        small = im.resize((280, max(1, int(round(h / f)))), Image.BILINEAR)
    px = small.load()
    sw, sh = small.size
    ob = small.split()[3].getbbox()
    if not ob:
        return None
    dark_pts = []
    for y in range(ob[1], ob[3]):
        for x in range(ob[0], ob[2]):
            r, g, b, a = px[x, y]
            if a > 180 and r < 42 and g < 36 and b < 36:
                dark_pts.append((x, y))
    eyes_all = []
    for blob in _cluster(dark_pts, 3, 55):
        x0, y0, x1, y1 = _bb(blob)
        bw, bh = x1 - x0, y1 - y0
        if bw > 16 or bh > 16 or bw < 2 or bh < 2:
            continue
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        n3, d3, _a3 = _ring(px, cx, cy, 3, sw, sh)
        _n6, _d6, a6 = _ring(px, cx, cy, 6, sw, sh)
        n9, d9, a9 = _ring(px, cx, cy, 9, sw, sh)
        if n3 and d3 / n3 < 0.35:
            continue
        if a6 + a9 < 4:
            continue
        if n9 and d9 / n9 > 0.55:
            continue
        eyes_all.append((a6 + a9 + d3 - d9, cx, cy, max(bw, bh)))
    eyes_all.sort(reverse=True)
    uniq = []
    for e in eyes_all:
        if any(math.hypot(e[1] - p[1], e[2] - p[2]) < 10 for p in uniq):
            continue
        uniq.append(e)
        if len(uniq) >= 6:
            break
    pair = []
    if len(uniq) >= 2:
        best = None
        for i, a in enumerate(uniq):
            for b in uniq[i + 1 :]:
                dy = abs(a[2] - b[2])
                dx = abs(a[1] - b[1])
                if dy > 14 or dx < 10 or dx > 70:
                    continue
                score = a[0] + b[0] - dy * 2
                if best is None or score > best[0]:
                    best = (score, a, b)
        if best:
            pair = [best[1], best[2]]
    if not pair and uniq:
        pair = [uniq[0]]
    span = 0.0
    eyes_n = len(pair)
    cw, ch = ob[2] - ob[0], ob[3] - ob[1]
    if eyes_n == 2:
        span = abs(pair[0][1] - pair[1][1]) * f
        xs = [e[1] for e in pair]
        ys = [e[2] for e in pair]
        mx, my = sum(xs) / 2, sum(ys) / 2
        sp = abs(pair[0][1] - pair[1][1])
        box = (mx - sp * 1.15, my - sp * 1.05, mx + sp * 1.15, my + sp * 1.35)
    elif eyes_n == 1:
        mx, my, d = pair[0][1], pair[0][2], max(pair[0][3], 6)
        k = 0.46 * min(cw, ch)
        box = (mx - k * 0.62, my - k * 0.55, mx + k * 0.48, my + k * 0.58)
    else:
        lying = cw / max(ch, 1) > 1.18
        if lying:
            box = (ob[0], ob[1], ob[0] + 0.36 * cw, ob[3])
        else:
            box = (ob[0], ob[1], ob[0] + 0.48 * cw, ob[1] + 0.55 * ch)
    hb = _fur_bbox(px, box, sw, sh)
    head_w = (hb[2] - hb[0]) * f
    head_h = (hb[3] - hb[1]) * f
    conf = 0.9 if eyes_n == 2 else (0.8 if eyes_n == 1 else 0.35)
    return {
        "canvas": (w, h),
        "span": span,
        "head_w": head_w,
        "head_h": head_h,
        "head": 0.5 * (head_w + head_h),
        "eyes": eyes_n,
        "conf": conf,
    }


def content_vis_h(path: Path, ref: float, pose_scale: float, scene_zoom: float) -> float:
    try:
        from PIL import Image
    except ImportError:
        return 0.0
    im = Image.open(path).convert("RGBA")
    box = im.split()[3].getbbox()
    if not box:
        return 0.0
    return (box[3] - box[1]) * (ref * pose_scale / im.size[1]) * scene_zoom


def pose_scale_for(rel: str, override: str | None, table: dict[str, float]) -> float:
    if override:
        return float(override)
    rel = rel.split("#", 1)[0] if rel not in table else rel
    if rel in table:
        return table[rel]
    name = Path(rel).name
    static = re.sub(r"-\d{2}\.(?:png|webp)$", r".png", name)
    for alt in (f"dog/{static}", f"dog/{static.replace('.png', '.webp')}"):
        if alt in table:
            return table[alt]
    return 1.0


def screen_span(m: dict[str, Any], pose_scale: float, dog_zoom: float) -> float:
    if not m or m["span"] <= 0:
        return 0.0
    return m["span"] * (DOG_REF * pose_scale / m["canvas"][1]) * dog_zoom


def screen_head(m: dict[str, Any], pose_scale: float, dog_zoom: float) -> float:
    if not m or m.get("head", 0) <= 0:
        return 0.0
    return m["head"] * (DOG_REF * pose_scale / m["canvas"][1]) * dog_zoom


def suggest_scale(cur: float, got: float, want: float) -> float:
    if got <= 0:
        return cur
    return round(cur * want / got, 3)


def audit_section(
    *,
    body: str,
    rpy: str,
    scale_text: str,
    pose_files: dict[str, tuple[str, str | None]],
    assets: Path,
    game: Path,
    preview_dir: Path | None = None,
) -> tuple[list[str], list[str]]:
    """Return (fails, hints). pose_files: pose → (primary_rel, override_scale)."""
    fails: list[str] = []
    hints: list[str] = []
    scales = parse_scale_rpy(scale_text)
    pose_scale = parse_pose_scales(rpy)
    char_scale = parse_char_scales(rpy)
    dog_at, char_at = parse_transforms(rpy)
    yuan_paths = parse_yuan_paths(rpy)
    persp = parse_persp(scale_text)
    pv = parse_pv_pt(scale_text)
    # 2026-10-03：透視 transform（pv_dz／pv_cz("點")）也要對到場名，否則分支線性走訪時會落到前一個 bg
    for m in TRANSFORM_RE.finditer(rpy):
        head = "\n".join(m.group(2).splitlines()[:24])
        dm = re.search(r'pv_dz\("(\w+)"', head)
        cm = re.search(r'pv_cz\("(\w+)"', head)
        if dm and dm.group(1) in pv:
            dog_at.setdefault(m.group(1), pv[dm.group(1)][0])
        if cm and cm.group(1) in pv:
            char_at.setdefault(m.group(1), pv[cm.group(1)][0])
    grouped = group_by_place(body, dog_at)
    s08 = parse_s08_alley(scale_text)
    pv_used = pv_points_used(body, rpy, pv)
    person_h = _const(scale_text, "PERSON_H_M", 1.62)
    walk_px = _const(scale_text, "WALK_PX", 1197.5)
    dog_ratio = _const(scale_text, "DOG_PERSON_RATIO", 0.3346)

    for place, poses in grouped.items():
        sc = scales.get(place, {})
        fit = sc.get("fit") or ANCHORS.get(place, {}).get("fit", place)
        char_z = sc.get("char")
        dog_z = sc.get("dog")
        feet_y = SCREEN_H * FEET_Y
        ys = sorted(pv[n][2] for n in pv_used if pv[n][0] == place)
        if place in persp and ys:
            hor, cam = persp[place]
            feet_y = ys[len(ys) // 2]
            char_z = round(person_h / (cam * walk_px) * (feet_y - hor), 4)
            dog_z = round(char_z * dog_ratio, 4)
            fit = f"透視 PERSP（horizon {hor}／cam_h {cam}；本段腳底中位 y={feet_y}）"
        elif place == "alley" and s08:
            # S08 巷口：讀 scale.rpy S08_ALLEY（只讀不改；size_y 處的人／狗 zoom）
            feet_y = s08["size_y"]
            char_z = round(s08["char_k"] * (feet_y - s08["horizon"]), 4)
            dog_z = round(char_z * s08["dog_ratio"], 4)
            fit = (f"S08_ALLEY（horizon {s08['horizon']}／char_k {s08['char_k']}／"
                   f"dog_ratio {s08['dog_ratio']}；size_y={feet_y}）")
        print(f"[C] 場 {place}  對景={fit}  char={char_z}  dog={dog_z}", flush=True)

        if place in DEPTH_SKIP or place in CU_SKIP:
            print(f"[C] 場 {place}  深度／特寫例外，不套同場頭距", flush=True)
            continue

        anchor = ANCHORS.get(place)
        yuan = first_yuan_in_place(body, char_at, place)
        if anchor and char_z and yuan:
            rel = yuan_paths.get(yuan)
            png = resolve_png(rel, assets, game) if rel else None
            if png:
                ps = char_scale.get(rel, 1.0) if rel else 1.0
                vis = content_vis_h(png, CHAR_REF, ps, char_z)
                if vis:
                    head_y = feet_y - vis
                    if anchor.get("kind") == "door":
                        door_h = anchor["bot"] - anchor["top"]
                        ratio = vis / door_h if door_h else 0
                        lintel = anchor["top"]
                        note = (
                            f"人 visH={vis:.0f}  門高={door_h}  "
                            f"人/門={ratio:.2f}  頭頂y={head_y:.0f} 楣={lintel}"
                        )
                        print(f"[C] 對景 {place}  {note}", flush=True)
                        base = re.sub(r"_s\d\d$", "", yuan)
                        squat = base in {"leash", "squat_side"} or "squat" in base
                        if squat:
                            if ratio > 0.72:
                                fails.append(
                                    f"{place} 蹲姿幾乎跟{anchor['fit']}一樣高（{note}；應約 0.50–0.68）"
                                )
                            elif ratio < 0.45:
                                hints.append(f"{place} 蹲姿相對{anchor['fit']}偏矮（{note}）")
                        elif ratio > 1.02 or head_y < lintel - 8:
                            fails.append(f"{place} 人高過{anchor['fit']}（{note}）")
                        elif ratio < 0.60:
                            hints.append(f"{place} 人相對{anchor['fit']}偏矮（{note}）")
                    elif anchor.get("kind") == "window":
                        win_h = anchor["bot"] - anchor["top"]
                        ratio = vis / win_h if win_h else 0
                        note = (
                            f"人 visH={vis:.0f}  窗高={win_h}  人/窗={ratio:.2f}  "
                            f"（遠牆，人可略高於窗）"
                        )
                        print(f"[C] 對景 {place}  {note}", flush=True)
                        if ratio > 1.45 or ratio < 0.70:
                            hints.append(f"{place} 人相對{anchor['fit']} {note}")
                    else:
                        frac = vis / SCREEN_H
                        print(
                            f"[C] 對景 {place}  人 visH={vis:.0f}  佔屏={frac:.2f}  {anchor['fit']}",
                            flush=True,
                        )
                        if frac > 0.70 or frac < 0.38:
                            hints.append(f"{place} 前景人 visH 佔屏 {frac:.2f}（{anchor['fit']}）")

        if not dog_z:
            continue

        rows = []
        for pose in poses:
            info = pose_files.get(pose)
            if not info:
                continue
            rel, override = info
            png = resolve_png(rel, assets, game)
            if not png:
                continue
            m = measure_head(png)
            if not m:
                hints.append(f"{pose} 頭距量不到（缺 Pillow 或空圖）")
                continue
            ps = pose_scale_for(rel, override, pose_scale)
            span_s = screen_span(m, ps, dog_z)
            head_s = screen_head(m, ps, dog_z)
            vis = content_vis_h(png, DOG_REF, ps, dog_z)
            rows.append((pose, m, ps, span_s, vis, rel, head_s))
            print(
                f"[C] 頭距 {pose}  eyes={m['eyes']} conf={m['conf']:.2f} "
                f"span={m['span']:.0f}px  screen={span_s:.1f}  "
                f"head={head_s:.1f}  visH={vis:.0f}  scale={ps:.3f}",
                flush=True,
            )

        if len(rows) < 2:
            continue
        mother_name = MOTHER_POSE.get(place)
        # 透視場變體（*_pv／*_s09）與母尺同 PNG → 去尾碼比對（2026-10-03）
        mom = next((r for r in rows if re.sub(r"_(?:pv|s\d\d)$", "", r[0]) == mother_name), None)
        if mom is None:
            mom = next((r for r in rows if r[1]["eyes"] == 2), rows[0])
        print(f"[C] 頭距母尺 {place}＝{mom[0]}  screen={mom[3]:.1f}", flush=True)

        standing = next((r for r in rows if r[4] > 0 and not _lying_name(r[0])), None)
        yuan_rel = yuan_paths.get(yuan) if yuan else None
        yuan_png = resolve_png(yuan_rel, assets, game) if yuan_rel else None
        if standing and yuan_png and char_z:
            ps = char_scale.get(yuan_rel, 1.0)
            char_vis = content_vis_h(yuan_png, CHAR_REF, ps, char_z)
            if char_vis > 0 and standing[4] / char_vis > 0.50:
                fails.append(
                    f"{place} 站姿 {standing[0]} visH/{yuan}={standing[4]/char_vis:.2f}（幼犬應約 0.28–0.37）"
                )
            elif char_vis > 0:
                print(
                    f"[C] 幼犬比 {place}  {standing[0]} visH/{yuan}={standing[4]/char_vis:.2f}",
                    flush=True,
                )

        for pose, m, ps, span_s, vis, rel, head_s in rows:
            if pose == mom[0]:
                continue
            if pose in SKIP_EYE_SPAN:
                continue
            mom_span, mom_head = mom[3], mom[6]
            use_span = (
                m["eyes"] == 2
                and mom[1]["eyes"] == 2
                and span_s > 0
                and mom_span > 0
            )
            png_ratio = (
                m["span"] / mom[1]["span"] if use_span and mom[1]["span"] else 0
            )
            painted_alike = PNG_SPAN_LO <= png_ratio <= PNG_SPAN_HI
            if use_span and painted_alike:
                got, want, kind = span_s, mom_span, "兩眼距"
            elif (not use_span) and head_s > 0 and mom_head > 0 and m["conf"] >= 0.75:
                got, want, kind = head_s, mom_head, "頭框"
            elif use_span and not painted_alike:
                continue
            else:
                hints.append(
                    f"{place} {pose} 頭距信心不足（{m['eyes']}眼），不改 scale"
                )
                continue
            delta = (got - want) / want * 100
            need = suggest_scale(ps, got, want)
            msg = (
                f"{place} {pose} {kind}相對 {mom[0]} Δ{delta:+.0f}%  "
                f"scale {ps:.3f}→{need:.3f}"
            )
            if abs(delta) < HINT_PCT:
                continue
            if kind == "兩眼距" and abs(delta) >= FAIL_PCT:
                fails.append(msg + "（畫布／scale 讓頭忽大忽小）")
            else:
                hints.append(msg)

    _ = preview_dir
    return fails, hints


def _lying_name(pose: str) -> bool:
    return any(
        k in pose
        for k in ("sleep", "parallel", "low", "chin", "door_edge", "guard_door")
    )
