# -*- coding: utf-8 -*-
"""Tone audit dump for Ch1 Trust V3 dialogue."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import dialogue_parser as p

SCRIPT = HERE.parents[1] / "game" / "script.rpy"

ABSTRACT = re.compile(
    r"(借(?!錢)|睡成|蓋章|切開兩個|兩個世界|記進身體|談好條件|"
    r"恢復成只剩|用很大的手|翻書|把陌生|半公分|那一軌|很少播放|"
    r"不借|像對合約|唯一還熱|變空的安靜|刺耳)"
)
METAPHOR_HEAVY = re.compile(r"像(?!是|要|在|有|被|把)")
EMDASH = re.compile(r"[—–-]{1,2}")


def score_line(text: str) -> list[str]:
    flags: list[str] = []
    if ABSTRACT.search(text):
        flags.append("abstract")
    if text.count("像") >= 2 or ( "像" in text and len(text) > 40 and ("——" in text or "—" in text)):
        flags.append("metaphor_stack")
    if len(text) >= 72:
        flags.append("long")
    if text.count("——") + text.count("—") >= 2:
        flags.append("emdash_heavy")
    # poetic compression that often confuses
    if re.search(r"把.{1,8}(成|進|回|成了)", text) and "像" in text:
        flags.append("poetic_compress")
    return flags


def main() -> None:
    all_items = []
    for sec in p.list_sections(SCRIPT):
        data = p.load_section(SCRIPT, sec["id"])
        for it in data["items"]:
            if it.get("readonly"):
                continue
            flags = score_line(it["text"])
            all_items.append(
                {
                    "id": sec["id"],
                    "title": sec["title"],
                    "line": it["line"],
                    "kind": it["kind"],
                    "speaker": it.get("speaker_label"),
                    "text": it["text"],
                    "len": len(it["text"]),
                    "flags": flags,
                }
            )

    flagged = [x for x in all_items if x["flags"]]
    by_sec: dict[str, list] = {}
    for x in flagged:
        by_sec.setdefault(x["id"], []).append(x)

    report = {
        "total_editable": len(all_items),
        "flagged": len(flagged),
        "by_section_counts": {
            sid: {
                "total": sum(1 for x in all_items if x["id"] == sid),
                "flagged": len(items),
                "kinds": {
                    k: sum(1 for x in all_items if x["id"] == sid and x["kind"] == k)
                    for k in ("narration", "dialogue", "thought", "choice")
                },
            }
            for sid, items in [(s["id"], by_sec.get(s["id"], [])) for s in p.list_sections(SCRIPT)]
        },
        "priority": [
            x
            for x in flagged
            if set(x["flags"]) & {"abstract", "metaphor_stack", "poetic_compress"}
            or ("long" in x["flags"] and x["len"] >= 80)
        ],
        "all_flagged": flagged,
    }

    out = HERE / "_tone_audit.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out}")
    print(f"total={report['total_editable']} flagged={report['flagged']} priority={len(report['priority'])}")
    for x in report["priority"]:
        print(f"{x['id']}:L{x['line']} {x['flags']} | {x['text']}")


if __name__ == "__main__":
    main()
