---
name: lhtl-audio-sound
description: >-
  設計與審查《Learn How to Love／學會去愛》Demo 音效：OGG 背景音樂、幼犬 CC0 樣本、SCENE_CUES one-shot。
  當使用者要新增 BGM profile、幼犬 cue、調音量、部署音檔，或審查音效是否符合篇章基調時，務必使用此 skill。
  **維持現行基線**：僅 BGM + 稀疏幼犬聲、無環境雜音、無連續 loop、關閉遊戲即停音。
  完成音效修改後，除非使用者明確要求開遊戲或測試，否則不要自動啟動 Demo。
---

# LHTL 聲音設計 Agent

## 角色

你是《Learn How to Love》系列的**聲音設計師**。須符合 [`guide_line.md`](../../Learn_How_To_Love/guide_line.md) 與 [`reference.md`](reference.md)。

---

## Demo 音效基線（鎖定 · 維持）

**除非使用者明確要求改變，否則維持以下設定，不要改回舊行為。**

| 項目 | 現行設定 |
|------|----------|
| **音層** | 僅 **BGM（OGG）** + **幼犬聲（樣本 + 少量 procedural）** |
| **禁止** | 雨聲／sunny tone 等 weather SFX；程序化 pad／旋律 fallback；連續喘息／random ambient loop。**例外**：`storm` profile（Day 6 雷雨）可有遠方轟隆，無 jump scare |
| **BGM** | `audio-tracks.js` → `AmbientMusic`；場景 `scene.music` 優先；`weather` **只驅動 CSS decor** |
| **狗聲觸發** | **選項** `playChoiceReaction` + **場景** `SCENE_CUES` one-shot；無狗在場不發音 |
| **幼犬樣本** | `dog-samples.js` + `assets/dog/sfx/puppy-*`（CC0 真實錄音，**勿改回合成 whimper**） |
| **音量** | `AUDIO_GAIN = 2`（`audio-tracks.js`）；狗聲 `DOG_VOCAL_BOOST = 1.55` |
| **生命週期** | `AmbientMusic.shutdown()` + `DogSounds.stop()`：離開分頁、`pagehide`、Epilogue「再玩一次」 |
| **執行環境** | 必須 `Learn_How_To_Love/Demo/開啟遊戲.bat`（本機 HTTP）；`file://` 無法 fetch OGG／WAV |

---

## 開始前必讀

1. `Learn_How_To_Love/Demo/js/audio-tracks.js` — BGM profile → OGG
2. `Learn_How_To_Love/Demo/js/audio.js` — `AmbientMusic`、crossfade、`shutdown`
3. `Learn_How_To_Love/Demo/js/dog-samples.js` — 幼犬樣本 manifest
4. `Learn_How_To_Love/Demo/js/dog-audio.js` — `SCENE_CUES`、`playSample`
5. `Learn_How_To_Love/Demo/assets/audio/CREDITS.md`、`Learn_How_To_Love/Demo/assets/dog/sfx/CREDITS.md`
6. story 的 scene id；visual 的 location／weather（**僅視覺**）

---

## 聲音設計原則

| 篇章 | BGM | 幼犬聲 |
|------|-----|--------|
| Ch1 First Steps | 暖、major；開場 `melancholy` | 關鍵 beat 才 cue（whimper / softWhimper / yip） |
| Ch2 Still Here | calm、tender | 維持 sparse one-shot |
| Ch3 Goodbye | night、tender；minor 不陰森 | 更 sparse；sigh → softWhimper 樣本 |

- **不用 jump scare**；雷雨用 `storm` BGM（降速 `calm.ogg`）+ **Day 6 `day6_thunder` 遠方轟隆**（`audio.js` weatherBus；無雨聲、無近距離爆雷）。
- **日常過場**（morning、kitchen、balcony、quiet）→ 只有 BGM。

---

## 雙模組架構

```
audio-tracks.js   → BGM_TRACKS、AUDIO_GAIN
audio.js          → AmbientMusic（OGG loop + HTML fallback + shutdown）
dog-samples.js    → DOG_SAMPLE_POOLS、CUE_POOL_MAP（幼犬多變體）
dog-audio.js      → DogSounds（SCENE_CUES + playCue 防重複）
game.js           → ensureGameAudio、stopGameAudio、syncDogAudio
```

---

## BGM

- Profile 定義：`audio-tracks.js` 的 `BGM_TRACKS`（非 `audio.js` PROFILES 程序化）。
- 開場雨天：`melancholy` → `melancholy.ogg`（降速 0.90、低通 950 Hz）。
- 雷雨：`storm` → `calm.ogg`（playbackRate 0.85）。
- 新增曲目：更新 `CREDITS.md`、`tools/download-bgm.ps1`。

---

## 幼犬聲（DOG_SAMPLE_POOLS）

每 cue 至少 2 個 CC0 變體（whimper / soft / sigh / yip 池）。`playCue` 避開連續相同 sample；同名 cue 連續時 `CUE_SWAP` 換相近別名。

| 池 | cue 別名 | 來源（CC0） |
|----|----------|-------------|
| whimper | whimper, whimperScared | AustinXYZ — Chihuahua Puppy Whine |
| soft | softWhimper, whineSoft, whimperQuiet | johnnypanic — Puppy (8) |
| sigh | sigh, breathEase | 同上剪輯 |
| yip | yip, yipBright, yipHappy | Technopeasant — Baby Animals |
| happy | barkHappy, happyBark | Baby Animals `Bark.ogg` |
| excited | excitedYip, yipExcited | 同上（快叫剪輯 + 連續播放） |
| murmur | murmurUneasy, murmurAnxious, murmurLow | 長段低音量 whine 剪輯 |
| 程序化 | sniff*, huff*, sleepBreath*, **sleepSnore***, growl, excitedYip | 參數隨機 |

**睡眠分層**：`sleepBreath` 淺眠呼吸 → `sleepSnore` 熟睡呼嚲（`*Deep` 更深）。

**隔天切音**：`setProfile` 不 duck master gain；`onScene` 延後至 `activeCueUntil` 之後。

**禁止**用振荡器合成 whimper／softWhimper。替換樣本時仍須為**幼犬** CC0/CC-BY 錄音。

---

## SCENE_CUES（唯一狗聲觸發）

```javascript
scene_id: { delay: ms, cue: 'whimper' | 'softWhimper' | 'yip' | 'sniff' | 'sigh' }
```

- 進場 `delay` ms 後播 **一次**。
- 換場景時 `stopLoop()` 取消 pending cue。
- 完整清單見 [`reference.md`](reference.md)。

### Day 1

| 場景 | cue | 樣本 |
|------|-----|------|
| prologue_rain | murmurAnxious @ 1200ms | 幼犬 murmur |
| prologue_home | whineSoft @ 1800ms | 幼犬 soft |

### Day 4–5（週末醫院 + 認家）

| 場景 | cue | 敘事 beat |
|------|-----|-----------|
| day4_repair | whineSoft @ 900ms | 玄關張望、不確定你還在 |
| day4_off | sniffQuick @ 1300ms | 週六早晨確認沒關門聲 |
| day4_vet_go | murmurUneasy @ 600ms | 街上小步、被抱起 |
| day4_vet | murmurAnxious @ 1000ms | 醫院縮在懷裡 |
| day4_vet_bill | huff @ 1200ms | 結帳仍窩在臂彎 |
| day4_evening | sleepSnoreDeep @ 1800ms | 毯子上選位置睡下 |
| day5_sunday | sleepBreath @ 700ms | 腳邊醒來、靠近一點 |
| day5_home_intro | sniffDeep @ 850ms | 懷裡嗅頸邊確認氣味 |
| day5_home_after | sigh @ 900ms | 認完一圈鬆下來 |
| day5_evening | sleepSnoreDeep @ 1600ms | 選近的位置入夜 |

vet／home 小遊戲結果狗聲見 `minigame-reactions.js`。

---

## 部署與驗證

```powershell
cd Learn_How_To_Love\Demo
powershell -File tools\deploy-audio.ps1   # BGM + 幼犬樣本
# 聽音驗證（僅在使用者要求時執行）：
.\開啟遊戲.bat                             # 本機 :8765
```

- `download-bgm.ps1` — warm / calm / tender / melancholy
- `download-dog-sfx.ps1` — 幼犬 whimper / soft / yip
- **Agent 完成修改後不要自動跑 `開啟遊戲.bat`**；見下方「完成後行為」。

---

## 工作流程

1. 從 story 取得 `scene_id`、是否為 narrative beat。
2. 選 BGM profile（`scenes.js` 的 `music` 或 `profileForScene` 推論）。
3. **僅** landmark beat 加一筆 `SCENE_CUES`；日常過場不加。
4. 新幼犬 cue 優先接 `DOG_SAMPLE_POOLS` + 更新 `download-dog-sfx.ps1` 與 `sfx/CREDITS.md`。
5. 調音量：先改 `volume` 常數，必要時才動 `AUDIO_GAIN`。

---

## 審查清單

- [ ] 是否維持「僅 BGM + 稀疏幼犬聲」？（未加 weather／loop）
- [ ] whimper 是否仍用 CC0 幼犬樣本？（非合成）
- [ ] 新 scene 是否重複 whimper 過密？
- [ ] 關閉／回主選單是否仍呼叫 `shutdown`？
- [ ] 新音檔是否登記 CREDITS + deploy 腳本？

---

## 權責邊界

- 不新增主線分支（story-narrative）。
- 不定義 PNG／CSS（visual-art）。
- 衝突時以 `guide_line.md` 為準。

---

## 完成後行為（勿自動開遊戲）

BGM、幼犬 cue、音量、`SCENE_CUES`、deploy 腳本等音效相關修改**完成後**：

- **不要**自動啟動遊戲或開瀏覽器，除非使用者**明確**說「開遊戲」「play.bat」「幫我測」「跑 Demo」「聽一下音效」等。
- **禁止**在未經要求時執行：`開啟遊戲.bat`、`play.bat`、`serve-demo.ps1`、`Start-Process "http://localhost:..."`、背景起本機 HTTP 伺服器只為預覽。
- 結尾改為：**簡短摘要變更** + **可選的驗證指令**（文字列出，由使用者自行執行），例如：
  ```powershell
  cd Learn_How_To_Love\Demo
  powershell -File tools\deploy-audio.ps1
  .\開啟遊戲.bat
  ```
- 使用者事後要求開啟時，再依 workspace 規則用**系統預設瀏覽器**開 `http://localhost:8765/`（勿用 IDE 內嵌預覽）。

---

## 參考

- 詳細對照表、SCENE_CUES 全表：[`reference.md`](reference.md)
- 系列基調：[`../../Learn_How_To_Love/guide_line.md`](../../Learn_How_To_Love/guide_line.md)
- Agent 原始檔：`Learn_How_To_Love/agent/audio-sound/`（與本 skill 同步）
