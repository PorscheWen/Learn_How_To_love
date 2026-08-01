## Week／Day 章節跳轉（對齊 agents/plot.md）
## 從主選單／遊戲內選章：用 full_restart → chapter_jump（比 jump_out_of_context 穩）

init python:
    WEEKS = [
        {"id": "week0", "title": "Week 0", "subtitle": "信任的開始", "ready": True},
        {"id": "week1", "title": "Week 1", "subtitle": "即將開放", "ready": False},
        {"id": "week2", "title": "Week 2", "subtitle": "即將開放", "ready": False},
        {"id": "week3", "title": "Week 3", "subtitle": "即將開放", "ready": False},
    ]

    WEEK0_DAYS = [
        {"day": 1, "title": "Day 1｜雨天的紙箱", "label": "d1_street_rain", "ready": True},
        {"day": 2, "title": "Day 2｜混亂的客廳", "label": "d2_morning_mess", "ready": True},
        {"day": 3, "title": "Day 3｜第一次出門買東西", "label": "d3_empty_can", "ready": True},
        {"day": 4, "title": "Day 4｜半夜的哭聲", "label": "d4_bedtime", "ready": True},
        {"day": 5, "title": "Day 5｜小狗狗肯靠近一點", "label": "d5_afternoon_light", "ready": True},
        {"day": 6, "title": "Day 6｜小意外與道歉", "label": "d6_chewed_cord", "ready": True},
        {"day": 7, "title": "Day 7｜紙箱以外的名字", "label": "d7_box_to_balcony", "ready": True},
    ]

    WEEK_DAYS = {
        "week0": WEEK0_DAYS,
    }

    ## 相容舊名稱（若他處仍引用）
    CHAPTER_DAYS = WEEK0_DAYS

    def get_week(week_id):
        for w in WEEKS:
            if w["id"] == week_id:
                return w
        return WEEKS[0]

    def get_week_days(week_id):
        return WEEK_DAYS.get(week_id, [])

    def week_is_ready(week_id):
        return bool(get_week(week_id).get("ready"))

    def week_subtitle(week_id):
        return str(get_week(week_id).get("subtitle") or "")

    def week_tab_rows():
        """扁平列：(id, title, ready)"""
        return [(w["id"], w["title"], bool(w.get("ready"))) for w in WEEKS]

    def week_day_rows(week_id):
        """扁平列：(day, title, label, ready) — 給 screen for 迴圈用。"""
        rows = []
        for d in get_week_days(week_id):
            rows.append((
                int(d.get("day", 0)),
                str(d.get("title") or ""),
                str(d.get("label") or ""),
                bool(d.get("ready")),
            ))
        return rows

    def seed_chapter_day(day):
        """章節跳轉：寫入合理前置 flags（不劇透後續日）。"""
        reset_game_state()
        store.story_day = int(day)
        if day >= 2:
            store.trust = max(store.trust, 2)
            store.knowledge_score = max(store.knowledge_score, 1)
            store.flags["towel_dried"] = True
            store.flags["bathed"] = False
            store.flags["fed"] = True
            store.flags["gave_space"] = True
            store.flags["slept_in_living"] = True
            store.flags["named"] = False
            store.dog_name = ""
            store.dog_label = "小狗狗"
            if "landmark_cardboard_rain" not in store.landmarks:
                store.landmarks.append("landmark_cardboard_rain")
            if "landmark_first_space" not in store.landmarks:
                store.landmarks.append("landmark_first_space")
        if day >= 3:
            store.flags["named"] = True
            store.dog_name = "布丁"
            store.dog_label = "布丁"
            store.flags["calm_after_mess"] = True
            store.flags["pad_introduced_gently"] = True
            if "landmark_messy_morning" not in store.landmarks:
                store.landmarks.append("landmark_messy_morning")
        if day >= 4:
            store.flags["bought_puppy_kibble"] = True
            store.flags["bowls_side_by_side"] = True
            store.flags["fed"] = True
            if "landmark_first_shop" not in store.landmarks:
                store.landmarks.append("landmark_first_shop")
        if day >= 5:
            store.trust = max(store.trust, 3)
            store.knowledge_score = max(store.knowledge_score, 2)
            store.flags["said_im_here"] = True
            store.flags["opened_for_visible"] = True
            store.flags["same_room_apart"] = True
            store.flags["morning_gentle"] = True
            store.flags["visible_sleep_ok"] = True
            if "landmark_midnight_whine" not in store.landmarks:
                store.landmarks.append("landmark_midnight_whine")
            if "landmark_visible_circle" not in store.landmarks:
                store.landmarks.append("landmark_visible_circle")
        if day >= 6:
            store.trust = max(store.trust, 4)
            store.knowledge_score = max(store.knowledge_score, 3)
            store.flags["let_dog_choose_distance"] = True
            store.flags["sniff_then_pet_ok"] = True
            store.flags["touched_back"] = True
            store.flags["blanket_five_min"] = True
            if "landmark_first_lean" not in store.landmarks:
                store.landmarks.append("landmark_first_lean")
        if day >= 7:
            store.trust = max(store.trust, 5)
            store.knowledge_score = max(store.knowledge_score, 4)
            store.flags["secured_cord_first"] = True
            store.flags["owned_the_mess"] = True
            store.flags["traded_toy_ok"] = True
            store.flags["gave_chew_outlet"] = True
            store.flags["puppy_proofed_night"] = True
            if "landmark_chew_accident" not in store.landmarks:
                store.landmarks.append("landmark_chew_accident")

    def prepare_chapter_jump(day, label_name):
        persistent.lhtl_v2_jump_day = int(day)
        persistent.lhtl_v2_jump_label = str(label_name)
        renpy.save_persistent()

    def start_chapter_day(day, label_name):
        """從主選單／overlay／遊戲內都能穩進指定 Day。"""
        prepare_chapter_jump(day, label_name)
        renpy.full_restart(transition=False, label="chapter_jump")

    class StartChapterDay(Action):
        """捕捉 day／label，避免 for 迴圈延遲綁定。"""

        def __init__(self, day, label_name):
            self.day = int(day)
            self.label_name = str(label_name) if label_name else ""

        def get_sensitive(self):
            return bool(self.label_name)

        def __call__(self):
            if not self.label_name:
                return
            start_chapter_day(self.day, self.label_name)

    class SetChapterWeek(Action):
        def __init__(self, week_id):
            self.week_id = str(week_id)

        def __call__(self):
            store.chapter_week_id = self.week_id
            renpy.restart_interaction()

default chapter_week_id = "week0"


label chapter_jump:
    $ init_text_speed()
    $ _d = getattr(persistent, "lhtl_v2_jump_day", 1) or 1
    $ _lab = getattr(persistent, "lhtl_v2_jump_label", None) or "d1_street_rain"
    $ seed_chapter_day(_d)
    jump expression _lab
