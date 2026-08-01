# -*- coding: utf-8 -*-
"""全遊戲線資產靜態驗收：
1. scene/show 引用的 image 都有定義
2. at 引用的 transform 都有定義
3. play_bgm/dog_sfx 的 key 都在對照表
4. 引用的實體檔案（bg/dog/char/audio/gallery）是否存在（缺檔=警告，引擎會退 fallback）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
## options.rpy 會把 Version3/assets 加進 config.searchpath
ASSETS = (ROOT / ".." / "assets").resolve()
SCRIPT = (GAME / "script.rpy").read_text(encoding="utf-8")
SCREENS = (GAME / "screens.rpy").read_text(encoding="utf-8")
ALL_RPY = "\n".join(
    p.read_text(encoding="utf-8") for p in GAME.glob("*.rpy")
)

fails: list[str] = []
warns: list[str] = []


def fail(msg: str) -> None:
    fails.append(msg)
    print(f"[FAIL] {msg}")


def warn(msg: str) -> None:
    warns.append(msg)
    print(f"[WARN] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def loadable(rel: str) -> bool:
    """模擬 renpy.loadable：game/、game/images/ 與 Version3/assets 搜尋路徑。"""
    return (
        (GAME / rel).exists()
        or (GAME / "images" / rel).exists()
        or (ASSETS / rel).exists()
    )


# ---------- 1. image 定義 vs scene/show 使用 ----------
## `image x = ...` 與 ATL `image x:` 兩種寫法都算定義
defined_images = set(re.findall(r"^image ([\w ]+?)\s*[:=]", ALL_RPY, re.M))

used_images = set()
for m in re.finditer(r"^\s*(?:scene|show)\s+([a-z][\w ]*?)(?:\s+at\s|\s+with\s|\s*:|\s*$)", ALL_RPY, re.M):
    name = m.group(1).strip()
    if name in ("expression", "black") or name.startswith("screen "):
        continue
    used_images.add(name)

missing_defs = sorted(u for u in used_images if u not in defined_images)
if missing_defs:
    for u in missing_defs:
        fail(f"scene/show 使用未定義 image：{u}")
else:
    ok(f"scene/show 引用 {len(used_images)} 個 image 全部有定義")

# ---------- 2. transform 定義 vs at 使用 ----------
BUILTIN_TF = {
    "left", "right", "center", "truecenter", "top", "topleft", "topright",
    "default", "reset",
}
defined_tf = set(re.findall(r"^transform (\w+)", ALL_RPY, re.M))
used_tf = set(re.findall(r"\bat ([a-z]\w+)", ALL_RPY))
missing_tf = sorted(t for t in used_tf if t not in defined_tf and t not in BUILTIN_TF)
if missing_tf:
    for t in missing_tf:
        fail(f"at 使用未定義 transform：{t}")
else:
    ok(f"at 引用 {len(used_tf)} 個 transform 全部有定義")

# ---------- 3. BGM／SFX key ----------
alias_block = SCRIPT.split("aliases = {", 1)[1].split("}", 1)[0]
bgm_keys = set(re.findall(r'"(\w+)":', alias_block))
used_bgm = set(re.findall(r'play_bgm\(\s*"(\w+)"', ALL_RPY))
missing_bgm = sorted(used_bgm - bgm_keys)
if missing_bgm:
    for k in missing_bgm:
        fail(f"play_bgm 用了未登記 profile：{k}")
else:
    ok(f"play_bgm {len(used_bgm)} 個 profile 全部在對照表")

sfx_block = SCRIPT.split("DOG_SFX = {", 1)[1].split("}", 1)[0]
sfx_keys = set(re.findall(r'"(\w+)":', sfx_block))
used_sfx = set(re.findall(r'dog_sfx\(\s*"(\w+)"', ALL_RPY))
missing_sfx = sorted(used_sfx - sfx_keys)
if missing_sfx:
    for k in missing_sfx:
        fail(f"dog_sfx 用了未登記 cue：{k}")
else:
    ok(f"dog_sfx {len(used_sfx)} 個 cue 全部在對照表")

# ---------- 4. 實體檔案存在性（缺檔=警告：引擎退 fallback） ----------
ref_paths = set()
for pat in (
    r'optional_background\(\s*\n?\s*"([^"]+)"',
    r'dog_sprite\("([^"]+)"',
    r'char_sprite\("([^"]+)"',
    r'"((?:audio|gallery|theme|bg|dog|char)/[^"]+\.(?:png|jpg|webp|ogg|wav|mp3))"',
):
    ref_paths.update(re.findall(pat, ALL_RPY))
    ref_paths.update(re.findall(pat, SCREENS))

by_kind: dict[str, list[str]] = {}
for rel in sorted(ref_paths):
    if "%" in rel:  # python 樣板字串，非實際路徑
        continue
    if not loadable(rel):
        kind = rel.split("/", 1)[0]
        by_kind.setdefault(kind, []).append(rel)

present = len(ref_paths) - sum(len(v) for v in by_kind.values())
ok(f"引用實體檔案 {len(ref_paths)} 個，存在 {present} 個")
for kind, lst in sorted(by_kind.items()):
    warn(f"{kind}/ 缺 {len(lst)} 個檔（引擎退 fallback）：{', '.join(Path(p).name for p in lst[:8])}"
         + ("…" if len(lst) > 8 else ""))

# ---------- 結果 ----------
print()
if fails:
    print(f"共 {len(fails)} 項 FAIL、{len(warns)} 項 WARN")
    raise SystemExit(1)
print(f"[OK] 引用一致性全部通過（{len(warns)} 項缺檔警告）")
raise SystemExit(0)
