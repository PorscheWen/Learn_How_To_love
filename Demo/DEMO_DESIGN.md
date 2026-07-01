# Learn How to Love — Demo 設計文件

**篇章：** Chapter 1: First Steps（信任）  
**切片：** 接回家第 1–7 天（週三傍晚帶回家 → 次週二）  
**預估遊玩時間：** 40–50 分鐘  
**平台：** 瀏覽器（本機 HTTP）；架構預留 Steam／Electron 擴充  
**參考：** [`Other_games.md`](../Other_games.md) 溫情互動建議

---

## 一、Demo 目標

1. 驗證「感受 + 羈絆 → 特別事件」核心循環是否動人。
2. 展示狗的感官視角（氣味、色溫、場景切換；**無數字面板**）。
3. 驗證 **Other_games 互動層**：呼吸空檔撫摸、手繪日記、溫柔打字節奏、環境音。
4. 產出可匯出的 Demo 存檔 JSON（跨作原型）。

---

## 二、內容流程架構（核心）

對照 `js/content-flow.js`，每個場景依序經過：

```
narrative（打字機＋淡入）
    ↓
breath（留白 · 可撫摸 · 空白鍵／點字幕跳過）
    ↓
choice │ minigame │ name/gender prompt
    ↓
下一場景
```

| 階段 | 玩家可做 | 程式 |
|------|----------|------|
| **narrative** | 空白鍵／點字幕加速顯示 | `scrollRevealText` + `is-revealing` 淡入 |
| **breath** | **撫摸小狗**（拖曳）、等待或快進 | `skippableDelay`；`ContentFlow.canPet` |
| **choice** | 選項推進 | `showChoices` |
| **minigame** | 寵物店／醫院／認家／如廁／雷雨 | `game.js` 各 `run*Minigame` |

### 撫摸互動（非即時）

- 僅在 **breath 空檔**（文字播完、選項未出）且狗在場時。
- 情緒：`content` / `sleepy` / `attached`；`scene.pettable` 時另開 `shy` / `curious` / `anxious` 等。
- 拖曳狗圖 ≥ 26px 觸發；冷卻 1.5s；首次 +1 Trust。
- 游標 `grab`；狗圖輕微 **呼吸動畫**（`dogBreathe`）。

### 手繪日記（雙軌）

| 軌道 | UI | 資料 |
|------|-----|------|
| **日記頁** | 🐾 → 日記頁；依 Day 分組 | `ALBUM_ENTRIES` + `state.memories` |
| **時刻快照** | 🐾 → 時刻快照 | `moment-gallery.js` + IndexedDB |

### 音訊層（Other_games · ASMR）

| 層 | 模組 | 說明 |
|----|------|------|
| BGM | `audio.js` | 場景 profile crossfade |
| 環境白噪音 | `setSceneAmbience` | 雨、風、室內等 |
| 幼犬 cue | `dog-audio.js` | 稀疏 one-shot |
| 推進 tick | `playAdvanceTick` | 木質輕「啵」取代系統音 |

---

## 三、七天時間軸（現行主線）

| Day | 星期 | 重點 | 小遊戲 |
|-----|------|------|--------|
| 1 | 週三 | 雨天相遇、第一夜 | — |
| 2 | 週四 | 請假、寵物店、取名、在家試探 | 挑用品 `shop` |
| 3 | 週五 | 上班擔心、門口重逢、如廁、尿墊之夜 | 如廁 `potty` |
| 4 | 週六 | 修復線、**寵物醫院** | 問診 `vet` |
| 5 | 週日 | **懷裡認家** | 氣味地圖 `home` |
| 6 | 週一 | 雷雨或靜日 | 雷雨安撫 `thunder`（條件） |
| 7 | 週二 | 默契、Epilogue | — |

> 主人班表：`systems.js` `DEMO_DAY_CALENDAR`（週一～五 08:00–17:00 上班）。

---

## 四、系統（Demo 版）

### 隱藏數值

| 數值 | 範圍 | 說明 |
|------|------|------|
| Trust | 0–100 | 跟脚、修復、撫摸微量加成 |
| Bond | Lv1 → Lv2 | Demo 結束目標 Lv2 習慣 |

### 可見回饋

- 狗 pose／情緒圖、色溫（`#app.cold` / `content`）
- 氣味列（嗅覺 UI）
- 行為字幕 `.dog-behavior`
- **不顯示** Trust／Bond 數字

### 特別事件（節錄）

| 事件 | 類型 | 觸發 |
|------|------|------|
| 門口的等待 | Memory | Day 3 提早回家 |
| 尿墊之夜 / 靠膝 | Memory / Moment | Day 3 深夜選擇 |
| 寵物醫院 | Memory | Day 4 結帳 |
| 家的氣味 | Memory | Day 5 認家小遊戲佳績 |
| 雷雨 | Memory | Day 6 條件分支 |

---

## 五、場景腳本欄位（`scenes.js`）

| 欄位 | 用途 |
|------|------|
| `text` / `sub` | 主／副字幕 |
| `dogPose` | 故事動作圖 |
| `sceneArt` | NPC 疊圖（店員、獸醫） |
| `hideDog` | 無狗場景 |
| `pettable` | 開放撫摸情緒＋自訂提示 |
| `petHint` | breath 空檔底部提示文案 |
| `minigame` | `shop` / `vet` / `home` / `potty` / `thunder` / `walk` |
| `breathMs` | 留白長度（預設 1200ms） |

---

## 六、模組對照

```
Demo/
├── js/content-flow.js   # 場景階段、撫摸判定、日記分組
├── js/game.js           # 引擎：打字、breath、撫摸、小遊戲
├── js/scenes.js         # 場景與分支
├── js/systems.js        # Trust / Bond / 存檔 / ALBUM_ENTRIES
├── js/moment-gallery.js # 場景快照
├── js/audio.js          # BGM + 環境音 + advance tick
└── css/style.css        # 暖色 UI、呼吸動畫、日記版型
```

---

## 七、跨作存檔（匯出 JSON）

```json
{
  "dogName": "string",
  "dogGender": "male|female",
  "trustFinal": 0,
  "bondLevel": 2,
  "memories": ["door_wait", "vet_visit", "..."],
  "flags": { "afraidOfThunder": false },
  "demoVersion": "1.1",
  "flowVersion": 5
}
```

---

## 八、Other_games 對照（未納入 Demo 範圍）

| 建議 | 狀態 |
|------|------|
| Electron / Steamworks 打包 | 待正式版 |
| 語系 JSON 抽離 | 待正式版（現文案在 `scenes.js`） |
| Live2D | 以 CSS 呼吸動畫替代 |
| Steam 成就 | 待正式版 |

---

## 九、驗收清單

- [ ] 通關 40–50 分鐘（含閱讀）
- [ ] Bond Lv1 → Lv2
- [ ] breath 空檔可撫摸且出現提示
- [ ] 日記頁依 Day 分組、快照可瀏覽
- [ ] 至少 2 Moment + 2 Memory
- [ ] 無 stat 數字面板
- [ ] 存檔可匯出 JSON
- [ ] 結尾：「羈絆才剛開始寫。」
