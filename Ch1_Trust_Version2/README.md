# Learn How to Love — Ch1_Trust_Version2

全新故事架構工作區（與正式產線 `Ch1_Trust/game/` 分離）。  
寫作方法：**清晰框架 + 一次只做一件事**。

節奏弧：相遇 → 混亂 → 磨合 → 成長 → 建立羈絆。

---

## 檔案地圖

| 檔案 | 用途 |
|------|------|
| `agents/00_core_settings.md` | 第一步：核心設定（角色／機制／文筆） |
| `agents/plot.md` | 第二步：7 天節奏大綱（**每天 3～4 分歧＋雙小遊戲**；背景須對齊早／午／晚） |
| `agents/01_style_guide.md` | 劇本格式與文筆檢查 |
| `agents/02_trust_flags.md` | 信任度與 flags 契約 |
| `agents/03_character_bible.md` | 角色聖經 |
| `agents/04_minigames.md` | 每日知識／信任小遊戲規格 |
| `agents/image.md` | FLUX 2 Pro 生圖規範（**印象派油畫** STYLE LOCK） |
| `agents/image_bg.md` | 背景命名 `bg-{place}-{light}`、家族基準、時段對照 |
| `agents/audio.md` | **BGM／SFX**：劇情與 bg → `assets/audio/*.ogg` 對照 |
| `agents/tester.md` | **遊戲測試手冊** |
| `prompts/01_lock_settings.md` | 可複製：鎖定設定 Prompt |
| `prompts/02_plot_outline.md` | 可複製：大綱 Prompt |
| `prompts/03_write_day_script.md` | 可複製：分天寫劇本 Prompt |
| `week0/day1_rainy_cardboard.md` | Day1 劇本（場景表含**時段／bg**） |
| `week0/day2_messy_living_room.md`～`day7_*.md` | Day2～7 劇本（檔名英文） |
| `Renpy_game/` | **Ren'Py 可玩版**（Day1～7；主選單選 Day） |
| `assets/` | bg／dog／char／audio（`Renpy_game/game/assets` junction） |

---

## 三步驟（請照做）

1. 讀 `agents/00_core_settings.md` → 只回「設定已理解」
2. 產出／維護 `agents/plot.md`（不要寫對白）
3. `@plot.md` 只寫**一天** → 存進 `week0/`

潤稿用 Ctrl+K 口令見 `prompts/03_write_day_script.md`。

---

## 每日章節必備

- 劇情分歧 **3～4** 個
- 學習狗狗知識遊戲 **1** 個（`knowledge`，**固定 5 題**）
- 增加信任遊戲 **1** 個（`trust`）
- 場景表標明 **時段** 與 `bg-{place}-{light}`（見 `image_bg.md`）
- 音樂對齊 `audio.md`（開場／日終 Profile；實體檔在 `assets/audio/`）

## 目前進度

- [x] 核心設定／7 天大綱／小遊戲規格
- [x] Week0 Day1～7 劇本（檔名英文）
- [x] 美術：油畫 STYLE LOCK＋`image_bg.md` 命名
- [x] Ren'Py Day1～7 可玩（含 BGM＋幼犬聲＋章節跳轉）
- [x] 主選單／快捷：**選擇章節**（Day）
- [ ] 潤稿／美術缺圖（如 `char-sit-floor`）

---

## 遊玩（Ren'Py）

```
Ch1_Trust_Version2\Renpy_game\開啟遊戲.bat
```

- 從頭：開始遊戲（Day1 → … → Day7）
- 跳關：主選單 **選擇章節** → Day 1～7

詳見 `Renpy_game/README.md`。測試依 **`agents/tester.md`**。

---

## 下一步（建議）

- 潤稿：對單一場景用 Ctrl+K（`prompts/03_write_day_script.md`）
- 生圖：`agents/image.md`＋`image_bg.md`；同 place 只改日夜
- 音樂：`agents/audio.md` → 場景 `play music` 落地
- Ren'Py：潤稿、缺圖補齊、結局分支細修

---

*更新：2026-07-12｜Day1～7 可玩、Learn How to Love、章節只選 Day*
