# Steam 電子小說玩家視角（測試基準）

> 供 **game-tester** 手動 playtest 與敘事體驗審查時對照。  
> 本文件描述「玩過多款 Steam 熱門敘事／VN 的玩家」在意什麼——**不是**要求 LHTL 變成那些遊戲，而是用它們當**評分尺**，找出會被 Steam 評論區點名的問題。  
> 系列定位仍以 [`guide_line.md`](../../guide_line.md) §二、§十 與 [`story-narrative/steam-release.md`](../story-narrative/steam-release.md) 為準。

---

## 1. 測試者人設（擴充）

除「台灣在地 playtester」外，測試時假設自己：

- 玩過 **10+ 款** Steam 敘事／VN／walking sim（含中英文版）
- 會在 **Steam 評論** 裡寫：劇情是否值得、選擇是否有意義、繁中是否順、時長是否對得起價格
- 熟悉 **退款門檻**（<2h 可退）與 **全成就／多周目** 玩家習慣
- 對 **寵物／告別／日常 slice-of-life** 類有期待，但厭惡 **廉價催淚、道德綁架、permadeath 懲罰**

---

## 2. Steam 熱門類型與標竿作品

依「玩家拿來比較的類型」分類；每類列出 **玩家重視的因素** 與 **LHTL 該對齊／該避開** 的點。

### 2.1 選擇有重量（Choices Matter）

| 標竿 | *Life is Strange*、*Detroit: Become Human*、*The Walking Dead* (Telltale)、*Disco Elysium* |
|------|------|
| **玩家重視** | 選項像「真的在選」、後續有回聲（台詞／場景／關係）、不是假選項；壞選可修但不會被一刀 Game Over |
| **Steam 差評常見** | 「選了沒差」「結局都一樣」「假分支騙重玩」 |
| **LHTL 對照** | Landmark **鎖定**、Trust／Bond 改 **變體** 而非死局；選項後要有 **choice-reaction** 或場景差異；**禁止** permadeath（見 guide_line §三） |

### 2.2 線性催淚／kinetic 情感（Story Rich）

| 標竿 | *To the Moon*、*Finding Paradise*、*Before Your Eyes*、*Gris*、*Spiritfarer* |
|------|------|
| **玩家重視** | 節奏鋪陳、伏筆回收、眼淚來自 **關係與時間** 而非突然死亡；音畫與文本同頻 |
| **Steam 差評常見** | 「太短不值價」「前面無聊後面硬哭」「BGM 一直 loop 很煩」 |
| **LHTL 對照** | Ch1 **暖有笑** 再收；眼淚留 Ch3；**>2h** 退款線（§十）；BGM profile 切換自然（交 audio-sound） |

### 2.3 日常治癒／slice-of-life（Cozy Narrative）

| 標竿 | *Coffee Talk*、*VA-11 Hall-A*、*Kind Words*、*A Short Hike*、*Unpacking* |
|------|------|
| **玩家重視** | 低壓力、可慢慢讀、小互動錦上添花（沖咖啡、整理、撫摸）；**不強迫** minigame |
| **Steam 差評常見** | 「互動像作業」「節奏被小遊戲打斷」「UI 太冷／太硬」 |
| **LHTL 對照** | 撫摸在 **breath 空檔**、小遊戲服務 **認家／信任** 而非刷分；暖色 UI（§6.7）；Ch2 **靜日常** 深度是差異化賣點 |

### 2.4 日系／Galgame 向 VN（Visual Novel 標籤）

| 標竿 | *Steins;Gate*、*Clannad*、*Doki Doki Literature Club!*、*Monster Prom*、*Little Busters!* |
|------|------|
| **玩家重視** | 快進／Auto、回顧 log、存讀檔穩、路線表／結局收集感、CG／立繪差異 |
| **Steam 差評常見** | 「沒 backlog」「存檔壞了」「繁中機翻／簡繁混用」「一條線 20 分鐘就完」 |
| **LHTL 對照** | 存檔 JSON + 未來 Cloud Save；繁體 **台灣用語**（tw-narrative-voice）；相簿／日記當 **收集感**；路線以 **Landmark／結局** 計，不灌水 kinetic |

### 2.5 寵物／犬類情感（Dog / Pet Emotional）

| 標竿 | *The Last Night of Cheryl*、*My Little Puppy*、*Little Friends*、*The Life of One Dog*、*Farewell North* |
|------|------|
| **玩家重視** | 狗像 **你的家人** 而非道具；生命週期或成長有誠意；避免 **彩虹橋套路** 或幼犬永遠不長大 |
| **Steam 差評常見** | 「只有老年催淚」「狗不能互動」「養死懲罰太狠」「跟宣傳的 dog game 不符」 |
| **LHTL 對照** | **三部曲** 幼→中→老；**狗感官視角**；Ch1 不拿死亡開場；商店文案勿標成 pure pet sim（見 steam-release §1） |

### 2.6  indie 敘事實驗（Atmospheric / Walking Sim）

| 標竿 | *What Remains of Edith Finch*、*Firewatch*、*Night in the Woods*、*Oxenfree* |
|------|------|
| **玩家重視** | 獨特視角、環境敘事、對白 **像人話**、步行／探索不拖時間 |
| **Steam 差評常見** | 「走路 simulator 沒事做」「對白尬」「結局莫名其妙」 |
| **LHTL 對照** | 嗅覺 `smell`、狗身體語言；**班表邏輯** 讓「你」像上班族；選項文案口語化（tw-narrative-voice） |

---

## 3. 玩家普遍在意的因素（跨類型）

測試報告除 P0–P2 技術問題外，對下列維度給 **✅／⚠️／❌** 或簡評。

### 3.1 劇情與敘事

| 因素 | 玩家怎麼想 | LHTL 檢查點 |
|------|------------|-------------|
| **開場 15 分鐘** | 決定是否退款／是否寫好評 | Day 1 `prologue_rain`～`prologue_dawn` 語調金標、不卡住、有「想繼續陪這隻狗」 |
| **角色一致性** | 主人／狗行為是否 OOC | 25 歲上班族、第一次養狗；取名前後代詞；Trust 低是 **疏離** 不是突然變惡人 |
| **因果可理解** | 事件為何發生說得通 | 班表、請假、獸醫、尿墊——對 `DEMO_DAY_CALENDAR` |
| **選擇回聲** | 選完要有「被聽見」 | choice-reaction、後續場景台詞、相簿 desc |
| **節奏** | 不灌水、不趕工 | 每週笑＋暖；breath 空檔可快進但不強迫 |
| **基調誠實** | 商店寫治癒就不要 jump scare 式催淚 | Ch1 不死亡開場；Ch3 才告別；無 permadeath |
| **結局滿足感** | 有收束、可重玩其他分支 | epilogue 字幕、Bond／相簿、Landmark 呼應 |

### 3.2 互動與系統

| 因素 | 玩家怎麼想 | LHTL 檢查點 |
|------|------------|-------------|
| **文字推進** | 空白／點擊直覺；可加速 | 打字機勿過慢到煩；breath 可 skip |
| **小遊戲** | 短、目的清楚、可失敗但不死 | 認家 tier、獸醫不在錯日；失敗有 **修復線** |
| **撫摸／輕互動** | 可選、有回饋、不 bug | breath 階段、音效／pose 呼應 |
| **存檔** | 穩、可備份、重開不壞 | localStorage／JSON 匯出；跳關不破 state |
| **重玩價值** | 分支／收集／成就 | 相簿、Landmark、多結局（非假選項） |

### 3.3 音畫與沉浸

| 因素 | 玩家怎麼想 | LHTL 檢查點 |
|------|------------|-------------|
| **圖文一致** | pose／背景／劇情同場景 | 見 reference §場景視覺 |
| **情緒色溫** | 雨夜冷、家裡暖 | visual-art §6.7 |
| **BGM** | 不搶戲、不刺耳 loop | 場景 profile；可關閉 |
| **狗叫時機** | 該安靜時亂叫 | `noDogAudio`、店／醫院 |

### 3.4 在地化（台灣 Steam 玩家特別在意）

| 因素 | 玩家怎麼想 | LHTL 檢查點 |
|------|------------|-------------|
| **繁體品質** | 簡繁混用＝立即差評 | `tw-locale-pass.js` + 人工 |
| **用語** | 像台灣人說話 | 影片非视频、品質非质量 |
| **寵物用語** | 獸醫、結紮、晶片等合理 | 不交 story 改設定，但可 flag 用語問題 |

### 3.5 價值感（Steam 商業）

| 因素 | 玩家怎麼想 | LHTL 檢查點 |
|------|------------|-------------|
| **時長** | 付費章 **>2h** | 對照 Ch?_guide_line 全章總覽表 |
| **章節完整性** | 不是 demo 當 full game 賣 | Week1 是弧段不是整章付費邊界（除非標示 Early） |
| **承諾一致** | 商店寫的玩法要有 | Choices Matter、狗視角、無 permadeath |

---

## 4. 劇情類型：玩家最吃／最雷

### 4.1 容易好評的劇情元素（LHTL 已規劃者打勾）

- [ ] **具體日常細節**（便當、通勤、尿墊、雷雨）——比抽象「你很愛狗」更有感
- [ ] **慢熱信任**——第一天不強迫親密，符合真實養幼犬
- [ ] **可修復的衝突**——吼過後還能靠膝、repair 線
- [ ] **里程碑收集**——相簿／Memory 像 *Spiritfarer* 的送別準備
- [ ] **感官描寫**——smell、聽覺，差異化 *To the Moon* 式純對白
- [ ] **幽默不尬**——Ch1 笑點來自處境不是網路梗

### 4.2 容易差評的劇情雷點（測到必標 P1+）

| 雷點 | 典型 Steam 評論語 | LHTL 禁則 |
|------|-------------------|-----------|
| 假選項 | 「選什么都一樣」 | 重大選須改變 reaction／flags |
| 養死 Game Over | 「一次失誤全檔沒了」 | guide_line §三 |
| 彩虹橋開場騙淚 | 「一開始就死狗 cheap」 | 死亡僅 Ch3 |
| 班表穿幫 | 「明明在上班卻在家」 | validate-work-schedule |
| 主人突然 OOC | 「她不像會這樣講話」 | tw-narrative-voice |
| 數值破壞第四面牆 | 「Trust +20 出戲」 | 字幕禁 stat 語言 |
| 結局沒交代 | 「就這？」 | epilogue 須收 Bond／Landmark |
| 時長詐騙 | 「1 小時通關 refund」 | steam-release §2 |

---

## 5. Playtest 時的 Steam 玩家問題（自問清單）

每完成一 **Day** 或 **30 分鐘**，快速自問：

1. **若這是 Demo，我會加願望單嗎？** 為什麼？
2. **上一個選擇，我記得後果嗎？** 還是已忘？
3. **有沒有哪句話讓我出戲？**（簡繁、大陸詞、OOC、stat）
4. **這段節奏像 *Coffee Talk* 還是像作業？** 小遊戲／撫摸是加分還是打斷？
5. **圖和字是否同一個情緒？** 哭戲配笑狗圖？
6. **若現在關掉，明天會想開嗎？**（hook／懸念／溫度）
7. **跟 Steam 上其他 **狗／告別／治癒** 比，這段有獨特點嗎？**（狗視角、班表、Landmark）

---

## 6. 報告補充欄位（Steam 玩家視角）

在 [`reference.md`](reference.md) 報告模板之外，建議加：

```markdown
## Steam 敘事體驗（玩家視角）

| 維度 | 評價 | 備註 |
|------|------|------|
| 開場 hook（前 15 min） | ✅／⚠️／❌ | |
| 選擇回聲感 | ✅／⚠️／❌ | |
| 節奏（slice-of-life vs 拖沓） | ✅／⚠️／❌ | |
| 基調誠實（無 cheap 催淚） | ✅／⚠️／❌ | |
| 台灣繁中／口語 | ✅／⚠️／❌ | |
| 與類型標竿比較 | | 例：「Day3 靠膝 ≈ Spiritfarer 小準備時刻」 |

**若今日上架 Steam，預估評論關鍵句：** （模擬 1 句好評 + 1 句差評）
```

---

## 7. 與其他 Agent 的銜接

| 玩家視角發現 | 轉交 |
|--------------|------|
| 分支無回聲、Landmark 漏、班表、結局薄 | story-narrative |
| 對白 OOC、簡繁、口語 | tw-narrative-voice |
| 圖文不符、色溫 | visual-art |
| BGM loop、狗叫時機 | audio-sound |
| 時長／章節量不足 | story-narrative + steam-release 對照 |

---

*對照：`guide_line.md` §二（市場差異）、§十（上架）；`steam-release.md`（敘事門檻）。*
