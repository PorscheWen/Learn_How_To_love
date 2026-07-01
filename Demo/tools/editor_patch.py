#!/usr/bin/env python3
"""Apply structured content edits to Demo JS source files."""
from __future__ import annotations

import re
from typing import Any


def js_escape_single(text: str) -> str:
    return (
        text.replace('\\', '\\\\')
        .replace("'", "\\'")
        .replace('\r', '')
        .replace('\n', '\\n')
    )


def js_escape_template(text: str) -> str:
    return (
        text.replace('\\', '\\\\')
        .replace('`', '\\`')
        .replace('\r', '')
        .replace('\n', '\\n')
    )


def _skip_string(source: str, i: int) -> int:
    quote = source[i]
    i += 1
    while i < len(source):
        if source[i] == '\\':
            i += 2
            continue
        if source[i] == quote:
            return i + 1
        i += 1
    return len(source)


def _find_bracket_block(source: str, open_pos: int) -> int | None:
    depth = 0
    i = open_pos
    while i < len(source):
        ch = source[i]
        if ch in ("'", '"', '`'):
            i = _skip_string(source, i)
            continue
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None


def _find_brace_block(source: str, open_pos: int) -> int | None:
    depth = 0
    i = open_pos
    while i < len(source):
        ch = source[i]
        if ch in ("'", '"', '`'):
            i = _skip_string(source, i)
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None


def _find_object_block(source: str, marker: str) -> tuple[int, int] | None:
    m = re.search(rf'\b{re.escape(marker)}:\s*\{{', source)
    if not m:
        return None
    start = m.start()
    open_pos = m.end() - 1
    end = _find_brace_block(source, open_pos)
    if end is None:
        return None
    return start, end


def _replace_literal_field(block: str, prop: str, body: str, quote: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf'(\s{re.escape(prop)}:\s*(?:\([^)]*\)\s*=>\s*)?)'
        rf'(?:applyDogPronouns\s*\(\s*)?'
        rf'([\'`])(?:\\.|(?!\2).)*?\2'
        rf'(?:\s*,\s*s\s*\))?',
        re.DOTALL,
    )
    if not pattern.search(block):
        return block, False

    def _repl(m: re.Match[str]) -> str:
        return f'{m.group(1)}{quote}{body}{quote}'

    new_block = pattern.sub(_repl, block, count=1)
    return new_block, True


def patch_scene_field(source: str, scene_id: str, prop: str, inner: str, use_template: bool) -> tuple[str, bool]:
    span = _find_object_block(source, scene_id)
    if not span:
        return source, False
    start, end = span
    block = source[start:end]
    quote = '`' if use_template else "'"
    body = js_escape_template(inner) if use_template else js_escape_single(inner)
    new_block, ok = _replace_literal_field(block, prop, body, quote)
    if not ok:
        return source, False
    return source[:start] + new_block + source[end:], True


def patch_scene_choice(source: str, scene_id: str, choice_index: int, inner: str) -> tuple[str, bool]:
    span = _find_object_block(source, scene_id)
    if not span:
        return source, False
    start, end = span
    block = source[start:end]
    choices_m = re.search(r'\bchoices:\s*\[', block)
    if not choices_m:
        return source, False
    choices_start = choices_m.end() - 1
    choices_end = _find_bracket_block(block, choices_start)
    if choices_end is None:
        return source, False
    choices_body = block[choices_start:choices_end]
    text_matches = list(re.finditer(r"\btext:\s*'((?:\\.|[^'\\])*)'", choices_body))
    if choice_index >= len(text_matches):
        return source, False
    m = text_matches[choice_index]
    body = js_escape_single(inner)
    new_choices = (
        choices_body[: m.start(1)]
        + body
        + choices_body[m.end(1) :]
    )
    new_block = block[:choices_start] + new_choices + block[choices_end:]
    return source[:start] + new_block + source[end:], True


def patch_choice_reaction_key(source: str, old_key: str, new_key: str) -> tuple[str, bool]:
    if not old_key or not new_key or old_key == new_key:
        return source, False
    needle = f"'{old_key}'"
    if needle not in source:
        return source, False
    return source.replace(needle, f"'{new_key}'", 1), True


def patch_choice_reaction(source: str, key: str, inner: str, use_template: bool, new_key: str | None = None) -> tuple[str, bool]:
    out = source
    if new_key and new_key != key:
        out = out.replace(f"'{key}'", f"'{new_key}'", 1)
        key = new_key
    m = re.search(rf"'{re.escape(key)}':\s*\{{", out)
    if not m:
        return out, False
    start = m.start()
    open_pos = m.end() - 1
    end = _find_brace_block(out, open_pos)
    if end is None:
        return out, False
    block = out[start:end]
    quote = '`' if use_template else "'"
    body = js_escape_template(inner) if use_template else js_escape_single(inner)
    new_block, ok = _replace_literal_field(block, 'text', body, quote)
    if not ok:
        return out, False
    return out[:start] + new_block + out[end:], True


def patch_minigame_line(source: str, game: str, tier: str, prop: str, inner: str, use_template: bool) -> tuple[str, bool]:
    game_span = _find_object_block(source, game)
    if not game_span:
        return source, False
    g_start, g_end = game_span
    game_block = source[g_start:g_end]
    tier_span = _find_object_block(game_block, tier)
    if not tier_span:
        return source, False
    t_start, t_end = tier_span
    tier_block = game_block[t_start:t_end]
    quote = '`' if use_template else "'"
    body = js_escape_template(inner) if use_template else js_escape_single(inner)
    new_tier, ok = _replace_literal_field(tier_block, prop, body, quote)
    if not ok:
        return source, False
    new_game = game_block[:t_start] + new_tier + game_block[t_end:]
    return source[:g_start] + new_game + source[g_end:], True


def patch_album_field(source: str, mem_id: str, prop: str, inner: str) -> tuple[str, bool]:
    marker = 'const ALBUM_ENTRIES = {'
    album_pos = source.find(marker)
    if album_pos < 0:
        return source, False
    open_pos = source.find('{', album_pos)
    album_end = _find_brace_block(source, open_pos)
    if album_end is None:
        return source, False
    section = source[album_pos:album_end]
    rel_span = _find_object_block(section, mem_id)
    if not rel_span:
        return source, False
    rel_start, rel_end = rel_span
    start = album_pos + rel_start
    end = album_pos + rel_end
    block = source[start:end]
    body = js_escape_single(inner)
    new_block, ok = _replace_literal_field(block, prop, body, "'")
    if not ok:
        return source, False
    return source[:start] + new_block + source[end:], True


def patch_smell_add_array(source: str, scene_id: str, items: list[str]) -> tuple[str, bool]:
    span = _find_object_block(source, scene_id)
    if not span:
        return source, False
    start, end = span
    block = source[start:end]
    arr = '[' + ', '.join(f"'{js_escape_single(x)}'" for x in items) + ']'
    m = re.search(r'\bsmellAdd:\s*\[', block)
    if not m:
        return source, False
    open_pos = m.end() - 1
    close_pos = _find_bracket_block(block, open_pos)
    if close_pos is None:
        return source, False
    rel_open = m.start()
    new_block = block[:rel_open] + 'smellAdd: ' + arr + block[close_pos:]
    return source[:start] + new_block + source[end:], True


def patch_scene_text_function(source: str, scene_id: str, fn_body: str) -> tuple[str, bool]:
    span = _find_object_block(source, scene_id)
    if not span:
        return source, False
    start, end = span
    block = source[start:end]
    m = re.search(r'\btext:\s*(\([^)]*\)\s*=>\s*\{)', block)
    if not m:
        return source, False
    text_prop_start = m.start()
    open_pos = m.end() - 1
    close_pos = _find_brace_block(block, open_pos)
    if close_pos is None:
        return source, False
    tail = close_pos
    while tail < len(block) and block[tail] in ' \t\n\r':
        tail += 1
    if tail < len(block) and block[tail] == ',':
        tail += 1
    new_assign = 'text: ' + fn_body.strip()
    if not new_assign.rstrip().endswith(','):
        new_assign = new_assign.rstrip() + ','
    new_block = block[:text_prop_start] + new_assign + block[tail:]
    return source[:start] + new_block + source[end:], True


def patch_smell_add(source: str, scene_id: str, inner: str, is_array: bool, use_template: bool) -> tuple[str, bool]:
    if is_array:
        items = [x.strip() for x in re.split(r'[、,，]', inner) if x.strip()]
        out, ok = patch_smell_add_array(source, scene_id, items)
        if ok:
            return out, True
    return patch_scene_field(source, scene_id, 'smellAdd', inner, use_template)


def apply_edit(source: str, edit: dict[str, Any]) -> tuple[str, bool]:
    meta = edit.get('meta') or {}
    inner = edit.get('sourceText', '')
    use_template = bool(edit.get('useTemplate'))
    prop = meta.get('prop')

    if meta.get('file') == 'scenes.js' or edit.get('file') == 'scenes.js':
        scene_id = meta.get('sceneId')
        if prop == 'choice':
            return patch_scene_choice(source, scene_id, int(meta.get('choiceIndex', 0)), inner)
        if prop == 'smellAdd':
            return patch_smell_add(
                source,
                scene_id,
                inner,
                bool(meta.get('isArray')),
                use_template,
            )
        if meta.get('isTextFunction'):
            return patch_scene_text_function(source, scene_id, inner)
        return patch_scene_field(source, scene_id, prop, inner, use_template)

    if edit.get('file') == 'choice-reactions.js':
        return patch_choice_reaction(
            source,
            meta.get('reactionKey', ''),
            inner,
            use_template,
            meta.get('newChoiceKey'),
        )

    if edit.get('file') == 'minigame-reactions.js':
        return patch_minigame_line(
            source,
            meta.get('game', ''),
            meta.get('tier', ''),
            meta.get('prop', ''),
            inner,
            use_template,
        )

    if edit.get('file') == 'systems.js':
        return patch_album_field(source, meta.get('memId', ''), meta.get('prop', ''), inner)

    return source, False


def apply_edits(files: dict[str, str], edits: list[dict[str, Any]]) -> tuple[dict[str, str], list[str], list[str]]:
    out = dict(files)
    applied: list[str] = []
    failed: list[str] = []

    for edit in edits:
        fname = edit.get('file')
        if fname not in out:
            failed.append(f"{edit.get('id', '?')}: 找不到 {fname}")
            continue
        new_source, ok = apply_edit(out[fname], edit)
        if ok:
            out[fname] = new_source
            applied.append(str(edit.get('id', fname)))
            meta = edit.get('meta') or {}
            if fname == 'scenes.js' and meta.get('prop') == 'choice':
                new_key = meta.get('newChoiceKey')
                if new_key and 'choice-reactions.js' in out:
                    old_key = f"{meta.get('sceneId', '')}::{meta.get('oldChoiceText', '')}"
                    renamed, ren_ok = patch_choice_reaction_key(
                        out['choice-reactions.js'], old_key, new_key,
                    )
                    if ren_ok:
                        out['choice-reactions.js'] = renamed
                        applied.append(f'reaction-key:{new_key}')
        else:
            failed.append(str(edit.get('id', '?')))

    return out, applied, failed
