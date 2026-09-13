# Version3｜狗外型鎖定｜image_dog.md

> 對齊：`game_guild.md` · `image.md` · `outline_trilogy_ch1_10sections.md`  
> **定稿：** Option **B｜wiry**  
> **基準參考：** `assets/dog/dog-ref-canonical.png`（之後所有 pose 必須像同一隻）  
> **風格錨點（2026-07-25 用戶定稿）：** `assets/dog/refs/`（`ref-anxious-*`／`ref-side-profile`／`ref-behind-legs`／`ref-refuse-stranger`）  
> 預設名：**小7**（超商暱稱）；玩家可改 → `dogLabel(s)`；圖檔**勿寫死狗名**。  
> 落選候選 A／C／D 與暫存 `dog-option-*.png` **已刪除**，勿再引用。  
> **生圖順序：** 先用 Cursor `GenerateImage`（必附 `dog-ref-canonical.png` ＋至少一張 `refs/`）；FLUX 僅備援。

---

## 0. 一致性原則（必讀）

| 規則 | 說明 |
|------|------|
| **同一隻** | 毛色區塊、耳形、眼型、體型比例，換 pose **也不能變樣** |
| **頭距** | 同場換 pose 用**頭大小**當尺（`image_scale.md` §0.1）；不要對齊全身 visH／bbox |
| **軟分軌** | 高低信任**只改 pose／距離／表情**，不換外型、不換品種感 |
| **分層** | 狗 PNG **獨立一層**；不要畫進背景 |
| **禁純種** | 不要畫成柯基／貴賓／柴犬／哈士奇等一眼認得出的純種 |
| **禁寫字** | 圖上不能有文字、logo、信任數值／HUD |

產新 pose 前：先對照 `dog-ref-canonical.png` 與 `assets/dog/refs/`，再貼下方 **IDENTITY LOCK**。

---

## 1. 定稿外型（Option B｜wiry｜2026-07-25 錨點）

### 1.1 身分卡

| 項目 | 鎖定 |
|------|------|
| 代號 | **B｜wiry**（硬毛、略亂的那隻） |
| 品種感 | 台灣街上常見的 **雜毛混種**（有點像㹴／牧羊犬混出來的，但**絕對不是純種㹴**） |
| 年齡 | **大概兩到三個月** 的小狗（身子還小、緊湊，不是成犬） |
| 體型 | **短腿、結實偏瘦**；像路邊撿來的幼犬；寫實比例，**不要 Q 版** |
| 頭臉 | 臉帶一點稜角、吻部精實；嘴邊跟眉際有 **硬毛鬍鬚感**；眼神要讀得出「有靈魂的大眼睛」 |
| 耳 | **軟軟的 V 形垂耳**貼著頭；耳緣跟耳尖是 **深褐到栗褐色** |
| 眼 | **又大又暖的深褐色**；眼睛要有明顯亮點；能做出擔憂、警戒、求護衛 |
| 鼻 | 小小的、濕潤的 **黑鼻頭** |
| 毛質 | **短到中長、硬毛、略亂**；筆觸要粗厚成一團一團的，不要絲滑細毛 |
| 毛色 | 主色是 **蜜金／金棕色**；背脊有一條 **偏深、帶灰的鞍斑**；耳尖深褐；吻周跟胸口偏 **奶油到淺蜜色** |
| 尾 | 中短、自然下垂或微微捲；會跟著情緒動 |

### 1.2 毛色區塊（不可改）

> 中文說明｜生圖時仍用下方英文色名，兩邊對齊、不要各寫各的。

| 部位 | 中文 | 生圖用色名 |
|------|------|------------|
| 主體 | 蜜金／金棕 | `honey-gold` / `golden-tan` |
| 耳尖＋耳緣＋背脊鞍斑 | 較深的栗褐／深褐帶灰 | `deeper chestnut` / `dark brown grizzle` |
| 胸口＋吻周＋腳掌前緣 | 奶油／淺棕 | `cream` / `light tan` |
| 鼻 | 黑 | `black` |
| 眼 | 暖深褐＋亮點 | `warm dark brown` + catchlight |

```text
主體：honey-gold / golden-tan
耳尖＋耳緣＋背脊 saddle：deeper chestnut / dark brown grizzle
胸口＋吻部周圍＋腳掌前緣：cream / light tan
鼻：black
眼：warm dark brown + catchlight
```

### 1.3 畫風錨點（對齊用戶定稿圖）

> 白話：厚油彩、筆觸很重、毛是一塊一塊的顏料感；左上方暖光；純黑底方便去背。下面整段直接貼給生圖用。

```text
Thick-impasto impressionistic oil painting of ONE puppy.
Heavy tactile brushstrokes; fur as chunky paint clumps, not fine strand realism.
Soft directional warm key light from above-left; dark studio isolation.
Subject centered on SOLID FLAT BLACK (#000000) background for cutout.
Not a photograph, not anime, not chibi, not smooth 3D render.
```

### 1.4 與落選方案的差別（勿混用）

| 代號 | 千萬別畫成這樣（落選，檔案已刪） |
|------|--------------------------|
| A fluffy | 毛太蓬、臉太圓，貴賓感太重 |
| C round | 圓臉、毛太密，偏 Q 版／貼圖感 |
| D slender | 身子太修長優雅，像模特兒站姿 |

**B 要抓的感覺（生圖關鍵詞）：** wiry、scruffy、impasto、honey-tan、dark-tipped floppy ears、grizzled saddle、soulful dark-brown eyes、black studio bg。  
（白話：硬毛略亂、厚筆觸、蜜金色、耳尖偏深、背脊有鞍斑、有靈魂的深褐眼、純黑棚拍底。）

---

## 2. IDENTITY LOCK（每張狗圖必貼）

生圖時把整段貼在 STYLE 之後、POSE 之前：

```text
SAME PUPPY IDENTITY LOCK (Option B wiry — MUST match dog-ref-canonical.png and assets/dog/refs/):
One continuous character across all poses. About 2-3 months old Taiwanese scruffy wiry mixed-breed puppy (not purebred terrier, not corgi, not poodle, not shiba, not husky). Compact short-legged puppy body, slightly thin street-puppy build. Wiry short-to-medium messy coat rendered as thick impasto paint clumps. Honey golden-tan fur; darker chestnut-brown floppy ear tips and a grizzled darker saddle along the back; cream-light tan muzzle area and chest. Soft V-shaped floppy ears close to the head. Large round warm dark-brown eyes with catchlights (soulful "puppy-dog eyes" when looking up). Small wet black nose. Slightly angular scruffy street-puppy face with wiry brow and muzzle whiskers (NOT round plush face, NOT fluffy show-dog coat, NOT slender elegant silhouette). Thick-impasto impressionistic oil painting. Believable puppy proportions. No text, no logo, no name tag, no trust HUD.
```

### STYLE（與 image.md 一致 · 對齊用戶錨點）

```text
Thick-impasto impressionistic oil painting. Heavy visible brushstrokes, painterly impasto texture, soft blended edges, tactile canvas tooth. Warm amber key light from above-left. Soft atmospheric depth, storybook concept-art feel. Not a photograph, not DSLR realism, not anime cel shading, not hard black outlines, not chibi, not flat vector, not smooth 3D.
```

### 去背底板

```text
Centered full body (or clearly readable crop). SOLID FLAT BLACK (#000000) background for cutout. No floor plane, no scenery, no props unless the pose requires a minimal prop (shoe / wire / partial human lower leg / harness).
```

落地後執行：`python tools/remove_ai_bg.py INPUT OUTPUT`

---

## 3. Pose 產出契約

| 規則 | 說明 |
|------|------|
| 表情＋動作 | **每張**都要一起改：耳／眼／嘴／尾／身體姿勢 |
| 信任可讀 | 低信任＝離遠／貼牆／僵住／耳朵平；高信任＝靠近／貼腿／背對睡 |
| 檔名 | `dog-{pose}.png`（例：`dog-anxious.png`）；**不要**再開 Week 子資料夾 |
| 路徑 | `Ch1_Trust_Version3/assets/dog/` |
| 禁 | 同 pose 拿別名湊數；不要把狗畫進背景 |

### Pose 表（對齊 image.md §6.2）

| 檔名 | 表情 | 動作 | 主用 | 錨點 |
|------|------|------|------|------|
| `dog-ref-canonical.png` | 中性側臉 | 全身側立母版 | 外型基準 | `refs/ref-side-profile` |
| `dog-anxious.png` | 擔憂上望 | 低趴、下巴貼前爪 | 低信任備援（S06～） | `refs/ref-anxious-*` |
| `dog-s04-anxious.png` | 擔憂上望 | 低趴、下巴近前爪（S04 橫式填滿畫風） | **S02** 後門；**S05** 低信任開場；**S07** 門縫爪子（`s07_low`） | 生成 |
| `dog-halfstep.png` | 警戒好奇 | 「既不碰你、也不放你走」的半步 | S02 記憶；**S07** 走到床邊／前腳半步／跟到門線；**S08** 聞帶／門檻前／繞鞋 | 生成 |
| `dog-sniff-bento.png` | 小心試探 | 聞米粒／便當味 | S02 距離＋ | 生成 |
| `dog-stair-watch.png` | 警戒 | 靠牆、面向門口方向 | S03 | 生成 |
| `dog-door-sleep.png` | 睏但守門 | 睡在房門外 | S03 鉤子 | 生成 |
| `dog-coat-sniff.png` | 借溫 | 聞／靠外套 | S03 外套 | 生成 |
| `dog-parallel.png` | 放鬆一點 | 兩步遠地板、下巴貼地 | S04 | 生成 |
| `dog-ear-perk.png` | 聽見新聲 | 趴著、耳根抬起朝向聲源 | S04 冷氣喀／耳機；**S07** 碰被角／輕吠 | 生成 |
| `dog-chin-hover.png` | 被突發大聲嚇到 | 耳平、下巴離地一公分 | S04 電視；**S07** 咳嗽停住／留門縫 | 生成 |
| `dog-head-turn.png` | 找誰在吵 | 前身抬起、頭轉向聲源 | S04 手機笑聲 | 生成 |
| `dog-head-up.png` | 聽出聲音不一樣 | 趴著、頭抬向椅上的人 | **S05** 開會尖聲 | 生成 |
| `dog-chair-paw.png` | 把伸手當邀請 | 後腳站、前腳搭上椅緣短木邊 | **S05** 碰耳機線後 | 生成 |
| `dog-chair-stuck.png` | 被回授嚇到 | 後縮、前腳仍卡在椅緣 | **S05** 選擇高峰 | 生成 |
| `dog-chin-floor.png` | 安靜趴定 | 下巴完整貼地 | S04 距離＋ | 生成 |
| `dog-kitchen-door.png` | 跟著觀望 | 停在廚房門檻外 | S04 記憶 | 生成 |
| `dog-ear-flat.png` | 被尖聲嚇到 | 耳朵平、往後退 | S05 語氣− | 生成 |
| `dog-sniff-wire.png` | 好奇 | 聞耳機線 | S05 鉤子 | 生成 |
| `dog-behind-legs.png` | 求保護 | 四腳踏地、縮在小腿邊偷看（不懸空） | S06 | 生成 |
| `dog-s06-retreat.png` | 警戒退開 | 四腳踏地、貼牆後退 | **S06** 低信任／讓摸後 | 生成 |
| `dog-s06-flinch.png` | 被膠帶聲嚇到 | 四腳踏地、低蹲彈一下、頭朝左 | **S06** 紙箱／膠帶 | 生成 |
| `dog-s06-watch-hand.png` | 看那隻手會不會停 | 四腳站、抬頭看左上方的手 | **S06** 鄰居伸手／放下手 | 生成 |
| `dog-s06-freeze.png` | 被摸時僵住 | 四腳鎖死、尾夾、頭朝門 | **S06** 讓摸當下 | 生成 |
| `dog-forehead-nudge.png` | 輕輕道謝 | 四腳踏地、額頭頂小腿 | S06 記憶 | 生成 |
| `dog-guard-door.png` | 不安守門 | 趴在房門口 | **S07** 門線／選 A 摸背後／天亮換腳 | 生成 |
| `dog-nose-fingertip.png` | 輕觸 | 鼻尖碰指尖 | **S07** 清晨指尖＠`dog_bedroom_nose_cu` | 生成 |
| `dog-street-tense.png` | 繃緊 | 貼牆／僵住（**無**胸背帶） | **僅 S04** 客廳；S08 巷口改 `s08-tense` | 生成 |
| `dog-s08-tense.png` | 繃緊 | 貼牆／縮步；**有胸背帶** | **S08** 巷口受驚／硬拖＠behind；空機車 far→behind | 生成 |
| `dog-leash-wait.png` | 累但仍信任 | 穿胸背帶、停步等待 | S08 扣帶後／門檻／跟上／選 A·C；S09 玄關 | 生成 |
| `dog-harness-bite.png` | 適應裝備 | 咬胸背帶布邊 | S08 穿胸背帶 | 生成 |
| `dog-drink-bowl.png` | 急喝水 | 低頭喝水碗 | S08 回家；結局 A | 生成 |
| `dog-shoe-sleep.png` | 安心 | 靠燕麥灰平底鞋邊睡 | S08 記憶 | 生成 |
| `dog-farewell.png` | 告別上望 | 坐著抬頭（無牽繩／無胸背帶） | S09 客廳 | 生成 |
| `dog-paper-bag-sniff.png` | 聞紙袋 | 聞交接用的紙袋 | S09 玄關 | 生成 |
| `dog-cafe-refuse.png` | 拒絕示警 | 胸背帶＋牽繩、貼腳、對伸手僵住 | S09 咖啡廳 | 生成 |
| `dog-cafe-tense.png` | 夾在兩人中間僵住 | 僵住、面向認得的人 | S09 咖啡廳低信任 | 生成 |
| `dog-refuse-stranger.png` | 拒絕 | 胸背帶＋牽繩、低蹲對伸手僵住 | S09 備援 | `refs/ref-refuse-stranger` |
| `dog-back-sleep.png` | 信任落地 | **背對**睡在伸手就碰得到的地方 | 結局 A | 生成 |
| `dog-check-sleep.png` | 選了人，還在確認 | 睡得近，但眼睛睜著確認 | 結局 B | 生成 |
| `dog-door-edge.png` | 信任很薄 | 睡門邊、不看人 | 結局 D | 生成 |

---

## 3.5 動畫序列幀（Seedance 產線｜2026-08-01 新增）

> 靜態 pose 之外的**循環動畫**：以現有 pose PNG 為首尾幀，用 Seedance 圖生影片後抽幀去背。

| 規則 | 說明 |
|------|------|
| 產線 | `tools/seedance-generate.py`（圖生影片，`--pad --ratio 3:4` 防裁切）→ `tools/video-to-frames.py`（抽幀＋白背去背）→ **裁回原圖框架**（見下） |
| 路徑 | `assets/dog/wag/dog-{動作}-{NN}.png`（動作一個子資料夾） |
| 動作純度 | **一個動畫只做一個動作**（如搖尾巴）；耳朵翻起、吐舌等多餘動作的幀直接剔除 |
| 亮度 | 各幀非透明區域平均亮度須標準化（以原圖首幀為基準調 gain，模型輸出偏暗約 10%） |
| **裁回原框（必做）** | `--pad` 會改變畫布幾何（底部留白變大），貼底錨點下狗會**浮空 +90～135px**；抽幀後必須依 pad 幾何把每幀裁回原圖區域再放大回原圖尺寸（橫式 1112×834 crop (111,120,1001,714)→1536×1024；直式 834×1112 crop (120,111,714,1001)→1024×1536），參考 `tools/output/seedance/normalize-frames.py` |
| 縮放 | 裁回原框後 `DOG_POSE_SCALE` **直接沿用靜態 pose 原值**；靜態本身用頭距，勿用 visH 另算 |
| 播放 | 幀數少（<8）用 **ping-pong 來回**避免循環接縫；ATL `pause 0.12` |
| 一致性 | 首幀必用現有 pose PNG，抽幀後逐幀檢查毛色／鞍斑／耳形（同 §5 清單） |

### 已落地動畫

| 動作 | 幀 | 首幀來源 | 用處 |
|------|----|-----------|------|
| `dog wag`（搖尾巴） | `wag/dog-wag-01~05.png`（ping-pong） | `dog-ref-canonical.png` | **S04** 尾隨廚房；S05 取名後 |
| `dog door_sleep`（熟睡呼吸，pause 0.35） | `door-sleep/dog-door-sleep-01~05.png` | `dog-door-sleep.png` | S03 大門外／玄關 |
| `dog back_sleep`（深勻呼吸，pause 0.38） | `back-sleep/dog-back-sleep-01~05.png` | `dog-back-sleep.png` | 結局 A |
| `dog check_sleep`（淺呼吸＋眼微睜，pause 0.32） | `check-sleep/dog-check-sleep-01~05.png` | `dog-check-sleep.png` | 結局 B |
| `dog door_edge`（淺快呼吸，pause 0.26） | `door-edge/dog-door-edge-01~05.png` | `dog-door-edge.png` | 結局 D |
| `dog sniff_wire`（嗅耳機線，順播 pause 0.24） | `sniff-wire/dog-sniff-wire-01~05.png` | `dog-sniff-wire.png` | S05 記憶點 |
| `dog guard_door`（醒著守門呼吸，pause 0.28） | `guard-door/dog-guard-door-01~05.png` | `dog-guard-door.png` | S07 |
| `dog drink_bowl`（舔水，pause 0.10） | `drink-bowl/dog-drink-bowl-01~05.png` | `dog-drink-bowl.png` | S08 回家／結局 A 前 |
| `dog farewell`（尾巴貼地輕掃，pause 0.20） | `farewell/dog-farewell-01~05.png` | `dog-farewell.png` | S09 告別 |

呼吸動畫幀序＝吸氣淺→深（依 content bbox 高度排序），ping-pong 播放即一次完整呼吸；亮度已校正到與靜態原圖一致（模型輸出偏暗約 10%）。

第二批挑幀策略：`sniff_wire` 取「碰線→抬起→再碰線」完整週期**順播**（首尾同相位、無縫）；`farewell` 依 content bbox **寬度**排序（＝尾巴掃地位置）ping-pong；`drink_bowl`／`guard_door` 取連續幀 ping-pong。

2026-08-01 尺寸修正：八個動畫姿勢的幀已全部裁回原圖框架（修正浮空），縮放沿用靜態原值；`sniff_wire` 模型延長到原圖框外的耳機線以窄幅 alpha 淡出收尾（y 1030→1075、左緣 60px）。修正前原幀備份於 `Renpy_game/tools/output/seedance/prenorm-backup/`。

### 3.6 S04 客廳可見高（2026-09-06 鎖定｜舊 visH）

> **未來重校改頭距**（`image_scale.md` §0.1）。下列 63px／76px 是舊算法，未重校前暫留；**不要再開 visH 標靶。**

客廳趴姿切換時，舊算法把**可見內容高度**對齊 `dog-parallel`（客廳約 63px；`DOG_POSE_SCALE` 在 `script.rpy`）。不要為了「圖比較滿」再加大 zoom。站姿 `street-tense` 在客廳約 **76px**（趴的 1.2 倍），與 S05 站姿族同一檔。

| 檔名 | `DOG_POSE_SCALE` | 主用 |
|------|------------------|------|
| `dog-parallel.png` | **0.524**（母尺） | 兩步遠地板 |
| `dog-chin-floor.png` | 0.424 | Dist＋下巴貼地 |
| `dog-ear-perk.png` | 0.414 | 冷氣喀 |
| `dog-chin-hover.png` | 0.558 | 電視突然大聲 |
| `dog-head-turn.png` | **0.369** | 手機笑聲找聲源 |
| `wag/dog-wag-01~05.png` | **0.750** | 尾隨廚房（勿用 `halfstep`，客廳會到 121px） |
| `s04_low` | **0.369** | 關浴室後客廳觀望（同一張 `s04-anxious`；**不要**用後門 0.551，客廳會到 95px） |
| `dog-street-tense.png` | 0.808 | 低信任開場／硬抱合照後（客廳約 76px） |

廚房門檻 `kitchen-door` 用 `dog_kitchen_threshold`（深度例外，不套客廳趴姿尺）。

S02 後門第一次見面用 `dog-s04-anxious`（**0.551**），不用舊 `dog-anxious`（1.575，留白尺，客廳會大一倍）。S04 客廳若要用這張圖，走 `s04_low`／`s05_anxious` 的 0.369。

### 3.7 S05 早會姿（2026-09-06｜舊 visH）

> 同 §3.6：未重校前暫留；**新 pose／重校用頭距**，不要再開「站姿 76px」。

趴姿仍對齊 `parallel` 外框高（客廳約 63px）。站姿／搭椅舊算法對齊**身體厚度**，可見高約趴姿的 **1.20 倍（約 76px）**——後腳站起會比較高，但胸寬同一隻。`chair-paw` 不得再用 parallel 的 0.524（會到約 99px）。S02／S03 共用 pose 用 `s05_*` 別名。予安在左、狗在右且面左。椅緣可留一小段木邊，不要整張椅子。

| 檔名 | `DOG_POSE_SCALE` | 主用 |
|------|------------------|------|
| `dog-head-up.png` | **0.332** | 開會尖聲抬頭（趴姿，對齊 parallel；圖檔面左） |
| `dog-chair-paw.png` | **0.401** | 前腳搭椅緣（站姿族，約 76px） |
| `dog-chair-stuck.png` | **0.472** | 回授後縮、前腳卡住（同站姿族） |
| `s05_anxious` | 0.369 | 低信任開場；Tone 選 C 當下改 `dog_mid` 觀望 |
| `s05_ear_flat` | **0.409** | 選擇後耳平（站姿族；約 76px） |
| `s05_stair_watch` | **0.82**（S06 覆蓋；S03 靜態仍 0.615） | S06 開場鄰居看見養狗（走廊頭距；對齊 retreat） |
| `sniff-wire` 幀 | **0.605** | 低頭嗅線（對齊 parallel 63px）。會後特寫仍用此 pose，場景 zoom `living_wire` **0.30** |
| 靜態 `dog-sniff-wire.png` | **0.401** | 動畫缺幀時備援 |

落地：予安坐左（`char_chair_left`，面右看狗）；狗用 `dog_near`／`mid`／`far`（不翻轉，面左）。低信任開場 `s05_anxious`；尖聲只一次 `head_up`；開會碰線一次 `sniff_wire`＠`dog_near` 即進 `chair_paw`；回授時仍搭椅，主管應名再切 `chair_stuck`；選 A 耳平後停一拍再 `parallel`；選 B `s05_ear_flat`＠far；選 C `s05_anxious`＠mid。會後 hide 予安、`sniff_wire`＠`dog_living_wire_cu`（zoom `living_wire` **0.30**；解鎖回憶 `sniff_wire`）。鄰居看見養狗改在 S06（`s05_stair_watch`＠走廊頭距 0.82）。不改 S02／S03 全域 scale。

### 3.8 S06 走廊姿（2026-09-10）

躲／退／嚇到皆**四腳踏地**，`padB ≈ 8`。同場用**頭**當比例尺（母尺 `s06-retreat` **0.557**），不要再用 bbox 高或胸寬把站姿縮成迷你狗、把蹲縮放大成另一隻。遠近只改 `xalign`。予安梯廳外出裝見 `image_char.md`。

| 檔名 | `DOG_POSE_SCALE` | 主用 |
|------|------------------|------|
| `s05_stair_watch` | **0.82** | 開場看見養狗（覆蓋；S03 `stair_watch` 仍 0.615） |
| `dog-behind-legs.png` | **0.38** | 高 Tone 躲腿後 |
| `dog-s06-retreat.png` | **0.557** | 低信任貼牆／讓摸後（頭距母尺） |
| `dog-s06-flinch.png` | **0.38** | 膠帶聲彈一下（蹲縮族） |
| `dog-s06-watch-hand.png` | **0.58** | 看鄰居伸過來的手（直立，頭距對齊 retreat） |
| `dog-s06-freeze.png` | **0.62** | 被摸當下僵住（直立，頭距對齊 retreat） |
| `forehead-nudge` | **0.578** | 進屋後額碰頭特寫＠`dog_entrance_nudge_cu`（只留 bg＋放大；zoom `entrance_nudge` **0.28**；解鎖回憶 `forehead_nudge`）。禁客廳 `dog_nudge` |

站位：鄰居 `char_s06_neighbor`（0.22）、予安 `char_s06_yuan`（0.60）、狗 far／mid／near／behind **0.42／0.50／0.54／0.66**。躲腿先 show 狗再 show 人。同場人身高見 `CHAR_POSE_SCALE`（`carry_pup` **1.056**）。

### 3.9 S07 病床／守門（2026-09-13）

臥室狗尺 0.139（同客廳地板），遠近只改 xalign。頭距母尺 `guard_door` **0.438**。指尖特寫另開 `bedroom_nose` **0.30**（頭仍對齊母尺再靠近）。**禁**舊 `dog-anxious` 1.575。**禁**把 S05 站姿 `s05_ear_flat` 拿回臥室（頭會縮小）。**禁**臥室用 `coat_sniff`（圖內有外套）。

| 檔名／標籤 | `DOG_POSE_SCALE` | 主用 |
|------------|------------------|------|
| `s07_low` | **0.43** | 開場門縫爪子；低信任來回；選 B 回房＠`dog_bedroom_far` |
| `halfstep` | **0.580** | 走到床邊／叼拖鞋回門／前腳半步／跟到門線 |
| `ear_perk` | **0.414** | 鼻尖碰被角；輕吠確認 |
| `chin_hover` | **0.558** | 咳嗽停住；選 C 停在縫外 |
| `s05_ear_flat` | **0.409** | **僅**選 B 客廳：`dog_sick_far`→`dog_sick_sofa` |
| `guard_door` | **0.438** | 門線趴守；選 A 摸背 near→far→mid；天亮 `dog_bedroom_shift` |
| `nose_tip` | **0.65** | 清晨指尖特寫＠`dog_bedroom_nose_cu`（只留 bg＋放大；頭距對齊 `guard_door`；zoom `bedroom_nose` **0.30**；解鎖回憶 `nose_touch`） |

予安病床 `char_bedroom` **0.18** 見 `image_char.md`（沿床躺、面向左看狗）。

**旁白對位（與 `section_07_sick_guard.md` 同表）：** 爪子 `s07_low`＠far → 高信任 `halfstep` 進房／`ear_perk` 被角／`guard_door` 回門；低信任 `s07_low` far↔mid。床墊 `halfstep`、咳嗽 `chin_hover`、耳鳴 `ear_perk`＠far。選 A near 摸背→mid；選 B 客廳 far→sofa；選 C far 停縫。倒水後 `halfstep`→門線。天亮 `shift`；指尖 `nose_tip`＠`dog_bedroom_nose_cu`。

### 3.10 S08 胸背帶／巷口（2026-09-13）

扣帶前禁 `leash_wait`。巷口同尺 0.124，遠近只改 xalign。硬拖維持 `dog_behind_walk`，**禁** `far_walk` 走到予安前面。**禁**巷口無背帶 `halfstep`／`s04_low`／`ear_perk`、禁客廳 `street_tense`。

| 檔名／標籤 | `DOG_POSE_SCALE` | 主用 |
|------------|------------------|------|
| `s04_low`／`halfstep` | **0.369／0.580** | 扣帶前玄關；躺 visH≈58、站≈111（姿勢差）。解帶後硬拖 `s04_low`＠far。**禁** `s07_low` 0.43 進玄關 |
| `harness_bite`／`leash_wait` | **0.572／0.556** | 扣上之後；門檻進出 `leash_wait` |
| `s08_tense` | **0.572** | 巷口受驚／硬拖；站 visH 可低於坐姿 leash_wait。禁 `street_tense` 0.808 |
| `drink_bowl` | **0.564** | 返家衝水碗＠mid（低頭 visH 略矮） |
| `shoe_sleep` | **0.414** | 橫躺 visH≈55，對齊 `s04_low`；先 hide yuan |

人：玄關 `leash` **0.33**（visH≈368）；巷口 `walk` **0.32**（≈386），樹下切蹲仍 alley 0.32（≈357）。`CHAR_POSE_SCALE` **1.0**，勿再縮蹲姿。完整 visH 表見 `image_scale.md` §S08 確認。

玄關 xalign：far **0.60**／mid **0.66**／near **0.70**。巷口：behind **0.88**／far **0.56**／mid **0.63**／near **0.68**。

**旁白對位（與 `section_08_corner_walk.md` 同表）：** 兩步看 `s04_low`＠far → 鼻尖 `halfstep` 再退 → 聞帶 `halfstep` → 扣上 `harness_bite`／`leash_wait`。門檻 near→mid→near。巷口 behind；空機車 far_walk→behind。選 A mid→near；選 B 留 behind；選 C mid→near。鞋邊 `halfstep`→`shoe_sleep`；下午 `halfstep`＠mid。

---

## 4. 完整 Prompt 模板（複製）

```text
{STYLE}

{IDENTITY LOCK — Option B wiry}

{POSE_AND_EXPRESSION — change BOTH body action AND facial expression;
 convey trust distance: retreat / half-step / parallel rest / back-to-back sleep}

Centered, readable full body or clear crop. SOLID FLAT BLACK (#000000) background for cutout.
No bird nest, no straw nest, no cardboard nest styling on the dog itself.
No text, no logo, no purebred markers, no trust meter UI.
```

### Cursor GenerateImage 注意

- `reference_image_paths` 必含：`assets/dog/dog-ref-canonical.png`，建議再加 `assets/dog/refs/ref-anxious-b.png`
- `aspect_ratio`：直式 pose 用 `"3:4"`；S04 客廳趴姿／`s04-anxious`／S05 `head-up` 用 `"4:3"`；S05 搭椅／卡住用 `"3:4"`
- 產完 → `python tools/remove_ai_bg.py …` → 覆蓋 `assets/dog/dog-{pose}.png`

---

## 5. 一致性審查清單（定稿前打勾）

- [ ] 對得上 `dog-ref-canonical.png` 與 `assets/dog/refs/`（同一隻 B）
- [ ] 蜜金／金棕主體＋深耳尖＋背脊鞍斑＋奶油吻周都還在
- [ ] 毛質仍是 **硬毛略亂＋厚油彩筆觸**（wiry／scruffy／impasto），沒漂成蓬毛或光滑短毛
- [ ] 仍是短腿小狗，沒變成成犬／Q 版
- [ ] 耳朵是軟垂的，不是尖尖直立的純種感
- [ ] 又大又深褐的眼睛＋亮點都還在
- [ ] 表情跟身體動作都有改（不是只換背景）
- [ ] 沒有文字／logo／信任數字
- [ ] 狗是獨立透明 PNG，沒嵌進背景
- [ ] 沒有自動開遊戲

### 不一致時怎麼辦

1. 重貼 **IDENTITY LOCK**，並明確寫 `must match dog-ref-canonical.png and refs/`  
2. 加 `--no`：`fluffy coat, round plush face, purebred, chibi, photorealistic, cream background`  
3. 還是漂＝用基準圖做 img2img／edit，**只改 pose**

---

## 6. 與其他檔的關係

| 檔案 | 職責 |
|------|------|
| **本檔 `image_dog.md`** | 小7 **外型鎖定＋pose 一致性** |
| `image.md` | 總美術規範、人物／背景／STYLE |
| `image_bg.md` | 背景地點／光線；**背景不要有人、也不要有狗** |
| `image_scale.md` | 每場人／狗 zoom（S02＝`SCALE_S02`；S04–S10＝`SCALE`） |
| `game_guild.md` | 信任用距離／睡姿讓人感覺得到，不顯示數字 |

`image.md` 的狗章節以本檔為準；衝突時以 **本檔 Option B** 為準。

---

## 7. 變更紀錄

| 日期 | 內容 |
|------|------|
| 2026-07-19 | Option B wiry 定稿；正式狗資產 |
| 2026-07-25 | 用戶提供 5 張錨點圖 → 備份至 `assets/_backup_unused/_backup_20260725_183542/`；重寫 IDENTITY／STYLE；落地 canonical／anxious／behind-legs／refuse-stranger；其餘 pose 依新鎖全量重產 |
| 2026-07-28 | 新增 `dog-farewell`／`dog-cafe-refuse`／`dog-cafe-tense`；S09 朝向見 `section_09_almost_handoff.md` |
| 2026-08-01 | 新增動畫序列幀產線（§3.5）；落地 `dog wag` 搖尾巴 5 幀（S05 取名後）；工具 `seedance-generate.py`／`video-to-frames.py` |
| 2026-08-01 | 落地四個睡姿呼吸動畫：`door_sleep`／`back_sleep`／`check_sleep`／`door_edge`（各 5 幀，S03＋結局 A／B／D）；fast 模型 i2v 不送 `camerafixed` |
| 2026-08-01 | 落地第二批動作動畫：`sniff_wire`（S05）／`guard_door`（S07）／`drink_bowl`（S08）／`farewell`（S09）；中繼檔保留於 `Renpy_game/tools/output/seedance/` |
| 2026-08-01 | 修正八個動畫姿勢浮空（S03／S05／S07／S08／S09／結局）：幀裁回原圖框架、scale 沿用靜態原值；產線新增「裁回原框」必做步驟 |
| 2026-09-06 | S04 進房聲響三姿：`ear-perk`／`chin-hover`／`head-turn` |
| 2026-09-06 | S02 後門 anxious 改用 `dog-s04-anxious`（S04 橫式畫風）；舊 `dog-anxious` 留作後段低信任備援 |
| 2026-09-06 | S04 客廳狗可見高對齊 `parallel`：`head-turn` 0.369；尾隨改 `wag`；`wag` 幀 0.750 |
| 2026-09-06 | S05 早會三姿：`head-up`／`chair-paw`／`chair-stuck`；低信任開場改 `s04-anxious` |
| 2026-09-09 | S06 躲腿／退縮／額頭改四腳踏地；新增 `s06_retreat`；不再用舊 anxious 浮空尺 |
| 2026-09-09 | S06 走廊改頭距母尺 `retreat` 0.557：stair_watch 0.82／behind／flinch 0.38／watch-hand 0.58／freeze 0.62；人物 `char_s06_*` |
| 2026-09-10 | S06 站位補 near **0.54**；予安梯廳外出裝＋鞋（對齊 `image_char.md`）；`carry_pup` CHAR_POSE_SCALE 1.056 |
| 2026-09-13 | S07 指尖 `nose_tip` 改頭距 0.65＋`bedroom_nose` 0.30；不再豁免 visH |
| 2026-09-13 | **頭距鎖定：** 未來狗 pose 一律用頭當比例尺；特寫仍比頭；S04／S05 visH 僅暫留 |
| 2026-09-13 | S07 臥室頭距：`s07_low` 0.43 對齊 `guard_door`；選 B 回房不再用 `s05_ear_flat` |
| 2026-09-13 | S07 狗移動對齊旁白：halfstep／ear_perk／chin_hover／far-mid-near；客廳 sofa 退開 |
| 2026-09-10 | S08 巷口改 `s08_tense`（有胸背帶 0.572）；扣帶前無背帶；`street_tense` 只留 S04 |
| 2026-09-13 | S08 人／狗尺確認：玄關 0.33／0.128、巷口 0.32／0.124；躺 visH≈58、站≈111 是姿勢；勿縮 `leash` 蹲姿 |
| 2026-09-07 | S05 站姿族收到約 76px：`chair-paw` 0.401／`chair-stuck` 0.472／`s05_ear_flat` 0.409／`s05_stair_watch` 0.572；切姿收斂（一次抬頭、一次嗅線） |
| 2026-09-07 | S04 切姿收斂（選前回到 parallel）；選 C 客廳用 `s04_low` 0.369；勿把後門 anxious 0.551 拿進客廳 |

---

*更新：2026-09-13｜頭距為主尺；特寫可重用＋回憶 sniff_wire／forehead_nudge／nose_touch；S08 人／狗尺確認*
