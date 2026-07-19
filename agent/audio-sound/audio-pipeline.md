# 音訊資產管線參考（audio-pipeline）

> GitHub 生態：`fmod`、`wwise`、`godot audio bus`、`procedural music generation`、`music-generation-transformers`

---

## 1. 資產管理

### 資料夾結構

```
/audio/bgm
/audio/sfx/ui
/audio/sfx/character
/audio/ambience
```

**LHTL 現行對照：**

| 管線路徑 | 專案路徑 |
|----------|----------|
| bgm | `Demo/assets/audio/*.ogg` |
| sfx/character | `Demo/assets/dog/sfx/puppy-*` |
| ambience | §6.8 正式版規劃（Demo 未實作） |

### 命名規範

| 類型 | 範例 |
|------|------|
| BGM | `bgm_ch1_trust_theme.ogg` |
| UI | `sfx_ui_click_01.wav` |
| 環境 | `amb_forest_night_loop.ogg` |

### 格式

- **BGM：** `.ogg`（壓縮率高、loop 友善）
- **短音效：** `.wav`（低延遲、one-shot）

---

## 2. 實作方式

### 簡單遊戲（LHTL Demo 現行）

- `AmbientMusic`（`audio.js`）+ `DogSounds`（`dog-audio.js`）全域 singleton
- BGM crossfade、`SCENE_CUES` one-shot
- 音量：`AUDIO_GAIN`、`DOG_VOCAL_BOOST`（`audio-tracks.js`）

### 複雜遊戲（正式版推薦）

使用 **FMOD** 或 **Wwise**：

- 設計師在圖形介面設定音樂層切換（例：血量 &lt;20% 時 explore → tense crossfade）
- 程式只觸發事件：

```csharp
FMODUnity.RuntimeManager.PlayOneShot("event:/Player/Footstep_Grass");
```

**遷移注意：** 現行 `BGM_TRACKS` profile 可映射為 FMOD Event 名稱；`SCENE_CUES` 映射為 one-shot Event。

---

## 3. AI 音樂／音效生成

| 工具 | 用途 |
|------|------|
| Suno／Udio | BGM placeholder、風格探索 |
| `suno-ai/bark` 等 | 語音／音效實驗（幼犬聲仍以 CC0 錄音為準） |

### 工作流程

1. Python 腳本或 Colab 執行模型（或 Suno／Udio Web UI）
2. Prompt 範例：`A calm, melancholic piano loop for a rainy night scene, lofi, 120bpm`
3. 生成多版本 → 挑選 → 匯出 `.wav`／`.mp3` → 轉 **`.ogg`** → 放入 `assets/audio/`
4. 登記 `CREDITS.md`；作曲 brief 見 [`music-composition`](../music-composition/SKILL.md)

---

## 4. 部署腳本（LHTL）

```powershell
cd Learn_How_To_Love\Demo
powershell -File tools\deploy-audio.ps1
powershell -File tools\download-bgm.ps1
powershell -File tools\download-dog-sfx.ps1
```

新音檔須同步更新對應 download 腳本與 CREDITS。

---

## 5. Pitfalls

- 手動複製音檔、無命名規範 → 後期難追蹤場景對應
- Demo 加 weather SFX／ambient loop → 違反 Demo 基線（見 audio-sound SKILL）
- AI 產出未檢查 loop 接縫 → 遊戲內明顯斷點
- `file://` 無法 fetch → 須本機 HTTP 或 Electron 打包後測試
