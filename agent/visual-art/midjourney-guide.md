# LHTL · Midjourney Standard 水彩狗資產指南

> 對應 [`reference.md`](reference.md) 角色外型聖經。定稿後存 `Ch1_Trust/game/assets/dog/Week0/dog-{pose}.png`，再跑 `remove_dog_bg.py`。
>
> **最簡操作**：見 [`art-workflow-quick.md`](art-workflow-quick.md)，用 `Ch1_Trust/game/tools/art-pose.ps1` 一鍵複製 prompt / 存檔去背。

---

## 1. 訂閱與模式

| 項目 | 建議 |
|------|------|
| 方案 | **Standard $30/月**（Relax 無限；Fast ~900 張/月） |
| 試用 | 先 **月付**，滿意再改年付 |
| 批量試 pose | **`--relax`** 或 Web UI 選 Relax |
| 定稿前快速確認 | Fast（省在每月額度內） |
| 商用 | ✅ Standard 含商用（一般 indie OK） |

---

## 2. 風格參考 `--sref`

### 準備

1. 主參考圖：`Demo/assets/dog/dog-anxious.png`（或現有最滿意的水彩幼犬 PNG）
2. 上傳到 Midjourney（Discord `/describe` 或直接拖進對話）取得 **sref URL**  
   或 Web：Settings → 使用已上傳圖片的 link
3. 記下 sref 代碼，例如：`--sref 1234567890`

### 固定參數（每張都加）

```
--sref {你的sref代碼} --sw 100 --stylize 150 --ar 3:4
```

| 參數 | 用途 |
|------|------|
| `--sref` | 鎖水彩筆觸、毛色、臉型 |
| `--sw 100` | 風格權重拉滿（偏離時改 80～120 試） |
| `--stylize 150` | 略降預設誇張，較像 indie gouache |
| `--ar 3:4` | 直式全身幼犬，方便去背疊進遊戲 |

### 角色一致 `--cref`（可選）

若臉型仍飄，再加 `--cref {同一張或另一張滿意狗圖}` + `--cw 80`。

---

## 3. 基底 Prompt（複製區）

**Web UI（midjourney.com/imagine）**：直接貼**純文字描述**，**不要**加 `/imagine`（Discord 才用斜線指令）。

**單狗（多數 pose）：**

```
Digital watercolor gouache illustration, single scruffy golden-tan mixed breed puppy, 2-4 months old, honey ochre fur, darker brown ears and back, lighter cream chest and muzzle, semi-floppy ears, warm dark brown eyes, soft watercolor brushstrokes, no hard black outlines, gentle indie game character sprite, centered full body, clean white background, {POSE_ENGLISH} --sref {SREF} --sw 100 --stylize 150 --ar 3:4 --no text, logo, multiple dogs, purebred breed, corgi, poodle, shiba, husky, photorealistic, 3d render, chibi, black outline, background scene
```

將 `{POSE_ENGLISH}` 換成下方表格；`{SREF}` 換成你的 sref 代碼。

**情緒可讀（Week0 鎖定）：** `pose-prompts.json` 每條含 `POSE:`（身體動作）+ `EMOTION:`（臉／耳／尾）；MJ 若各張都像同一姿勢，檢查是否漏複製整段或 sref `--sw` 過高蓋過描述。

---

## 4. 情緒圖（12 · Feeling fallback）

| 檔名 | `{POSE_ENGLISH}` |
|------|------------------|
| `dog-anxious.png` | crouching low, ears back, worried eyes, tail tucked, nervous |
| `dog-curious.png` | head tilted, one ear up, sniffing forward, cautious curiosity |
| `dog-content.png` | relaxed sitting, soft smile, tail gently curved, calm happy |
| `dog-hurt.png` | ears flat, eyes wet, small whimper pose, subdued hurt |
| `dog-excited.png` | bouncing slightly, mouth open happy, tail mid-wag |
| `dog-attached.png` | leaning forward trustingly, gentle eye contact, wanting closeness |
| `dog-sleepy.png` | eyes half closed, yawning or drowsy sitting, relaxed paws |
| `dog-playful.png` | play bow, front legs down, rear up, playful energy |
| `dog-alert.png` | ears perked, alert stance, watching something off-frame |
| `dog-shy.png` | avoiding eye contact, body turned slightly away, timid |
| `dog-hungry.png` | nose down toward empty bowl, eager sniffing |
| `dog-angry.png` | low growl stance, ears back, guarded not aggressive |

---

## 5. 故事 Pose（Demo / Ch1 · 複製即用）

| 檔名 | `{POSE_ENGLISH}` |
|------|------------------|
| `dog-box.png` | shivering inside damp cardboard box, fur slightly wet, eyes barely open; **rainy overcast dim cool lighting, dark damp shadows** |
| `dog-wet.png` | wrapped in towel, only eyes peeking out, fur damp, tiny and scared |
| `dog-dryer.png` | sitting on bath mat, damp fur, cream hair dryer aimed gently from side, sniffing warm air, cautious ears half-back |
| `dog-corner.png` | pressed into corner of box, treating small area as safe boundary |
| `dog-kitchen.png` | sniffing beside food bowl, too afraid to eat yet |
| `dog-potty.png` | head down sniffing floor, searching for right spot |
| `dog-toy.png` | carrying small toy in mouth, trotting back, checking owner still there |
| `dog-doorway.png` | spinning in doorway, tail wagging hard, excited |
| `dog-doorway-wait.png` | standing at living room edge, watching owner, not barking, hopeful |
| `dog-doorway-lie.png` | lying on entryway tile, ears toward door, hopeful but shy |
| `dog-stair.png` | paused on stairs, looking back waiting |
| `dog-walk.png` | walking a few steps then looking back to confirm owner follows |
| `dog-park.png` | nose deep in soil near tree roots, sniffing |
| `dog-follow-close.png` | walking at owner's feet, steps syncing |
| `dog-follow-far.png` | following at distance, ready to flee if needed |
| `dog-thunder.png` | crouched under table, whole body trembling |
| `dog-knee.png` | head gently resting against woman's upper thigh, only lap and upper thigh visible, NO feet NO calves NO face |
| `dog-night-accident.png` | guilty shrinking in corner after accident, trembling |
| `dog-window.png` | gazing out window, ears twitching at wind |
| `dog-sad-day.png` | quietly leaning close while owner is sad, no playfulness |
| `dog-home.png` | sleeping at sofa foot, chest rising and falling |
| `dog-balcony.png` | nose through balcony railing gap, deep sniff |
| `dog-repair.png` | half step into entryway then back, still testing |
| `dog-vet-carry.png` | cradled in woman's arms, nose in sleeve cuff, no face, clinic fear |
| `dog-vet-walk.png` | held in arms, trembling at bright noisy street |
| `dog-held.png` | cradled in arms, stiff but not struggling, cream sleeve cuff only |
| `dog-sunday-wake.png` | waking at owner's feet, slightly closer than yesterday |
| `dog-home-settle.png` | chin on lap, trusting rest, upper thigh only NO lower legs |
| `dog-explore.png` | nose to ground, tail half raised, mapping scents |
| `dog-slipper.png` | wet muzzle, guilty look, slipper nearby, caught expression |
| `dog-chew.png` | peeking from distance, ears back, afraid to approach |

### Ch1 Week2 專用（須獨立 PNG）

| 檔名 | `{POSE_ENGLISH}` |
|------|------------------|
| `dog-alert-ears.png` | ears locked toward door, low whimper, hiding behind legs |
| `dog-leash.png` | leash taut, body frozen at elevator door, stiff fear |
| `dog-phone-pose.png` | head tilt for camera, playful awareness of being photographed |
| `dog-sock.png` | running with sock in mouth, tail spinning like a flag |
| `dog-park-tree.png` | nose buried in dirt at tree roots, deep sniff |
| `dog-park-play.png` | touching noses with another dog, tail spiral wag (**主角仍為同一幼犬，另一隻略小或模糊**） |
| `dog-bite-teach.png` | play mouthing stopped mid-bite, pausing to look at hand |

### 序列（paw-smell）

| 檔名 | `{POSE_ENGLISH}` |
|------|------------------|
| `dog-paw-smell-1.png` | cautiously sniffing owner's outstretched hand |
| `dog-paw-smell-2.png` | nose closer to palm, one paw slightly lifted |
| `dog-paw-smell-3.png` | gentle nose touch to hand, trust moment |

---

## 6. 操作流程

```
1. Midjourney Relax 生成 4 格 → 挑最像 dog-anxious 的一格
2. U1～U4 放大 → Vary (Subtle) 微調直到滿意
3. 下載 PNG → 存 Ch1_Trust/game/assets/dog/Week0/dog-{pose}.png
4. 去背：
   cd Learn_How_To_Love
   python Ch1_Trust/game/tools/remove_dog_bg.py
5. 遊戲內開啟確認；必要時在 style.css 補 .dog-img[src*="pose-id"] 動畫
```

Week3+ 成犬感：`assets/dog/Week3/`（仍用同一 sref，prompt 加 `slightly older adolescent puppy, 5-7 months, longer legs`）。

---

## 7. 常見問題

| 問題 | 處理 |
|------|------|
| 變成柯基／柴犬 | 加 `--no corgi, shiba, poodle, husky`；提高 `--sw` |
| 硬黑描邊 | 加 `no hard black outlines`；降 `--stylize` 到 100 |
| 背景不是白底 | 加 `clean white background`；去背腳本修 |
| 多狗同框 | 加 `--no multiple dogs` |
| knee 露出腳 | 重生成；prompt 強調 `NO feet NO calves` |
| Relax 太慢 | 正常；批量試稿開著即可 |

---

## 8. 完整範例（doorway-lie）

```
Digital watercolor gouache illustration, single scruffy golden-tan mixed breed puppy, 2-4 months old, honey ochre fur, darker brown ears and back, lighter cream chest and muzzle, semi-floppy ears, warm dark brown eyes, soft watercolor brushstrokes, no hard black outlines, lying on entryway tile, ears toward door, hopeful but shy, centered full body, clean white background, gentle indie game character sprite --sref {SREF} --sw 100 --stylize 150 --ar 3:4 --no text, logo, multiple dogs, purebred, photorealistic, chibi, black outline, background scene
```

---

## 9. 與其他工具分工

| 階段 | 工具 |
|------|------|
| **定稿 watercolor PNG** | **Midjourney + sref（本指南）** |
| 去背 | `remove_dog_bg.py` 或 `art-pose.ps1 finish`（**例外：`dog-box.png` 保留紙箱，不去背**） |
| 一鍵 prompt | `Ch1_Trust/game/tools/art-pose.ps1 mj {pose}` · 狗友 `art-companion.ps1 mj {pose}` |

---

## 10. 狗友 NPC｜阿黃（ah-huang）

與主角幼犬**分開繪製**：成年**中型金毛**（2–3 歲），穩定友善；同一 gouache 水彩筆觸，但體型明顯大於幼犬。

| 檔名 | 用途 |
|------|------|
| `sit.png` | `week2_elevator_dog` |
| `sniff-greet.png` | 問候／備用 |
| `play.png` | `week2_park_play` |
| `leash.png` | `week3_leash_tangle` |

**流程：**

```powershell
cd Ch1_Trust\game\tools
.\art-companion.ps1 batch          # 匯出 prompts/（含 MJ_SREF）
# Midjourney Relax → 下載 sit.png 等 → 放入 mj-batch-companion/downloads/
.\art-companion.ps1 finish-downloads
node ..\tools\validate-companion-ah-huang.js
```

單張：`.\art-companion.ps1 mj sit` → 下載後 `.\art-companion.ps1 finish sit 路徑.png`

Prompt 規格：`agent/visual-art/companion-prompts.json`
