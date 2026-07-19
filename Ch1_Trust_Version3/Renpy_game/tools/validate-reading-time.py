from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "game" / "script.rpy"
TEXT = SCRIPT.read_text(encoding="utf-8")

STRING_LINE = re.compile(r'^\s*(?:\w+\s+)?"((?:[^"\\]|\\.)*)"\s*$')

SECTIONS = [
    ("S01", "section_01_fluorescent_over_moon"),
    ("S02", "section_02_backdoor_glance"),
    ("S03", "section_03_stairwell_temp_border"),
    ("S04", "section_04_shared_quiet"),
    ("S05", "section_05_two_voices"),
    ("S06", "section_06_corridor_third_person"),
    ("S07", "section_07_sick_guard"),
    ("S08", "section_08_corner_walk"),
    ("S09", "section_09_almost_handoff"),
    ("S10", "section_10_share_the_key"),
]

ENDINGS = [
    ("A", "ending_ch1_back_to_back"),
    ("B", "ending_ch1_chosen_learning"),
    ("C", "ending_ch1_handed_over"),
    ("D", "ending_ch1_thin_ice"),
]


def clean_visible(text: str) -> str:
    text = re.sub(r"\{[^}]*\}", "", text)
    return re.sub(r"\[[^]]*\]", "", text)


def label_slice(label: str, next_label: str | None) -> str:
    part = TEXT.split(f"label {label}:", 1)[1]
    if next_label:
        part = part.split(f"label {next_label}:", 1)[0]
    return part


def shortest_menu_route_stats(source: str) -> tuple[int, int, int]:
    """Count shared text plus the shortest textual branch of every menu."""
    lines = source.splitlines()
    chars = blocks = 0
    menus: list[list[tuple[int, int]]] = []

    for index, line in enumerate(lines):
        match = STRING_LINE.match(line)
        if match:
            chars += len(clean_visible(match.group(1)))
            blocks += 1

        if not re.match(r"^\s*menu:\s*$", line):
            continue

        menu_indent = len(line) - len(line.lstrip())
        branches: list[tuple[int, int]] = []
        cursor = index + 1

        while cursor < len(lines):
            indent = len(lines[cursor]) - len(lines[cursor].lstrip())
            if lines[cursor].strip() and indent <= menu_indent:
                break

            is_choice = (
                indent == menu_indent + 4
                and re.match(r'^\s*"[^"]+":\s*$', lines[cursor])
            )
            if is_choice:
                branch_chars = branch_blocks = 0
                branch_cursor = cursor + 1
                while branch_cursor < len(lines):
                    branch_indent = len(lines[branch_cursor]) - len(
                        lines[branch_cursor].lstrip()
                    )
                    if (
                        lines[branch_cursor].strip()
                        and branch_indent <= menu_indent + 4
                    ):
                        break
                    branch_match = STRING_LINE.match(lines[branch_cursor])
                    if branch_match:
                        branch_chars += len(clean_visible(branch_match.group(1)))
                        branch_blocks += 1
                    branch_cursor += 1
                branches.append((branch_chars, branch_blocks))
            cursor += 1

        if branches:
            menus.append(branches)

    for branches in menus:
        chars -= sum(item[0] for item in branches) - min(item[0] for item in branches)
        blocks -= sum(item[1] for item in branches) - min(item[1] for item in branches)

    return chars, blocks, len(menus)


def estimated_minutes(chars: int, blocks: int, menus: int = 0) -> float:
    # 保守估算：300 個中文字／分＋每次點擊 1.5 秒＋每組選項 9 秒＋標題卡 4 秒。
    return chars / 300 + blocks * 1.5 / 60 + menus * 0.15 + 4 / 60


results: list[tuple[str, float, int, int]] = []
for index, (name, label) in enumerate(SECTIONS[:-1]):
    next_label = SECTIONS[index + 1][1]
    chars, blocks, menus = shortest_menu_route_stats(label_slice(label, next_label))
    results.append((name, estimated_minutes(chars, blocks, menus), chars, blocks))

s10_shared = shortest_menu_route_stats(
    label_slice(SECTIONS[-1][1], ENDINGS[0][1])
)
for index, (ending_name, ending_label) in enumerate(ENDINGS):
    next_label = ENDINGS[index + 1][1] if index + 1 < len(ENDINGS) else None
    ending = shortest_menu_route_stats(label_slice(ending_label, next_label))
    chars = s10_shared[0] + ending[0]
    blocks = s10_shared[1] + ending[1]
    results.append(
        (f"S10-{ending_name}", estimated_minutes(chars, blocks), chars, blocks)
    )

failed = False
for name, minutes, chars, blocks in results:
    minimum = 8.0 if name in {"S08", "S09"} else 5.0
    status = "OK" if minutes >= minimum else "FAIL"
    print(
        f"[{status}] {name}: {minutes:.2f} 分 "
        f"（最短路徑 {chars} 字／{blocks} 段，門檻 {minimum:.0f} 分）"
    )
    failed = failed or minutes < minimum

raise SystemExit(1 if failed else 0)
