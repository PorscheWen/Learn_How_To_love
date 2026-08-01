# 信任度與 Flags｜Version2

---

## trust

| 值域建議 | 意義（敘事用，非 UI 必顯示） |
|----------|------------------------------|
| ≤ 0 | 高度警戒，距離遠 |
| 1～3 | 可同室，接觸需慢 |
| ≥ 4 | 敢靠近腿邊／短接觸摸背 |
| ≥ 6 | Day7 溫柔收養結局（含小遊戲加分後門檻） |

單次抉擇／信任小遊戲建議落在 `−2`～`+2`。

另見：`knowledge_score`（知識小遊戲累積）、`knowledge_correct_today`（0～5）、`minigame_clear.*`（當日雙小遊戲是否過關）— 詳 `04_minigames.md`（知識每天 **5 題**，≥4 過關）。

---

## Day1 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.bathed` | Day1 沖澡失敗嘗試／結束多為 `false`（只擦乾） | Day2+ 清潔劇情 |
| `flags.fed` | 成功進食後 | Day2 胃口／便便 |
| `flags.grabbed_from_box` | 分歧1 選抓出箱 | Day5 接觸回聲 |
| `flags.touched_too_soon` | 餵食時摸頭 | Day5 摸頭場景回聲 |
| `flags.gave_space` | 放食物後退／信任小遊戲成功 | Day4／5 距離互動 |
| `flags.slept_in_living` | 分歧4 陪客廳 | Day4 分離焦慮對照 |
| `flags.named` | Day2 命名「布丁」 | 此後對白可用名字 |
| `flags.adopted` | Day7 | 結局 |
| `minigame_clear.kg_d1_puppy_first_aid` | Day1 知識遊戲 | 成就／複習 |
| `minigame_clear.tg_d1_space_feed` | Day1 信任遊戲 | 成就／信任加成 |

---

## Day2 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.yelled_at_mess` | 分歧1 提高音量 | Day4／6 語氣回聲 |
| `flags.calm_after_mess` | 分歧1 深呼吸 | Day2 日終距離 |
| `flags.harsh_cleaner` / `flags.gentle_clean` | 分歧2 清潔 | 氣味／舒適敘事 |
| `flags.soft_voice_ok` | `tg_d2_soft_voice` 成功 | 成就 |
| `flags.knows_potty_routine` | `kg_d2_potty_myths` ≥4 | 定點提示 |
| `flags.forced_onto_pad` / `flags.pad_introduced_gently` | 分歧3 尿墊 | Day3+ 定點 |
| `flags.took_half_day` / `flags.rushed_day` | 分歧4 請假 | 當日節奏 |
| `minigame_clear.kg_d2_potty_myths` | 知識過關 | 成就 |
| `minigame_clear.tg_d2_soft_voice` | 信任過關 | 成就 |

---

## Day3 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.bought_adult_kibble` / `flags.bought_puppy_kibble` | 分歧1 飼料 | 餵食順利度 |
| `flags.shop_splurge` / `flags.shop_minimal` | 分歧2 荷包 | 風味 |
| `flags.removed_old_bowl` / `flags.bowls_side_by_side` / `flags.chose_bowl_freely` | 換碗／信任小遊戲 | 進食敘事 |
| `minigame_clear.kg_d3_food_shelf` | 知識過關 | 成就 |
| `minigame_clear.tg_d3_two_bowls` | 信任過關 | 成就 |

---

## Day4 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.slammed_door_silent` / `flags.said_im_here` | 分歧1 關門 | 分離練習 |
| `flags.headphones_night` / `flags.opened_for_visible` | 分歧2 | Day5 距離 |
| `flags.visible_sleep_ok` | `tg_d4_visible_sleep` | 里程碑 |
| `flags.hugged_all_night` / `flags.same_room_apart` | 分歧3 安撫 | 永續性敘事 |
| `flags.blamed_morning` / `flags.morning_gentle` | 分歧4 天亮 | 關係溫度 |
| `minigame_clear.kg_d4_separation` | 知識過關 | 成就 |
| `minigame_clear.tg_d4_visible_sleep` | 信任過關 | 成就 |

---

## Day5 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.hugged_too_fast` / `flags.let_dog_choose_distance` | 分歧1 | Day6／7 接觸 |
| `flags.sniff_then_pet_ok` | `tg_d5_sniff_then_pet` | 摸背解鎖敘事 |
| `flags.touched_head_again` / `flags.touched_back` | 分歧2 | Day7 命名摸背 |
| `flags.flash_photo` / `flags.blanket_five_min` | 分歧3 儀式 | 里程碑 |
| `minigame_clear.kg_d5_body_language` | 知識過關 | 成就 |
| `minigame_clear.tg_d5_sniff_then_pet` | 信任過關 | 成就 |

---

## Day6 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.yelled_at_chew` / `flags.secured_cord_first` | 分歧1 | Day7 結局克制度 |
| `flags.said_abandon_threat` / `flags.owned_the_mess` | 分歧2 | Day7 需更高 trust 補償 |
| `flags.traded_toy_ok` | `tg_d6_trade_toy` | 壓力測試通過 |
| `flags.ignored_after_chew` / `flags.gave_chew_outlet` | 分歧3 | 夜間氣氛 |
| `flags.locked_in_bathroom` / `flags.puppy_proofed_night` | 分歧4 | Day7 |
| `minigame_clear.kg_d6_why_chew` | 知識過關 | 成就 |
| `minigame_clear.tg_d6_trade_toy` | 信任過關 | 成就 |

---

## Day7 相關 flags

| Flag | 寫入時機 | 誰讀取 |
|------|----------|--------|
| `flags.checklist_deferred` / `flags.checklist_started` | 分歧1 | 結局語氣 |
| `flags.forced_carrier` / `flags.towel_calm_trip` | 分歧2 路上 | 候診焦慮 |
| `flags.clinic_calm_ok` | `tg_d7_clinic_calm` | 結局溫柔度 |
| `flags.adopted` / `flags.deferred_adoption` | 分歧3 | 結局分支 |
| `flags.uses_proper_name` | 分歧4 | 結局呼叫 |
| `minigame_clear.kg_d7_care_checklist` | 知識過關 | 成就 |
| `minigame_clear.tg_d7_clinic_calm` | 信任過關 | 成就 |

---

## Landmark（可選）

| ID | 解鎖 |
|----|------|
| `landmark_cardboard_rain` | Day1 帶回紙箱幼犬 |
| `landmark_first_space` | Day1 給空間 |
| `landmark_messy_morning` | Day2 清晨意外 |
| `landmark_first_pad` | Day2 溫柔介紹尿墊 |
| `landmark_first_shop` | Day3 第一次補給 |
| `landmark_midnight_whine` | Day4 半夜哭聲 |
| `landmark_visible_circle` | Day4 可見圈陪睡成功 |
| `landmark_first_lean` | Day5 主動靠腳邊 |
| `landmark_chew_accident` | Day6 咬線意外 |
| `landmark_adopted` | Day7 選正式收養 |
| `landmark_week0_complete` | Day7 章節結束 |

---

*更新：2026-07-11｜Day1～7 flags 齊備*
