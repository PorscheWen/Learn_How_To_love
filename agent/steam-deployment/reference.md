# Steam 部署參考（steam-deployment）

> GitHub 生態關鍵字：`Steamworks.NET`、`Facepunch.Steamworks`、`GodotSteam`、`github actions for steam deployment`、`game-ci/steam-deploy`

---

## 1. GitHub Actions 範本（概念）

```yaml
# .github/workflows/steam_deploy.yml
name: Steam Deploy

on:
  workflow_dispatch:
    inputs:
      release_branch:
        description: 'Steam branch (beta/release)'
        default: 'beta'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install & Electron build
        run: |
          npm ci
          npm run build:electron   # 專案自訂：產出 dist/

      - name: Upload to Steam
        uses: game-ci/steam-deploy@v3
        with:
          username: ${{ secrets.STEAM_USERNAME }}
          password: ${{ secrets.STEAM_PASSWORD }}
          configVdf: ${{ secrets.STEAM_CONFIG_VDF }}
          appId: ${{ secrets.STEAM_APP_ID }}
          buildDescription: ${{ github.sha }}
          rootPath: dist
          depotId: ${{ secrets.STEAM_DEPOT_ID }}
          releaseBranch: ${{ inputs.release_branch }}
```

**注意：** 實際 `configVdf`／depot 結構依 Steam Partner 後台為準；`STEAM_BUILDER_KEY` 有時併入 config 或獨立 secret，依 `game-ci/steam-deploy` 文件調整。

---

## 2. LHTL 封裝路線

| 階段 | 工具 | 產出 |
|------|------|------|
| 現行 | 本機 HTTP Demo | 開發驗證 |
| Steam | **Electron** + `electron-builder` | `.exe`、`.app`、Linux AppImage |
| Steam API | `greenworks` 或 `steamworks.js` | 成就、Cloud Save、統計 |

### Electron 檢查項

- 鎖定 **16:9**；全螢幕／視窗縮放
- `file://` 或內建協議可載入 OGG／PNG（現行 Demo 依賴 HTTP 者須改 asset 路徑）
- 離線：BGM、幼犬樣本本地可播

---

## 3. 成就建議清單（草案）

| API id | 觸發條件 |
|--------|----------|
| `ACH_FIRST_PET` | 首次撫摸狗（§6.9） |
| `ACH_THUNDER_MEMORY` | 解鎖雷雨 Memory |
| `ACH_CH1_COMPLETE` | 完成 Ch1 主線 |
| `ACH_LANDMARK_PAW` | 觸發指定 Landmark（依章節擴充） |

成就字串須進在地化檔（`zh-TW.json`／`en.json`），不硬編碼於 JS。

---

## 4. Cloud Save 欄位（對照 guide_line §五）

最低限度同步：

- `dogName`、`memories[]`、`flags`、`favoriteSpot`
- Bond／Trust 關鍵選擇、Landmark 鎖定狀態
- `saveVersion` — 升級時須 migration 腳本

Steam Auto-Cloud：在 Partner 後台設定與本地存檔路徑一致。

---

## 5. Secrets 清單

| Secret | 用途 |
|--------|------|
| `STEAM_USERNAME` | CI 登入 |
| `STEAM_PASSWORD` | CI 登入（建議機器人帳號） |
| `STEAM_BUILDER_KEY` | 建置權限 |
| `STEAM_APP_ID` | App ID |
| `STEAM_DEPOT_ID` | Depot ID |
| `STEAM_CONFIG_VDF` | 可選；部分 Action 需要 |

---

## 6. 本機測試

1. 在執行檔目錄放置 `steam_appid.txt`（內容為 App ID 數字）。
2. 透過 Steam 客戶端啟動遊戲（或開發者模式）。
3. 驗證 `SetAchievement`／存檔上雲。

---

## 7. 與其他 Agent

| 需求 | Agent |
|------|-------|
| 章節時長、結局數、商店敘事 | story-narrative |
| 膠囊圖、截圖美術 | visual-art |
| 字串抽離 zh-TW／en | 本 skill 規劃；文案來源 tw-narrative-voice |

---

*與 `guide_line.md` §10.5 同步；衝突時以 guide_line 為準。*
