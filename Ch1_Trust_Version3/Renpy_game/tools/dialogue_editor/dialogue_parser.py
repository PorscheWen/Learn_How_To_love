# -*- coding: utf-8 -*-
"""Parse Ren'Py script.rpy into editable dialogue / narration / choices."""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

SPEAKER_LABELS = {
    "ya": "予安",
    "clerk": "超商店員",
    "neighbor": "鄰居",
    "coworker": "同事",
    "thought": "心裡話",
}

SECTION_META: list[dict[str, str]] = [
    {"id": "s01", "label": "section_01_fluorescent_over_moon", "title": "S01｜螢幕光比月亮亮"},
    {"id": "s02", "label": "section_02_backdoor_glance", "title": "S02｜後門那一瞥"},
    {"id": "s03", "label": "section_03_gate_temp_border", "title": "S03｜大門的臨時國界"},
    {"id": "s04", "label": "section_04_shared_quiet", "title": "S04｜共享同一種安靜"},
    {"id": "s05", "label": "section_05_two_voices", "title": "S05｜你的聲音有兩種"},
    {"id": "s06", "label": "section_06_corridor_third_person", "title": "S06｜樓梯間的第三者"},
    {"id": "s07", "label": "section_07_sick_guard", "title": "S07｜她倒下的那天"},
    {"id": "s08", "label": "section_08_corner_walk", "title": "S08｜走到轉角就好"},
    {"id": "s09", "label": "section_09_almost_handoff", "title": "S09｜差點交給別人"},
    {"id": "s10", "label": "section_10_share_the_key", "title": "S10｜把鑰匙分給心跳"},
    {"id": "ending_a", "label": "ending_ch1_back_to_back", "title": "結局 A｜背靠"},
    {"id": "ending_b", "label": "ending_ch1_chosen_learning", "title": "結局 B｜選定但還在學"},
    {"id": "ending_c", "label": "ending_ch1_handed_over", "title": "結局 C｜送走"},
    {"id": "ending_d", "label": "ending_ch1_thin_ice", "title": "結局 D｜薄冰"},
]

LABEL_RE = re.compile(r"^label\s+([A-Za-z0-9_]+)\s*:")
DIALOGUE_RE = re.compile(
    r"^(\s*)(ya|clerk|neighbor|coworker|thought)\s+(\".*\"|'.*')\s*$"
)
NARRATION_RE = re.compile(r'^(\s*)(".*"|\'.*\')\s*$')
CHOICE_RE = re.compile(r'^(\s*)(".*"|\'.*\')\s*:\s*$')
MENU_RE = re.compile(r"^(\s*)menu\s*:")
COMMENT_NOTE_RE = re.compile(r"^(\s*)##?\s*(.+)$")


@dataclass
class EditItem:
    line: int
    kind: str  # narration | dialogue | thought | choice | note
    speaker: str | None
    speaker_label: str | None
    text: str
    menu_index: int | None = None
    choice_index: int | None = None
    readonly: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def unquote(raw: str) -> str:
    """Decode a Ren'Py / Python string literal including quotes."""
    try:
        value = ast.literal_eval(raw)
    except (SyntaxError, ValueError):
        # Fallback: strip outer quotes and unescape common sequences.
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
            inner = raw[1:-1]
            return (
                inner.replace("\\n", "\n")
                .replace("\\t", "\t")
                .replace('\\"', '"')
                .replace("\\'", "'")
                .replace("\\\\", "\\")
            )
        return raw
    if not isinstance(value, str):
        return str(value)
    return value


def quote(text: str) -> str:
    """Encode text as a double-quoted Ren'Py string literal."""
    escaped = (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def find_label_spans(lines: list[str]) -> dict[str, tuple[int, int]]:
    """Map label name → (start_line_1based inclusive, end_line_1based exclusive)."""
    starts: list[tuple[str, int]] = []
    for i, line in enumerate(lines):
        m = LABEL_RE.match(line)
        if m:
            starts.append((m.group(1), i))
    spans: dict[str, tuple[int, int]] = {}
    for idx, (name, start) in enumerate(starts):
        end = starts[idx + 1][1] if idx + 1 < len(starts) else len(lines)
        spans[name] = (start + 1, end + 1)  # 1-based, end exclusive
    return spans


def parse_section(lines: list[str], start: int, end: int) -> list[EditItem]:
    """Parse one label span into editable items. start/end are 1-based, end exclusive."""
    items: list[EditItem] = []
    in_menu = False
    menu_indent = -1
    menu_index = 0
    choice_index = 0

    for line_no in range(start, end):
        raw = lines[line_no - 1]
        stripped = raw.strip()
        if not stripped:
            continue

        indent = len(raw) - len(raw.lstrip(" "))

        menu_m = MENU_RE.match(raw)
        if menu_m:
            in_menu = True
            menu_indent = len(menu_m.group(1))
            menu_index += 1
            choice_index = 0
            continue

        # Leave menu when indent returns to menu level (or above) on a non-choice line
        if in_menu and indent <= menu_indent and not stripped.startswith("#"):
            in_menu = False

        # Choice lines (must check before plain narration)
        if in_menu:
            choice_m = CHOICE_RE.match(raw)
            if choice_m and indent > menu_indent:
                choice_index += 1
                items.append(
                    EditItem(
                        line=line_no,
                        kind="choice",
                        speaker=None,
                        speaker_label=None,
                        text=unquote(choice_m.group(2)),
                        menu_index=menu_index,
                        choice_index=choice_index,
                    )
                )
                continue

        dlg = DIALOGUE_RE.match(raw)
        if dlg:
            speaker = dlg.group(2)
            kind = "thought" if speaker == "thought" else "dialogue"
            items.append(
                EditItem(
                    line=line_no,
                    kind=kind,
                    speaker=speaker,
                    speaker_label=SPEAKER_LABELS.get(speaker, speaker),
                    text=unquote(dlg.group(3)),
                    menu_index=menu_index if in_menu else None,
                )
            )
            continue

        # Skip non-string statements
        if stripped.startswith("$") or stripped.startswith("python:") or stripped.startswith("init "):
            continue
        if stripped.startswith(
            (
                "show ",
                "hide ",
                "scene ",
                "with ",
                "play ",
                "stop ",
                "queue ",
                "window ",
                "nvl ",
                "jump ",
                "call ",
                "return",
                "pause ",
                "if ",
                "elif ",
                "else:",
                "while ",
                "for ",
                "define ",
                "default ",
                "image ",
                "transform ",
                "screen ",
                "label ",
                "menu:",
            )
        ):
            continue

        note_m = COMMENT_NOTE_RE.match(raw)
        if note_m and stripped.startswith("##"):
            note_text = note_m.group(2).strip()
            if note_text and not note_text.startswith("---"):
                if any(k in note_text for k in ("一件事", "情感", "信任", "閘門", "記憶", "▷")):
                    items.append(
                        EditItem(
                            line=line_no,
                            kind="note",
                            speaker=None,
                            speaker_label=None,
                            text=note_text,
                            readonly=True,
                        )
                    )
            continue

        if stripped.startswith("#"):
            continue

        narr = NARRATION_RE.match(raw)
        if narr:
            items.append(
                EditItem(
                    line=line_no,
                    kind="narration",
                    speaker=None,
                    speaker_label="旁白",
                    text=unquote(narr.group(2)),
                    menu_index=menu_index if in_menu else None,
                )
            )

    return items


def list_sections(script_path: Path) -> list[dict[str, Any]]:
    lines = script_path.read_text(encoding="utf-8").splitlines()
    spans = find_label_spans(lines)
    out: list[dict[str, Any]] = []
    for meta in SECTION_META:
        span = spans.get(meta["label"])
        if not span:
            continue
        items = parse_section(lines, span[0], span[1])
        editable = [i for i in items if not i.readonly]
        out.append(
            {
                **meta,
                "start_line": span[0],
                "end_line": span[1] - 1,
                "counts": {
                    "narration": sum(1 for i in editable if i.kind == "narration"),
                    "dialogue": sum(1 for i in editable if i.kind == "dialogue"),
                    "thought": sum(1 for i in editable if i.kind == "thought"),
                    "choice": sum(1 for i in editable if i.kind == "choice"),
                    "total": len(editable),
                },
            }
        )
    return out


def load_section(script_path: Path, section_id: str) -> dict[str, Any]:
    meta = next((m for m in SECTION_META if m["id"] == section_id), None)
    if not meta:
        raise KeyError(f"未知章節：{section_id}")
    lines = script_path.read_text(encoding="utf-8").splitlines()
    spans = find_label_spans(lines)
    span = spans.get(meta["label"])
    if not span:
        raise KeyError(f"找不到 label：{meta['label']}")
    items = parse_section(lines, span[0], span[1])
    return {
        **meta,
        "start_line": span[0],
        "end_line": span[1] - 1,
        "items": [i.to_dict() for i in items],
    }


def apply_changes(script_path: Path, changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply text edits by line number. Only rewrites the string payload."""
    if not changes:
        return {"ok": True, "updated": 0}

    lines = script_path.read_text(encoding="utf-8").splitlines(keepends=True)
    # Normalize to list without keepends for editing, then join with \n
    bare = [ln.rstrip("\r\n") for ln in lines]
    updated = 0
    errors: list[str] = []

    # Apply high→low so line numbers stay valid (same file, independent lines)
    ordered = sorted(changes, key=lambda c: int(c["line"]), reverse=True)
    for ch in ordered:
        line_no = int(ch["line"])
        new_text = ch.get("text", "")
        if line_no < 1 or line_no > len(bare):
            errors.append(f"行號超出範圍：{line_no}")
            continue
        raw = bare[line_no - 1]

        dlg = DIALOGUE_RE.match(raw)
        if dlg:
            bare[line_no - 1] = f"{dlg.group(1)}{dlg.group(2)} {quote(new_text)}"
            updated += 1
            continue

        choice_m = CHOICE_RE.match(raw)
        if choice_m:
            bare[line_no - 1] = f"{choice_m.group(1)}{quote(new_text)}:"
            updated += 1
            continue

        narr = NARRATION_RE.match(raw)
        if narr:
            bare[line_no - 1] = f"{narr.group(1)}{quote(new_text)}"
            updated += 1
            continue

        errors.append(f"第 {line_no} 行不是可編輯對白／旁白／選項")

    if updated:
        script_path.write_text("\n".join(bare) + "\n", encoding="utf-8")

    return {"ok": not errors, "updated": updated, "errors": errors}
