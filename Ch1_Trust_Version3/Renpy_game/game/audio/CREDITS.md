# Version2／Demo BGM — 開源音樂資源

本資料夾的 **OGG 循環曲**。Version2 劇情／背景對照見 [`../../agents/audio.md`](../../agents/audio.md)。  
（若用於舊 Demo JS：檔案缺失時可退回 `js/audio.js` 程序化暖色 pad。）

## 已 bundled（需署名）

| 檔案 | Profile | 來源 | 授權 |
|------|---------|------|------|
| `warm.ogg` | warm, hopeful, sunny | [Peaceful Intro (Looping)](https://opengameart.org/content/peaceful-intro-looping) — Eric Matyas | CC-BY（需署名） |
| `calm.ogg` | calm, night, rain, tense | [Peace at last](https://opengameart.org/content/peace-at-last) — bart | CC-BY（需署名） |
| `tender.ogg` | tender, sunset | [Thoughtful Piano Theme](https://opengameart.org/content/thoughtful-piano-theme) — Trinnox | CC-BY（需署名） |
| `melancholy.ogg` | melancholy（開場雨天） | [Emotional Piano](https://opengameart.org/content/emotional-piano-0) — Centurion_of_war（solo 版） | CC0（建議仍署名） |
| `sick-guard.ogg` | sick_guard | [The Budding of Consciousness](https://opengameart.org/content/the-budding-of-consciousness-%E2%80%93-cc0-ambient-minimalist-theme-yoiyami-blue-series-%E2%80%93-no4) — Yoiyami | CC0 |
| `first-light.ogg` | hopeful | [First Light Particles](https://opengameart.org/content/first-light-particles-%E2%80%93-cc0-atmospheric-pianoambient-track) — Yoiyami | CC0 |
| `almost-gave.ogg` | almost_gave | [Yoiyami Core Theme](https://opengameart.org/content/yoiyami-core-theme-%E2%80%93-deep-blue-ambient-piano) — Yoiyami | CC0 |

**Steam／正式版建議在 credits 加入：**（Demo 已內建「音樂來源」對話框，intro 與 Epilogue 皆可開啟）

> Music: "Peaceful Intro" by Eric Matyas (soundimage.org); "Peace at last" by bart; "Thoughtful Piano Theme" by Trinnox; "Emotional Piano" by Centurion_of_war; "The Budding of Consciousness", "First Light Particles", and "Yoiyami Core Theme" by Yoiyami — via OpenGameArt.org

## 推薦 CC0（免署名，可替換或擴充）

| 資源 | 風格 | 連結 |
|------|------|------|
| Yoiyami — First Light Particles | 大氣鋼琴 ambient | https://opengameart.org/content/first-light-particles-cc0-atmospheric-pianoambient-track |
| Yoiyami — Yoiyami Core Theme | 深藍 emotional piano | https://opengameart.org/content/yoiyami-core-theme-deep-blue-ambient-piano |
| Dylann Taylor — Playful Piano | 四種變奏 + loop OGG | https://dylanntaylor.itch.io/playful-piano （**CC0**） |
| Michael Kalra — Grand Piano Vibes | 12 曲 + 14 loops | https://earentech.itch.io/free-grand-piano-vibes-music （CC BY-SA 4.0） |

## 新增曲目

1. 下載 OGG（建議 48kHz、可 seamless loop）。
2. 存成 `assets/audio/{profile}.ogg` 或更新 `js/audio-tracks.js` 的 `BGM_TRACKS`。
3. 在本表登記來源與授權。
4. 重新整理 Demo 驗證 crossfade。

## 一鍵下載（OpenGameArt 預設三曲）

```powershell
cd Learn_How_To_Love\Demo
powershell -File tools\download-bgm.ps1
```
