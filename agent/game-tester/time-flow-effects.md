# 時間流動與身心變化審查

> game-tester 專用。審查**故事時間推進**後，狗／主人／關係／外部事件是否在**生理、心理、行為、文案、視覺**上合理演進——不是 Day1 複製貼上。  
> 設定權威：[`guide_line.md`](../../guide_line.md) §四–§六、[`Ch1_guide_line.md`](../../Ch1_Trust/Ch1_guide_line.md) §七；角色外型見 [`visual-art/reference.md`](../visual-art/reference.md)。

---

## 一、時間軸層次（審查前先釐清）

| 層次 | Ch1 範例 | 審什麼 |
|------|----------|--------|
| **場內** | 同場 `text`→`sub`→選項 | 情緒弧是否在同一 beat 內合理 |
| **日** | Day 1→7 | 班表、早晚、過場語（「隔天早晨」） |
| **週** | Week1→4 | 技能累積、關係基調、笑暖節奏 |
| **章** | Ch1 幼犬 → Ch2 中年 → Ch3 老犬 | 年齡感、玩法重心、基調 |
| **跨作** | 存檔 Landmark → Ch3 閃回 | `favoriteSpot`、`dogFriends`、怕雷等是否被引用 |

**Ch1 鎖定：**
- 故事日 Day 1–28 + 快轉 Day 365（週年）
- 相遇時狗 **2–4 個月**；週年約 **1 歲**（仍幼犬段，非 Ch2 中年）
- Bond：Week1 末 Lv2 → Week4 末 Lv3 → 週年收束

---

## 二、狗狗：隨時間應有的變化

### 2.1 生理（Ch1 幼犬段）

| 時段 | 合理 | 不合理（要報） |
|------|------|----------------|
| Day 1–3 | 小、易累、控 bladder 差、易驚 | 像成犬穩定、長時間獨立無焦慮 |
| Week2+ | 體力略增、仍幼犬比例；社會化「第一次」 | 電梯／公園像「老手」無鋪墊 |
| Week3 走失 | 會開門縫、認家但衝動仍在 | 完全不懂家界線（若已 Memory 認家） |
| Day 365 | 比相遇大一圈，仍 golden-tan 同一隻 | 換品種感、突然老犬灰吻（留 Ch3） |

**視覺：** Ch1 全章同一 watercolor 幼犬；**禁止** Week2 突然用 aging PNG（`dog-grey-muzzle` 等屬 Ch2/3）。

### 2.2 心理／行為（Trust × Bond × flags）

| 維度 | 低 → 高 應見到的變化 |
|------|----------------------|
| **Trust** | 夾尾、僵、不進食 → 敢靠近、聽「輕一點」、雷雨可選靠膝 |
| **Bond** | 跟遠、不期待 → 靠膝、門口等、相簿滿是牠 |
| **技能累積** | 尿墊→拖鞋→防咬；吹風機仍怕但可「有準備」 |
| **社會化** | 鄰居腳步 Alert → 電梯阿黃 → 公園 play（需 `socialTier`） |
| **壞習慣修復** | `dryGentle`、`learnedGentleCorrection`、`biteTier` 應在後續 callback |

### 2.3 外部因素 → 身心反應（必查 callback）

| 外部事件 | 首次 | 時間後再遇 | 預期變化 |
|----------|------|------------|----------|
| 吹風機 | Day1 `prologue_dry` | `week2_dryer_truce` | 仍緊張，但主人有經驗；`dryGentle` 分支更穩 |
| 雷雨 | Day6 分支 | 後續怕雷 flag | 高 Trust 可選陪坐；低 Trust 仍 Alert |
| 硬拉電梯 | `week2_elevator_dog` | 公園／再出門 | `elevatorHardPull` 後 Trust 低、社會化慢 |
| 走失 | Week3 | Week3 末 recovery | Hurt→Attached；病後靠膝 |
| 獸醫 | Day4 | Week3 發燒 | 仍 murmur，但認得「去過會回家」 |
| 阿黃 | Week2 電梯 | `week2_park_play` | 第二次較不僵（非零，但進步） |

**P1：** 後段劇情完全無視前段 flag（例：吹風機場像第一夜零成長且無 `dryGentle` 差異）。  
**P2：** 有 flag 差異但文案太弱，玩家感受不到時間帶來的進步。

---

## 三、主人（「你」）：隨時間應有的變化

### 3.1 心理／能力弧（Ch1）

| 時段 | 敘事預期 | 不應出現 |
|------|----------|----------|
| Day 1 | 第一次養、慌、試錯 | 訓練師口吻、一次做對 |
| Day 2 請假 | 手忙腳亂但願意學 | 完美飼主 checklist |
| Week1 末 | 「選擇留下來」、Bond Lv2 | 仍像過客心態 |
| Week2 | 行事曆圍著牠、帶零食、記得關門 | 完全忘記 Day1 教訓 |
| Week3–4 | 走失後內疚／更小心；房東壓力 | 情緒無延續 |
| Day 365 | 一年默契；非完美但「這是家」 | 仍像剛相遇 |

### 3.2 外部人生事件（Ch1 輕量 / Ch2 加重）

| Ch1 | 班表、請假、加班暗示、外賣、視訊會議 |
| Ch2 | 結婚、換工作、孩子、父母生病——**狗不變，人變**（guide_line §四） |
| Ch3 | 照護取捨、安樂／治療選擇 |

**審查：** Day N 的「你」是否仍符合**當時**的飼主經驗值；Week2 不應寫成 Day1 的完全複製。

### 3.3 主人「年齡」

- Ch1 全程 **25 歲**；時間流動體現在**心態與生活節奏**，不是長出皺紋。
- Ch2/Ch3 可隨快轉略提「幾年過去」，視覺仍不露全臉。

---

## 四、關係與系統展現（隨時間）

| 系統 | 時間效應 | 測什麼 |
|------|----------|--------|
| **Bond Lv** | Week1 epilogue Lv2、Week4 Lv3 | epilogue 文案／HUD dots 與劇情匹配 |
| **相簿** | Memory 依時序解鎖 | 描述符合「那時」的關係深度 |
| **Landmark** | 鎖定、不可 S/L 刷掉 | 週年／Ch3 閃回有引用 |
| **flags** | `socialTier`、`phoneFullOfDog`、`favoriteSpot` | 後續場景條件分支合理 |
| **存檔** | 跨 session | 跳 Day 14 仍保留 Week1–2 選擇痕跡 |

**禁止：** 字幕出現「Trust +20」；應寫**行為與感受**的變化。

---

## 五、三部曲前瞻（Ch2 / Ch3 playtest 預留）

| 篇章 | 時間跳躍 | 狗 | 主人 | 玩法 |
|------|----------|-----|------|------|
| Ch2 | 快轉數年 | 中年、變穩、偶爾被忽略 | 人生事件多 | 默契、日常 |
| Ch3 | 老犬 9 歲+ | 慢、灰吻、氣味記憶 | 照護取捨 | 短散步、告別 |

**Ch2/3 審查加項：**
- aging PNG 與敘事一致（慢、不跳沙發）
- 老犬篇**不**用幼犬 yip 密度
- 閃回 Ch1 場景時，文案／色調像**記憶**而非當下重播

---

## 六、手動測試路線（時間弧）

### Ch1 最小集（至少一輪）

1. **Day1 吹風機溫柔** → Week2 `week2_dryer_truce`：對照 `dryGentle` 有無差異文案
2. **Day6 雷雨陪坐** vs **靜日**：後續 `flags`／怕雷相關（若已實作）
3. **Week1 末 Bond Lv2** → **Week2 intro**：基調從「帶回家」→「家以外也要一起面對」
4. **Week2 電梯三選** → **公園 play** 是否需 `socialTier` close
5. **存檔 Day7** → **載入跳 Day14**：關係深度連續

### 長弧（發布前）

- 主線 Day1→28 + 週年（若已實作）
- 低 Trust 線 vs 高 Trust 線各一：Week3 走失結局差異

---

## 七、報告用審查表

```markdown
## 時間流動與身心變化

| 維度 | 結果 | 備註 |
|------|------|------|
| 日／週過場合理 | ✅／⚠️／❌ | |
| 狗行為隨 Trust/Bond 演進 | ✅／⚠️／❌ | |
| 主人從新手→默契 | ✅／⚠️／❌ | |
| 外部事件 callback（吹風機等） | ✅／⚠️／❌ | |
| flags 影響後續分支 | ✅／⚠️／❌ | |
| Bond／相簿／epilogue 時序 | ✅／⚠️／❌ | |
| 無「時間倒流」式 reset 感 | ✅／⚠️／❌ | |
| Ch1 仍幼犬（無過早 aging） | ✅／⚠️／❌ | |
```

**Steam 玩家視角一句：** 「玩得越久，越覺得牠真的在長大、我也真的在學」 vs 「好像 Day1 重複播放」。

---

## 八、常見問題 → 負責 agent

| 問題 | 級別 | 負責 |
|------|------|------|
| Week2 場景心理像 Day1 零成長 | P1 | story-narrative |
| callback 場景無 flag 分支 | P1 | story-narrative |
| 幼犬段用老犬視覺 | P1 | visual-art |
| 主人突然變專家無鋪墊 | P2 | tw-narrative-voice |
| epilogue Bond 與劇情不符 | P1 | story-narrative / systems |
| 相簿 desc 寫成「已一年」但 Day 8 | P1 | story-narrative |

---

## 九、與其他文件

- 靜態一致（名字、pose）：[`character-consistency.md`](character-consistency.md)
- 班表：[`story-narrative/reference.md`](../story-narrative/reference.md) §主人作息
- Steam 節奏／時長：[`steam-vn-players.md`](steam-vn-players.md)
