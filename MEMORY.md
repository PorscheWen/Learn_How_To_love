# MEMORY.md — Learn How to Love 鎖定記憶

> **權威等級：** 本檔 = 最高敘事／世界觀鎖定。與 `guide_line.md` 衝突時以 `guide_line.md` 為準；本檔為 Hermes／Cursor／Gemini 的**濃縮必讀版**，禁止擅自改設定。  
> **完整規格：** `guide_line.md` · `Ch1_Trust/Ch1_guide_line.md` · `agent/`

---

## 0. 系列一句話

**不是寵物模擬器**，是家庭用十幾年學會愛的三部曲。玩家操作的是**時間、默契、無法 S/L 刷掉的選擇**，不是刷數值通關。

- 英文：Learn How to Love  
- 中文：學會去愛  
- Slogan：愛，是一起學會的事。

---

## 1. 三部曲（不可改結構）

| 章 | 副標 | 生命階段 | 主題 | 基調 |
|----|------|----------|------|------|
| Ch1 | First Steps | 幼犬 0–2 歲 | **信任** | 暖、有笑；不催淚開場 |
| Ch2 | Still Here | 中年 3–8 歲 | **日常** | 靜、節奏、被忽略與修復 |
| Ch3 | Goodbye | 老犬 9 歲+ | **告別** | 克制、尊嚴；死亡僅此章 |

**視角：** 全程**狗的感官**（嗅覺、聽覺、身體），非 stat 面板語言。

---

## 2. 不可動搖原則（違反 = 退稿）

1. **無 permadeath** — 養死永久 Game Over ❌  
2. **第一、二部不會因操作失誤養死** — 死亡與告別**只屬 Ch3**  
3. **後果服務「學會愛」** — 疏忽 → 關係受損、分支變體，非懲罰性死局  
4. **Landmark 觸發後鎖定** — 寫入跨作存檔，不可 S/L 刷完美  
5. **不替玩家判斷安樂對錯** — Ch3 三條主線皆完整  
6. **眼淚來自默契與告別** — 非廉價彩虹橋、非三作皆催淚  
7. **禁止：** 用死亡開場騙眼淚、純經營 sim、永遠幼犬感、道德綁架

---

## 3. 主人「你」（鎖定）

| 項目 | 值 |
|------|-----|
| 年齡 | **25 歲** |
| 性別／外型 | **長髮女性**上班族 |
| 住處 | 獨居小公寓 |
| 寵物經驗 | **第一次養寵物** |
| 性格 | 感情豐富、易共感、會內疚也溫柔 |
| 敘事 | **第二人稱「你」** |
| 班表 | 週一～五 **08:00–17:00** 上班；週六日放假 |
| 視覺 | Demo **不露全臉**；僅手、臂、膝上緣等局部 |

**班表審查：** 上班日白天主人不得無故在家（除非 `onLeave`／flags 明示請假）。

---

## 4. 狗狗（全系列同一隻）

| 項目 | 值 |
|------|-----|
| 品種感 | **混種幼犬** scruffy mixed breed（非柯基／柴犬等可辨識純種） |
| 毛色 | golden-tan / honey ochre |
| 筆觸 | 數位水彩；**無硬黑描邊** |
| 全系列 | **同一隻狗**；Ch2/3 僅 aging 變體，不換狗 |

### Ch1 年齡時間軸（必對）

| 故事日 | 狗年齡 | 禁止 |
|--------|--------|------|
| Day 1 相遇 | **~3 個月** | 成犬、老犬、6 月大體型 |
| Day 1–14 | ~3 月 | 灰吻、老犬步態 |
| Day 15+ Week3 | **4–5 月** | 仍須幼犬衝動，非成犬穩定 |
| Day 365 | **~1 歲** | 非老犬 |

---

## 5. 取名／代詞時間線（程式 + 文案一致）

| 階段 | 場景範圍 | 規則 |
|------|----------|------|
| 前 | `prologue_*`～`day2_petshop` | 僅「**牠**」，禁狗名 |
| 中 | `day2_naming`／`day2_gender` | UI 取名 |
| 後 | `day2_return`+ | `dogLabel(s)`／`dogPronoun(s)` |

- **禁止**在 `choice-reactions.js` 寫死狗名 → 用 `` `${dogLabel(s)}` `` 函式  
- 代詞：`female→她` `male→他` `else→牠`

---

## 6. 感受與羈絆（敘事用語）

**Feelings（範例）：** Anxious, Curious, Content, Attached, Hurt, Sleepy… — 用**感受**描寫，禁「+20 Trust」類遊戲化面板語。

**Bond 五階：** Stranger → Familiar → Rhythm → Anchor → One Life

**特別事件等級：**

- **Moment**（多）— 瞬間  
- **Memory**（中）— 相簿、可重溫  
- **Landmark**（少）— 鎖定、跨作存檔  

**公式：** `特別事件 = 章節節點 + Bond 門檻 + 感受 + （可選）flags`

---

## 7. Ch1 敘事節奏（每日必達）

| # | 標準 |
|---|------|
| D1 記憶點 | 每天至少 1 Memory／Moment + `ALBUM_ENTRIES` |
| D2 互動高峰 | 人對狗 1 句短對白 + 狗身體回應 |
| D3 日終 | 最後一場 `dayClose: true` 或 `breathMs` ≥ 2600 |

**文案分層：**

| 欄位 | 寫什麼 | 禁止 |
|------|--------|------|
| `text` | 現場、感官、動作 | 主題總結、說教 |
| `sub` | 心裡話，更慢更內斂 | 重複 text、雞湯 |
| `choices` | 第一人稱具體動作 | 抽象標籤 |
| `choice-reactions` | 狗身體反應 | NPC 台詞、店員對白 |

**選項分級：** A 續看｜B 風味｜C 分歧（每週 C ≤2–3）

**語調金標：** Day 1 `prologue_rain`～`prologue_dawn` — 繁體中文、**台灣用語**、親切溫柔。

---

## 8. 字幕 vs 狗狗反應（Demo 鎖定）

| 位置 | 內容 |
|------|------|
| `text`／`sub` | 旁白、對白、NPC — **字幕區** |
| `dog-behavior`／`choice-reactions` | **僅**狗動作／選項後反應 |
| 狗 PNG | 獨立疊層，**不畫進背景** |

---

## 9. 主要 NPC

| 名稱 | 類型 | 備註 |
|------|------|------|
| 寵物店店員 | 人類 | 中年大姐、親切 |
| 獸醫 | 人類 | 專業穩重 |
| **阿黃** | 狗友 companion | `week2_elevator_dog` 起；黃色混種 |

---

## 10. 跨作存檔（Landmark 必寫）

最低欄位：`dogName`、`dogGender`、`memories[]`、`flags`、`favoriteSpot`、Bond／Trust 關鍵選擇、`landmarks[]`（鎖定）

Ch3 須能閃回個人化記憶；壞結局章可重玩，**不清零全系列**。

---

## 11. 美術與音效基線（摘要）

- **版面：** 70% 主視覺 + 30% 底部字幕 overlay（沉浸式，勿回退上下硬切）  
- **UI：** 米白底 `#FAF6F0`、深棕字 `#4A3728`、圓角 16px+  
- **狗資產：** `Week0/`（~3 月）· `Week3/`（4–5 月）· MJ `--sref` 水彩  
- **Demo 音效：** 僅 BGM + 稀疏幼犬 one-shot；**無** weather 環境雜音 loop  

---

## 12. Hermes 產出契約

**首選模型：** `deepseek-v4-flash`（經 Nous Portal）— 長上下文、結構化 JSON；劇本批次產出用。審稿與引擎落地仍交 Cursor。

產出劇本／JSON 時**必須**：

1. 對照本檔 + `agent/story-narrative/SKILL.md`  
2. 輸出繁體台灣用語；禁簡體、禁硬編碼狗名（取名前用「牠」）  
3. 每場景含：`scene_id`、班表合理性、狗年齡感、`choices` 分級標註  
4. `choice-reactions` 鍵 = `` `場景Id::選項原文` ``（標點逐字一致）  
5. 產出後須可被 `node tools/validate-choice-reactions.js` 驗證  

**權責：** Hermes = 大量草稿 + 驗證；Cursor = 審稿後落地 `Ch1_Trust/game/js/`。

---

## 13. 權威文件索引

| 用途 | 路徑 |
|------|------|
| 系列聖經 | `guide_line.md` |
| Ch1 逐日 | `Ch1_Trust/Ch1_guide_line.md` |
| 角色 | `agent/character-bible/` |
| 分支 | `agent/branch-engine/` |
| 語氣 | `agent/tw-narrative-voice/` |
| 節奏 | `agent/narrative-pacing-revision.md` |
| Playable | `Ch1_Trust/game/js/scenes.js` |

---

*最後更新：2026-07-09 · 與 guide_line 同步維護*
