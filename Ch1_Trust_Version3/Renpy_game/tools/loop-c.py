# -*- coding: utf-8 -*-
"""Loop C：單段產線守門（無計時器）。

拍點未鎖 → 停產圖。已鎖 → 查缺檔、孤兒、同場寫死 zoom、別名重用、
對景（門／窗）人狗尺、同場狗頭距。
稿寫不新產 pose 時改出「要不要新圖」建議，不自動產 PNG、不刪資產；體感交 Loop B。
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

TOOLS = Path(__file__).resolve().parent
RENPY = TOOLS.parent
CH1 = RENPY.parent
GAME = RENPY / "game"
ASSETS = (CH1 / "assets").resolve()
SCRIPT = GAME / "script.rpy"

spec = importlib.util.spec_from_file_location("loop_b", TOOLS / "loop-b.py")
loop_b = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(loop_b)

spec_fit = importlib.util.spec_from_file_location("loop_c_fit", TOOLS / "loop_c_fit.py")
loop_c_fit = importlib.util.module_from_spec(spec_fit)
assert spec_fit.loader is not None
spec_fit.loader.exec_module(loop_c_fit)

SCALE_RPY = GAME / "scale.rpy"

SHOW_DOG_RE = loop_b.SHOW_DOG_RE
SCENE_BG_RE = loop_b.SCENE_BG_RE
GALLERY_RE = re.compile(r'(gallery/[^"\']+\.(?:png|webp|jpg))')
CHAR_SHOW_RE = re.compile(r"^\s*show yuan (\w+)", re.M)
INLINE_ZOOM_RE = re.compile(
    r"^\s*show dog \w+[^\n]*\bzoom\b|^\s*zoom\s+[\d.]+",
    re.M,
)
SPRITE_PATH_RE = re.compile(r'(?:dog_sprite|optional_background|char_sprite)\(\s*"([^"]+)"')
BODY_CUES = (
    (
        "蹲等",
        re.compile(r"蹲"),
        ("low", "sit", "parallel", "crouch", "guard_door", "shoe_sleep", "chin_floor"),
    ),
    (
        "探路",
        re.compile(r"探路|探鼻|探地面"),
        ("explore", "sniff", "leash_wait"),
    ),
    (
        "退縮",
        re.compile(r"退縮|縮回|縮回來|退開|退半步|不肯走"),
        ("retreat", "behind", "tense", "flinch", "freeze", "ear_flat", "anxious"),
    ),
    (
        "背對",
        re.compile(r"背對|背過身|轉過身"),
        ("back_sleep", "head_turn", "turn"),
    ),
)


def fail(msg: str) -> None:
    print(f"[C] FAIL {msg}", flush=True)


def loadable(rel: str) -> bool:
    rel = rel.replace("\\", "/")
    return (
        (GAME / rel).exists()
        or (GAME / "images" / rel).exists()
        or (ASSETS / rel).exists()
    )


def all_rpy() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in GAME.glob("*.rpy"))


def image_block(rpy: str, kind: str, name: str) -> str:
    pat = rf"^image {kind} {re.escape(name)}\b(.*?)(?=^image |\Z)"
    m = re.search(pat, rpy, re.M | re.S)
    return m.group(1)[:1200] if m else ""


def sprite_paths(block: str) -> list[str]:
    return loop_b.unique(SPRITE_PATH_RE.findall(block))


def pose_scale_override(block: str, rpy: str = "") -> str | None:
    m = re.search(
        r'dog_sprite\(\s*"[^"]+"(?:\s*,\s*"[^"]+")?\s*,\s*([0-9.]+)\s*[,)]',
        block,
    )
    if m:
        return m.group(1)
    # 2026-10-03：別名尺寫在表裡（key="路徑#別名"），image 定義不再寫數字
    k = re.search(r'\bkey\s*=\s*"([^"]+)"', block)
    if k and rpy:
        table = loop_c_fit.parse_pose_scales(rpy)
        if k.group(1) in table:
            return str(table[k.group(1)])
    return None


def lock_status(md: str) -> tuple[str, str]:
    if re.search(r"待鎖定|拍點未定|未鎖拍點", md):
        return "unlocked", "稿寫待鎖定／拍點未定"
    if "不新產 pose" in md or re.search(r"旁白\s*×\s*狗移動[^\n]*鎖定", md):
        return "locked_no_new", "旁白×狗移動已鎖；稿寫不新產 pose → 改出產圖建議"
    if re.search(r"落地畫面[^\n]*鎖定|鎖定旁白", md):
        return "locked", "落地畫面已鎖"
    if "### 旁白" in md and "pose" in md.lower():
        return "partial", "有對表但未標鎖定"
    return "unlocked", "沒有旁白×狗移動鎖定表"


def image_defined(rpy: str, kind: str, name: str) -> bool:
    return bool(re.search(rf"^image {kind} {re.escape(name)}\b", rpy, re.M))


def pose_ticks(cell: str) -> list[str]:
    tokens: list[str] = []
    for match in loop_b.TICK_RE.finditer(cell):
        token = match.group(1)
        if token in loop_b.NOT_POSE:
            continue
        if token.startswith("bg") or token.startswith("dog_") or token.startswith("char_"):
            continue
        tokens.append(token)
    return loop_b.unique(tokens)


def parse_shot_table(md: str) -> list[tuple[str, str, list[str]]]:
    rows: list[tuple[str, str, list[str]]] = []
    in_table = False
    for line in md.splitlines():
        if "旁白拍" in line and re.search(r"pose", line, re.I):
            in_table = True
            continue
        if not in_table:
            continue
        if re.match(r"^\|[\s:|-]+\|", line):
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        shot, pose_cell = cells[0], cells[1]
        if shot in ("旁白拍", "") or pose_cell == "pose":
            continue
        if set(shot) <= set("-: "):
            continue
        rows.append((shot, pose_cell, pose_ticks(pose_cell)))
    return rows


def pose_reads(names: list[str], needles: tuple[str, ...]) -> bool:
    blob = " ".join(names).lower()
    return any(n in blob for n in needles)


def primary_png(rpy: str, pose: str) -> str | None:
    paths = sprite_paths(image_block(rpy, "dog", pose))
    return paths[0] if paths else None


def pose_already_shown(pose: str, dogs: list[str], rpy: str) -> bool:
    if pose in dogs:
        return True
    if any(re.fullmatch(rf"s\d{{2}}_{re.escape(pose)}", d) for d in dogs):
        return True
    path = primary_png(rpy, pose)
    if not path:
        return False
    return any(primary_png(rpy, d) == path for d in dogs)


def advise_new_png(md: str, dogs: list[str], rpy: str) -> tuple[str, list[str]]:
    """已鎖段落：建議重用或考慮新產（不自動產圖）。"""
    rows = parse_shot_table(md)
    table_poses = loop_b.unique([p for _shot, _cell, poses in rows for p in poses])
    if not table_poses:
        table_poses = loop_b.md_pose_tokens(md)
    banned = set(loop_b.banned_tokens(md))

    missing_def: list[str] = []
    reusable: list[str] = []
    for pose in table_poses:
        if image_defined(rpy, "yuan", pose):
            continue
        if image_defined(rpy, "dog", pose):
            reusable.append(pose)
        elif pose not in banned:
            missing_def.append(pose)

    unread: list[str] = []
    for shot, pose_cell, poses in rows:
        dog_in_cell = [p for p in poses if not image_defined(rpy, "yuan", p)]
        empty = pose_cell.strip() in ("—", "-", "–") or not dog_in_cell
        if not empty:
            continue
        if re.search(r"不 show|無狗|不顯示", pose_cell + shot):
            continue
        for label, cue_re, needles in BODY_CUES:
            if not cue_re.search(shot):
                continue
            if pose_reads(list(dogs), needles):
                continue
            unread.append(f"旁白拍「{shot}」寫了{label}，pose 欄空白且本段 show 讀不出")

    reasons: list[str] = []
    if missing_def:
        joined = "、".join(f"`{p}`" for p in missing_def)
        reasons.append(f"稿表 pose 沒有 image dog 定義，無法重用：{joined}")
    reasons.extend(unread[:3])
    if reasons:
        return "consider", reasons

    why: list[str] = []
    if reusable:
        why.append(f"稿表 {len(reusable)} 個 pose 皆有圖可重用")
    else:
        why.append("沒有缺定義的稿表 pose")
    unshown = [p for p in reusable if not pose_already_shown(p, dogs, rpy)]
    if unshown:
        joined = "、".join(f"`{p}`" for p in unshown[:8])
        why.append(f"本段沒 show 的稿表 pose：{joined} → 改 show 即可")
    why.append("遠近改 xalign、頭距改 DOG_POSE_SCALE，不要重畫「變大」")
    return "reuse", why


def print_png_advice(verdict: str, reasons: list[str]) -> None:
    label = "考慮新產" if verdict == "consider" else "不新產"
    print(f"[C] 產圖建議：{label}", flush=True)
    for reason in reasons:
        print(f"[C]   · {reason}", flush=True)
    if verdict == "consider":
        print(
            "[C]   先問要不要產；未說「產這張」不要 Hermes／GenerateImage。"
            "頭距仍只改 DOG_POSE_SCALE",
            flush=True,
        )
    else:
        print("[C]   未說「產這張」不要 Hermes／GenerateImage", flush=True)


def list_pngs(*roots: Path) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        found.extend(root.rglob("*.png"))
        found.extend(root.rglob("*.webp"))
    return found


def orphan_dog_files(rpy: str) -> list[str]:
    used = set(re.findall(r'"((?:dog/)[^"]+\.(?:png|webp))"', rpy))
    used.update(re.findall(r'"((?:dog/)[^"]+)"', rpy))
    orphans: list[str] = []
    dog_root = ASSETS / "dog"
    if not dog_root.is_dir():
        return orphans
    for path in list_pngs(dog_root):
        rel = path.relative_to(ASSETS).as_posix()
        if rel not in used and rel.replace("\\", "/") not in used:
            # 動畫幀常只寫目錄樣板；檔名含 -01 且目錄有被引用則略過
            parent = path.parent.relative_to(ASSETS).as_posix()
            if any(u.startswith(parent + "/") or parent in u for u in used):
                continue
            orphans.append(rel)
    return orphans[:30]


def main() -> int:
    parser = argparse.ArgumentParser(description="Loop C：單段產線守門")
    parser.add_argument("section", nargs="?", help="S07 / 7 / 07")
    parser.add_argument("--orphans", action="store_true", help="加列 assets/dog 孤兒（全章）")
    args = parser.parse_args()

    if not SCRIPT.exists():
        fail(f"找不到 {SCRIPT}")
        return 2
    text = SCRIPT.read_text(encoding="utf-8")
    rpy = all_rpy()

    raw = (args.section or "").strip().upper().replace("SECTION", "").replace("S", "")
    nn = raw.zfill(2) if raw.isdigit() else None
    if nn is None:
        nn = loop_b.infer_nn(text)
    if nn is None:
        print("Usage: python tools/loop-c.py S07", flush=True)
        print("[C] 請指定一段 S01～S10；產圖前先跑本守門", flush=True)
        return 2
    if nn < "01" or nn > "10":
        fail(f"段落 {nn} 超出 S01～S10")
        return 2

    sliced = loop_b.slice_section(text, nn)
    if not sliced:
        fail(f"script.rpy 沒有 section_{nn}_* label")
        return 2
    full, slug, start, end, body = sliced
    md_path = loop_b.find_section_md(nn, slug)
    md = md_path.read_text(encoding="utf-8") if md_path and md_path.exists() else ""
    status, reason = lock_status(md) if md else ("unlocked", "找不到 section_*.md")

    dogs = loop_b.unique(SHOW_DOG_RE.findall(body))
    bgs = loop_b.unique(SCENE_BG_RE.findall(body))
    yuans = loop_b.unique(CHAR_SHOW_RE.findall(body))
    galleries = loop_b.unique(GALLERY_RE.findall(body))
    inline_zoom = bool(INLINE_ZOOM_RE.search(body))

    print("[C] Loop C 產線守門（改完／產圖前才跑，無計時器）", flush=True)
    print(f"[C] 段：S{nn}  label {full}  script.rpy:{start}-{end}", flush=True)
    print(f"[C] 稿：{md_path if md_path else '（缺）'}", flush=True)
    print(f"[C] 鎖定：{status}｜{reason}", flush=True)
    print(f"[C] show dog：{', '.join(dogs) or '—'}", flush=True)
    print(f"[C] scene bg：{', '.join(bgs) or '—'}", flush=True)
    print(f"[C] show yuan：{', '.join(yuans) or '—'}", flush=True)

    missing: list[str] = []
    aliases: list[str] = []
    pose_files: dict[str, tuple[str, str | None]] = {}
    for pose in dogs:
        block = image_block(rpy, "dog", pose)
        paths = sprite_paths(block)
        override = pose_scale_override(block, rpy)
        if not paths:
            fail(f"image dog {pose} 沒有 dog_sprite 路徑")
            missing.append(f"dog {pose}")
            continue
        primary, *rest = paths
        pose_files[pose] = (primary, override)
        exists = loadable(primary)
        note = f"{pose} → {primary}"
        if override:
            note += f"  scale={override}"
        if rest and not re.search(r"-\d{2}\.(?:png|webp)$", rest[0]):
            note += f"  fallback={rest[0]}"
            aliases.append(pose)
        elif rest:
            note += "  （動畫幀）"
        print(f"[C] pose {note}", flush=True)
        if not exists:
            alt = next((p for p in rest if loadable(p)), None)
            if alt:
                print(f"[C] HINT {pose} 主檔缺，目前吃 fallback {alt}", flush=True)
            else:
                fail(f"缺檔 {primary}（pose {pose}）")
                missing.append(primary)

    for bg in bgs:
        block = image_block(rpy, "bg", bg)
        paths = sprite_paths(block) or re.findall(r'"((?:bg/)[^"]+\.png)"', block)
        if not paths:
            print(f"[C] HINT image bg {bg} 路徑解析不到", flush=True)
            continue
        primary = paths[0]
        print(f"[C] bg {bg} → {primary}", flush=True)
        if not loadable(primary):
            fail(f"缺檔 {primary}（bg {bg}）")
            missing.append(primary)

    for rel in galleries:
        print(f"[C] gallery {rel}", flush=True)
        if not loadable(rel):
            fail(f"缺檔 {rel}")
            missing.append(rel)

    if inline_zoom:
        print("[C] HINT 本段 show dog 附近有寫死 zoom；遠近應只改 xalign／具名 transform", flush=True)

    if status in ("locked_no_new", "locked"):
        print("[C] 守門：缺檔只補「同名」或改 show 重用；新 PNG 見下方產圖建議", flush=True)
        print_png_advice(*advise_new_png(md, dogs, rpy))
        if nn == "08":
            print(
                "[C] HINT S08 閃避拍不新產：探路 `s08_explore`、驚嚇 `s08_startle`、"
                "抗拒 `s08_resist`、被帶半步 `leash_yank`→蹲 `leash`；頭距改 DOG_POSE_SCALE",
                flush=True,
            )
        if nn == "09":
            print("[C] HINT 鞋邊睡圖只在 S08 尾；S09 不要 overlay secret-shoe-sleep", flush=True)
    elif status == "partial":
        print("[C] 守門：先把旁白×狗移動表標鎖定，再決定產不產", flush=True)
    else:
        print("[C] STOP 產圖：拍點未鎖。只出待鎖定清單，不要 Hermes／GenerateImage", flush=True)

    fit_fails: list[str] = []
    if pose_files and SCALE_RPY.exists():
        scale_text = SCALE_RPY.read_text(encoding="utf-8")
        fit_fails, fit_hints = loop_c_fit.audit_section(
            body=body,
            rpy=rpy,
            scale_text=scale_text,
            pose_files=pose_files,
            assets=ASSETS,
            game=GAME,
        )
        for h in fit_hints:
            print(f"[C] HINT {h}", flush=True)
        for fmsg in fit_fails:
            fail(fmsg)

    if args.orphans:
        orphans = orphan_dog_files(rpy)
        if orphans:
            print(f"[C] HINT 孤兒 dog 檔（前 {len(orphans)}）：{', '.join(orphans[:12])}", flush=True)
        else:
            print("[C] 未掃到明顯孤兒 dog PNG（或 assets 無法列出）", flush=True)

    print("[C] 下一步：未鎖就停；已鎖先看產圖建議。缺檔補同名。頭距改 scale。體感走 Loop B。不要開遊戲。", flush=True)

    if status == "unlocked":
        print("[C] 結果：STOP 產圖", flush=True)
        return 2
    if missing:
        print(f"[C] 結果：FAIL 缺檔 {len(missing)}", flush=True)
        return 1
    if fit_fails:
        print(f"[C] 結果：FAIL 對景／頭距 {len(fit_fails)}", flush=True)
        return 1
    print("[C] 結果：可繼續（產圖與否依上方建議，未說「產這張」不產）", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
