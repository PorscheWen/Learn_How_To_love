## Version2 遊戲狀態（對齊 agents/02_trust_flags.md ｜ plot.md）

default trust = 0
default knowledge_score = 0
default knowledge_correct_today = 0
default smell_text = ""
default story_day = 1
default dog_name = ""
default dog_label = "小狗狗"
default flags = {}
default landmarks = []
default minigame_clear = {}
default knowledge_hud_title = "幼犬急救卡"
default toxic_food_picks = []

## —— 字幕節奏（字／秒；0＝瞬間顯示）——
default persistent.lhtl_v2_text_cps = 32

init python:
    TEXT_SPEED_PRESETS = [
        ("慢讀", 20),
        ("適讀", 32),
        ("快讀", 55),
        ("瞬間", 0),
    ]
    TEXT_SPEED_DEFAULT = 32
    ## 自動播放等待（數字愈大愈慢）
    AFM_BY_CPS = {
        20: 22,
        32: 18,
        55: 12,
        0: 10,
    }

    def apply_text_speed(cps):
        preferences.text_cps = int(cps)
        persistent.lhtl_v2_text_cps = int(cps)
        preferences.afm_time = AFM_BY_CPS.get(int(cps), 18)
        renpy.save_persistent()
        renpy.restart_interaction()

    def init_text_speed():
        cps = getattr(persistent, "lhtl_v2_text_cps", TEXT_SPEED_DEFAULT)
        if cps is None:
            cps = TEXT_SPEED_DEFAULT
        preferences.text_cps = int(cps)
        preferences.afm_time = AFM_BY_CPS.get(int(cps), 18)

    def text_speed_label():
        cps = preferences.text_cps
        for name, val in TEXT_SPEED_PRESETS:
            if val == cps:
                return name
        return "{} 字/秒".format(cps)

    ## Day2 隱藏知識｜5 選 4（狗不能吃的）—— True＝不能吃
    TOXIC_FOOD_CHOICES = [
        ("chocolate", "巧克力", True),
        ("grape", "葡萄／葡萄乾", True),
        ("onion", "生洋蔥／大蒜", True),
        ("xylitol", "含木糖醇的口香糖", True),
        ("carrot", "煮熟的紅蘿蔔", False),
    ]

    def toggle_toxic_food(key):
        picks = list(store.toxic_food_picks)
        if key in picks:
            picks.remove(key)
        elif len(picks) < 4:
            picks.append(key)
        store.toxic_food_picks = picks

    def toxic_food_pick_count():
        return len(store.toxic_food_picks)

    def toxic_food_is_picked(key):
        return key in store.toxic_food_picks

    def toxic_food_answer_correct():
        correct = {k for k, _name, bad in TOXIC_FOOD_CHOICES if bad}
        return set(store.toxic_food_picks) == correct

    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def add_trust(delta):
        store.trust = store.trust + int(delta)
        return store.trust

    def set_flag(key, value=True):
        store.flags[key] = value

    def get_flag(key, default=False):
        return store.flags.get(key, default)

    def clear_minigame(mid):
        store.minigame_clear[mid] = True

    def add_landmark(lid):
        if lid not in store.landmarks:
            store.landmarks.append(lid)

    def confirm_dog_name(buf=None):
        """寵物店取名確定：空則預設「布丁」，最多 10 字。"""
        raw = store.dog_name if buf is None else buf
        name = (raw or "").strip() or "布丁"
        name = name[:10]
        store.dog_name = name
        store.dog_label = name
        store.flags["named"] = True
        return name

    def reset_game_state():
        store.trust = 0
        store.knowledge_score = 0
        store.knowledge_correct_today = 0
        store.smell_text = ""
        store.story_day = 1
        store.dog_name = ""
        store.dog_label = "小狗狗"
        store.flags = {}
        store.landmarks = []
        store.minigame_clear = {}
        store.knowledge_hud_title = "幼犬急救卡"
        store.toxic_food_picks = []
        store.save_name = "第1天｜雨天的紙箱"
        store._bgm_profile = ""
        try:
            renpy.music.stop(channel="music", fadeout=0.5)
        except Exception:
            pass
        try:
            renpy.sound.stop(channel="sound")
        except Exception:
            pass

    def show_trust_toast(delta):
        ## 正式版偏柔：不強調數值累計，只提示方向
        if delta > 0:
            renpy.notify("{}好像……比較敢靠近一點".format(store.dog_label))
        elif delta < 0:
            renpy.notify("距離，好像又遠了一點")
