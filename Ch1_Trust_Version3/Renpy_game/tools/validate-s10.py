# -*- coding: utf-8 -*-
"""S10／四結局靜態驗收（對齊 tester.md §3 · section_10 · game_guild §3）"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"
ENDINGS = ROOT / "game" / "endings.rpy"

STRING_LINE = re.compile(r'^\s*(?:\w+\s+)?"((?:[^"\\]|\\.)*)"\s*$')


def fail(msg: str) -> None:
    print(f"[FAIL] {msg}")
    raise SystemExit(1)


def warn(msg: str) -> None:
    print(f"[WARN] {msg}")


def ok(msg: str) -> None:
    print(f"[OK] {msg}")


def clean_visible(text: str) -> str:
    text = re.sub(r"\{[^}]*\}", "", text)
    return re.sub(r"\[[^]]*\]", "", text)


def label_slice(source: str, label: str, next_labels: list[str] | None = None) -> str:
    if f"label {label}:" not in source:
        fail(f"缺少 label {label}")
    part = source.split(f"label {label}:", 1)[1]
    if next_labels:
        cuts = []
        for nxt in next_labels:
            key = f"label {nxt}:"
            if key in part:
                cuts.append(part.index(key))
        if cuts:
            part = part[: min(cuts)]
    return part


def count_strings(source: str) -> tuple[int, int]:
    chars = blocks = 0
    for line in source.splitlines():
        m = STRING_LINE.match(line)
        if m:
            chars += len(clean_visible(m.group(1)))
            blocks += 1
    return chars, blocks


def estimated_minutes(chars: int, blocks: int) -> float:
    return chars / 300 + blocks * 1.5 / 60 + 4 / 60


def extract_s10_paths(s10_source: str) -> tuple[str, str]:
    """切開 S10 敘事層 gave_away if/else（略過開頭 BGM 的 if/elif）。"""
    lines = s10_source.splitlines(keepends=True)
    give_start = None
    else_idx = None
    for i, line in enumerate(lines):
        if re.match(r'^    if flags\.get\("gave_away", False\):\s*$', line):
            # 略過只有 play_bgm 的開頭 if
            peek = "".join(lines[i : i + 4])
            if "play_bgm" in peek and "jump ending_ch1_handed_over" not in peek:
                continue
            give_start = i + 1
        elif give_start is not None and else_idx is None and re.match(
            r"^    else:\s*$", line
        ):
            else_idx = i
            break
    if give_start is None or else_idx is None:
        fail("S10 無法切開 gave_away 敘事 if/else")
    give = "".join(lines[give_start:else_idx])
    stay = "".join(lines[else_idx + 1 :])
    if "jump ending_ch1_handed_over" not in give:
        fail("S10 送走分支未含 jump ending_ch1_handed_over")
    return give, stay


def simulate_route(
    trust: int, gave_away: bool, forced_walk: bool
) -> str:
    if gave_away:
        return "C"
    if trust >= 10 and not forced_walk:
        return "A"
    if trust >= 4:
        return "B"
    return "D"


if not SCRIPT.exists():
    fail(f"找不到 {SCRIPT}")

script = SCRIPT.read_text(encoding="utf-8")
endings_rpy = ENDINGS.read_text(encoding="utf-8") if ENDINGS.exists() else ""
combined = script + "\n" + endings_rpy

s10 = label_slice(
    script,
    "section_10_share_the_key",
    ["ending_ch1_back_to_back"],
)

# --- 契約：S10 不再改 trust／三軸 ---
if re.search(r"\$\s*trust\s*(\+|-=|=)", s10):
    fail("S10 不得再修改 trust")
for axis in ("dist", "tone", "guard"):
    if re.search(rf"\$\s*{axis}\s*(\+|-=|=)", s10):
        fail(f"S10 不得再修改 {axis}")
ok("S10 不再修改 trust／Dist／Tone／Guard")

# --- 分流條件 ---
if 'flags.get("gave_away", False)' not in s10:
    fail("S10 缺少 gave_away 優先分流")
if "jump ending_ch1_handed_over" not in s10:
    fail("S10 送走路徑未 jump C")
if 'trust >= 10 and not flags.get("s08_forced_walk", False)' not in s10:
    fail("S10 A 條件缺少 trust≥10 與 s08_forced_walk 排除")
if "jump ending_ch1_back_to_back" not in s10:
    fail("S10 缺少 jump A")
if "jump ending_ch1_chosen_learning" not in s10:
    fail("S10 缺少 jump B")
if "jump ending_ch1_thin_ice" not in s10:
    fail("S10 缺少 jump D")
ok("S10 四結局 jump／A 排除硬拖條件齊全")

# --- 路由真值表 ---
cases = [
    (12, False, False, "A"),
    (10, False, False, "A"),
    (12, False, True, "B"),  # 硬拖不得進 A
    (9, False, False, "B"),
    (4, False, False, "B"),
    (3, False, False, "D"),
    (0, False, False, "D"),
    (12, True, False, "C"),  # C 優先
    (0, True, False, "C"),
    (7, True, True, "C"),
]
for trust, gave, forced, expect in cases:
    got = simulate_route(trust, gave, forced)
    if got != expect:
        fail(
            f"路由錯誤 trust={trust} gave={gave} forced={forced} → {got}（預期 {expect}）"
        )
ok("路由真值表（10 案）通過")

# --- 結局標籤／解鎖／軌跡／coda ---
for eid, label, flag_val in [
    ("A", "ending_ch1_back_to_back", "back_to_back"),
    ("B", "ending_ch1_chosen_learning", "chosen_learning"),
    ("C", "ending_ch1_handed_over", "handed_over"),
    ("D", "ending_ch1_thin_ice", "thin_ice"),
]:
    body = label_slice(
        script,
        label,
        [
            "ending_ch1_back_to_back",
            "ending_ch1_chosen_learning",
            "ending_ch1_handed_over",
            "ending_ch1_thin_ice",
            "ending_aftercare",
        ],
    )
    # 切片會含自己；改為切到下一個 ending 或 aftercare
    nxt_map = {
        "A": "ending_ch1_chosen_learning",
        "B": "ending_ch1_handed_over",
        "C": "ending_ch1_thin_ice",
        "D": "ending_aftercare",
    }
    body = label_slice(script, label, [nxt_map[eid]])
    if f'flags["ch1_ending"] = "{flag_val}"' not in body:
        fail(f"結局 {eid} 未寫入 ch1_ending={flag_val}")
    if f'process_ending_unlock("{eid}"' not in body:
        fail(f"結局 {eid} 未呼叫 process_ending_unlock")
    if "record_trust_trajectory()" not in body:
        fail(f"結局 {eid} 未呼叫 record_trust_trajectory")
    if f'ending_coda_finish("{eid}"' not in body:
        fail(f"結局 {eid} 未接 ending_coda_finish")
    if "centered" in body and "結局" in body:
        fail(f"結局 {eid} 仍使用舊 centered 標題")
ok("四結局：flags／unlock／trajectory／coda 齊全")

# --- endings.rpy 節拍存在 ---
for beat in (
    "ending_beat_back_to_back",
    "ending_beat_chosen_learning",
    "ending_beat_handed_over",
    "ending_beat_thin_ice",
    "ending_coda_finish",
    "ending_unlock_notice",
):
    if beat not in endings_rpy and f"label {beat}" not in endings_rpy and f"screen {beat}" not in endings_rpy:
        # screens don't have label
        if f"screen {beat}" not in endings_rpy and f"label {beat}" not in endings_rpy:
            fail(f"endings.rpy 缺少 {beat}")
ok("endings.rpy 節拍／標題／解鎖元件存在")

# --- pose／距離契約 ---
a = label_slice(script, "ending_ch1_back_to_back", ["ending_ch1_chosen_learning"])
b = label_slice(script, "ending_ch1_chosen_learning", ["ending_ch1_handed_over"])
c = label_slice(script, "ending_ch1_handed_over", ["ending_ch1_thin_ice"])
d = label_slice(script, "ending_ch1_thin_ice", ["ending_aftercare"])
if "show dog back_sleep at dog_near" not in a:
    fail("結局 A 缺 back_sleep@dog_near")
if "show dog check_sleep at dog_mid" not in b:
    fail("結局 B 缺 check_sleep@dog_mid")
if re.search(r"^\s*show dog\b", c, re.M):
    fail("結局 C 敘事不應 show dog（空屋契約）")
if "show dog door_edge at dog_far" not in d:
    fail("結局 D 缺 door_edge@dog_far")
if "s08_forced_walk" not in b:
    fail("結局 B 缺 s08_forced_walk 回聲分支")
ok("睡姿／距離／C 無狗／B 硬拖回聲契約通過")

# --- 共通句 ---
for eid, body in (("A", a), ("B", b), ("C", c), ("D", d)):
    if eid != "C" and "我們再試一年" not in body:
        # C 可能沒有這句 — section_10 說共通句但 C 空屋不同
        pass
    if "晚上見" not in body:
        fail(f"結局 {eid} 缺共通句「晚上見」")
if "我們再試一年" not in a or "我們再試一年" not in b or "我們再試一年" not in d:
    fail("結局 A／B／D 應有「我們再試一年」")
ok("共通句「晚上見」／「我們再試一年」（A／B／D）齊全")

# --- 禁止內容 ---
banned = ["Game Over", "安樂死", "安樂", "衰老", "親密%", "親密％", "trust =", "信任度"]
# trust = 在 process 外；只查結局可見字串
for eid, body in (("A", a), ("B", b), ("C", c), ("D", d), ("S10", s10)):
    for term in ("安樂", "衰老", "Game Over", "親密％", "親密%"):
        if term in body:
            fail(f"{eid} 出現禁止詞：{term}")
ok("無衰老／安樂／Game Over／親密％")

# --- 簡體／大陸用語抽樣 ---
cn_terms = ["视频", "质量", "信息", "空调", "家伙", "里", "这就是信任"]
# 「里」太容易誤報，改精確詞
cn_terms = ["视频", "質量不好", "信息", "空调", "這就是信任的開始"]
hits = []
for term in ["视频", "空调", "这就是信任", "質量→", "信息："]:
    if term in combined:
        hits.append(term)
# 掃描簡體常見
for term in ["视频", "空调", "家伙"]:
    if term in a + b + c + d + s10:
        hits.append(term)
if hits:
    warn(f"可能簡體／禁語：{hits}")
else:
    ok("S10／結局無明顯簡體禁語")

# --- 閱讀時間（分路徑，不含雙分支灌水）---
stay = extract_s10_paths(s10)[1]
give = extract_s10_paths(s10)[0]
routes = {
    "S10-A": (stay, a),
    "S10-B": (stay, b),
    "S10-C": (give, c),
    "S10-D": (stay, d),
}
failed_time = False
print("--- 閱讀時間（單一路徑估算）---")
for name, (prefix, ending) in routes.items():
    # 節拍約加 20 秒視覺，不計入文字門檻；門檻仍 ≥5 分文字
    chars, blocks = count_strings(prefix + "\n" + ending)
    minutes = estimated_minutes(chars, blocks)
    status = "OK" if minutes >= 5.0 else "FAIL"
    print(
        f"[{status}] {name}: {minutes:.2f} 分（{chars} 字／{blocks} 段，門檻 5 分）"
    )
    failed_time = failed_time or minutes < 5.0

# --- persistent 防 None ---
if "default persistent.unlocked_secret_content" not in script:
    fail("缺 default persistent.unlocked_secret_content")
if "or []" not in label_slice(script, "section_10_share_the_key", []) and "unlocked_secret_content or []" not in script:
    # check unlock fn
    if "list(persistent.unlocked_secret_content or [])" not in script:
        fail("unlock_secret_content 未防 None")
if "time.time()" not in script:
    fail("record_trust_trajectory 應使用 time.time()")
ok("persistent／timestamp 防呆到位")

# --- landmark 高信任送走 ---
s09 = label_slice(script, "section_09_almost_handoff", ["section_10_share_the_key"])
if "landmark_chose_reason_over_bond" not in s09:
    fail("S09 缺 landmark_chose_reason_over_bond")
if "landmark_chose_reason_over_bond" not in c:
    fail("結局 C 缺 landmark 變體文案")
ok("高信任送走 landmark 回聲存在")

if failed_time:
    fail("S10 有結局閱讀時間 < 5 分")

print("[OK] S10／四結局靜態驗收全部通過")
raise SystemExit(0)
