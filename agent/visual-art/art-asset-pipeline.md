# 美術資產管線參考（art-asset-pipeline）

> GitHub 生態：`aseprite-cli`、`texturepacker-cli`、`blender-cli`、`stable-diffusion-art`、`photoshop-scripting`

---

## 1. 源文件與導出分離

| 層級 | 路徑 | 打包進遊戲 |
|------|------|------------|
| 原始檔 | `src/art`、`raw_assets`、`mj-batch-week0/` | ❌ 否 |
| 遊戲資產 | `assets/dog/`、`assets/bg/` | ✅ 是 |

**LHTL 現行：**

- MJ 批次：`Ch1_Trust/game/assets/dog/mj-batch-week0/`
- 遊戲內：`Week0/dog-{pose}.png`、`bg/bg-{slug}.png`
- 去背：`Ch1_Trust/game/tools/remove_dog_bg.py`

---

## 2. 自動化腳本（CLI）

### 角色動畫（Aseprite — 若日後 sprite 動畫）

```bash
aseprite -b character.aseprite --sheet character_sheet.png --data character_sheet.json
```

LHTL 現以 **靜態水彩 PNG + CSS/GSAP 微動** 為主；序列幀見 `visualSequence`（`day4_paw_smell`）。

### UI 圖集（TexturePacker-cli）

將零散 UI icon 合併為 atlas，減少 draw calls——正式版 HUD 擴充時採用。

### LHTL 狗 pose 管線

```powershell
cd Ch1_Trust\game\tools
.\art-pose.ps1 mj doorway-lie
.\art-pose.ps1 finish doorway-lie C:\path\to\download.png
.\art-pose.ps1 regenerate Week0   # 批量
```

---

## 3. AI 生成輔助

| 用途 | 流程 |
|------|------|
| 狗 pose | Midjourney + `--sref`（`midjourney-guide.md`）→ `finish` → 去背 |
| 背景 | MJ/SD WebUI → Photoshop 修飾／分層 → `bg-{slug}.png` |
| 風格一致 | LoRA、sref、固定 prompt 錨點（`dog-anxious.png`） |

---

## 4. 壓縮與優化

- 匯出 `.png` 後用 **tinypng** 或類似工具批次壓縮
- 背景 `background-size: cover`；狗 PNG 透明 RGBA
- 避免把狗畫進背景（兩層資產契約）

---

## 5. Pitfalls

- ❌ 手動匯出、無腳本 → 改 PSD 後遊戲內資產過期
- ❌ `raw_assets` 被打進 Steam depot → 膨脹安裝包
- ❌ Week0／Week3 tier 混用 → 年齡感斷裂（見 SKILL §狗狗年齡）
- ❌ 未跑 `remove_dog_bg.py` → 白底進遊戲

---

## 6. 相關檔案

| 檔案 | 用途 |
|------|------|
| [`art-workflow-quick.md`](art-workflow-quick.md) | 兩步驟生圖 |
| [`midjourney-guide.md`](midjourney-guide.md) | MJ prompt／sref |
| `tools/art-pose.ps1` | mj / finish / batch |
| `tools/remove_dog_bg.py` | 去背 |
