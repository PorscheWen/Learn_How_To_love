# Learn How to Love · 學會去愛

敘事向寵物陪伴遊戲系列。本倉庫含 Ch1 Demo《First Steps》與 agent 技能文件。

## 快速開始（Demo）

```powershell
cd Demo
.\play.bat
```

瀏覽器開啟後（預設 `http://localhost:8765/`），從開場選「新開始」或「繼續」。

音訊／狗叫素材若缺失，可執行：

```powershell
cd Demo/tools
.\download-bgm.ps1
.\download-dog-sfx.ps1
```

## 目錄

| 路徑 | 說明 |
|------|------|
| 瀏覽器可玩 Demo（HTML / JS / CSS） |
| `Ch1_Trust/` | **Ch1 正式版第一週**（`game/` 可玩；見 `Ch1_Trust/README.md`） |
| `agent/` | 敘事、音效、視覺等 agent skills |
| `guide_line.md` | 系列設計聖經 |

## 授權與素材

遊戲內 BGM、音效來源見 `Demo/assets/audio/CREDITS.md`、`Demo/assets/dog/sfx/CREDITS.md`。
