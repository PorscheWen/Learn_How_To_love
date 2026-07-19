# Section 10｜把鑰匙分給心跳

> 對齊：`game_guild.md` · `outline_trilogy_ch1_10sections.md`  
> 定位：Ch1 結算；不再修改 trust，以睡眠距離落地四種關係溫度。

## 章節契約

| 項目 | 鎖定 |
|------|------|
| 一件事 | 鑰匙、牽繩與第二個水碗成為「留下」的物證 |
| trust | 本段不再加扣，只讀取既有結果 |
| C 優先 | `gave_away = true` → `ending_ch1_handed_over`，不受分數影響 |
| A | 留下、`trust 10～12`、`s08_forced_walk != true` |
| B | 留下、`trust ≥ 4`；也承接高信任但 S08 硬拖而被 A 排除的路徑 |
| D | 留下、`trust ≤ 3` |
| 禁止 | 不出現衰老、安樂、離別預告；不顯示 trust 數字 |
| 共通句 | 「我們再試一年」與「晚上見」；不同結局改變狗是否相信 |

**章節選擇摘要：** 鑰匙與牽繩掛在同一面牆上；夜深後，睡眠的距離替這段關係留下答案。

## 四結局

### A｜背靠

- Label：`ending_ch1_back_to_back`
- 狗背對予安睡在伸手可及處，最無防備的一側朝向房間。
- 隔天聽見「晚上見」只動耳朵，不起身確認。
- BGM：`ending_back` → `hopeful`。

### B｜選定但還在學

- Label：`ending_ch1_chosen_learning`
- 狗敢睡近，仍睜眼回頭確認；予安回答「我在」。
- 隔天會看她，但不追出門。
- BGM：`ending_learning`。

### C｜送走之後

- Label：`ending_ch1_handed_over`
- 公寓重新只剩冰箱嗡嗡；同事傳來安全抵達的照片。
- 「晚上見」出口後房間無人回頭；不宣判選擇對錯。
- 保留日後探視與修復可能。
- BGM：`ending_handover`。

### D｜薄冰同住

- Label：`ending_ch1_thin_ice`
- 牽繩已掛好，狗仍睡門邊、朝向出口。
- 予安不追、不要求留下換成立即信任。
- 「晚上見」後狗不看她，只在門闔上前動一下耳朵。
- BGM：`ending_thin_ice`。

## 美術

- 共用 `bg-living-night.png`
- A：`dog-back-sleep.png`
- B：`dog-check-sleep.png`
- D：`dog-door-edge.png`
- C 以空客廳與空掛勾為主，不強制顯示狗。

## 驗證

- 四個 ending labels 均可到達並寫入 `flags["ch1_ending"]`。
- A 必須檢查 `s08_forced_walk`；硬拖路徑不得進 A。
- C 必須優先於所有 trust 判定。
- 四結局皆正常結束，不顯示 Game Over。
