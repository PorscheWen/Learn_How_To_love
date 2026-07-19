# 生圖兩步驟（最簡版）

> 詳細 MJ 參數見 [`midjourney-guide.md`](midjourney-guide.md)

## 一次性設定

1. **Midjourney** 訂閱（Pro 含 Stealth；Standard 含 Relax 無限）
2. 上傳滿意的水彩幼犬參考圖，取得 **sref** 代碼
3. 複製 `.env.example` → `.env`，填入 `MJ_SREF=你的sref代碼`

---

## 每個 pose 只要 2 條指令

在 `Ch1_Trust/game/tools/` 執行：

```powershell
# ① 定稿（Midjourney 自動開啟，貼上，Relax 或 Fast 生成）
.\art-pose.ps1 mj doorway-lie

# ② 下載滿意的那張後存檔（多數 pose 會自動去背）
.\art-pose.ps1 finish doorway-lie C:\Users\你\Downloads\下載的圖.png

# rain 含紙箱 → 不去背
.\art-pose.ps1 finish box C:\Users\你\Downloads\下載的圖.png
```

完成 → `assets/dog/Week0/dog-doorway-lie.png` 可直接進遊戲。

---

## 分工

| 步驟 | 工具 | 做什麼 |
|------|------|--------|
| 寫 code | **Cursor** | scenes.js、guide |
| ① 定稿 | **Midjourney** | 水彩 PNG + sref |
| ② 存檔 | **art-pose.ps1 finish** | 命名 + 去背 |

---

## 批量（Week0 全部 52 pose）

```powershell
# 重新產生（歸檔舊圖至 _archive/，不用 version1）
.\art-pose.ps1 regenerate Week0

# 或只重匯 prompt
.\art-pose.ps1 batch Week0
```

產出：`assets/dog/mj-batch-week0/`

| 檔案 | 用途 |
|------|------|
| `prompts/01-dog-anxious.png.txt` | 依序複製貼到 MJ（開頭含 `LHTL Week0 dog-anxious` → 下載檔名可對照） |
| `manifest.json` | pose ↔ `dog-{pose}.png` ↔ `finish` 指令 |
| `status.json` | 已完成 / 缺漏 pose 數 |
| `downloads/` | 下載後改名 `dog-{pose}.png`，可 `finish-downloads Week0` 一次存檔 |

Relax 排隊貼上；每張滿意 → `.\art-pose.ps1 finish {pose} 下載路徑.png`

**定 sref 流程：** 先做 `anxious` → 寫入 `.env` 的 `MJ_SREF` → 再跑 `batch Week0` 或 `regenerate Week0`

```powershell
.\art-pose.ps1 list    # pose → dog-{pose}.png
.\art-pose.ps1 help
```

---

Week3 成長圖：`.\art-pose.ps1 finish doorway-lie 路徑.png -Tier Week3`
