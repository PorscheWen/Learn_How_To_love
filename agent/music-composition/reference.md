# LHTL BGM 參考表

> 整合落地見 `audio-sound` · 現行 manifest：`Ch1_Trust/game/js/audio-tracks.js`

## BGM_TRACKS（現行）

| Profile | OGG | volume | 變體參數 |
|---------|-----|--------|----------|
| warm | warm.ogg | 0.34 | — |
| calm | calm.ogg | 0.30 | — |
| tender | tender.ogg | 0.32 | — |
| hopeful | warm.ogg | 0.36 | — |
| sunny | warm.ogg | 0.32 | — |
| sunset | tender.ogg | 0.30 | — |
| night | calm.ogg | 0.26 | rate 0.93, filter 1300 Hz |
| rain | calm.ogg | 0.28 | filter 1500 Hz |
| tense | calm.ogg | 0.24 | rate 0.88, filter 850 Hz |
| storm | calm.ogg | 0.22 | rate 0.85, filter 800 Hz |
| melancholy | melancholy.ogg | 0.28 | rate 0.90, filter 950 Hz |

`AUDIO_GAIN = 2`（全域倍率，由 audio-sound 調整）。

## 場景 mood → profile 建議

| 敘事情境 | 建議 profile | 備註 |
|----------|--------------|------|
| 開場雨天、被遺棄 | melancholy | 降速鋼琴 |
| 日常在家、廚房、陽台 | warm / calm | 不搶戲 |
| 週末、公園、陽光 | sunny / hopeful | 略亮 |
| 黃昏、相處默契 | tender / sunset | 輕鋼琴 |
| 夜間、入睡 | night | 低通 calm |
| 醫院、等待 | tense | 略沉，非驚悚 |
| Day 6 雷雨 | storm | 遠方轟隆由 audio.js；BGM 降速 |
| 週 epilogue | tender | 具象收束，不煽情 |

## 授權來源（Demo bundled）

| 檔案 | 作者 | 授權 |
|------|------|------|
| warm.ogg | Eric Matyas — Peaceful Intro | CC-BY |
| calm.ogg | bart — Peace at last | CC-BY |
| tender.ogg | Trinnox — Thoughtful Piano Theme | CC-BY |
| melancholy.ogg | Centurion_of_war — Emotional Piano | CC0 |

Steam 正式版 credits 須完整署名（見 `CREDITS.md`）。

## 推薦 CC0 擴充（選曲用）

| 資源 | 風格 |
|------|------|
| Yoiyami — First Light Particles | 大氣鋼琴 ambient |
| Yoiyami — Yoiyami Core Theme | 深藍 emotional piano |
| Dylann Taylor — Playful Piano | 四種變奏 loop |
| Michael Kalra — Grand Piano Vibes | 12 曲 + loops |

## 新曲檢查

- [ ] OGG seamless loop（聽接縫）
- [ ] 與現行四曲音量平衡
- [ ] CREDITS.md 已登記
- [ ] profile 名稱與 story `music` 欄一致
