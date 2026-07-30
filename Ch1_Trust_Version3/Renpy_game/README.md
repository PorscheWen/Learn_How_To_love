# Learn How to Love｜Version3 Ren'Py

目前可玩內容：**Ch1 Trust｜Section 01～10 完整章節**（含背靠／選定／送走／薄冰四結局）。

篇幅契約：S01～S07 最短選項路徑皆至少 **5 分鐘**；S08／S09 各約 **8 分鐘**；S10 的 A～D 每條實際結局路線皆至少 **5 分鐘**。

### 商店／預告呈現（上架前鎖定）

- **類型：** 互動小說／純選擇敘事（無小遊戲、無信任數值條、無養死 Game Over）
- **預估時長：** 約 70～85 分鐘；平日可拆三段（S01～04／S05～08／S09～10）
- **預告片切入：** 請從 **S02 後門一瞥** 開始，15 秒內對比睡姿結局（A 背靠／B 回頭確認／D 門邊）
- **重玩價值：** 四結局；主選單「結局一覽」顯示已解鎖 A～D（未解鎖不劇透）；結局畫面可跳 S09 再試；第一次最推結局 B〈選定但還在學〉

## 啟動

執行：

```powershell
.\開啟遊戲.bat
```

啟動腳本會優先使用工作區既有 Ren'Py SDK；若不存在，首次執行會下載 Ren'Py 8.3.7，並安裝 SDK 內附的繁中字型。
主選單可使用「章節選擇」直接從 Section 01～10 開始；跳段會建立該段的預設前置狀態，不影響既有存檔。

### 開發快捷鍵

| 方式 | 作用 |
|------|------|
| 主選單 **「開發：全解鎖結局／隱藏」** | 一鍵解鎖並打開結局一覽（最穩） |
| **F8** 或 **Shift+U** | 同上（主選單／結局一覽／隱藏內容頁皆可） |

解鎖寫入 `persistent`，重開仍保留。點已解鎖項目可看靜幀／全文。

### 章節選擇大綱

- **Section 01｜螢幕光比月亮亮：** 予安習慣獨自度過加班的夜，直到店員提起後門那隻沒力氣的小狗。
- **Section 02｜後門那一瞥：** 她終於轉進後門，看見小7，也第一次試著在害怕面前放慢腳步。
- **Section 03｜大門的臨時國界：** 牠在大門外睡著；她不忍心，開門把牠帶回屋內直到天明。
- **Section 04｜共享同一種安靜：** 沙發與地板隔著兩步，他們不急著靠近，只練習在同一份安靜裡留下。
- **Section 05｜你的聲音有兩種：** 戴上耳機後，予安的聲音變得又快又尖；小7開始分辨，哪一種聲音會為牠慢下來。
- **Section 06｜走廊上的第三者：** 當陌生人的手伸向小7，予安第一次發現，自己已經站進了「我們」這一邊。
- **Section 07｜她倒下的那天：** 予安病得起不了身，小7不懂怎麼照顧人，只知道守在門口，試著等她回應。
- **Section 08｜走到轉角就好：** 第一次出門只為抵達巷口；世界太吵時，予安得決定要拉著牠，還是一起停下。
- **Section 09｜差點交給別人：** 同事真誠提出接手；在牽繩交出去以前，予安必須承認誰已經選過誰。
- **Section 10｜把鑰匙分給心跳：** 鑰匙與牽繩掛在同一面牆上；夜深後，睡眠的距離替這段關係留下答案。

## 已實作契約

- 女主固定為「予安」。
- 狗預設名「小7」，外型 **Option B｜wiry**（見 `../agents/image_dog.md`）；後續可由玩家改名。
- S01 的 `trust`、`dist`、`tone`、`guard` 全程維持 `0`；唯一風味選擇寫入 `flags["peeked_backdoor"]`。
- S02 依 `peeked_backdoor` 軟分軌開場；信任選擇組（蹲等 `+1`／硬抱 `−1`／趕走後良心回頭淨 `0`）為本段唯一動 trust 的選項組，路徑選擇寫入 `called_shelter`／`vet_first`／`gate_night`，溫柔路線加成後淨變動落在 `0～+2／−1`。演出採後門遠距進場、距離選擇、退一步測試與空紙箱離場四拍；蹲等路線以 `far → mid → near` 和 `melancholy → tender → warm` 回應信任。
- S03 完整實作路徑開場、外套風味、歸來信任選擇；夜裡見狗在**公寓大門外**睡著後**一定帶回屋內**（`entrance` 玄關／客廳軟分軌），待到天明再進 S04。背景序列：`gate-night` → `entrance-night` → `living-night` →（清晨）`entrance-day`／`living-day`。
- S04 完整實作平行安靜／硬抱合照／關浴室三種質地，以及「只到廚房門口」記憶點。
- S05 完整實作 Tone 軸、視訊早會、耳機回授／主管點名高峰、拔插頭「喀」聲回收，以及正式改名 UI；可保留「小7」或輸入最多 12 字的新名字，空白輸入沿用原名。
- S06 完整實作 Guard 軸、鄰居持續伸手說服、推車輪「喀、喀」壓力、選擇站位、「我們」與額頭輕碰記憶點。
- S07 完整實作發燒守門、起身失敗／耳鳴體感高峰、Tone 延續與「我還在」，並以兩道呼吸收束；禁止把小7寫成會拿藥或預知病情的靈犬。
- S08 完整實作胸背帶穿戴、低／中／高信任外出軟分軌、Dist 停等／硬拖／提早回家，以及鞋邊睡記憶點。巷口狗一開始在身後不願前進，再慢慢跟上；轉角機車呼嘯嚇退回身後。停等 `behind／far → mid → near`、提早回家 `mid` 鬆弧或硬拖全程緊張距離，最後用返家距離及同事提議收束四拍。
- S09 完整實作 G2 被選中、Guard 留下／送走硬分歧；同事維持真誠，送走不責罵玩家。
- S10 不再修改 trust，依 `gave_away`、trust 區間與 `s08_forced_walk` 分流 A～D 四結局。
- 本版維持純敘事選項，不加入小遊戲、牽繩微互動或快問快答；S08 張力由 Dist 選項與狗姿勢表達。
- 不顯示 trust 數字，不播放信任升級音效；狗的距離用 `dog_far`→`dog_mid` 位移表達。
- Section 標題卡使用 `section_title` 全螢幕淡入（主標 2.6 秒、副標延遲 1.2 秒浮現）；**重訪同一段時**副標加速、0.5 秒即提示點擊。
- S04／S06／S08 段末收束後直接接續；四結局後進入 `ending_aftercare`（推結局 B、可跳 S09 重試、可開結局一覽）。
- 主選單「結局一覽」：`persistent.unlocked_endings` 記錄 A～D；達成後可點開結局靜幀（`gallery/ending-*.png`）；未解鎖顯示「尚未解鎖」。
- 隱藏紀念照：結局 A 解鎖 `gallery/secret-lap-sleep.png` 與 `secret-back-to-back.png`；未解鎖顯示「？？？」與軟提示，不顯示親密％。
- 隱藏內容：各結局解鎖狗日記／予安心境／朋友視角全文（`hidden_content.rpy`）；主選單「隱藏內容」可閱讀。
- 結局收束：`endings.rpy` 的 `ending_coda_finish`（安靜睡姿節拍 → 標題卡 → 解鎖提示 → `ending_aftercare`）；`process_ending_unlock` 寫入日記／心境／朋友視角（A 另含紀念照＋Ch2 提示）；`sync_unlocked_ending_rewards` **必須回傳 `None`**（禁放進主選單 `action` 清單，否則 `True` 會開新遊戲）。
- 人物立繪：S08 玄關用 `char-yuan-leash`（蹲）、巷口用 `char-yuan-walk`（走路；樹下停等才切回蹲）；S09 客廳用 `char-yuan-farewell`、玄關用 `char-yuan-leash`（×0.8）、咖啡廳用 `char-yuan-cafe`＋`char-coworker-cafe`；缺檔有 fallback。
- 狗立繪：S07～S10 依守門、牽繩、告別、咖啡廳拒絕／僵住與三種睡姿切換；缺檔不阻擋遊戲。
- BGM：S07 使用專屬 `sick-guard.ogg`；S09 使用 `almost-gave.ogg`；結局依 A～D 切換，所有新增音源皆已登記於 `assets/audio/CREDITS.md`。
- 狗 SFX：`dog_sfx()` 以低音量播放稀疏 one-shot；S02／S03／S05／S06／S07／S08／S09 使用 `soft`、`whimper`、`murmur`、`bark`、`growl`，S01 與結局 C 空屋不播放。音源授權見 `assets/audio/sfx/CREDITS.md`。

### 選單 UI 契約（`screens.rpy`）

- 主選單：標題卡 `ymaximum 660`；「設定｜離開」並排 `hbox`（避免「離開」被裁出 720p 下緣）。
- 結局一覽／隱藏內容／章節選擇：`side "t c b"`＋viewport `yfill`；返回用 `If(main_menu, ShowMenu("main_menu"), Return())`。
- 存讀檔／設定／對話紀錄：共用 `game_menu`（標題／內容／返回分區）；設定頁**禁止**在 `game_menu` 的 side 中央放 `viewport`＋`yfill`（高度會歸零、整頁空白）；設定內容用一般 `vbox`；「離開遊戲」為 `Quit`，**不要**用 `MainMenu()`。
- 靜幀／紀念照：深色底＋標題置頂、關閉置底；點空白可關。

### 重新取名 UI 契約

- `script.rpy` 的 `dog_label` 與 `proposed_name` 必須以 `default` 宣告，讓存讀檔與 rollback 正常保留狀態。
- `screens.rpy` 必須保留 `screen input(prompt)`，且輸入元件使用 `input id "input"`；這是 `renpy.input()` 的必要畫面，刪除會造成 S05 取名時 crash。
- 改名後應立即在敘事使用新名字，並帶入 S06 與後續存檔；改名不影響 trust 或三軸。

## 資產覆寫

```text
../assets/
├─ bg/
│  ├─ bg-office-night.png
│  ├─ bg-convenience-night.png
│  ├─ bg-street-night.png
│  ├─ bg-living-night.png
│  ├─ bg-living-day.png
│  ├─ bg-backdoor-night.png
│  ├─ bg-stairwell-night.png
│  ├─ bg-gate-night.png
│  ├─ bg-entrance-night.png
│  ├─ bg-entrance-day.png
│  ├─ bg-corridor-day.png
│  ├─ bg-alley-day.png
│  ├─ bg-alley-night.png
│  ├─ bg-cafe-day.png
│  ├─ bg-kitchen-day.png
│  └─ bg-living-dusk.png
├─ char/
│  ├─ char-yuan-headphones.png
│  ├─ char-yuan-commute.png
│  ├─ char-yuan-block.png
│  ├─ char-yuan-leash.png
│  ├─ char-yuan-walk.png
│  ├─ char-yuan-farewell.png
│  ├─ char-yuan-cafe.png
│  ├─ char-clerk.png
│  ├─ char-neighbor.png
│  ├─ char-coworker.png
│  └─ char-coworker-cafe.png
├─ dog/
│  ├─ dog-ref-canonical.png
│  ├─ dog-anxious.png
│  ├─ dog-halfstep.png
│  ├─ dog-stair-watch.png
│  ├─ dog-door-sleep.png
│  ├─ dog-parallel.png
│  ├─ dog-kitchen-door.png
│  ├─ dog-ear-flat.png
│  ├─ dog-sniff-wire.png
│  ├─ dog-behind-legs.png
│  ├─ dog-forehead-nudge.png
│  ├─ dog-guard-door.png
│  ├─ dog-street-tense.png
│  ├─ dog-leash-wait.png
│  ├─ dog-shoe-sleep.png
│  ├─ dog-farewell.png
│  ├─ dog-cafe-refuse.png
│  ├─ dog-cafe-tense.png
│  ├─ dog-refuse-stranger.png
│  ├─ dog-back-sleep.png
│  ├─ dog-check-sleep.png
│  └─ dog-door-edge.png
├─ gallery/
│  ├─ ending-a-back.png
│  ├─ ending-b-learning.png
│  ├─ ending-c-handover.png
│  ├─ ending-d-thin-ice.png
│  ├─ secret-lap-sleep.png
│  └─ secret-back-to-back.png
└─ audio/
   ├─ calm.ogg
   ├─ warm.ogg
   ├─ tender.ogg
   ├─ melancholy.ogg
   ├─ sick-guard.ogg
   ├─ almost-gave.ogg
   └─ first-light.ogg
```

### 生圖政策（鎖定）

1. **預設用 Cursor `GenerateImage`** 產出背景／立繪；狗圖必附 `assets/dog/dog-ref-canonical.png`。
2. 綠幕立繪再以 `python tools/remove_ai_bg.py INPUT OUTPUT ...` 去背。
3. `tools/flux_*.py`（FLUX 2 Pro）僅在 Cursor 不可用、或使用者明確指定時當備援。
4. `assets/bg/`、`assets/char/`、`assets/dog/` 只放遊戲正式資產；綠幕來源放 `assets/dog_mj/`，去背完成後刪除遊戲目錄內的 `*-green.png`。
5. 不保留未引用備援圖、`assets/dog_old/` 舊圖或 `*-regen` 中介圖。

### 2026-07-19 美術更新

- 狗圖：19 張來源／正式資產（18 個遊戲 pose＋`dog-ref-canonical`）；重產 6 張關鍵全身 pose，移除未引用 `dog-door-sleepy`。
- 背景：正式背景含 S03 `gate-night`（公寓大門外側）；舊 `stairwell-night` 資產保留未刪。
- 清理：刪除 `assets/dog_old/`、角色／狗綠幕中介檔與測試暫存輸出。

S09／S10 正式圖已用 Cursor 落地（含 2026-07-28 S09：`farewell`／`cafe` 專用立繪、`bg-cafe-day`、四結局／拒絕 pose）。若備援重跑 `tools/flux_*.py`，請先輸出到工作暫存目錄；去背完成後只搬入透明正式檔，不把 `*-green.png` 留在 `assets/char/` 或 `assets/dog/`。朝向與 transform 見 `../agents/section_09_almost_handoff.md`。

## 驗證

```powershell
cd Renpy_game
python .\tools\validate-s01.py
python .\tools\validate-reading-time.py
python .\tools\validate-s10.py
python .\tools\validate-all-endings.py
python .\tools\validate-menus.py
python .\tools\validate-menu-layout.py
```

| 腳本 | 用途 |
|------|------|
| `validate-s01.py` | 結構／flags／trust／簡繁／結局解鎖骨架 |
| `validate-reading-time.py` | S01～S10 閱讀時間粗估（S10 雙分支會偏鬆） |
| `validate-s10.py` | S10 單一路徑 ≥5 分＋結局路由真值表 |
| `validate-all-endings.py` | 四結局 coda／解鎖／aftercare 對齊 |
| `validate-menus.py` | 主選單出口、返回、設定無 `MainMenu`、章節 Start 標籤 |
| `validate-menu-layout.py` | 1280×720 框高、side／yfill、設定禁 nested viewport |

S05 另需手動測試兩條取名路徑：保留「小7」與輸入新名字；並測空白輸入、存檔後讀檔、回溯及進入 S06。完整項目見 `../agents/tester.md` §4.2。
S09／S10 需各跑高信任留下、中信任留下、任意分數送走與低信任留下，確認 A～D 四標籤與 `s08_forced_walk` 排除 A 的規則。
選單實機：主選單 → 結局／隱藏／章節／設定／存讀檔 → 各自返回；設定內容須可見（非空白）；報告見 `../agents/tester_menus_report.md`。

若本機已有 Ren'Py SDK，也可執行：

```powershell
.\tools\renpy-sdk\renpy.exe . lint
```
