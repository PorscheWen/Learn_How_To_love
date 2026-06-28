# 聲音設計參考（Demo 基線）

> **維持現行設定**：BGM + 稀疏幼犬 one-shot；無 weather SFX、無連續 dog loop、無合成 whimper。

路徑前綴：`Learn_How_To_Love/Demo/` · Agent 原始檔：`Learn_How_To_Love/agent/audio-sound/`

---

## 檔案對照

| 檔案 | 職責 |
|------|------|
| `js/audio-tracks.js` | `BGM_TRACKS`、`AUDIO_GAIN`、`BGM_LOOP_PAD` |
| `js/audio.js` | `AmbientMusic`：OGG loop、crossfade、`shutdown` |
| `js/dog-samples.js` | `DOG_SAMPLE_POOLS`、`CUE_POOL_MAP` 幼犬 manifest |
| `js/dog-audio.js` | `SCENE_CUES`、`playCue`（樣本池 + 防連續重複）、`preload` |
| `js/game.js` | `ensureGameAudio`、`stopGameAudio`、`syncDogAudio` |
| `tools/deploy-audio.ps1` | 一鍵部署 BGM + 幼犬樣本 |
| `tools/download-bgm.ps1` | 下載 OGA BGM |
| `tools/download-dog-sfx.ps1` | 下載並剪輯 CC0 幼犬樣本 |

---

## BGM（`BGM_TRACKS`）

| Profile | OGG | 備註 |
|---------|-----|------|
| warm | warm.ogg | 預設室內 |
| calm | calm.ogg | 午後、content |
| tender | tender.ogg | attached、moment |
| hopeful | warm.ogg ↑vol | Day 7 |
| sunny | warm.ogg | 公園、陽台 |
| sunset | tender.ogg | 街道夕陽 |
| night | calm.ogg @0.93 | 深夜 |
| rain | calm.ogg | profile 名稱保留；**無**雨聲疊層 |
| tense | calm.ogg @0.88 | 衝突 |
| storm | calm.ogg @0.85 | 雷雨；**無**雷聲 |
| melancholy | melancholy.ogg @0.90 | **prologue_rain** 開場 |

授權：`assets/audio/CREDITS.md`

### 音量常數

- `AUDIO_GAIN = 2`（全域 BGM 倍率）
- `AmbientMusic`：`MASTER_VOLUME = capGain(0.58)`
- 狗 bus：`DOG_BUS_VOLUME = capDog(0.52)`，`DOG_VOCAL_BOOST = 1.55`

---

## BGM 引擎行為

- **播放**：fetch OGG → Web Audio loop；失敗 → HTML `<audio>` fallback。
- **停用**：程序化 pad／旋律。
- **雷雨 SFX**：`profile === 'storm'`（`day6_thunder`）→ `weatherBus` 低頻 rumble loop + 8–22s 隨機遠方轟隆；**選項點擊**（`day6_check` 雷雨線、`day6_thunder`）→ `triggerStormThunderOnChoice()` 額外轟隆。離開場景／`shutdown` 即停。
- **場景**：`scene.music` 優先；`scene.weather` → 主要驅動 `game.js` decor CSS。
- **關閉**：`AmbientMusic.shutdown()` 立即切斷 + suspend context。

---

## 幼犬樣本池（`DOG_SAMPLE_POOLS`）

| 池 | 變體檔 | cue 別名 | 授權 |
|----|--------|----------|------|
| whimper | puppy-whimper-a/b.wav | whimper, whimperScared | CC0 AustinXYZ |
| soft | puppy-soft-a/b.wav | softWhimper, whineSoft, whimperQuiet | CC0 johnnypanic |
| sigh | puppy-sigh-a/b.wav | sigh, breathEase | CC0 johnnypanic 剪輯 |
| yip | puppy-yip-a.ogg, puppy-yip-b.wav | yip, yipBright, yipHappy | CC0 Technopeasant |
| happy | puppy-bark-a/b.wav | barkHappy, happyBark | CC0 Technopeasant |
| excited | puppy-excited-a/b.wav | excitedYip, yipExcited | CC0 Technopeasant |
| murmur | puppy-murmur-a/b.wav | murmurUneasy, murmurAnxious, murmurLow | CC0 長段 whine |

程序化：`sniff` / `sniffQuick` / `sniffDeep`、`huff` / `huffSoft`、`growl`、**`sleepBreath*` / `sleepSnore*`**（淺眠呼吸 vs 熟睡呼嚲）、`excitedYip`（雙連叫）。

**防重複**：`pickFromPool` 避開 `lastSampleId`；`playCue` 若與上一 cue 同名則 `CUE_SWAP` 換相近 cue。

**隔天不切音**：BGM `setProfile` 維持 master volume；`onScene` 等 `activeCueUntil` 後再播場景 cue。

---

## 狗聲策略

1. **不**使用 `MOOD_PROFILES` 連續 loop（已移除）。
2. **場景** `SCENE_CUES[scene.id]` + **選項** `choice-reactions.js` / `StoryAgent` 觸發 one-shot。
3. `onScene` → `loadSamples()` → `setTimeout(delay)` → `playCue(cue)`。
4. 所有 vocal cue 經 `playCue` → 樣本池或程序化變體。

---

## SCENE_CUES（Demo 全表）

| scene_id | delay | cue | 樣本類型 |
|----------|-------|-----|----------|
| prologue_rain | 1200 | whimper | 幼犬 WAV |
| prologue_home | 2000 | softWhimper | 幼犬 WAV |
| day3_hurt | 900 | softWhimper | 幼犬 WAV |
| day3_potty_intro | 1100 | sniff | 程序化 |
| day3_night | 1500 | whimper | 幼犬 WAV |
| day3_night_after | 2400 | sleepSnoreDeep | 程序化 |
| day4_repair | 900 | whineSoft | 幼犬 WAV |
| day4_off | 1300 | sniffQuick | 程序化 |
| day4_vet_go | 600 | murmurUneasy | 幼犬 WAV |
| day4_vet | 1000 | murmurAnxious | 幼犬 WAV |
| day4_vet_bill | 1200 | huff | 程序化 |
| day4_evening | 1800 | sleepSnoreDeep | 程序化 |
| day5_sunday | 700 | sleepBreath | 程序化 |
| day5_home_intro | 850 | sniffDeep | 程序化 |
| day5_home_after | 900 | sigh | 幼犬 WAV |
| day5_evening | 1600 | sleepSnoreDeep | 程序化 |
| day6_thunder | 500 | murmurAnxious | 幼犬 WAV |
| day6_thunder_after | 1400 | sigh | → softWhimper WAV |
| day7_evening | 1600 | softWhimper | 幼犬 WAV |
| day7_moment | 1000 | sigh | → softWhimper WAV |
| epilogue | 2200 | sigh | → softWhimper WAV |

**無 cue 場景**（僅 BGM）：day3_morning、day3_curious、day3_kitchen、day3_balcony、day3_afternoon、day6_morning、day6_check、day6_quiet、day7_morning 等。day4_vet／day5_home_intro 小遊戲進行中由 `minigame-reactions.js` 播結果 cue。

---

## WEATHER（僅視覺）

| location / scene.weather | CSS decor | 音訊 |
|--------------------------|-----------|------|
| prologue_rain, window_rain | `.decor-rain` | 無 |
| living_storm | `.decor-storm` | **storm BGM + 遠方轟隆**（`audio.js`） |
| balcony, park, street… | `.decor-sunny` 等 | 無 |

---

## 部署指令

```powershell
cd Learn_How_To_Love\Demo
powershell -File tools\deploy-audio.ps1
.\開啟遊戲.bat
```

驗證：新開始 → 開場聽到 melancholy BGM + 幼犬 whimper；日常場景無狗聲；Epilogue 再玩一次 → 音樂立即停止。

---

## 篇章方向（維持基線前提下擴充）

### Chapter 1
- BGM major 為主；狗聲只在 SCENE_CUES 列出的 beat。

### Chapter 2
- 更多 calm、tender BGM；狗聲仍 sparse。

### Chapter 3
- night、tender BGM；狗聲更 sparse，優先 softWhimper／sigh。

---

## 推薦 CC0 資源（擴充用）

| 用途 | 連結 |
|------|------|
| BGM 鋼琴 ambient | [Yoiyami — First Light Particles](https://opengameart.org/content/first-light-particles-cc0-atmospheric-pianoambient-track) |
| 幼犬 whine | Freesound CC0：`AustinXYZ/350593`、`johnnypanic/728029` |
| 幼犬 yip | [Baby Animals Sounds Pack](https://opengameart.org/content/baby-animals-sounds-pack) |

新增樣本後：更新 `dog-samples.js`、`download-dog-sfx.ps1`、`sfx/CREDITS.md`。

---

## 與 visual 色溫對照

| 色溫 | 建議 BGM profile |
|------|------------------|
| warm / content | warm, calm, tender, sunny |
| cold / anxious | tense, melancholy, night |
| storm | storm（BGM only） |
| sunset moment | sunset → hopeful |
