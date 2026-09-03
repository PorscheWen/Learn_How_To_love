## 旁白／對白排版：一段最多兩行、句與句不黏在一起；出字速度依語氣。

init -1 python:
    import re

    _LHTL_TAG = re.compile(r"\{[^}]*\}")
    _LHTL_SLOW = (
        "安靜", "很輕", "睡著", "意識往下", "聲音很輕",
        "明天再說", "沒有答案", "像怕被自己聽見",
    )
    _LHTL_QUICK = ("叮", "電梯", "冷氣撞", "提袋出門", "微波")

    def lhtl_plain_len(text):
        return len(_LHTL_TAG.sub("", text or "").replace("\n", ""))

    def lhtl_quoted_ranges(text):
        """標出「」『』與直引號的完整範圍；沒閉合就收到句尾，避免中間被切開。"""
        ranges = []
        i = 0
        n = len(text or "")
        pairs = {"「": "」", "『": "』", '"': '"', "\u201c": "\u201d"}
        while i < n:
            closer = pairs.get(text[i])
            if closer:
                j = text.find(closer, i + 1)
                if j < 0:
                    j = n - 1
                ranges.append((i, j))
                i = j + 1
                continue
            i += 1
        return ranges

    def lhtl_pos_in_quotes(pos, ranges):
        return any(start < pos < end for start, end in ranges)

    def lhtl_quote_balance(text):
        plain = _LHTL_TAG.sub("", text or "")
        return (
            plain.count("「") == plain.count("」")
            and plain.count("『") == plain.count("』")
        )

    def lhtl_split_sentences(text):
        """依句號／驚嘆／問號／省略號切開；引號內的標點不切，整段圈住。"""
        raw = (text or "").replace("......", "……").strip()
        if not raw:
            return []
        if "\n" in raw:
            parts = []
            for line in raw.split("\n"):
                parts.extend(lhtl_split_sentences(line))
            return [p for p in parts if p]
        quoted = lhtl_quoted_ranges(raw)
        chunks = []
        start = 0
        i = 0
        length = len(raw)
        while i < length:
            if raw.startswith("……", i) and not lhtl_pos_in_quotes(i, quoted):
                piece = raw[start:i + 2].strip()
                if piece:
                    chunks.append(piece)
                start = i + 2
                i = start
                continue
            if raw[i] in "。！？" and not lhtl_pos_in_quotes(i, quoted):
                piece = raw[start:i + 1].strip()
                if piece:
                    chunks.append(piece)
                start = i + 1
                i = start
                continue
            i += 1
        tail = raw[start:].strip()
        if tail:
            chunks.append(tail)
        return chunks or [raw]

    def lhtl_est_lines(text, chars_per_line=40):
        n = max(1, lhtl_plain_len(text))
        return max(1, (n + chars_per_line - 1) // chars_per_line)

    def lhtl_group_beats(sentences, max_lines=2, chars_per_line=40):
        """相鄰句子合成一拍，畫面最多兩行；引號未閉合時併入下一句。"""
        beats = []
        current = []
        used = 0
        for sent in sentences:
            need = lhtl_est_lines(sent, chars_per_line)
            joined = lhtl_join_beat(current + [sent]) if current else sent
            if current and used + need > max_lines and lhtl_quote_balance("".join(current)):
                beats.append(current)
                current = [sent]
                used = need
            else:
                current.append(sent)
                used += need
                if not lhtl_quote_balance(joined) and used > max_lines:
                    used = max_lines
        if current:
            if beats and not lhtl_quote_balance("".join(current)):
                beats[-1].extend(current)
            else:
                beats.append(current)
        return beats

    def lhtl_join_beat(parts):
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        # 第一行打完稍停，其餘併在第二行，避免引號被拆到下一拍
        return parts[0] + "{w=0.16}\n" + "".join(parts[1:])

    def lhtl_cps_factor(text, kind):
        factor = {
            "thought": 0.52,
            "narrator": 0.78,
            "ya": 0.90,
            "clerk": 1.16,
            "neighbor": 1.06,
            "coworker": 0.94,
        }.get(kind, 0.80)
        if any(mark in text for mark in _LHTL_SLOW) or "……" in text:
            factor = min(factor, 0.60 if kind != "thought" else 0.48)
        elif kind == "narrator" and any(mark in text for mark in _LHTL_QUICK):
            factor = max(factor, 0.96)
        if lhtl_plain_len(text) <= 6:
            factor *= 0.72
        return max(0.35, min(1.35, factor))

    def lhtl_apply_cps(text, kind):
        if not text or "{cps" in text:
            return text
        paced = text.replace("......", "……")
        paced = paced.replace("……", "……{w=0.26}")
        return "{cps=*%.2f}%s{/cps}" % (lhtl_cps_factor(text, kind), paced)

    def lhtl_prepare_beats(what, kind):
        raw = str(what)
        sentences = lhtl_split_sentences(raw)
        if not sentences:
            return [lhtl_apply_cps(raw, kind)]
        beats = lhtl_group_beats(sentences)
        return [lhtl_apply_cps(lhtl_join_beat(parts), kind) for parts in beats]


    class LHTLCharacter(renpy.character.ADVCharacter):
        def __init__(self, name=None, **properties):
            self.lhtl_kind = properties.pop("lhtl_kind", "narrator")
            super(LHTLCharacter, self).__init__(name, **properties)

        def __call__(self, what, interact=True, *args, **kwargs):
            if (
                not interact
                or what is None
                or kwargs.get("multiple")
            ):
                return super(LHTLCharacter, self).__call__(
                    what, interact=interact, *args, **kwargs
                )
            beats = lhtl_prepare_beats(what, self.lhtl_kind)
            result = None
            for beat in beats:
                result = super(LHTLCharacter, self).__call__(
                    beat, interact=interact, *args, **kwargs
                )
            return result
