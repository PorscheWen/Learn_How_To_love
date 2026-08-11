# Nous Portal · API 與本機設定

> **金鑰與端點以本檔為準。** 實際金鑰值寫入 `Learn_How_To_Love/tools/hermes/.env`（已 gitignore，勿提交）。

---

## 1. 金鑰對照表

| 環境變數 | 用途 | 取得方式 |
|----------|------|----------|
| `NOUS_API_KEY` | Nous Inference API（`sk-nous-…`）· 劇本／chat completions | [Nous Portal](https://portal.nousresearch.com) Dashboard |
| `CURSOR_API_KEY` | Cursor SDK pipeline（`hermes code`／`pipeline` 寫碼） | [Cursor Integrations](https://cursor.com/dashboard/integrations) |
| （OAuth） | 官方 Hermes CLI · **生圖 FLUX／TTS** Tool Gateway | 終端執行 `hermes login`（token 存 `%LOCALAPPDATA%\hermes\auth.json`） |

**生圖／TTS 一鍵 job** 用 OAuth，**不需**在 `.env` 填 `NOUS_API_KEY`。  
**Inference API** 腳本／批次文本才需要 `NOUS_API_KEY`。

---

## 2. 寫入 `tools/hermes/.env`

```env
# 金鑰說明見 Ch1_Trust/Nous_Portal.md
NOUS_API_KEY=sk-nous-xxxxxxxx
CURSOR_API_KEY=cursor_xxxxxxxx

HERMES_GAME_CWD=../../Ch1_Trust_Version3/Renpy_game
HERMES_CONTENT_MODEL=deepseek/deepseek-v4-pro
HERMES_AGENT_PROVIDER=nous
HERMES_AGENT_MODEL=google/gemini-2.5-pro
HERMES_AGENT_CWD=../..
HERMES_PORTAL_HOST=127.0.0.1
HERMES_PORTAL_PORT=8780
```

複製範本：`tools/hermes/.env.example` → `tools/hermes/.env`，再依上表填入。

---

## 3. Inference API 範例（curl）

```bash
curl --request POST \
  --url https://inference-api.nousresearch.com/v1/chat/completions \
  --header "Authorization: Bearer $NOUS_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
  "model": "deepseek/deepseek-v4-pro",
  "messages": [
    { "role": "system", "content": "You are a helpful AI agent." },
    { "role": "user", "content": "Generate scene JSON for LHTL Ch1." }
  ],
  "max_tokens": 4096
}'
```

PowerShell：

```powershell
$headers = @{ Authorization = "Bearer $env:NOUS_API_KEY"; "Content-Type" = "application/json" }
$body = @{
  model = "deepseek/deepseek-v4-pro"
  messages = @(
    @{ role = "system"; content = "You are a helpful AI agent." }
    @{ role = "user"; content = "with FLUX 2 Pro and OpenAI TTS for LHTL assets" }
  )
  max_tokens = 4096
} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "https://inference-api.nousresearch.com/v1/chat/completions" -Method Post -Headers $headers -Body $body
```

---

## 4. 生圖／TTS（Tool Gateway）

| 工具 | 模型／服務 | 本機觸發 |
|------|------------|----------|
| **所有生圖（背景＋狗 pose）** | **FLUX 2 Pro（`fal-ai/flux-2-pro`）** | Portal `一鍵產生` 或 `python hermes.py agent --job lhtl-flux-…` |
| 旁白 | OpenAI TTS（Portal Gateway） | `python hermes.py agent --job lhtl-tts-week4-intro` |

**風格鎖定（Version2）：** 印象派油畫（見 `agents/image.md`）；背景命名 `bg-{place}-{light}`（見 `agents/image_bg.md`）。狗 pose 對齊 `assets/dog/dog-anxious.png`（golden-tan 幼犬、乾淨底方便去背）。

**浴室／吹風機相關 job：**

```powershell
cd Learn_How_To_Love\tools\hermes
python hermes.py agent --job lhtl-flux-bathroom-night   # → Renpy_game/game/assets/bg/bg-bathroom-night.png
python hermes.py agent --job lhtl-flux-dog-dryer        # → …/dog/Week0/dog-dryer.png
python hermes.py agent --job lhtl-flux-dog-wet          # → …/dog/Week0/dog-wet.png
```

美術落地目錄：**`Ch1_Trust_Version3/assets/`**（及 Ren'Py 引用路徑）。舊 HTML `Ch1_Trust/game/` **已不在本倉庫**。

前置：`hermes login` 且 `config.yaml` 內 `image_gen.use_gateway: true`、`tts.use_gateway: true`。

啟動本地 Portal UI：

```powershell
cd Learn_How_To_Love\tools\hermes
.\start-portal.ps1
# → http://127.0.0.1:8780/
```

---

## 5. Agent 行為（重要）

- **修改 `Ch1_Trust_Version3/` 後，不要自動開啟遊戲**，除非使用者明確要求。
- 驗證：`python Ch1_Trust_Version3/Renpy_game/tools/validate-*.py`；開遊戲僅在使用者說「開遊戲」「測試」時執行對應 `開啟遊戲.bat`。

---

*最後更新：2026-08-11 · Playable＝Version3 Ren'Py*
