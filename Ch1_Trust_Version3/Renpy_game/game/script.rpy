## Version3｜Ch1 Trust
## Section 01：螢幕光比月亮亮
## Section 02：後門那一瞥
## Section 03：大門的臨時國界
## Section 04：共享同一種安靜
## Section 05：你的聲音有兩種
## Section 06：樓梯間的第三者
## Section 07：她倒下的那天
## Section 08：走到轉角就好
## Section 09：差點交給別人
## Section 10：把鑰匙分給心跳

default trust = 0
default dist = 0
default tone = 0
default guard = 0
default dog_label = "小7"
default proposed_name = ""
default entry_trust = 0
default flags = {"peeked_backdoor": False}
default current_section = "s01"
default save_name = "Section 01｜螢幕光比月亮亮"
default _current_bgm = None
default seen_section_titles = {}
default persistent.unlocked_endings = []
default persistent.unlocked_secret_photos = []
default persistent.unlocked_secret_content = []
default persistent.playthrough_trajectories = []


init python:
    def optional_displayable(path, fallback):
        """正式資產存在時使用；否則回傳 fallback。"""
        if renpy.loadable(path):
            return path
        return fallback

    # 立繪來源高度混雜（1024／1536），先歸一化再交給 char_*／dog_* transform。
    # 畫面定位：腳底落在字幕框上方（約 ypos 0.86），水平依場景；transform zoom 為基線 ×1。
    # 2026-07-25：狗／人物全量重產後，依 content bbox 重算 DOG_POSE_SCALE（見 tools/recalibrate_sprites.py）。
    CHAR_REF_H = 1280.0   # char_right zoom 0.36（全段 ×0.8 基線）
    DOG_REF_H = 1536.0    # dog_near zoom 0.272（全段 ×0.8 基線）

    def scaled_sprite(path, fallback, ref_h):
        if renpy.loadable(path):
            w, h = renpy.image_size(Image(path))
            return Transform(path, zoom=ref_h / float(h))
        if isinstance(fallback, str) and renpy.loadable(fallback):
            return scaled_sprite(fallback, Solid("#00000000"), ref_h)
        return fallback

    def char_sprite(path, fallback=Solid("#00000000")):
        return scaled_sprite(path, fallback, CHAR_REF_H)

    # 各 pose 內容高度佔畫布比例不同；scale 使 dog_near 時站姿≈200px、臥姿≈150px。
    DOG_POSE_SCALE = {
        "dog/dog-anxious.png": 0.519,
        "dog/dog-back-sleep.png": 0.427,
        "dog/dog-behind-legs.png": 0.608,
        "dog/dog-check-sleep.png": 0.452,
        "dog/dog-chin-floor.png": 0.424,
        "dog/dog-coat-sniff.png": 0.656,
        "dog/dog-door-edge.png": 0.434,
        "dog/dog-door-sleep.png": 0.42,
        "dog/dog-drink-bowl.png": 0.564,
        "dog/dog-ear-flat.png": 0.695,
        "dog/dog-forehead-nudge.png": 0.543,
        "dog/dog-guard-door.png": 0.438,
        "dog/dog-halfstep.png": 0.583,
        "dog/dog-harness-bite.png": 0.572,
        "dog/dog-kitchen-door.png": 0.577,
        "dog/dog-leash-wait.png": 0.556,
        "dog/dog-nose-fingertip.png": 0.384,
        "dog/dog-paper-bag-sniff.png": 0.630,
        "dog/dog-parallel.png": 0.524,
        "dog/dog-refuse-stranger.png": 0.656,
        "dog/dog-shoe-sleep.png": 0.414,
        "dog/dog-sniff-bento.png": 0.648,
        "dog/dog-sniff-wire.png": 0.466,
        "dog/dog-stair-watch.png": 0.615,
        "dog/dog-street-tense.png": 0.808,
        "dog/dog-farewell.png": 0.468,
        "dog/dog-cafe-refuse.png": 0.975,
        "dog/dog-cafe-tense.png": 0.892,
    }

    # 搖尾巴序列幀（Seedance 圖生影片抽幀，見 tools/seedance-generate.py）
    # scale 依 content bbox 對齊 dog-anxious 站姿（tools 計算值 0.850）
    # 5 幀已做亮度標準化；播放採來回（ping-pong）避免循環接縫跳動
    DOG_POSE_SCALE.update({
        "dog/wag/dog-wag-%02d.png" % i: 0.850 for i in range(1, 6)
    })

    # 動畫序列幀（同產線；各 5 幀）
    # 幀已用 tools 的 normalize-frames 裁回原圖框架（同畫布、同留白、同位置），
    # 因此 scale 直接沿用各自靜態 pose 的原值；勿再另行換算。
    ANIM_POSE_SCALE = {
        "door-sleep": 0.42,
        "back-sleep": 0.427,
        "check-sleep": 0.452,
        "door-edge": 0.434,
        "sniff-wire": 0.703,
        "drink-bowl": 0.564,
        "farewell": 0.468,
        "guard-door": 0.438,
    }
    for _pose, _scale in ANIM_POSE_SCALE.items():
        DOG_POSE_SCALE.update({
            "dog/%s/dog-%s-%02d.png" % (_pose, _pose, i): _scale
            for i in range(1, 6)
        })

    def dog_sprite(path, fallback=Solid("#00000000")):
        scale = DOG_POSE_SCALE.get(path, 1.0)
        if renpy.loadable(path):
            w, h = renpy.image_size(Image(path))
            zoom = (DOG_REF_H * scale) / float(h)
            # 腳底清字幕改由 transform ypos≈0.86 負責；方形畫布不再額外下沉補償。
            return Transform(path, zoom=zoom)
        if isinstance(fallback, str):
            return dog_sprite(fallback)
        return fallback

    def optional_background(path, fallback_color):
        if renpy.loadable(path):
            return Transform(path, fit="cover", xysize=(1280, 720))
        return Solid(fallback_color)

    def play_bgm(profile, fade=2.0):
        """依 audio.md 掛載 BGM。別名可帶音量（tense = calm @0.88）。

        同 profile 不重播；同檔不同 profile（如 blank_night↔night）只調音量，
        避免場景轉換反覆切斷 BGM。
        """
        aliases = {
            # S01 加班空白：深藍 ambient（與主選單 calm.ogg 分開，進章有明顯換曲）
            "blank_night": ("audio/almost-gave.ogg", 0.88),
            "calm": ("audio/calm.ogg", 1.0),
            "warm": ("audio/warm.ogg", 1.0),
            "tender": ("audio/tender.ogg", 1.0),
            "melancholy": ("audio/melancholy.ogg", 1.0),
            "night": ("audio/almost-gave.ogg", 0.93),
            "stair_border": ("audio/melancholy.ogg", 0.92),
            # S03 大門：與主選單／S01 的 calm 分開，避免章節直達同檔 if_changed 後靜音
            "gate_border": ("audio/melancholy.ogg", 0.92),
            "shared_quiet": ("audio/warm.ogg", 1.0),
            "tense": ("audio/calm.ogg", 0.88),
            "two_voices": ("audio/calm.ogg", 1.0),
            "guard_corridor": ("audio/calm.ogg", 1.0),
            "sick_guard": ("audio/sick-guard.ogg", 1.0),
            "corner_walk": ("audio/warm.ogg", 1.0),
            "almost_gave": ("audio/almost-gave.ogg", 1.0),
            "ending_back": ("audio/tender.ogg", 1.0),
            "ending_learning": ("audio/warm.ogg", 1.0),
            "ending_handover": ("audio/melancholy.ogg", 1.0),
            "ending_thin_ice": ("audio/calm.ogg", 0.95),
            "hopeful": ("audio/first-light.ogg", 1.0),
        }
        entry = aliases.get(profile)
        if not entry:
            return
        filename, volume = entry
        if not renpy.loadable(filename):
            return
        playing = renpy.music.get_playing(channel="music")
        # 同 profile 且正在播：略過
        if playing == filename and store._current_bgm == profile:
            return
        # 同檔不同別名：只調音量，不切斷循環
        if playing == filename:
            store._current_bgm = profile
            renpy.music.set_volume(volume, delay=fade, channel="music")
            return
        # 無聲、換檔、或章節直達後 _current_bgm 已清空：強制 play
        store._current_bgm = profile
        renpy.music.play(
            filename,
            channel="music",
            loop=True,
            fadein=fade,
            if_changed=False,
        )
        renpy.music.set_volume(volume, delay=fade, channel="music")

    DOG_SFX = {
        "whimper": ("audio/sfx/puppy-whimper-a.wav", 0.34),
        "murmur": ("audio/sfx/puppy-murmur-a.wav", 0.32),
        "soft": ("audio/sfx/puppy-soft-a.wav", 0.28),
        "sigh": ("audio/sfx/puppy-sigh-a.wav", 0.22),
        "bark": ("audio/sfx/puppy-bark-a.wav", 0.32),
        "growl": ("audio/sfx/dog-growl.ogg", 0.22),
    }

    def dog_sfx(cue, volume=None):
        """播放稀疏幼犬 one-shot；缺檔時靜默略過，不阻斷劇情。"""
        entry = DOG_SFX.get(str(cue or "").strip())
        if not entry:
            return
        filename, default_volume = entry
        if not renpy.loadable(filename):
            return
        relative_volume = default_volume if volume is None else volume
        try:
            renpy.sound.play(
                filename,
                channel="sound",
                relative_volume=relative_volume,
            )
        except TypeError:
            renpy.sound.play(filename, channel="sound")


# ---------- Section 標題卡：字幕緩慢浮現 ----------

transform title_slow_fade(delay=0.0):
    alpha 0.0
    yoffset 14
    pause delay
    easein 2.6 alpha 1.0 yoffset 0

screen section_title(title, subtitle, revisit=False):
    zorder 200
    modal True
    add Solid("#17120FF2")
    vbox:
        align (0.5, 0.46)
        spacing 26
        text title at title_slow_fade(0.0):
            xalign 0.5
            font CJK_FONT
            size 40
            color LHTL_TEXT_LIGHT
            kerning 2
        text subtitle at title_slow_fade(1.2 if not revisit else 0.15):
            xalign 0.5
            font CJK_FONT
            size 26
            color LHTL_TEXT_SOFT
            kerning 4
    # 首次等字幕淡入；重訪提早顯示「點擊繼續」，減少空等。
    timer (4.0 if not revisit else 0.5) action Show("section_title_hint")
    key "dismiss" action Return()
    button:
        background None
        xfill True
        yfill True
        action Return()

screen section_title_hint():
    zorder 210
    text "點擊繼續" at title_slow_fade(0.0):
        align (0.5, 0.84)
        font CJK_FONT
        size 18
        color "#8A7763"

init python:
    def show_section_title(title, subtitle):
        seen = store.seen_section_titles
        revisit = bool(seen.get(title))
        seen[title] = True
        renpy.call_screen(
            "section_title", title=title, subtitle=subtitle, revisit=revisit
        )
        renpy.hide_screen("section_title_hint")
        renpy.with_statement(Dissolve(0.5 if revisit else 0.8))

    def unlock_ending(ending_id):
        """解鎖結局代號 A～D；寫入 persistent，跨存檔保留。不劇透內容。"""
        unlocked = list(persistent.unlocked_endings or [])
        if ending_id not in unlocked:
            unlocked.append(ending_id)
            persistent.unlocked_endings = unlocked

    def ending_unlocked(ending_id):
        return ending_id in (persistent.unlocked_endings or [])

    def unlock_secret_photo(photo_id):
        """解鎖隱藏紀念照；寫入 persistent。不顯示親密％或進度條。"""
        unlocked = list(persistent.unlocked_secret_photos or [])
        if photo_id not in unlocked:
            unlocked.append(photo_id)
            persistent.unlocked_secret_photos = unlocked

    def secret_photo_unlocked(photo_id):
        ## 結局 A 已解鎖者一併可見（含舊存檔），不強制重打。
        unlocked = persistent.unlocked_secret_photos or []
        known = (
            "lap_sleep", "forehead_nudge", "behind_legs",
            "shoe_sleep", "nose_touch", "water_bowl",
            "back_to_back",
        )
        if photo_id in known:
            if ending_unlocked("A"):
                return True
            ## 舊存檔僅有 lap／背靠鍵時，視為整組紀念照已開
            if photo_id in unlocked:
                return True
            if "lap_sleep" in unlocked or "back_to_back" in unlocked:
                return True
            return False
        return photo_id in unlocked

    # ========== 彩蛋名字判定 ==========
    PET_NAMES_EASTER_EGG = {
        "毛毛": "fluffy_name",
        "旺旺": "wangwang_name",
        "小黑": "xiaohei_name",
        "月月": "moon_name",
        "咪咪": "meimei_name",
        "皮皮": "pipi_name",
        "點點": "dian_name",
        "球球": "ball_name",
    }

    def check_easter_egg_name(name):
        """
        檢查取名是否觸發彩蛋。
        回傳彩蛋 key（用於 S06 隱藏台詞），或 None（無彩蛋）。
        """
        if not name:
            return None
        normalized = str(name or "").strip()
        return PET_NAMES_EASTER_EGG.get(normalized)

    def unlock_secret_content(content_id):
        """解鎖隱藏內容（如 Ch2 伏筆、角色小傳等）；寫入 persistent。"""
        unlocked = list(persistent.unlocked_secret_content or [])
        if content_id not in unlocked:
            unlocked.append(content_id)
            persistent.unlocked_secret_content = unlocked

    def secret_content_unlocked(content_id):
        """檢查隱藏內容是否已解鎖。"""
        return content_id in (persistent.unlocked_secret_content or [])

    # ========== 結局後解鎖邏輯 ==========
    def process_ending_unlock(ending_id, trust_value):
        """
        在結局演出後調用，自動解鎖相應的隱藏內容與結局圖。
        ending_id: A / B / C / D
        trust_value: 當前信任數值（用於變體內容）
        """
        eid = str(ending_id or "").upper()
        unlock_ending(eid)

        # 各結局共通：狗日記／予安心境／朋友視角
        unlock_secret_content("dog_diary_" + eid.lower())
        unlock_secret_content("character_aftercare_" + eid.lower())
        unlock_secret_content("friend_perspective_" + eid.lower())

        # 結局 A：六張紀念照＋Ch2 提示（無背對背）
        if eid == "A":
            for _pid in (
                "lap_sleep", "forehead_nudge", "behind_legs",
                "shoe_sleep", "nose_touch", "water_bowl",
            ):
                unlock_secret_photo(_pid)
            unlock_secret_content("ch2_trust_foundation_hint")

        # Ch2 開場溫度＋本周目種子（供後章讀取；玩家當下無感）
        entry_by_ending = {
            "A": "stable",
            "B": "learning",
            "C": "absent",
            "D": "repair",
        }
        entry = entry_by_ending.get(eid)
        if entry:
            store.flags["ch2_entry"] = entry
        persistent.ch2_from_ch1 = {
            "ending": eid,
            "entry": entry,
            "trust": int(trust_value or 0),
            "busy_calendar": bool(store.flags.get("ch2_seed_busy_calendar")),
            "water_bowl": bool(store.flags.get("ch2_seed_water_bowl")),
            "lease_pet": bool(store.flags.get("ch2_seed_lease_pet")),
            "hooks": bool(store.flags.get("ch2_seed_hooks")),
            "forced_walk": bool(store.flags.get("s08_forced_walk")),
            "dog_no_collar": bool(store.flags.get("ch2_seed_dog_no_collar")),
            "dog_had_someone": bool(store.flags.get("ch2_seed_dog_had_someone")),
            "yuan_family_unread": bool(store.flags.get("ch2_seed_yuan_family_unread")),
        }

        renpy.save_persistent()

    def sync_unlocked_ending_rewards():
        """舊存檔／已解鎖結局：補齊隱藏內容與紀念照（可安全重入）。

        不可回傳非 None：主選單 button action 清單若收到 True，
        會結束主選單互動並被當成「開始新遊戲」。
        """
        changed = False
        for eid in ("A", "B", "C", "D"):
            if not ending_unlocked(eid):
                continue
            before_photos = list(persistent.unlocked_secret_photos or [])
            before_content = list(persistent.unlocked_secret_content or [])
            process_ending_unlock(eid, getattr(store, "trust", 0))
            if (
                list(persistent.unlocked_secret_photos or []) != before_photos
                or list(persistent.unlocked_secret_content or []) != before_content
            ):
                changed = True
        if changed:
            renpy.save_persistent()
        return None

    def dev_unlock_all_gallery():
        """開發用：一鍵解鎖結局 A～D、紀念照與隱藏文章。必須回傳 None。

        禁止在此呼叫 renpy.restart_interaction()：會沖掉選單按鈕。
        任何例外都吞掉，避免擋住 ShowMenu。
        """
        try:
            before = (
                tuple(persistent.unlocked_endings or []),
                tuple(persistent.unlocked_secret_photos or []),
                tuple(persistent.unlocked_secret_content or []),
            )
            for eid in ("A", "B", "C", "D"):
                process_ending_unlock(eid, 10)
            persistent.unlocked_endings = ["A", "B", "C", "D"]
            photos = list(persistent.unlocked_secret_photos or [])
            for pid in (
                "lap_sleep", "forehead_nudge", "behind_legs",
                "shoe_sleep", "nose_touch", "water_bowl",
            ):
                if pid not in photos:
                    photos.append(pid)
            persistent.unlocked_secret_photos = photos
            contents = list(persistent.unlocked_secret_content or [])
            for cid in (
                "dog_diary_a", "dog_diary_b", "dog_diary_c", "dog_diary_d",
                "character_aftercare_a", "character_aftercare_b",
                "character_aftercare_c", "character_aftercare_d",
                "friend_perspective_a", "friend_perspective_b",
                "friend_perspective_c", "friend_perspective_d",
                "ch2_trust_foundation_hint",
            ):
                if cid not in contents:
                    contents.append(cid)
            persistent.unlocked_secret_content = contents
            after = (
                tuple(persistent.unlocked_endings or []),
                tuple(persistent.unlocked_secret_photos or []),
                tuple(persistent.unlocked_secret_content or []),
            )
            if before != after:
                renpy.save_persistent()
                renpy.notify("已全解鎖：結局 4／4｜隱藏內容可讀")
        except Exception:
            pass
        return None

    def open_gallery_image(path, title=""):
        """主選單開大圖：用 new context + scene，避開 Show／ShowMenu 疊層不畫圖。"""
        if not renpy.loadable(path):
            renpy.notify("找不到圖檔：" + path)
            return None
        renpy.call_in_new_context("gallery_pic_label", path, title)
        return None

    def open_secret_photo(photo_id):
        """隱藏紀念照：與結局靜幀走同一條 gallery_pic_label。"""
        meta = SECRET_PHOTO_META.get(photo_id)
        if not meta:
            renpy.notify("找不到紀念照：" + str(photo_id))
            return None
        return open_gallery_image(meta["path"], meta["title"])

    # ========== 信任軌跡記錄 ==========
    def record_trust_trajectory():
        """
        在結局時記錄本周目的信任走勢供後續查看。
        存檔於 persistent 中，重新遊玩不影響既有結局解鎖。
        """
        import time

        trajectories = list(persistent.playthrough_trajectories or [])
        trajectories.append({
            "ending": store.flags.get("ch1_ending", "Unknown"),
            "final_trust": store.trust,
            "dist_axis": store.dist,
            "tone_axis": store.tone,
            "guard_axis": store.guard,
            "dog_name": store.dog_label,
            "timestamp": time.time(),
        })
        persistent.playthrough_trajectories = trajectories

    TRAJECTORY_ENDING_TITLES = {
        "back_to_back": "結局 A｜背靠",
        "chosen_learning": "結局 B｜選定但還在學",
        "handed_over": "結局 C｜送走之後",
        "thin_ice": "結局 D｜薄冰同住",
    }

    def _trajectory_axis_word(value):
        if value >= 2:
            return "穩定"
        if value == 1:
            return "漸穩"
        if value == 0:
            return "還在學"
        return "待修復"

    def latest_trajectory_summary():
        """結局一覽「本輪旅程」小卡：回傳兩行文字，尚無紀錄時回 None。"""
        trajectories = persistent.playthrough_trajectories or []
        if not trajectories:
            return None
        latest = trajectories[-1]
        title = TRAJECTORY_ENDING_TITLES.get(latest.get("ending"), "尚未走到結局")
        line_top = "{}｜{}".format(latest.get("dog_name") or "小7", title)
        line_bottom = "最終信任 {}/12｜距離 {}・語氣 {}・守護 {}".format(
            latest.get("final_trust", 0),
            _trajectory_axis_word(latest.get("dist_axis", 0)),
            _trajectory_axis_word(latest.get("tone_axis", 0)),
            _trajectory_axis_word(latest.get("guard_axis", 0)),
        )
        return [line_top, line_bottom]


image bg office_night = optional_background(
    "bg/bg-office-night.png", "#141B24"
)
image bg convenience_night = optional_background(
    "bg/bg-convenience-night.png", "#26313A"
)
image bg street_night = optional_background(
    "bg/bg-street-night.png", "#171E29"
)
image bg living_night = optional_background(
    "bg/bg-living-night.png", "#211913"
)
## 結局一覽／隱藏紀念照（gallery／）
image gallery secret_lap_sleep = "gallery/secret-lap-sleep.png"
image gallery secret_forehead_nudge = "gallery/secret-forehead-nudge.png"
image gallery secret_behind_legs = "gallery/secret-behind-legs.png"
image gallery secret_shoe_sleep = "gallery/secret-shoe-sleep.png"
image gallery secret_nose_touch = "gallery/secret-nose-touch.png"
image gallery secret_water_bowl = "gallery/secret-water-bowl.png"
image gallery secret_back_to_back = "gallery/secret-back-to-back.png"
image gallery ending_a_back = "gallery/ending-a-back.png"
image gallery ending_b_learning = "gallery/ending-b-learning.png"
image gallery ending_c_handover = "gallery/ending-c-handover.png"
image gallery ending_d_thin_ice = "gallery/ending-d-thin-ice.png"
image bg backdoor_night = optional_background(
    "bg/bg-backdoor-night.png", "#131A22"
)
image bg clinic_night = optional_background(
    "bg/bg-clinic-night.png", "#1A2430"
)
image bg stairwell_night = optional_background(
    "bg/bg-stairwell-night.png", "#202A31"
)
## S03 公寓大門外側
image bg gate_night = optional_background(
    "bg/bg-gate-night.png", "#171E29"
)
image bg entrance_night = optional_background(
    "bg/bg-entrance-night.png", "#2A2218"
)
image bg entrance_day = optional_background(
    "bg/bg-entrance-day.png", "#C4B59A"
)
image bg living_day = optional_background(
    "bg/bg-living-day.png", "#B8A58D"
)
image bg living_dusk = optional_background(
    "bg/bg-living-dusk.png", "#6B5A48"
)
image bg stairwell_day = optional_background(
    "bg/bg-stairwell-day.png", "#C9B896"
)
image bg alley_day = optional_background(
    "bg/bg-alley-day.png", "#B7AA93"
)
image bg alley_night = optional_background(
    "bg/bg-alley-night.png", "#1A222C"
)
image bg cafe_day = optional_background(
    "bg/bg-cafe-day.png", "#B9A78F"
)
image bg kitchen_day = optional_background(
    "bg/bg-kitchen-day.png", "#C4B59A"
)
image bg kitchen_night = optional_background(
    "bg/bg-kitchen-night.png", "#211913"
)

## 選單底圖（章節／結局／存讀檔／設定）
image lhtl_menu_bg = optional_background(
    "theme/menu-bg.png", "#17120F"
)
## 主選單標題主視覺
image lhtl_title_bg = optional_background(
    "theme/title-main.png", "#17120F"
)

init 1 python:
    ## 讓 Ren'Py 預設選單層也吃到 theme（與自訂 screen 一致）
    if renpy.loadable("theme/menu-bg.png"):
        gui.game_menu_background = Transform(
            "theme/menu-bg.png", fit="cover", xysize=(1280, 720)
        )
    if renpy.loadable("theme/title-main.png"):
        gui.main_menu_background = Transform(
            "theme/title-main.png", fit="cover", xysize=(1280, 720)
        )

image yuan headphones = char_sprite("char/char-yuan-headphones.png")
image yuan headphones_off = char_sprite(
    "char/char-yuan-headphones-off.png", "char/char-yuan-commute.png"
)
image yuan commute = char_sprite("char/char-yuan-commute.png")
image yuan sofa = char_sprite(
    "char/char-yuan-sofa.png", "char/char-yuan-commute.png"
)
image yuan squat_side = char_sprite(
    "char/char-yuan-squat-side.png", "char/char-yuan-leash.png"
)
image yuan carry_pup = char_sprite(
    "char/char-yuan-carry-pup.png", "char/char-yuan-commute.png"
)
image yuan sick_bed = char_sprite(
    "char/char-yuan-sick-bed.png", "char/char-yuan-commute.png"
)
image yuan leash_pass = char_sprite(
    "char/char-yuan-leash-pass.png", "char/char-yuan-cafe.png"
)
image clerk stand = char_sprite("char/char-clerk.png")
image yuan block = char_sprite(
    "char/char-yuan-block.png", "char/char-yuan-commute.png"
)
image neighbor stand = char_sprite("char/char-neighbor.png")
image yuan leash = char_sprite(
    "char/char-yuan-leash.png", "char/char-yuan-commute.png"
)
## S08 巷口散步：站／走握牽繩（勿用蹲姿 leash）
image yuan walk = char_sprite(
    "char/char-yuan-walk.png", "char/char-yuan-cafe.png"
)
image yuan farewell = char_sprite(
    "char/char-yuan-farewell.png", "char/char-yuan-leash.png"
)
image yuan cafe = char_sprite(
    "char/char-yuan-cafe.png", "char/char-yuan-leash.png"
)
image coworker stand = char_sprite(
    "char/char-coworker.png", "char/char-neighbor.png"
)
image coworker cafe = char_sprite(
    "char/char-coworker-cafe.png", "char/char-coworker.png"
)

## S08 巷口機車道具（停放／轉角切過）
image scooter parked = optional_displayable(
    "prop/scooter-parked.png", Solid("#00000000")
)
image scooter pass = optional_displayable(
    "prop/scooter-pass.png", Solid("#00000000")
)

image dog anxious = dog_sprite("dog/dog-anxious.png")
image dog halfstep = dog_sprite("dog/dog-halfstep.png")
image dog sniff_bento = dog_sprite(
    "dog/dog-sniff-bento.png", "dog/dog-halfstep.png"
)
image dog stair_watch = dog_sprite(
    "dog/dog-stair-watch.png", "dog/dog-anxious.png"
)
# 呼吸循環（幀缺失時 dog_sprite 落回靜態圖；熟睡＝呼吸慢而勻）
image dog door_sleep:
    dog_sprite("dog/door-sleep/dog-door-sleep-01.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-02.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-03.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-04.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-05.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-04.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-03.png", "dog/dog-door-sleep.png")
    pause 0.35
    dog_sprite("dog/door-sleep/dog-door-sleep-02.png", "dog/dog-door-sleep.png")
    pause 0.35
    repeat
image dog coat_sniff = dog_sprite(
    "dog/dog-coat-sniff.png", "dog/dog-door-sleep.png"
)
image dog parallel = dog_sprite(
    "dog/dog-parallel.png", "dog/dog-halfstep.png"
)
image dog chin_floor = dog_sprite(
    "dog/dog-chin-floor.png", "dog/dog-parallel.png"
)
image dog kitchen_door = dog_sprite(
    "dog/dog-kitchen-door.png", "dog/dog-halfstep.png"
)
image dog ear_flat = dog_sprite(
    "dog/dog-ear-flat.png", "dog/dog-anxious.png"
)
# S05 嗅耳機線：幀序＝鼻碰線→抬起→再碰線 完整週期，順播即無縫循環（約 1.2 秒）
image dog sniff_wire:
    dog_sprite("dog/sniff-wire/dog-sniff-wire-01.png", "dog/dog-sniff-wire.png")
    pause 0.24
    dog_sprite("dog/sniff-wire/dog-sniff-wire-02.png", "dog/dog-sniff-wire.png")
    pause 0.24
    dog_sprite("dog/sniff-wire/dog-sniff-wire-03.png", "dog/dog-sniff-wire.png")
    pause 0.24
    dog_sprite("dog/sniff-wire/dog-sniff-wire-04.png", "dog/dog-sniff-wire.png")
    pause 0.24
    dog_sprite("dog/sniff-wire/dog-sniff-wire-05.png", "dog/dog-sniff-wire.png")
    pause 0.24
    repeat
image dog behind_legs = dog_sprite(
    "dog/dog-behind-legs.png", "dog/dog-anxious.png"
)
image dog forehead_nudge = dog_sprite(
    "dog/dog-forehead-nudge.png", "dog/dog-halfstep.png"
)
# S07 守門：醒著趴等的呼吸，比睡姿稍快（ping-pong 一圈約 2.2 秒）
image dog guard_door:
    dog_sprite("dog/guard-door/dog-guard-door-01.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-02.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-03.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-04.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-05.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-04.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-03.png", "dog/dog-guard-door.png")
    pause 0.28
    dog_sprite("dog/guard-door/dog-guard-door-02.png", "dog/dog-guard-door.png")
    pause 0.28
    repeat
image dog nose_tip = dog_sprite(
    "dog/dog-nose-fingertip.png", "dog/dog-halfstep.png"
)
image dog street_tense = dog_sprite(
    "dog/dog-street-tense.png", "dog/dog-anxious.png"
)
image dog leash_wait = dog_sprite(
    "dog/dog-leash-wait.png", "dog/dog-halfstep.png"
)
image dog harness_bite = dog_sprite(
    "dog/dog-harness-bite.png", "dog/dog-leash-wait.png"
)
# S08 回家／結局 A 前：低頭舔水（ping-pong 一圈約 0.8 秒）
image dog drink_bowl:
    dog_sprite("dog/drink-bowl/dog-drink-bowl-01.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-02.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-03.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-04.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-05.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-04.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-03.png", "dog/dog-drink-bowl.png")
    pause 0.10
    dog_sprite("dog/drink-bowl/dog-drink-bowl-02.png", "dog/dog-drink-bowl.png")
    pause 0.10
    repeat
# S09 告別：坐著抬頭，尾巴貼地左右輕掃......不確定的搖，比 S05 wag 收斂
# 幀序依尾巴位置排序（content bbox 寬度），ping-pong 一趟約 1.6 秒
image dog farewell:
    dog_sprite("dog/farewell/dog-farewell-01.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-02.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-03.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-04.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-05.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-04.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-03.png", "dog/dog-farewell.png")
    pause 0.20
    dog_sprite("dog/farewell/dog-farewell-02.png", "dog/dog-farewell.png")
    pause 0.20
    repeat
image dog paper_bag = dog_sprite(
    "dog/dog-paper-bag-sniff.png", "dog/dog-farewell.png"
)
image dog cafe_refuse = dog_sprite(
    "dog/dog-cafe-refuse.png", "dog/dog-refuse-stranger.png"
)
image dog cafe_tense = dog_sprite(
    "dog/dog-cafe-tense.png", "dog/dog-street-tense.png"
)
image dog shoe_sleep = dog_sprite(
    "dog/dog-shoe-sleep.png", "dog/dog-parallel.png"
)
image dog refuse_stranger = dog_sprite(
    "dog/dog-refuse-stranger.png", "dog/dog-ear-flat.png"
)
# 結局 A：背對熟睡，呼吸最深最勻（信任落地）
image dog back_sleep:
    dog_sprite("dog/back-sleep/dog-back-sleep-01.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-02.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-03.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-04.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-05.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-04.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-03.png", "dog/dog-back-sleep.png")
    pause 0.38
    dog_sprite("dog/back-sleep/dog-back-sleep-02.png", "dog/dog-back-sleep.png")
    pause 0.38
    repeat

# 結局 B：睡得近但眼睛微睜，呼吸稍淺（還在確認）
image dog check_sleep:
    dog_sprite("dog/check-sleep/dog-check-sleep-01.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-02.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-03.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-04.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-05.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-04.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-03.png", "dog/dog-check-sleep.png")
    pause 0.32
    dog_sprite("dog/check-sleep/dog-check-sleep-02.png", "dog/dog-check-sleep.png")
    pause 0.32
    repeat

# 結局 D：睡門邊，呼吸淺而略快（睡得不安穩）
image dog door_edge:
    dog_sprite("dog/door-edge/dog-door-edge-01.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-02.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-03.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-04.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-05.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-04.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-03.png", "dog/dog-door-edge.png")
    pause 0.26
    dog_sprite("dog/door-edge/dog-door-edge-02.png", "dog/dog-door-edge.png")
    pause 0.26
    repeat

# 搖尾巴循環動畫（5 幀來回播放，約 1 秒一圈）
image dog wag:
    dog_sprite("dog/wag/dog-wag-01.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-02.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-03.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-04.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-05.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-04.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-03.png", "dog/dog-anxious.png")
    pause 0.12
    dog_sprite("dog/wag/dog-wag-02.png", "dog/dog-anxious.png")
    pause 0.12
    repeat


# 腳底錨在字幕框上緣附近（720×108 → y≈0.86），水平依場景分開，避免人狗／兩人糊成一團。
# 全段立繪統一 ×0.8 基線（舊 0.45／0.34 → 0.36／0.272），S01～S10／結局同尺，遠近仍用 far／mid／near。
# 2026-07-25 重產後由 tools/recalibrate_sprites.py 對齊；2026-08-04 全段 ×0.8 統一。
transform char_center:
    xalign 0.50
    yanchor 1.0
    ypos 0.86
    zoom 0.384

transform char_right:
    xalign 0.74
    yanchor 1.0
    ypos 0.86
    zoom 0.36

transform char_left:
    xalign 0.26
    yanchor 1.0
    ypos 0.86
    zoom 0.36

# 狗的距離＝畫面上的信任條：near／far 之間用移動表達，不顯示數字。
transform dog_far:
    xalign 0.58
    yanchor 1.0
    ypos 0.86
    zoom 0.208

transform dog_mid:
    xalign 0.50
    yanchor 1.0
    ypos 0.86
    zoom 0.24

transform dog_near:
    xalign 0.42
    yanchor 1.0
    ypos 0.86
    zoom 0.272

# S02 後門初遇：狗靠紙箱偏左、予安遠在右側；蹲下後才緩緩靠近（勿一開場就貼在一起）。
# 靠近段 zoom 對齊 dog_mid／dog_near；距離靠 xalign，勿再額外縮小主體。
transform dog_backdoor_far:
    xalign 0.32
    yanchor 1.0
    ypos 0.86
    zoom 0.16

transform dog_backdoor_mid:
    xalign 0.46
    yanchor 1.0
    ypos 0.86
    xzoom -0.24
    yzoom 0.24

transform dog_backdoor_near:
    xalign 0.58
    yanchor 1.0
    ypos 0.86
    xzoom -0.272
    yzoom 0.272

transform char_backdoor_far:
    xalign 0.90
    yanchor 1.0
    ypos 0.86
    zoom 0.304

transform char_backdoor_squat:
    xalign 0.82
    yanchor 1.0
    ypos 0.86
    zoom 0.32

# S03 梯廳門外狗窩：靠公寓門（左側門墊／牆角；與 day／night 同構圖），勿落在中央樓梯口；狗 far×0.9（0.208×0.9）
transform dog_far_stair:
    xalign 0.22
    yanchor 1.0
    ypos 0.86
    zoom 0.187

# 予安在右、圖檔狗面朝左時：水平翻轉使人狗互視（抬眼／靠近／鼻尖等）。
transform dog_far_to_yuan:
    xalign 0.56
    yanchor 1.0
    ypos 0.86
    xzoom -0.208
    yzoom 0.208

transform dog_mid_to_yuan:
    xalign 0.48
    yanchor 1.0
    ypos 0.86
    xzoom -0.24
    yzoom 0.24

transform dog_near_to_yuan:
    xalign 0.40
    yanchor 1.0
    ypos 0.86
    xzoom -0.272
    yzoom 0.272

# 客廳右前景木椅／凳：予安坐姿對齊椅面（bg-living-day 書櫃前矮凳）。
transform char_chair:
    xalign 0.74
    yanchor 1.0
    ypos 0.905
    zoom 0.304

# 舊名相容（S04 已改椅子）
transform char_sofa:
    xalign 0.74
    yanchor 1.0
    ypos 0.905
    zoom 0.304

# 狗在椅左地板（地毯側），面朝予安；與坐姿分開避免糊成一團。
transform dog_chair_mid:
    xalign 0.46
    yanchor 1.0
    ypos 0.86
    xzoom -0.224
    yzoom 0.224

transform dog_chair_near:
    xalign 0.52
    yanchor 1.0
    ypos 0.86
    xzoom -0.24
    yzoom 0.24

transform dog_sofa_mid:
    xalign 0.46
    yanchor 1.0
    ypos 0.86
    xzoom -0.224
    yzoom 0.224

transform dog_sofa_near:
    xalign 0.52
    yanchor 1.0
    ypos 0.86
    xzoom -0.24
    yzoom 0.24

# S04 尾隨：先定點在椅旁，再慢慢走向廚房方向（左側門線）；勿直接套 ease 造成瞬移。
transform dog_follow_start:
    xalign 0.46
    yanchor 1.0
    ypos 0.86
    zoom 0.224

transform dog_follow_from_chair:
    xalign 0.46
    yanchor 1.0
    ypos 0.86
    zoom 0.224
    parallel:
        ease 3.4 xalign 0.16
        ease 3.4 zoom 0.192

# 病床／枕頭構圖偏左寬：狗再往中左，避免與床沿手／枕重疊。
transform dog_sick_mid:
    xalign 0.36
    yanchor 1.0
    ypos 0.86
    xzoom -0.224
    yzoom 0.224

transform dog_sick_far:
    xalign 0.32
    yanchor 1.0
    ypos 0.86
    xzoom -0.192
    yzoom 0.192

# 人＋狗同框：人在右（char_right≈0.74），狗在人左側／腿後，勿貼到左側陌生人身上。
transform dog_far_pair:
    xalign 0.50
    yanchor 1.0
    ypos 0.86
    zoom 0.176

transform dog_mid_pair:
    xalign 0.56
    yanchor 1.0
    ypos 0.86
    zoom 0.184

transform dog_near_pair:
    xalign 0.60
    yanchor 1.0
    ypos 0.86
    zoom 0.192

# S06：予安面向左擋鄰居；狗躲在她身後（更靠右、疊在人下方）。
transform dog_behind_pair:
    xalign 0.82
    yanchor 1.0
    ypos 0.86
    zoom 0.176

# 頂額：圖檔自帶小腿裁切 → 隱藏予安立繪，單圖靠右對齊腿位。
transform dog_nudge:
    xalign 0.68
    yanchor 1.0
    ypos 0.86
    zoom 0.224

# 玄關：地墊在門前偏中，避免狗貼進門板。
transform dog_entrance_far:
    xalign 0.50
    yanchor 1.0
    ypos 0.87
    zoom 0.192

transform dog_entrance_mid:
    xalign 0.54
    yanchor 1.0
    ypos 0.87
    zoom 0.216

# S08 玄關穿帶（與全段 ×0.8 基線相同）
transform char_right_s08:
    xalign 0.74
    yanchor 1.0
    ypos 0.86
    zoom 0.36

transform dog_entrance_far_s08:
    xalign 0.50
    yanchor 1.0
    ypos 0.87
    zoom 0.192

transform dog_entrance_mid_s08:
    xalign 0.58
    yanchor 1.0
    ypos 0.87
    zoom 0.216

# S08 玄關互視：狗面朝予安（右）
transform dog_entrance_mid_s08_to_yuan:
    xalign 0.56
    yanchor 1.0
    ypos 0.87
    xzoom -0.216
    yzoom 0.216

# S08 巷口散步：同 ×0.8 基線；狗可靠近予安（右），勿貼左牆太遠。
# 前進方向偏左；身後＝予安右側（不願走）；近／中／遠＝逐漸跟上。
transform char_right_walk:
    xalign 0.74
    yanchor 1.0
    ypos 0.86
    zoom 0.32

transform dog_behind_walk:
    xalign 0.88
    yanchor 1.0
    ypos 0.86
    zoom 0.176

transform dog_far_walk:
    xalign 0.56
    yanchor 1.0
    ypos 0.86
    zoom 0.192

transform dog_mid_walk:
    xalign 0.63
    yanchor 1.0
    ypos 0.86
    zoom 0.216

transform dog_near_walk:
    xalign 0.68
    yanchor 1.0
    ypos 0.86
    zoom 0.24

# S08 機車：停放靠左牆（空車）／轉角呼嘯偏中前（×0.8，人物下層）
transform scooter_parked:
    xalign 0.14
    yanchor 1.0
    ypos 0.90
    zoom 0.38

transform scooter_pass:
    xalign 0.38
    yanchor 1.0
    ypos 0.88
    zoom 0.368

# ------------------------------------------------------------
# S09 朝向／位置（劇情準則）；尺寸已與全段 ×0.8 基線對齊
# 基線：char 0.36、dog_near 0.272、dog_mid 0.24、dog_far 0.208
#
# 客廳告別：圖檔予安面向左、狗抬頭偏左 → 予安在左、狗在右時
#   須水平翻轉予安，兩人才對望（攤手朝狗）。
# 玄關：予安蹲姿面向左；狗 leash-wait 面向右 → 予安右／狗左即可對望。
# 咖啡廳：同事左→右；予安右→左；狗依劇情（拒絕對同事／其餘對予安）。
# ------------------------------------------------------------

# S09 客廳告別
transform char_right_farewell:
    xalign 0.40
    yanchor 1.0
    ypos 0.86
    ## 圖檔面左；翻轉後面右對狗（x／y 同量避免拉寬）
    xzoom -0.36
    yzoom 0.36

transform dog_farewell_near:
    xalign 0.62
    yanchor 1.0
    ypos 0.87
    zoom 0.272

# S09 玄關牽繩（對齊全段 entrance／near）
transform char_right_s09:
    xalign 0.74
    yanchor 1.0
    ypos 0.86
    zoom 0.36

transform dog_entrance_far_s09:
    xalign 0.50
    yanchor 1.0
    ypos 0.87
    zoom 0.208

transform dog_entrance_mid_s09:
    xalign 0.62
    yanchor 1.0
    ypos 0.87
    zoom 0.272

# S09 咖啡廳人物
transform char_left_cafe:
    xalign 0.22
    yanchor 1.0
    ypos 0.86
    zoom 0.36

transform char_right_cafe:
    xalign 0.78
    yanchor 1.0
    ypos 0.86
    zoom 0.36

# 拒絕：貼予安腳邊，面向左側同事（圖檔面右 → 翻轉）
transform dog_cafe_near_guard:
    xalign 0.64
    yanchor 1.0
    ypos 0.86
    xzoom -0.272
    yzoom 0.272

# 留下：貼鞋側，面向右側予安（圖檔面右，不翻）
transform dog_cafe_near_home:
    xalign 0.66
    yanchor 1.0
    ypos 0.86
    zoom 0.272

# 僵住／交繩拉扯：兩人中間，面向予安（圖檔面右）
transform dog_cafe_mid:
    xalign 0.48
    yanchor 1.0
    ypos 0.86
    zoom 0.24


define narrator = Character(
    None,
    what_font=CJK_FONT,
    what_color="#000000",
    what_size=gui.text_size,
)
define ya = Character(
    "予安",
    what_font=CJK_FONT,
    who_font=CJK_FONT,
    what_color="#000000",
    who_color=LHTL_ACCENT_DARK,
)
define clerk = Character(
    "超商店員",
    what_font=CJK_FONT,
    who_font=CJK_FONT,
    what_color="#000000",
    who_color="#6E6340",
)
define neighbor = Character(
    "鄰居",
    what_font=CJK_FONT,
    who_font=CJK_FONT,
    what_color="#000000",
    who_color="#5F6D57",
)
define coworker = Character(
    "同事",
    what_font=CJK_FONT,
    who_font=CJK_FONT,
    what_color="#000000",
    who_color="#6E5D72",
)
define thought = Character(
    None,
    what_font=CJK_FONT,
    what_color="#3A2E24",
    what_size=23,
    what_prefix="（",
    what_suffix="）",
)


label reset_story_state:
    $ trust = 0
    $ dist = 0
    $ tone = 0
    $ guard = 0
    $ dog_label = "小7"
    $ proposed_name = ""
    $ flags = {"peeked_backdoor": False}
    $ _current_bgm = None
    $ renpy.music.stop(channel="music", fadeout=0.0)
    return


## 結局／隱藏紀念照大圖（從主選單 call_in_new_context 進來）
label gallery_pic_label(path="gallery/ending-a-back.png", title=""):
    scene expression Solid("#17120F")
    ## 用 Transform 一次定好尺寸，避免 show expression 字串 path 偶發不畫
    show expression Transform(path, fit="contain", xysize=(1200, 640)) as gallery_pic zorder 10:
        xalign 0.5
        yalign 0.52
    show screen gallery_pic_chrome(title)
    pause
    hide screen gallery_pic_chrome
    hide gallery_pic
    return


label start:
    call reset_story_state
    $ current_section = "s01"

    jump section_01_fluorescent_over_moon


# 章節選擇使用獨立入口，確保跳段時不沿用舊存檔的 trust／flags。
label start_section_01:
    call reset_story_state
    $ current_section = "s01"
    jump section_01_fluorescent_over_moon


label start_section_02:
    call reset_story_state
    # 跳過 S01 時採用「昨晚沒有繞去看」的預設開場。
    $ flags["peeked_backdoor"] = False
    $ current_section = "s02"
    jump section_02_backdoor_glance


label start_section_03:
    call reset_story_state
    # 章節直達採 S02 溫柔暫住的中性正向狀態。
    $ trust = 2
    $ dist = 1
    $ flags.update({"peeked_backdoor": False, "dist_ok": True, "gate_night": True})
    $ current_section = "s03"
    jump section_03_gate_temp_border


label start_section_04:
    call reset_story_state
    # 章節直達視為已通過 G1，避免缺少前段旗標。
    $ trust = 3
    $ dist = 2
    $ flags.update({"dist_ok": True, "s03_returned": True, "entered_home": True})
    $ current_section = "s04"
    jump section_04_shared_quiet


label start_section_05:
    call reset_story_state
    $ trust = 5
    $ dist = 3
    $ flags.update({"entered_home": True, "s04_parallel": True})
    $ current_section = "s05"
    jump section_05_two_voices


label start_section_06:
    call reset_story_state
    $ trust = 6
    $ dist = 3
    $ tone = 1
    $ flags.update({"entered_home": True, "s04_parallel": True, "s05_soft_voice": True})
    $ current_section = "s06"
    jump section_06_corridor_third_person


label start_section_07:
    call reset_story_state
    $ trust = 7
    $ dist = 3
    $ tone = 1
    $ guard = 1
    $ flags.update({"entered_home": True, "s04_parallel": True, "s05_soft_voice": True, "s06_protected": True})
    $ current_section = "s07"
    jump section_07_sick_guard


label start_section_08:
    call reset_story_state
    $ trust = 8
    $ dist = 3
    $ tone = 2
    $ guard = 1
    $ flags.update({"entered_home": True, "s05_soft_voice": True, "s06_protected": True, "s07_reassured": True})
    $ current_section = "s08"
    jump section_08_corner_walk


label start_section_09:
    call reset_story_state
    ## 8：讓「留下」(+2) 恰好過結局 A 門檻（trust>=10），重試迴圈才收集得到 A
    $ trust = 8
    $ dist = 3
    $ tone = 2
    $ guard = 1
    $ flags.update({
        "entered_home": True,
        "s05_soft_voice": True,
        "s06_protected": True,
        "s07_reassured": True,
        "s08_waited": True,
        "s08_forced_walk": False,
        "s08_returned_early": False,
    })
    $ current_section = "s09"
    jump section_09_almost_handoff


label start_section_10:
    call reset_story_state
    $ trust = 8
    $ dist = 3
    $ tone = 2
    $ guard = 2
    $ flags.update({
        "entered_home": True,
        "s06_protected": True,
        "s08_forced_walk": False,
        "s09_stayed": True,
        "gave_away": False,
    })
    $ current_section = "s10"
    jump section_10_share_the_key


label section_01_fluorescent_over_moon:
    $ current_section = "s01"
    $ save_name = "Section 01｜螢幕光比月亮亮"
    $ play_bgm("blank_night", fade=1.5)

    scene bg office_night
    with dissolve

    $ show_section_title("Section 01", "螢幕光比月亮亮")

    show yuan headphones at char_center
    with dissolve

    "週四深夜。予安關掉簡報最後一頁的動畫，游標在「儲存」上停了半秒。上班的人都懂：點下去，下一份常會自己冒出來。"
    "辦公室只剩冷氣的風聲......顯然沒人記得關。她戴上耳機，白噪音選雨聲；外面沒下雨，耳機裡有。"

    "電梯往下跳，她數：十四、十三、十二。"

    ## 超商起維持 blank_night（almost-gave），勿切回主選單同款 calm；同曲不重播
    scene bg convenience_night
    with dissolve

    show yuan commute at char_right
    show clerk stand at char_left
    with dissolve

    "便利商店門一開，冷氣撞上來。她走向微波櫃，便當盒透明膜起了一層霧......今晚的晚餐，看起來比她更有溫度。"

    clerk "小姐，要加水嗎？"
    ya "不用，謝謝。"

    "尾音收得乾淨。這是上班的聲音：禮貌、短、不留尾巴。"
    "她已經很久沒用另一種：句子講一半、會拖長、對著空氣自言自語的那種低聲。"
    "一個人住久了，低聲像很少點開的播放清單......還在，只是不播。"

    "微波「叮」的一聲。她正要結帳，店員把關東煮湯汁擦掉一滴，忽然像想起什麼。"

    clerk "對了，小7 今天好像沒力氣跑了。"
    ya "嗯？"

    clerk "後門那隻狗啊。我們都叫牠小7......老待在卸貨區。"
    clerk "瘦瘦的。前幾天還會晃到騎樓，今天丟垃圾，牠幾乎沒站起來。我跟店長講了，明天再看要不要叫人來。"

    ya "喔。"
    "標準的「喔」。不承諾、不追問、剛好夠禮貌。台灣便利商店夜班的外交辭令，大概就是這個音節。"

    hide clerk
    with dissolve

    ## 巷口：同曲略升音量（night = almost-gave @0.93），不重啟
    $ play_bgm("night", fade=2.0)
    scene bg street_night
    with dissolve

    show yuan commute at char_center
    with dissolve

    "她提袋出門。夜風從袖口鑽進去。巷口路燈把柏油路照成淺黃，機車一台一台睡死在格子裡......比很多人都準時。"
    "後門在另一側：卸貨區、壓扁紙箱、濕紙箱混隔夜油的氣味。"
    "這條路她走了兩年。轉角永遠只是轉角......直到有人開始在轉角放一隻狗。"
    "腳在轉角前慢了半拍。只有半拍。人的猶豫，常常短得像系統延遲。"

    menu:
        "繞去看一眼":
            $ flags["peeked_backdoor"] = True
            "她告訴自己，只看一眼，不算答應什麼。自我說服是免費的，而且常買一送一。"
            ## 場景切到後門：只遠望，不放狗立繪（留給 S02 正式相遇）；BGM 維持 night，勿搶 S02 melancholy。
            scene bg backdoor_night
            with Dissolve(1.0)
            show yuan commute at char_right
            with Dissolve(0.5)
            "她繞到轉角邊。卸貨區的燈壞了一盞，紙箱在陰影裡疊成模糊形狀。深處像有什麼動了一下，也可能只是塑膠袋......夜裡這兩種常長得很像。"
            "她沒有走近。站了兩秒，便轉回原路。兩秒：剛好夠良心癢一下，又剛好不夠做成決定。"
            thought "便當會涼。"
            scene bg street_night
            with Dissolve(0.8)
            show yuan commute at char_center
            with Dissolve(0.4)

        "照原路回家":
            $ flags["peeked_backdoor"] = False
            thought "便當會涼。便當真的會涼。"
            "她沒轉進去。步伐穩得像設定好的導航......目的地：床；途經點：無。"

    "耳機裡的雨還在下，她忽然覺得吵，把音量轉小。"
    "世界變大：遠處的狗叫、樓上電視、自己的呼吸。原來關掉白噪音，現實會自己補播。"

    ## 回家三拍：玄關進門 → 客廳坐下吃便當 → 廚房開冰箱；BGM 維持 night 同曲
    scene bg entrance_night
    with Dissolve(1.0)

    show yuan commute at char_right
    with dissolve

    "公寓門「嘀」一聲。"
    "她把便當袋換到另一隻手，彎腰換拖鞋。玄關燈只照得到自己進來的那一小塊......剛好夠承認：人回來了。"

    scene bg living_night
    with Dissolve(1.0)

    show yuan sofa at char_left
    with Dissolve(0.6)

    "她坐在沙發邊緣吃便當。電視沒開，螢幕黑著。"

    "吃到一半，手機亮起。備忘錄搜尋建議浮出三個月前的舊項目：「週六早上10點，動保處......領養須知影印本。」"
    "日期已經灰掉，後面沒有完成的勾。她盯了兩秒，把通知往旁邊滑掉......現代人處理罪惡感的標準手勢。"
    "店員那句「幾乎沒站起來」卻還掛在耳朵邊，像沒撕乾淨的標價貼紙：明明該丟掉，偏偏黏著。"

    scene bg kitchen_night
    with Dissolve(1.0)

    show yuan commute at char_right
    with Dissolve(0.5)

    "她打開冰箱。"
    "低沉的嗡嗡從門縫裡漏出來，像廚房裡有人在輕輕唸經......其實只是壓縮機上班。"
    "門上的冷光落在腳邊。她盯著那塊空地，忽然想到：如果真把什麼帶回來，牠會待在哪裡？"
    "念頭才成形，她便把冰箱門關上。冷氣嗡聲停了一瞬，整間屋子更安靜......安靜最會逼人繼續想。"
    thought "我連自己都常常忘記吃晚餐。"
    "通訊軟體最上面還停著家人一則未讀，日期是兩週前。她沒有點開。未讀有時是一種距離管理。"
    $ flags["ch2_seed_yuan_family_unread"] = True

    "手機搜尋框裡，她打了「路邊 小狗 沒力氣」。建議結果跳出脫水、失溫、通報電話。"
    "她沒有點進去。手指一個字一個字退回空白......沒搜尋過，就比較像沒責任。至少表面上。"
    "幾秒後，她又把通報電話抄在那筆舊備忘下面。只抄號碼，沒寫用途，也沒改過期日期。準備，但不承諾：這是她最熟的格式。"

    ya "不要。"
    "聲音很輕，像怕被自己聽見。自己通常是最難騙過的聽眾。"

    scene bg living_night
    with Dissolve(0.9)

    hide yuan
    with dissolve

    "上床前，手機最後亮一次：明天十點開會、週五要交的檔。"
    "行事曆翻到下一頁，『專案衝刺』已經把半個月塗成忙碌色。她看了一眼，沒點進去......有些忙，看一眼就夠累。"
    $ flags["ch2_seed_busy_calendar"] = True
    "她點開備忘，打了幾個字又刪掉。刪掉的是：「明天如果還在......」刪除鍵有時比送出鍵更誠實。"

    thought "還在什麼。"

    ## 入睡：維持 night，不再切曲
    if flags["peeked_backdoor"]:
        "意識往下沉。腳步聲在想像裡又走一遍：便利商店、微波的叮、那個「喔」、只站了兩秒的後門轉角。"
        "予安睡著了。窗外月亮大概還在；今晚螢幕光先贏了......城市裡這種比賽，月亮很少拿冠軍。"
        "而那隻她遠遠看過一眼、卻沒走近的狗，是否還趴在後門陰影裡......這個問題，被她很成功、也很短暫地，留在了夢的外面。成功與否，明天再驗收。"
    else:
        "意識往下沉。腳步聲在想像裡又走一遍：便利商店、微波的叮、那個「喔」、沒有走近的轉角。"
        "予安睡著了。窗外月亮大概還在；今晚螢幕光先贏了......城市裡這種比賽，月亮很少拿冠軍。"
        "而那隻她沒有去看的狗，是否還趴在後門陰影裡......這個問題，被她很成功、也很短暫地，留在了夢的外面。成功與否，明天再驗收。"

    centered "{size=30}{color=#F7EFE4}直到明天。{/color}{/size}"

    # S01 僅為風味分歧，不得改動 trust／Dist／Tone／Guard。
    $ renpy.block_rollback()
    jump section_02_backdoor_glance


## ------------------------------------------------------------
## Section 02：後門那一瞥
## 進段 trust = 0；唯一動 trust 的是「信任選擇（距離 Dist）」那一組。
## flags 寫入：called_shelter／vet_first／gate_night／dist_ok／s02_conscience_return
## s02_conscience_return：趕走後回頭寫入；S02 反應鏡頭、喝水與 BGM 收束讀取。
## 演出四拍：進場畫面 → 關鍵動作 → 反應鏡頭 → 離場鉤子
## BGM：melancholy →（蹲等／良心回頭）tender → 抱走後 warm
## ------------------------------------------------------------

label section_02_backdoor_glance:
    $ current_section = "s02"
    $ save_name = "Section 02｜後門那一瞥"
    $ play_bgm("melancholy", fade=2.5)

    # ...... 進場畫面：關螢幕（辦公室）→ 超商店員 ......
    scene bg office_night
    with Dissolve(1.2)

    $ show_section_title("Section 02", "後門那一瞥")

    "週五傍晚。予安還是最後一批關螢幕的人。簡報交出去了，身體卻像還欠一份存檔......這種帳，系統不會幫你勾銷。"
    "耳機掛在脖子上，這次沒開白噪音。外面有真的風；偶爾也該讓耳朵加班以外的班。"

    scene bg convenience_night
    with Dissolve(1.0)

    show clerk stand at char_left
    with dissolve

    clerk "小姐，小7 還在。"
    "說得很快，像怕自己太關心。關心這件事，夜班店員通常比客人更先學會節制。"
    clerk "後門那隻。店長說動保明天才排得到。你要是……算了，當我沒說。"

    ya "喔。"
    "比昨晚短半拍。熟練度在上升，良心未必。"

    hide clerk
    with dissolve

    scene bg street_night
    with Dissolve(0.9)

    show yuan commute at char_center
    with dissolve

    "她提便當到巷口。轉角在左邊......兩年來從不轉進去的那個轉角。地圖上很近，習慣上很遠。"

    if flags["peeked_backdoor"]:
        "昨晚繞過去看過一眼。此刻腳步比較穩，像赴一個沒說出口的約......最可怕的約，往往沒寫進行事曆。"
    else:
        "昨晚沒有繞過去。轉角突然變得很近，近得像地板自己往前送了一步。地板通常不會這樣，除非你心裡已經先走了。"

    "她轉進去了。這一步沒有音效，卻比很多決策更響。"

    scene bg backdoor_night
    with Dissolve(1.5)

    "卸貨區比想像窄。機車棚陰影把地面切成深淺。垃圾桶邊，壓扁的紙箱翹著邊角......城市的臨時家具。"
    "氣味是濕紙箱混隔夜油，還有一點點體溫味，淡到幾乎像錯覺。錯覺如果持續太久，就會變成問題。"

    "然後她看見了。"

    show dog anxious at dog_backdoor_far
    with Dissolve(1.2)
    pause 0.4
    show yuan commute at char_backdoor_far
    with Dissolve(0.8)
    pause 0.7

    "不是那種擺出來給人看的棄養。沒有綁絲帶、沒有紙條、沒有「請好心人收留」。廣告文案缺席，現實反而更難處理。"
    "可牠身上仍殘一點洗衣粉混舊衣的味道——淡、短，不太像只在這條巷子過夜。像曾靠近過某個人，後來那個人沒再回來。"
    $ flags["ch2_seed_dog_no_collar"] = True
    $ flags["ch2_seed_dog_had_someone"] = True
    "一隻瘦的混種幼犬趴在紙箱邊。毛質略硬亂，毛色偏蜂蜜褐，耳尖較深，胸口一塊髒掉的奶油白。短腿、偏瘦，肋骨在呼吸裡一下一下顯出來。事實很清楚：牠還活著，而且不輕鬆。"

    "予安停在兩步外。手還提著便當袋，指節沒有收緊，也沒有伸出去。兩步：上班族最常見的安全距離單位。"
    "她的手指向前動了半寸，又自己縮回袋繩上......靠近之後，常常會有人離開。這句話她沒說出口。"
    "狗的鼻子動了。便當袋、鞋底、她垂在身側的手指。鼻尖往前一點，又縮回紙箱陰影......評估風險的速度，不輸面試官。"
    "眼睛圓、深褐、亮得不太公平。在這種地方，不該有這麼亮的東西；偏偏就有。"

    "她先眨眼。"
    "狗先看開。耳尖微微一顫，視線落到水泥縫。"
    pause 0.9
    "那半秒裡，世界很安靜。安靜到她聽見自己吞口水的聲音......證明身體比理智更早簽到。"

    # ...... 關鍵動作（距離 Dist）...... 本段唯一動 trust 的選項組 ......
    menu:
        "蹲下，側身等待（不伸手）":
            $ trust += 1
            $ dist += 1
            $ flags["dist_ok"] = True
            $ flags["s02_conscience_return"] = False
            show yuan squat_side at char_backdoor_squat
            with Dissolve(0.7)
            "予安把便當袋放到地上，慢慢蹲下。膝蓋輕響一聲。她側著身，讓自己看起來小一點......對狗來說，縮小尺寸有時比說抱歉有用。"
            show dog anxious at dog_backdoor_far
            with Dissolve(0.5)
            "狗往後縮半步，屁股碰紙箱，沙沙響。前爪扒住箱緣，像隨時要鑽回去。撤退計畫寫在四肢上。"
            "她沒追。掌心朝上，停在膝蓋外，什麼都沒伸。不伸手，是今晚最難的伸手。"
            ya "嚇到了嗎。"
            "開會時那種尖銳的語氣收不回來，獨處時放軟的低聲還不熟，擠出來只有這一句。語言設定尚未更新完畢。"
            pause 0.6
            $ play_bgm("tender", fade=2.5)
            # ① 先靠近，但停在可退的距離
            show dog halfstep at dog_backdoor_mid
            with Dissolve(1.4)
            pause 0.7
            $ dog_sfx("soft")
            "很久，狗自己往前挪了半步。停在「碰得到氣味、碰不到手」的距離。尾巴不搖，像先報到、再觀望。"
            "她沒有伸手。距離還在，這半步才算數。"
            pause 0.5
            # ② 拿出飯盒 → 才更靠近
            "她掀開便當蓋，用筷子挑出一點白飯，放在掌心外的地上......離自己遠，離狗近。手收回來，停在空氣裡。談判桌，就地取材。"
            show dog sniff_bento at dog_backdoor_near
            with Dissolve(1.5)
            pause 0.7
            $ dog_sfx("soft")
            "飯香一落地，狗才再靠近。舌尖點了一下米粒，又點一下。每吞一口就抬眼看她......信任是分期付款，每期都要對帳。"
            "她的手指動了一下，又收回袖口。伸出去很容易；難的是，之後還站在原地。"
            thought "我可以什麼都不做。"
            pause 0.5
            # ③ 拿出水 → 退後一步
            "她把瓶蓋擰開，倒一點水推進去。塑膠蓋在水泥地上輕輕一響。"
            show dog anxious at dog_backdoor_mid
            with Dissolve(0.8)
            pause 0.5
            $ dog_sfx("murmur")
            "狗往後退了一步。不是拒喝，是對手突然換動作的警戒......水聲太像未知。"
            "她把手收回腿側，蓋子留在原地，自己也不再靠近。"
            pause 0.5
            # ④ 解釋後才又靠前
            ya "動保明天才來。明天。"
            "明天兩個字在巷子裡彈了一下，就消了。明天是個很方便的字，幾乎能裝下所有還沒做的決定。"
            "她補得很輕：「先喝一點。我不抓你。」"
            pause 0.6
            show dog halfstep at dog_backdoor_near
            with Dissolve(1.3)
            pause 0.5
            $ dog_sfx("soft")
            "狗又往前。鼻尖先確認蓋緣，才低頭喝了兩口。水聲很小，舌尖一下一下點著......很小的聲音，很大的進度。"
            "喝完，牠停在「既不碰你、也不放你走」的距離。尾巴輕貼腿側。中立，但不是冷漠。"
            pause 0.6
            "胸口某處鬆了一下。不是整個人鬆下來，只是「至少今晚牠還喝得動」那種小小的鬆一口氣。"

        "直接伸手抱／抓":
            $ trust -= 1
            $ dist -= 1
            $ flags["dist_ok"] = False
            $ flags["s02_conscience_return"] = False
            "她沒等。手臂伸過去。效率很高，體貼很低。"
            pause 0.4
            show dog ear_flat at dog_backdoor_far
            with Dissolve(0.3)
            $ dog_sfx("whimper")
            "狗整隻縮成一團，喉嚨裡擠出一聲短促的嗚。爪子在她袖口抓出淺痕......回饋來得比她預期快。"
            "懷裡那團溫度硬得像一塊石頭，掙得她差點抓不住。原來「抱起來」跟「接住」不是同一個專案。"
            "她只好先放回紙箱邊。"
            show dog anxious at dog_backdoor_far
            with Dissolve(0.6)
            pause 0.5
            "狗貼著紙箱，肩膀一下一下抖。耳朵貼平，鼻尖轉向陰影，不看她。不看，有時是最清楚的評價。"
            thought "抱到了。可是好像哪裡不對。"

        "拍腿趕開，轉身就走":
            $ trust -= 1
            $ dist -= 1
            $ flags["dist_ok"] = False
            $ flags["s02_conscience_return"] = True
            "她拍了拍腿，發出趕貓趕狗的嘖聲。聲音很熟；心裡卻沒那麼熟。"
            show dog ear_flat at dog_backdoor_far
            with Dissolve(0.4)
            $ dog_sfx("murmur")
            "狗縮回紙箱深處，只剩尾巴尖露在外面。紙箱邊角輕輕顫了一下。撤退成功，勝利很醜。"
            hide dog
            with Dissolve(0.5)
            "她轉身。走了五步。"
            pause 0.8
            "第六步停住。五步是逃避，六步開始像後悔。"
            thought "牠幾乎沒站起來......店員是這樣說的。"
            $ trust += 1
            "她轉回去。"
            show dog anxious at dog_backdoor_far
            with Dissolve(0.8)
            "狗還在原地，眼睛在陰影裡亮著，像在等一個重播。有些觀眾很有耐心，特別是沒地方去的時候。"
            show yuan squat_side at char_backdoor_squat
            with Dissolve(0.5)
            "這次她蹲下來，什麼都不做。膝蓋輕響，手貼在自己腿側。什麼都不做，偶爾是正確的進階操作。"
            $ play_bgm("tender", fade=2.5)
            show dog halfstep at dog_backdoor_mid
            with Dissolve(1.4)
            pause 0.8
            "很久，狗的鼻子重新伸出來一點。停在紙箱邊，不再後退，也不再靠近。停在中間，往往是今晚能拿到的最高分。"

    # ...... 反應鏡頭（硬抓／良心回頭補拍；蹲等路線已在上方走完靠近節拍）......
    if flags["dist_ok"]:
        "予安站起來，往後退一步......測試。生活裡很多關係，都靠退半步來確認。"
        "狗跟著往前半步，停在她舊鞋印的位置。"
        "她再退。狗不再跟，只盯著腳踝，像怕腳踝長出另一雙鞋。合理的恐懼，來自合理的經驗。"
    elif flags.get("s02_conscience_return", False):
        "「動保明天才來。」她對狗說，也對自己說。「明天。」"
        "明天兩個字在巷子裡彈了一下，就消了。明天是個很方便的字，幾乎能裝下所有還沒做的決定。"
        show dog halfstep at dog_backdoor_mid
        with Dissolve(0.8)
        "狗留在紙箱邊，鼻尖卻沒有再縮回陰影。那半步很小，像只肯把回頭這件事記下一半......帳本先寫一半，也算開工。"
        pause 0.6
        "予安站起來，往後退一步。"
        "狗沒跟，只抬起鼻尖追著她的鞋印。距離還在，但不再像一道關上的門。"
    else:
        "「動保明天才來。」她對狗說，也對自己說。「明天。」"
        "明天兩個字在巷子裡彈了一下，就消了。明天是個很方便的字，幾乎能裝下所有還沒做的決定。"
        show dog anxious at dog_backdoor_far
        with Dissolve(0.6)
        "狗往前一點，又縮回去，停在「既不碰你、也不放你走」的距離外緣。邊界感很強，幾乎像受過訓練。"
        pause 0.6
        "予安站起來，往後退一步。"
        "狗沒跟。只把下巴壓低，盯著她的鞋尖，肩膀還緊。"

    "店員從騎樓探頭：「小姐？要不要我幫你打給......」"
    ya "我知道了。我……先處理。"
    "語氣比較低、比較慢。不是客服音，像對自己下指令。指令對象：猶豫。"

    # ▷ 路徑選擇（風味為主；少動 trust）...... 靠近節拍結束後才出現
    menu:
        "下一步怎麼辦？"

        "留地址，等動保明天":
            $ flags["called_shelter"] = True
            "她跟店員留了電話和地址，說如果明天動保來得早，先通知她。"
            "說完才發現，自己已經把「這件事」變成「我的事」。責任感有時長這樣：先簽名，再懷疑。"

        "先帶去夜間急診":
            $ flags["vet_first"] = True
            "她查了最近的夜間動物醫院。掛號費比一個便當貴四倍......緊急的價格，從來不便宜。"
            "指尖在螢幕上停了一秒，按下「導航開始」。一秒，剛好夠後悔，又剛好不夠取消。"
            if flags["dist_ok"]:
                $ trust += 1

        "先帶到公寓大門過一夜":
            $ flags["gate_night"] = True
            "只是大門口。不是家裡。她先跟自己談好條件......條件談得越清楚，越像在騙自己這不算養。"
            if flags["dist_ok"]:
                $ trust += 1

    ## 壞路徑維持 melancholy（同曲不重播）；好路徑已在 tender
    "予安看著那隻狗。狗看著便當袋，又看她的臉，最後看向巷口......車燈一掃，巷口明暗忽然翻了一頁。故事還沒寫完，頁卻先翻了。"
    ya "今晚不算數。"
    "聲音輕得像怕被巷子聽見。嗓音穩，袖口卻先被她往下拉——像先替自己留一扇能退出去的門。"

    # 蹲等路線已在節拍內喝過水；其他路線此處補水
    if flags["dist_ok"]:
        "空便當盒收進袋子。瓶蓋還留在原地，水痕已經淡了。"
    else:
        "她把空便當盒收進袋子，留一點水在瓶蓋裡推過去。"
        if flags.get("s02_conscience_return", False):
            show dog halfstep at dog_backdoor_mid
            with Dissolve(0.5)
            $ dog_sfx("soft")
            "狗停在紙箱邊喝了兩口，身體沒有靠近，鼻尖卻一直朝著她。距離可以談，方向已經選好了。"
        else:
            show dog anxious at dog_backdoor_far
            with Dissolve(0.5)
            $ dog_sfx("whimper")
            "狗先看她的手，才湊近瓶蓋，喝了兩口。每喝一口就抬眼確認一次......風險控管做得比很多大人好。"
        pause 0.7
        "胸口某處鬆了一下。不是整個人鬆下來，只是「至少今晚牠還喝得動」那種小小的鬆一口氣。小小的，卻能撐到下一幕。"

    # ...... 離場鉤子 ......
    ya "我抱你一下。只是抱。很快。"
    "她事先預告，像對同事預告會議延遲。預告不能消除衝擊，只能讓對方少一點措手不及。"

    if flags["dist_ok"]:
        show dog halfstep at dog_backdoor_near
        with Dissolve(0.8)
        "她沒從正面撲。側身，手臂穿過胸腹下方，用力平均，像搬一份怕散的文件......重要的東西，都怕散。"
        hide dog
        show yuan carry_pup at char_center
        with Dissolve(0.6)
        "狗僵住，短促嗚了一聲，爪子在她袖口抓出淺痕。她痛得吸氣，卻沒鬆手，也沒罵。痛可以記，手不能鬆。"
    else:
        show dog anxious at dog_backdoor_mid
        with Dissolve(0.8)
        "這次她放慢很多。手從側邊伸，停一下，再托住。慢，不保證成功，但比較像道歉。"
        hide dog
        show yuan carry_pup at char_center
        with Dissolve(0.6)
        "狗還是僵住，嗚了一聲，抓痕疊在剛才那道旁邊。"
        "她痛得吸氣，卻沒鬆手，也沒罵。"

    ya "抱歉。我也不會。我們……先離開這裡。"
    "第一次，低聲聽起來比較像她自己。不是客服，也不是簡報，是予安。"

    hide yuan
    with dissolve

    "機車棚燈管閃了一下。紙箱空了。陰影少了一塊活的東西......空，有時比滿更明顯。"

    scene bg street_night
    with Dissolve(1.5)
    show yuan carry_pup at char_center
    with Dissolve(0.5)

    $ play_bgm("warm", fade=3.0)

    if flags.get("vet_first", False):
        "導航把她帶向夜間急診。狗的心臟隔著她的手臂跳得很快。她的心臟也是。兩份心跳，一份便當錢換不來的加班。"
    else:
        "走向公寓的路上，狗的心臟隔著她的手臂跳得很快。她的心臟也是。兩份心跳，一份便當錢換不來的加班。"
    pause 0.6
    "兩個節奏疊在一起，亂，但沒有停下。亂著往前，也算前進。"

    if flags.get("vet_first", False):
        # 急診路線：夜間動物醫院短場 → 再回公寓大門（S03）；勿先演客廳自我介紹。
        scene bg clinic_night
        with Dissolve(1.2)
        show yuan carry_pup at char_center
        with Dissolve(0.5)
        "夜間動物醫院的燈比巷子冷。玻璃門後空著幾張等候椅，櫃檯燈還亮著......急診的夜，通常比故事短。"
        "醫生看了一眼，語氣很平：餓、脫水，外加一身要慢慢養的疲倦。沒有戲劇性的病名，卻有一份要帶走的藥袋。"
        "掛號單捏在掌心，比便當袋重。狗的鼻子埋進她外套褶裡，嗅消毒水、藥味，與一點點害怕的味道。"
        hide yuan
        with Dissolve(0.5)
        "藥袋輕輕敲著手腕。診所的白光退了；接下來，只剩鐵門、門牌，與門縫底下那條細光。"
    else:
        "電梯門要關時，她用肩膀擋住。狗的鼻子埋進她外套褶裡，嗅加班、關東煮，與一點點害怕的味道。害怕通常最香，鼻子最誠實。"
        "門關上。樓層燈一格一格往上跳。"
        "她沒有數。第一次，她忘了數......有些習慣，需要一隻狗才能暫時離職。"

        scene bg entrance_night
        with Dissolve(1.0)
        show yuan carry_pup at char_right
        with Dissolve(0.4)

        "公寓門「嘀」一聲。玄關燈亮起。她側身進門，便當袋與那一小團蜂蜜褐一起跨過門檻。"

        scene bg living_night
        with Dissolve(1.0)
        show yuan carry_pup at char_right
        with Dissolve(0.4)

        "予安低頭看牠。"
        ya "我叫予安。"
        thought "然後覺得可笑......狗又不辦證件。"
        ya "他們叫你小7……你要不要換一個，再說。"

        pause 0.8
        centered "{size=30}{color=#F7EFE4}今晚不算數。{/color}{/size}"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_03_gate_temp_border


## ------------------------------------------------------------
## Section 03：大門的臨時國界
## 一件事：門內／門外兩個世界......關上大門→開門歸來→夜裡見牠睡著、不忍心帶回門內直到天明。
## 情感：女主掙扎（不敢養／不忍心）× 狗對陌生氣味與聲響的恐懼。
## flags 寫入：coat_bed／s03_returned／s03_ignored／entered_home／delayed_entry
## ------------------------------------------------------------

label section_03_gate_temp_border:
    $ current_section = "s03"
    $ save_name = "Section 03｜大門的臨時國界"
    $ trust = max(0, min(12, trust))
    $ play_bgm("gate_border", fade=2.5)

    scene bg gate_night
    with Dissolve(1.5)

    $ show_section_title("Section 03", "大門的臨時國界")

    if flags.get("vet_first", False):
        "從夜間急診回來時，已經過了午夜。藥袋還在手腕旁輕敲；醫生剛才那幾句，仍像收據一樣清楚。"
        "予安抱著牠站在公寓大門前。眼前只剩鐵門、門牌，與門縫底下那條細光......診所的白光，暫時退到記憶裡。"
        show yuan carry_pup at char_center
        with Dissolve(0.4)
    elif flags.get("called_shelter", False):
        "她把留給動保的電話再確認一次，然後把手機收回口袋。明天有人會來。至少在流程上，她已經是個負責的人了。"
        "可今晚還沒結束。她站在公寓大門前，把狗放在門邊轉角......門外這一側。"
    else:
        "她站在公寓大門前，把狗放在門邊轉角......門外這一側。"

    "騎樓地面涼，大門感應燈嗡地亮了一下。門裡是上樓回家的路；門外是這塊臨時的地。分配很清楚。"
    "狗的鼻子急促地動。機車廢氣、陌生人的鞋、油煙與鐵門的金屬味，全擠在同一個轉角。肩膀繃緊，尾巴夾著......把自己收小，好少佔一點陌生。"
    thought "帶進去，就像要養了。不帶進去，牠今晚睡在大門外面。"
    ya "今晚不算數。"
    "她又說一次。不像安慰，比較像蓋章：今晚這筆，先不算。連她自己都沒料到，會講得這麼硬。"

    ## 狗留下的位置：公寓門邊牆角（門外這一側；勿靠樓梯口）
    scene bg stairwell_night
    with Dissolve(1.0)

    menu:
        "脫下外套，鋪成一塊臨時墊子":
            $ flags["coat_bed"] = True
            "她脫下外套鋪平，紙盤裡倒了半瓶水。"
            show dog coat_sniff at dog_far_stair
            with Dissolve(0.8)
            $ dog_sfx("soft")
            "狗縮在外套邊，先嗅衣領再嗅袖口。氣味熟一點，身體才敢放下半寸；耳朵仍朝向巷口。"

        "把外套折好，留一小塊能靠著的地方":
            $ flags["coat_bed"] = False
            "她把外套折成靠墊，擺在門邊牆角，紙盤裡倒了半瓶水。"
            show dog coat_sniff at dog_far_stair
            with Dissolve(0.8)
            $ dog_sfx("soft")
            "牠只靠著衣角取暖，還沒把這裡當成可以待的地方。"

    show dog stair_watch at dog_far_stair
    with Dissolve(1.0)

    $ dog_sfx("murmur")
    "牠盯著那扇門，像在背規則：門開＝人還會出現；門關＝自己一個人。"
    "鼻子湊進門縫底下，抽一下，又抽一下——確認這扇門關上去之後，還會不會再打開。"
    "對面騎樓燈亮了一下，又滅。狗的爪子在磁磚上刮出短響。"
    "她把手伸向大門門把，又縮回來。指尖發涼。不是怕進門；是怕自己太快答應「留下」。"

    # 進門：門外大門 → 玄關關門 → 客廳。狗留在門外，先藏立繪。
    hide dog
    scene bg entrance_night
    with Dissolve(1.0)

    "予安推開大門，跨過門檻，把門關上。聲音很輕。門裡是有熱水的地方；門外，是今晚的問題。"
    "玄關全是她的氣味。門外那一小團蜂蜜褐，忽然失去唯一熟悉的來源。"

    scene bg living_night
    with Dissolve(1.0)

    "洗澡水開得很熱。熱水沖在肩上，心口那一塊卻沒熱起來。有些事，溫度解決不了。"
    thought "明天送走。明天讓日子變回：冰箱、螢幕、一個人。"
    "她嘴裡的「明天」特別短。趕時間的人常用這個字；想躲的人也是。"
    "水聲裡，她好像聽見爪子又刮了一下。也可能只是水管。她兩種都不想查。"

    scene bg entrance_night
    with Dissolve(0.9)

    "她擦乾頭髮，站在玄關通向大門那一側。門外沒有聲音。好事，也是壞事......安靜代表兩種答案。"
    thought "最好的意思是：牠還在。還是：牠已經走了。"
    "兩個答案她都不想要。她把手放上大門門把。門把被她握熱了；其餘地方都涼。"

    # ▷ 信任選擇（距離 Dist）...... 本段唯一動 trust 的選項組
    menu:
        "開門蹲在兩步外，輕聲說「我還在」，再補水":
            $ trust += 2
            $ dist += 1
            $ flags["s03_returned"] = True
            $ flags["s03_ignored"] = False
            $ flags["s03_choice"] = "return"
            scene bg stairwell_night
            with Dissolve(1.0)
            show dog stair_watch at dog_far_stair
            with Dissolve(0.6)
            "她還是開了大門。狗還在。窩更靠牆，更能看見鐵門打開的角度。外套被拖歪一角。"
            "門一開，牠先退半步，耳朵貼平。予安停在兩步外蹲下......膝蓋響了一下，狗的肩膀又緊半寸。"
            ya "我還在。明天……再說。"
            "聲音放軟了，不是開會時那種尖銳。狗不懂句子，但聽得出：這個人沒在吼。鼻子伸向鞋尖，停在半公分外......好奇心比勇氣多一點。"
            $ dog_sfx("soft")
            "她補了一點水。指尖碰到紙盤時，自己也在抖。"
            hide dog
            scene bg entrance_night
            with Dissolve(0.9)
            "她把門關上。玄關又只剩她；門外，仍是狗的值班。"
            $ play_bgm("tender", fade=2.2)

        "開門用腳把牠趕進角落，提高音量說「別擋路」":
            $ trust -= 2
            $ dist -= 1
            $ flags["s03_returned"] = False
            $ flags["s03_ignored"] = False
            $ flags["s03_choice"] = "shoo"
            scene bg stairwell_night
            with Dissolve(1.0)
            show dog stair_watch at dog_far_stair
            with Dissolve(0.6)
            "她開了大門。煩躁來得比心疼快......鞋尖把衣角推回牆邊，也把狗逼得更裡面。"
            ya "別擋路。"
            "音量碰上鐵門與騎樓壁，彈回來更硬。狗貼住牆，耳朵壓平：這聲，記住，下次先退。"
            $ dog_sfx("whimper")
            hide dog
            scene bg entrance_night
            with Dissolve(0.9)
            "她把大門關上。玄關燈還在嗡。安靜得過分......像她剛把該聽的聲音關在門外。"

        "只看一眼就關門，整晚不再開門":
            $ trust -= 1
            $ dist -= 1
            $ flags["s03_returned"] = False
            $ flags["s03_ignored"] = True
            $ flags["s03_choice"] = "ignore"
            scene bg stairwell_night
            with Dissolve(0.8)
            show dog stair_watch at dog_far_stair
            with Dissolve(0.5)
            "她把大門開一道縫，看見水盤還有水，便告訴自己這樣就夠了。責任感有時長這樣：只確認最低標。"
            "狗抬眼確認人還在不在。她沒有走近，也沒有說話。"
            hide dog
            scene bg entrance_night
            with Dissolve(1.0)
            "大門關上後，她背靠門板，數自己的呼吸。那一側忽然空了；她選擇當作沒聽見。"

    # 夜裡睡不著 → 大門門把 → 門外睡覺的狗 → 不忍心帶回門內。
    hide dog
    scene bg living_night
    with Dissolve(1.0)

    "夜裡，大門外傳來爪子急促刮過磁磚的聲音，隨即縮回牆角。"
    "予安坐起來。不是狗叫......是爪子，短、急。騎樓地面很涼，門裡卻很暖。"
    "她躺回去，又坐起來。手機螢幕亮了一下，她沒有打開任何搜尋。"

    scene bg entrance_night
    with Dissolve(0.9)

    "她穿上拖鞋，沒開大燈，把手放上大門門把。掌心出汗，門把反而變涼。"

    scene bg stairwell_night
    with Dissolve(1.0)

    hide dog
    show dog door_sleep at dog_far_stair
    with Dissolve(1.2)

    if flags.get("s03_ignored", False):
        "門一開，狗睡在轉角更遠的牆邊。背朝巷口，臉仍朝公寓大門，四隻腳收得很緊。"
    elif flags.get("s03_choice") == "shoo":
        "門一開，狗睡在被趕進的那個角落。身體縮成一小團，耳朵還壓著。"
    else:
        "門一開，狗睡在外套邊。背朝巷口，臉朝大門能打開的角度，呼吸淺而短。"

    "予安蹲在兩步外......一腳還在門裡的暖，一腳踩在門外的涼。事實很簡單：她比較站不住的是後者。"
    "她忽然覺得「今晚不算數」這句話很醜。"
    ya "今晚……算了。"
    "她不忍心看：門這一側，一隻狗把陌生地方睡成自己的床。"

    # ▷ 閘門 G1（進門權）...... 一定帶回門內；差別只在進門後的距離質地。
    menu:
        "輕輕引牠進屋，讓牠待在看得見的地方":
            $ flags["entered_home"] = True
            $ flags["delayed_entry"] = False
            "予安把外套連同那一小團一起抱起來。狗在臂彎裡僵了一下，隨後才發現沒有被扔下。"
            scene bg entrance_night
            with Dissolve(1.0)
            ## 進門時清醒：確認氣味／緊繃，尚未入睡
            if trust >= 2 or flags.get("s03_returned", False):
                show dog halfstep at dog_entrance_mid
                with Dissolve(0.7)
                "跨過門檻。牠的鼻子貼著袖口，確認門裡的氣味：咖啡、洗衣精、她。"
            else:
                show dog ear_flat at dog_entrance_far
                with Dissolve(0.7)
                "跨過門檻時，牠全身還繃著。門一關，下巴才肯放下半公分......信任這種東西，有時是用公分算的。"
            "她把門關好，燈只留這一盞。"
            scene bg living_night
            with Dissolve(1.2)
            show dog parallel at dog_mid
            with Dissolve(0.8)
            "外套鋪進客廳地板，離沙發兩步。狗轉了一圈，背朝門、臉朝她躺下......仍怕，但怕得比較近。眼睛還睜著，盯了她一會兒。"

        "帶進來，但先只放到玄關......明天再算":
            $ flags["entered_home"] = True
            $ flags["delayed_entry"] = True
            "她還是把大門開大，把牠帶進門裡。手在抖......這一步比「明天送走」更難收回。"
            thought "先進玄關就好。不要整間屋子。"
            scene bg entrance_night
            with Dissolve(1.2)
            show dog parallel at dog_entrance_far
            with Dissolve(0.8)
            "玄關地墊變成新的折衷：人說已進屋，狗的判斷是......還貼著門比較安心。"
            "予安坐在牠看得見的地方。今晚的家，暫時只有門檻到鞋櫃這麼寬。"

    $ play_bgm("tender", fade=2.2)
    if flags.get("delayed_entry", False):
        scene bg entrance_night
        show dog door_sleep at dog_entrance_far
        with Dissolve(0.8)
    else:
        scene bg living_night
        show dog door_sleep at dog_mid
        with Dissolve(0.8)

    "後半夜很安靜。門外腳步遠過，狗的耳朵動一下，確認門仍關著、人仍在，才敢繼續睡。"
    "予安沒有再把牠送回門外。她聽兩種呼吸慢慢對上拍子。"
    thought "只到天明。天明以後的事，天明再說。"

    ## 隔天早上：狗已醒，抬頭與女主對望
    if flags.get("delayed_entry", False):
        scene bg entrance_day
        with Dissolve(1.4)
        show dog parallel at dog_entrance_far
        with Dissolve(0.6)
        "清晨。窗光先到玄關地墊。狗已經醒了，仍在那一小塊，看她，又看客廳深處。"
    else:
        scene bg living_day
        with Dissolve(1.4)
        show dog parallel at dog_mid_to_yuan
        with Dissolve(0.6)
        "清晨。窗光先到地板。狗已經醒了，還在那兩步遠......恐懼會醒來，但人不曾消失。"

    ya "……早。"
    "狗不回答，只是抬著頭，視線越過地板，和她的眼睛對上。牠還在門裡......這比任何句子都清楚。"

    if flags.get("called_shelter", False):
        "手機震動一次：動保單位改期，說下週才排得到。她看完，沒有回。"
    elif flags.get("vet_first", False):
        "玄關角落還放著夜間急診的藥袋。電解質包裝已經空了，袋子扁扁的。"

    ## 清晨鉤子輕切 warm；S04 開場 shared_quiet 同檔不重播
    $ play_bgm("warm", fade=2.0)

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_04_shared_quiet


## ------------------------------------------------------------
## Section 04：共享同一種安靜
## 一件事：椅子與地板平行存在。唯一動 trust 的選項組為相處方式。
## flags 寫入：s04_parallel／s04_forced_photo／bathroom_closed
## 畫面：予安坐客廳右前景木椅（char_chair）；狗尾隨廚房用 dog wag＋位移動畫
## ------------------------------------------------------------

label section_04_shared_quiet:
    $ current_section = "s04"
    $ save_name = "Section 04｜共享同一種安靜"
    $ trust = max(0, min(12, trust))
    $ play_bgm("shared_quiet", fade=2.5)

    if flags.get("delayed_entry", False):
        scene bg entrance_day
        with Dissolve(1.5)
    else:
        scene bg living_day
        with Dissolve(1.5)

    $ show_section_title("Section 04", "共享同一種安靜")

    if flags.get("delayed_entry", False):
        "昨晚牠只肯待在玄關那一小塊；天亮後，地墊上的光移了一格，牠沒有跟著挪。"
        scene bg living_day
        with Dissolve(1.0)
        "牠才把前腳往客廳深處挪了一寸，一次只賭一寸。"
        "予安沒關門，只留一條細光的門縫......「算不算數」這種問題，晚點再算。"
    else:
        "門開著，狗已經在客廳過了一夜。沒有剪綵，沒有儀式，就是留下來了。"

    "沒有新買的碗，沒有訓練課程，也沒有「從今天起我們是家人」這種台詞......比較像兩個剛搬進來的室友，還沒對過生活公約。"
    "能拿出來的，只有予安的客廳、昨天沒洗的馬克杯、黑著的電視，和離椅子兩步遠的一塊地板。家，暫時就這麼大。"

    if trust >= 2 or flags.get("entered_home", False):
        show yuan sofa at char_chair
        show dog parallel at dog_chair_mid
        with Dissolve(1.0)
        "她在書櫃前的木椅坐下，拿出手機。狗選了那塊地板......看得見她，也看得見門，兩條退路都沒放棄。"
    else:
        show yuan sofa at char_chair
        show dog anxious at dog_far_to_yuan
        with Dissolve(1.0)
        "她在書櫃前的木椅坐下，拿出手機。狗在門邊僵了一會兒，最後選了靠牆的地板......離她更遠，但門還在看得見的角度。"

    "冷氣喀地一聲啟動。狗的耳朵豎起半秒又放下......牠不是在看她，是在確認屋子還會不會再出聲。"
    "電視忽然自己亮了一下，大概是遙控器被壓到，音量大得像整間辦公室被搬進了客廳。"
    "狗耳朵貼平，下巴離地只剩一公分......這棟房子顯然還有很多牠沒摸清的脾氣。"

    "予安把音量轉小，再小，小到幾乎只剩字幕在動。"
    show dog parallel at dog_chair_mid
    with Dissolve(0.7)
    pause 0.5
    "過了一會兒，狗的下巴才貼上地板......牠的原諒，來得比音量調整慢半拍。"

    "手機自動播到下一段短影片，笑聲忽然炸開，她慌忙按停，聲音斷在一半。"
    "狗沒有立刻趴回去，牠先看電視，再看手機，最後看她的手......像在替這間屋子裡的噪音排一張嫌疑名單。"
    "予安把手機倒扣在椅座邊，手掌離開時，塑膠殼碰上木面，只發出很輕的一聲。"
    ya "今天已經夠多了，對吧。"
    "狗的耳朵朝她轉了一下......沒有靠近，但也沒挪到更遠的地方，這在今天已經算進步。"
    thought "牠在看得見的地方就好。我也不用一直叫牠過來。"
    "她把原本要說的「過來」咬掉，改把雙腳往後收，留出一條從地板到門口的空路......這句話沒說出口，但意思傳到了。"

    # ▷ 信任選擇（距離 Dist）...... 本段唯一動 trust 的選項組
    menu:
        "繼續各坐各的；牠在看得見的地方就好":
            $ trust += 2
            $ dist += 1
            $ flags["s04_parallel"] = True
            $ flags["s04_forced_photo"] = False
            $ flags["bathroom_closed"] = False
            "予安把手機螢幕亮度調暗......螢光比窗外的光還搶戲，她忽然不想贏這一場。"
            ya "你就待在那。我也待在這。"
            "句子沒說完，語氣很低。狗不回答，尾巴輕輕貼著腿側，算是收到了。"
            show dog parallel at dog_chair_mid
            with Dissolve(0.8)
            pause 0.6
            show dog chin_floor at dog_chair_near
            with Dissolve(1.0)
            $ dog_sfx("sigh")
            "幾分鐘後，牠的耳朵鬆下來，下巴完整貼住地板......這場安靜，沒人搶著當主角。"

        "把牠硬抱上椅子，先合照一下":
            $ trust -= 2
            $ dist -= 1
            $ flags["s04_parallel"] = False
            $ flags["s04_forced_photo"] = True
            $ flags["bathroom_closed"] = False
            $ play_bgm("tense", fade=1.8)
            "她忽然覺得這畫面該留下來，手臂從狗胸前穿過，把牠抱上椅子，沒問過牠的意見。"
            "相機還沒對焦，懷裡的身體先僵住；爪子急著找地，尾巴夾進腹下。"
            hide dog
            show dog anxious at dog_far
            with Dissolve(0.7)
            pause 0.6
            $ dog_sfx("whimper")
            "予安按下快門，立刻把牠放回地板。照片裡她在笑，狗的眼睛卻只盯著逃跑的方向......這張合照，只有一半的人同意入鏡。"
            "她沒有刪照片，也沒再拍第二張。有些紀念，拍一次就夠心虛了。"
            show dog anxious at dog_far
            with Dissolve(0.5)

        "把牠關進浴室；那裡比較好清理":
            $ trust -= 2
            $ dist -= 1
            $ flags["s04_parallel"] = False
            $ flags["s04_forced_photo"] = False
            $ flags["bathroom_closed"] = True
            $ play_bgm("tense", fade=1.8)
            "她把紙盤和舊毛巾移進浴室，把門關到只剩最後一條光。"
            $ dog_sfx("whimper")
            "門後傳來一聲很低的鼻音，接著什麼都沒有......安靜有時候比哭聲更難聽。"
            "十分鐘後，予安發現自己根本沒在看手機，她一直在聽那扇門有沒有動靜。"
            "她重新打開門，自己退到走廊另一端，把選擇權讓出去。"
            show dog anxious at dog_far
            with Dissolve(0.8)
            "狗沒有立刻出來。等牠終於走回客廳，選的是比原來更遠、也更靠近出口的位置......這道浴室的門，牠記住了。"

    "時間從上午滑到傍晚。予安回完兩封工作訊息，洗掉昨天的馬克杯，又坐回椅子......一天的進度條，大概就長這樣。"
    if flags.get("s04_parallel", False):
        "狗抬眼看她幾次，沒有起身。她把這當成安靜成立，不是邀請......兩者常常長得很像。"
    else:
        "狗抬眼時先找出口。等她回到原位，牠才把下巴放下。"
    "窗光移過地板一塊又一塊。她起身倒水之前，那團蜷著的毛始終留在原位，準時得像一件家具。"

    "傍晚，她口渴，起身去廚房倒水。腳步一離開椅子，地板上那塊焦糖色也立刻跟著動了。"

    ## 尾隨：先定點（避免從椅旁／門邊瞬移），再慢走＋搖尾，最後切廚房 POV
    hide yuan
    with Dissolve(0.45)
    show dog halfstep at dog_follow_start
    with Dissolve(0.7)
    pause 0.35
    show dog wag at dog_follow_from_chair
    pause 3.5

    ## 廚房 POV（bg-kitchen-day 構圖＝從水槽邊往客廳看）：狗停在門線外
    ## 記憶點短切 tender（第一次主動跟上），收束再回 warm
    scene bg kitchen_day
    with Dissolve(1.0)
    show dog kitchen_door at dog_mid
    with Dissolve(0.8)

    $ play_bgm("tender", fade=1.8)
    $ dog_sfx("soft")
    "不是撲上來討食。牠只跟到廚房門口，在門檻外停住，像遵守一條沒人畫出來的線。"
    "只到門口，不進來......這條線，牠自己劃的。"
    "水龍頭的水聲停住時，牠的耳朵還朝著廚房：人在裡面，牠就留在線外守著。"

    "予安在水槽邊站住，手裡的杯子涼涼的。"
    "她看著那雙停在門線上的前腳。牠沒有往出口退，反而是因為她離開了椅子，才第一次主動跟上來......方向反了，意義卻不小。"
    "她沒叫牠再走一步，也沒關廚房的門。有些邀請，用不著說出口。"

    ## 廚房記憶點後回 warm；平行安靜路徑同檔不重播
    $ play_bgm("warm", fade=2.2)

    ## 回客廳：scene 已清空廚房 POV 的狗，依分支恢復原本的人狗位置
    scene bg living_day
    show yuan sofa at char_chair
    if flags.get("s04_parallel", False):
        show dog chin_floor at dog_chair_near
    else:
        show dog anxious at dog_far
    with Dissolve(1.0)

    "倒完水，她走回椅子。狗也回到地板原位，下巴貼地，安靜重新合上，像什麼都沒發生過。"
    "她順手把水碗挪到廚房門檻外緣......人進出都會經過，牠卻不必跨進那條線一步。"
    $ flags["ch2_seed_water_bowl"] = True
    "手機亮起會議提醒：明天早會，鏡頭可開可關。予安看了一眼耳機，那條會把聲音變尖銳的線，正安分地掛在椅邊。"
    "狗的耳朵朝耳機方向動了一下，又放下......牠顯然還不知道，那條線明天會派上用場。"

    thought "明天，會不會有兩種聲音。"
    "今晚，先只要一種聲音......小的、慢的、夠兩個人耗下去的那種。"
    "她把耳機線捲好，塞進椅子旁邊看不見的縫。明天再開，也不算晚。"

    $ trust = max(0, min(12, trust))
    centered "{size=30}{color=#F7EFE4}安靜，也可以是一起。{/color}{/size}"

    $ renpy.block_rollback()
    jump section_05_two_voices


## ------------------------------------------------------------
## Section 05：你的聲音有兩種
## 一件事：早會中小7進入鏡頭。唯一動 trust 的選項組為 Tone 反應。
## flags 寫入：s05_soft_voice／s05_sharp_voice／s05_repaired
## ------------------------------------------------------------

label section_05_two_voices:
    $ current_section = "s05"
    $ save_name = "Section 05｜你的聲音有兩種"
    $ trust = max(0, min(12, trust))
    $ play_bgm("two_voices", fade=2.5)

    scene bg living_day
    with Dissolve(1.5)

    $ show_section_title("Section 05", "你的聲音有兩種")

    "早上八點五十七分，予安把筆電墊高，確認鏡頭只拍得到書櫃和半面乾淨的牆......鏡頭前的人生，永遠比較整潔。"
    "耳機一戴上，她的肩膀也跟著坐直，像切換了另一個版本的自己。"

    show yuan headphones at char_right
    with dissolve

    if flags.get("s04_parallel", False) or trust >= 4:
        show dog parallel at dog_mid
        with Dissolve(0.8)
        "[dog_label]趴在離椅子兩步遠的地板，下巴靠近椅腳......牠已經學到，待在看得見的地方，不一定會被趕走。"
    else:
        show dog anxious at dog_far
        with Dissolve(0.8)
        "[dog_label]仍留在靠門的位置，不看螢幕，只用耳朵聽她在房間裡走動......這雙耳朵比眼睛誠實。"

    "九點整，會議開始，沒有一秒鐘的餘裕。"
    ya "早，檔案我昨晚補好了。第三頁的數字，我等一下再確認。"
    "予安的聲音俐落清楚，每一句都收在句點上，不留尾音。"
    "狗抬起頭。同一個人，聲音卻換了一種更尖銳的版本，牠聽得出差別，只是說不出理由。"

    "同事問了一句進度，予安一邊回答，一邊用腳把滑落的充電線勾回桌下......身兼二職，還沒加班費。"
    "[dog_label]的鼻尖跟著那條線移動，前腳才剛往前，螢幕裡又有人同時開口。三種聲音疊在一起，牠立刻把腳收回去。"
    "予安看見了，卻不能停下來解釋。她對鏡頭點頭、記下修改項目，右手仍懸在桌邊、掌心朝下，像想把整間屋子的節奏按慢一點。"
    thought "牠不知道哪一句不是在對牠說。"

    "同事臨時請她開鏡頭。她按下按鈕，螢幕裡出現自己，也多了一截從椅腳旁探出來的蜂蜜色耳朵......會議室從沒這麼可愛過。"
    $ dog_sfx("soft")
    "[dog_label]嗅到垂下來的耳機線，往前半步，鼻尖碰了一下，線輕輕晃動。"
    "予安伸手去擋，牠卻當那是邀請，前腳搭上了椅緣。"
    "耳機插頭被扯鬆一點，兩端的聲音瞬間疊成一記尖銳回授......會議室的可愛，維持不到十秒。"
    "[dog_label]整個縮了一下，前腳卻卡在椅緣，退也不是、靠近也不是。"
    "螢幕裡，主管叫了她的名字。"
    ya "有，我在。"
    "她回答得太快。麥克風還開著，狗正抬頭看她......下一句話會落在哪一邊，她只有半秒鐘決定。"

    # ▷ 信任選擇（Tone）...... 本段唯一動 trust 的選項組
    menu:
        "先關麥克風、拿下耳機，再輕聲把牠抱下來":
            $ trust += 2
            $ tone += 1
            $ flags["s05_soft_voice"] = True
            $ flags["s05_sharp_voice"] = False
            $ flags["s05_repaired"] = False
            "予安先按下靜音。耳機拿下來的瞬間，房間忽然變大......冷氣聲、狗的呼吸、自己的心跳，全都回來了。"
            show yuan headphones_off at char_right
            with Dissolve(0.5)
            ya "等一下喔。我不是在兇你。"
            "她的手臂從胸腹下方托住牠，慢慢放回地板，沒有順手一推了事。"
            show dog ear_flat at dog_far_to_yuan
            with Dissolve(0.5)
            pause 0.5
            "狗站在原地看她，耳朵先貼著，過了一會兒才鬆開一點......原諒總是比道歉慢半拍。"
            show dog parallel at dog_mid_to_yuan
            with Dissolve(0.8)

        "不關麥克風，用開會的聲音說「下去」":
            $ trust -= 2
            $ tone -= 1
            $ flags["s05_soft_voice"] = False
            $ flags["s05_sharp_voice"] = True
            $ flags["s05_repaired"] = False
            ya "下去。"
            "兩個字又快又直，連同事那端都安靜了半秒......這句話顯然不只是說給狗聽的。"
            "狗的耳朵立刻貼平，前腳從椅緣滑下，退回靠門的位置，一步都不多留。"
            hide dog
            show dog ear_flat at dog_far
            with Dissolve(0.7)
            pause 0.5
            $ dog_sfx("whimper")
            thought "我只是要牠下去。可是牠聽見的，好像不只這樣。"

        "先急著把牠抱開，會後再蹲下來道歉":
            $ trust -= 1
            $ tone -= 1
            $ flags["s05_soft_voice"] = False
            $ flags["s05_sharp_voice"] = False
            $ flags["s05_repaired"] = True
            "她怕同事看見，手臂先一步把狗抱離椅邊......力道比自己預想得急，效率倒是很高。"
            "狗落地後退了一步，耳朵壓低。予安已經打開麥克風，那句抱歉只能先記在帳上。"
            hide dog
            show dog ear_flat at dog_far
            with Dissolve(0.7)
            pause 0.5
            $ dog_sfx("murmur")

    "會議繼續。四十分鐘後，她闔上筆電，拿下耳機......世界終於安靜回一種聲音。"
    show yuan headphones_off at char_right
    with Dissolve(0.5)

    "耳罩離開後，她才發現自己咬緊了牙。椅子往後挪時，[dog_label]的爪子縮了一下，她立刻停住不動。"
    ya "好了。現在這句是對你說的。"

    if flags.get("s05_repaired", False):
        "她蹲到兩步外，把手放在膝上，把姿態放到比狗還低。"
        ya "剛才太急了，對不起。"
        $ trust += 1
        $ tone += 1
        "狗沒有馬上靠近。等那句話在空氣裡站穩，牠才往前挪了半步。"
    elif flags.get("s05_sharp_voice", False):
        ya "剛剛……太大聲了。"
        "狗仍停在門邊，耳朵轉向她，沒有完全別開......算不上原諒，但也沒關上門。"
    else:
        "狗等到耳機不再傳出人的聲音，才慢慢抬起頭，像在確認警報解除。"

    $ play_bgm("tender", fade=2.2)

    hide dog
    show dog sniff_wire at dog_mid
    with Dissolve(1.0)

    $ dog_sfx("soft")
    "[dog_label]走到桌邊，鼻尖碰了碰垂下來的耳機線......像在確認：那個尖銳的聲音，真的關掉了。"
    "予安把耳機放到桌上，將線收好。"
    ya "關了。"
    "她把鬆掉的插頭完整拔下。喀的一聲很輕，卻是這場早會裡，第一個沒有從耳機裡折回來的聲音。"

    "狗又從桌腳縫裡確認了一次，直到耳機真的不再冒出人的聲音。"
    "會議筆記最後一頁，多了一行不是工作的字：「先拿下耳機。」她盯著那五個字，沒有劃掉。"
    "忙起來的自己向來不可靠，她需要的提醒，得比記憶更頑固才行。"
    "行事曆又跳出下個月的衝刺週......回程會更晚。她把提醒關掉，卻沒有刪。"
    $ flags["ch2_seed_busy_calendar"] = True

    "她打開手機裡的動物醫院資料，姓名欄還空著，游標一閃一閃地催著。"
    menu:
        "保留超商叫牠的名字「小7」":
            $ dog_label = "小7"
            "予安在姓名欄填上「小7」......這名字從超商後門一路跟過來，短短一個字加數字，卻已經有人為牠回過頭。"

        "替牠換一個新名字":
            $ proposed_name = renpy.input("想怎麼叫牠？", default=dog_label, length=12).strip()
            if proposed_name:
                $ dog_label = proposed_name
            "予安把「[dog_label]」念得很輕。狗未必聽得懂名字的意思，耳朵卻誠實地朝她動了一下。"

    show dog wag at dog_mid
    with Dissolve(0.8)
    "名字落定的那幾秒，[dog_label]的尾巴輕輕搖了起來......弧度不大，卻是今天的第一次，統計上算是重大進展。"

    "手機跳出房東訊息：若有養寵物，記得補報備。語氣不兇，只附一張表格連結，官僚體系難得溫柔一次。"
    $ flags["ch2_seed_lease_pet"] = True
    "她把連結存進備忘，沒有立刻填......這種表格，永遠有明天。"

    "門外傳來電梯開門聲，有人拖著紙箱經過，腳步停在她門前。"
    show dog stair_watch at dog_mid
    with Dissolve(0.5)
    neighbor "妳有養狗喔？"
    "狗的身體比她更早聽懂了「陌生」這兩個字。"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_06_corridor_third_person


## ------------------------------------------------------------
## Section 06：樓梯間的第三者
## 一件事：陌生人伸手時予安站在哪裡。唯一動 trust 的選項組為 Guard。
## flags 寫入：s06_protected／s06_allowed_touch／s06_sent_inside
## ------------------------------------------------------------

label section_06_corridor_third_person:
    $ current_section = "s06"
    $ save_name = "Section 06｜樓梯間的第三者"
    $ trust = max(0, min(12, trust))
    ## 樓梯間一段先靜音（承接 S05 後不立刻起樂）
    $ renpy.music.stop(channel="music", fadeout=1.2)
    $ _current_bgm = None

    scene bg stairwell_day
    with Dissolve(1.5)

    $ show_section_title("Section 06", "樓梯間的第三者")

    "門外站著隔壁新搬來的鄰居，紙箱疊在推車上，最上面那箱歪了一角......像是特地示範什麼叫沒放好。"

    show neighbor stand at char_left
    show yuan commute at char_right
    with dissolve

    neighbor "好可愛。妳新養的喔？"
    "予安還沒想好怎麼回答，[dog_label]倒是先做了決定：往後退，肩膀撞上門框。"
    neighbor "我摸一下，牠應該不會咬吧？"
    "鄰居往前一步，手已經伸出去了......比自我介紹還快。"
    $ dog_sfx("murmur")

    if tone >= 1 or flags.get("s05_soft_voice", False):
        ## 狗先畫、予安再疊 → 看起來躲在腿後
        show dog behind_legs at dog_behind_pair
        show yuan commute at char_right
        with Dissolve(0.8)
        "狗的耳朵貼低，躲到予安的小腿後；鼻尖湊近褲管，最後還是沒碰......牠比誰都懂得留一步。"
    else:
        show dog anxious at dog_far_pair
        with Dissolve(0.8)
        "狗貼著牆，耳朵壓低。牠沒有躲到予安身後，只替自己留著一條能退回屋裡的路......牠的逃生規劃向來比人清楚。"

    "推車上的紙箱忽然滑了一寸，鄰居回頭扶住，鞋尖也順勢往前......這棟樓裡，每個人都很會往前。"
    "膠帶撕開的短響一到，[dog_label]整隻彈了一下——比看陌生人的手還快。鼻子急促動兩下：舊紙箱、陌生洗衣精，與頭頂那隻停住的手。"
    "予安原本扶著門。往後退一步，門就會替她把場面關掉；笑一下說「沒關係」，尷尬也散得比較快......禮貌一直是最省事的逃生梯。"
    "可是狗的後腳已經抵住門檻。再退一步，就只剩屋內那條看不見外面的路。"
    neighbor "牠是不是很膽小？我家的狗以前摸兩次就熟了。"
    neighbor "我不會突然摸啦，先讓牠聞一下就好。"
    "推車輪子卡進磁磚縫，前後推了兩下......喀、喀。每響一次，[dog_label]的肩膀就往她腿後再縮一點。那點重量隔著褲管輕輕發抖，比任何一句話都誠實。"
    "話沒有惡意。這才是最麻煩的地方......沒有惡意的話，最難拒絕。"
    thought "要保護牠，不一定要先證明別人做錯了。"
    "牠先看的從來不是那隻手，而是那隻手會不會停下來。"

    # ▷ 信任選擇（Guard）...... 本段唯一動 trust 的選項組
    menu:
        "往前半步擋住，說「牠還在適應，先不要摸」":
            $ trust += 2
            $ guard += 1
            $ flags["s06_protected"] = True
            $ flags["s06_allowed_touch"] = False
            $ flags["s06_sent_inside"] = False
            ## 擋人圖朝左對鄰居；狗留在予安身後
            hide yuan
            show dog behind_legs at dog_behind_pair
            show yuan block at char_right
            with Dissolve(0.6)
            "予安往前半步，剛好卡在那隻手和狗中間......不是撲上去，是精準卡位。"
            ya "不好意思，牠還在適應。今天先不要摸牠。"
            neighbor "喔，好啊。我只是看牠很可愛。"
            ya "我知道，謝謝妳。"
            "樓梯間只安靜了兩秒，鄰居就把手收了回去......在這棟樓，兩秒已經算識相。"
            show dog behind_legs at dog_behind_pair
            show yuan block at char_right
            with Dissolve(0.6)
            pause 0.7

        "怕場面尷尬，讓鄰居摸一下":
            $ trust -= 2
            $ guard -= 1
            $ flags["s06_protected"] = False
            $ flags["s06_allowed_touch"] = True
            $ flags["s06_sent_inside"] = False
            ya "可以吧……輕一點就好。"
            "手掌落下時，狗整個僵住，尾巴貼緊腹側，眼睛只看著門內......那是牠唯一還敢想的地方。"
            hide dog
            show dog ear_flat at dog_far_pair
            with Dissolve(0.7)
            pause 0.6
            neighbor "牠好乖喔。"
            "予安第一次發現，「乖」有時候只是沒有退路的另一種說法。"

        "先把牠抱回屋裡，避免惹麻煩":
            $ trust -= 1
            $ guard -= 1
            $ flags["s06_protected"] = False
            $ flags["s06_allowed_touch"] = False
            $ flags["s06_sent_inside"] = True
            "予安彎身把狗抱起來，動作不重，卻快得像在收拾一件還沒發生的麻煩。"
            ya "不好意思，牠怕生。"
            hide dog
            with dissolve
            pause 0.5
            "門關上了。事情確實變簡單，只是牠沒看見她到底站在哪一邊。"

    neighbor "可是這棟可以養嗎？"

    if flags.get("s06_protected", False):
        "予安低頭，[dog_label]仍停在她腿後......這次沒有人需要重新確認立場。"
    else:
        "予安看向門內，沒有立刻接話。"

    ya "我會去跟管理室確認。"
    "她頓了一下。"
    ya "我們還在適應。"
    "「我們」兩個字說出口，比她預想的自然許多......說完才發現，這種話一出口就收不回去。"

    neighbor "好啦，那我先不吵牠。下次遠遠打招呼。"
    "予安點頭。拒絕並沒有讓樓梯間塌下來。她低頭看狗......牠只知道，那隻伸過來的手，最後停住了。"

    "電梯門關上。予安退回屋內，沒有急著把門甩上......今天沒有人需要用力證明什麼。"

    scene bg entrance_day
    with Dissolve(1.2)

    hide neighbor
    hide yuan
    show yuan commute at char_right

    if flags.get("s06_sent_inside", False):
        "狗在鞋櫃旁等著。予安把門留開，退到兩步外，把決定權留給牠。"
    else:
        "她等[dog_label]自己跨過門線，才把樓梯間的聲音關在外面。"

    $ play_bgm("tender", fade=2.2)

    if flags.get("s06_protected", False) or trust >= 5:
        ## forehead_nudge 圖含小腿裁切：隱藏予安全身，避免雙腿疊影
        hide yuan
        show dog forehead_nudge at dog_nudge
        with Dissolve(1.0)
        $ dog_sfx("soft")
        "[dog_label]往前半步，額頭很輕地碰了一下她的小腿......不是撲，也不是討摸，碰完就退開，像放下一句很短的話，懶得等回覆。"
        ya "……不客氣。"
        "她說完才覺得自己有點好笑，跟一隻狗道謝......可這一次，她沒有把話吞回去。"
        show yuan commute at char_right
        hide dog
    else:
        show dog halfstep at dog_far_pair
        with Dissolve(1.0)
        "狗往前走了半步，鼻尖停在褲管外一點點，最後沒有碰上。予安沒有追，只讓那段距離留到下一次。"

    "樓梯間又傳來推車輪子壓過磁磚縫的聲音。[dog_label]抬頭，身體先朝門的方向繃了一下。"
    "予安沒有急著說「沒事」......空話誰都會說。她先走到門邊確認鎖好，才回到牠看得見的位置坐下。"
    "狗聽不懂緊張是什麼，只看見她的手沒有再伸過來。過了一會兒，牠把原本懸著的前腳放回地板。"
    "樓梯間安靜下來。那半步，沒有被催促。"

    centered "{size=30}{color=#F7EFE4}今晚，站的位置就夠了。{/color}{/size}"

    "她把這句話留給自己，沒打算說給誰聽。"
    "玄關燈還亮著。[dog_label]在鞋櫃旁繞了一圈，最後挑了個能同時看見她與門的位置趴下......牠向來很會挑位置。"
    "予安沒有關燈。今晚先讓樓梯間那一點餘波，慢慢散掉。"
    "她把鞋子擺整齊，動作比平常慢一點......怕再發出像推車輪那樣突然的聲響。"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_07_sick_guard


## ------------------------------------------------------------
## Section 07：她倒下的那天
## 一件事：予安發燒，小7守在房門線。唯一動 trust 的選項組延續 Tone。
## flags 寫入：s07_reassured／s07_shut_out／s07_door_ajar
## ------------------------------------------------------------

label section_07_sick_guard:
    $ current_section = "s07"
    $ save_name = "Section 07｜她倒下的那天"
    $ trust = max(0, min(12, trust))
    $ play_bgm("sick_guard", fade=2.5)

    scene bg living_night
    with Dissolve(1.5)

    $ show_section_title("Section 07", "她倒下的那天")

    "凌晨兩點十三分，予安被自己的冷醒了過來......身體比鬧鐘準時。"
    "客廳的燈還亮著，鬧鐘在桌上震了第三次。她想伸手關掉，手臂卻重得像壓著一條濕毛巾。"
    "額頭燙，喉嚨乾，連吞口水都要先想一下才敢動。門外，有爪子刮過地板。"

    if trust >= 5 or flags.get("s06_protected", False):
        show dog guard_door at dog_near
        with Dissolve(0.8)
        "[dog_label]走到床邊，鼻尖碰了一下垂落的被角，又把她忘在客廳的拖鞋叼到門邊......牠沒有醫學常識，但很會整理現場。"
        "牠不知道拖鞋能做什麼，只記得她起床時總會穿上。"
    else:
        show dog anxious at dog_far
        with Dissolve(0.8)
        "[dog_label]沒有進房，只在門口來回兩趟，發出一聲短短的輕吠，又立刻安靜。"
        "像怕自己的聲音，也會被關在外面。"

    ya "現在幾點……"
    $ dog_sfx("bark")
    "狗又叫了一聲。不是催促，更像確認房間裡還有沒有回答。"

    "予安想撐起身體，手肘才離開床，視線便暗了一圈......身體顯然沒打算配合。她重新躺下，棉被被汗黏在膝後。"
    "床邊的水杯是空的，手機在客廳充電。她平常替所有東西安排好位置，今晚每一樣都恰好離她差一點。"
    "[dog_label]聽見床墊下沉，前腳往前半步，又因她突然咳嗽停住。"
    "牠低頭聞自己的腳，再聞門外，像把房間裡每一條能走的路重新排過一次。"
    ya "我知道你也不知道怎麼辦。"
    "這句話說完，她反而沒有那麼急著要求牠安靜。"
    "耳鳴忽然蓋過冷氣聲，尖銳地停在腦後。予安閉上眼，連門口的影子都被那道聲音沖淡。"
    "過了幾秒，[dog_label]短短叫了一聲。那聲音不大，卻從耳鳴裡穿進來，讓她重新找到房門的方向。"
    "她想回應，喉嚨只剩乾痛；想伸手，手臂仍沉在床沿。這一次，她得先決定要把哪一種聲音送回去。"

    # ▷ 信任選擇（Tone）...... 本段唯一動 trust 的選項組
    menu:
        "摸摸牠的背，低聲說「我還在」":
            $ trust += 2
            $ tone += 1
            $ flags["s07_reassured"] = True
            $ flags["s07_shut_out"] = False
            $ flags["s07_door_ajar"] = False
            show yuan sick_bed at char_right
            with Dissolve(0.5)
            "予安把手移到床沿，指尖很輕地碰了碰狗背。"
            ya "我還在。只是有點不舒服。"
            show dog guard_door at dog_sick_far
            with Dissolve(0.5)
            pause 0.5
            show dog guard_door at dog_sick_mid
            with Dissolve(0.8)
            $ dog_sfx("soft")
            "[dog_label]聽不懂後半句，卻聽得懂那個熟悉的低聲。牠沒有再叫，只把身體放回門線上。"

        "煩躁地說「吵死了」，把牠關到客廳":
            $ trust -= 2
            $ tone -= 1
            $ flags["s07_reassured"] = False
            $ flags["s07_shut_out"] = True
            $ flags["s07_door_ajar"] = False
            ya "吵死了……讓我睡一下。"
            "門闔上的聲音不大。外面的爪步停了，過了一會兒，才慢慢退到沙發旁。"
            hide dog
            show dog ear_flat at dog_far
            with Dissolve(0.7)
            pause 0.5
            $ dog_sfx("whimper")

        "說「等一下，我不舒服」，把門留一條縫":
            $ flags["s07_reassured"] = False
            $ flags["s07_shut_out"] = False
            $ flags["s07_door_ajar"] = True
            ya "等一下。我不舒服，不是在兇你。"
            "她把門留了一條縫。狗停在縫外，沒有靠近，也沒有離開。"
            show dog guard_door at dog_sick_mid
            with Dissolve(0.7)
            pause 0.5
            $ dog_sfx("murmur")

    scene bg kitchen_night
    with Dissolve(0.9)
    hide dog
    show yuan commute at char_right
    with Dissolve(0.4)

    "予安扶著牆去倒水，杯子碰到流理台，比平常更響。水柱濺到手背，她花了兩次才轉緊水龍頭......生病這件事，連水龍頭都跟著添亂。"
    ya "沒關係。你待在那裡就好。"

    scene bg living_night
    with Dissolve(0.9)
    hide yuan
    with Dissolve(0.3)

    if flags.get("s07_shut_out", False):
        show dog ear_flat at dog_far
        with Dissolve(0.5)
        "她回房前重新把門打開。[dog_label]仍在沙發旁，抬眼確認了一次，沒有跟過來。"
        "予安把一條乾毛巾放在門邊，留給下一次靠近。"
    else:
        show dog guard_door at dog_sick_mid
        with Dissolve(0.6)
        "[dog_label]跟到房門口便停下。牠趴在那條線上，頭朝客廳，耳朵卻留一隻向著她。"
        ya "謝啦。"
        "以前都是她聽狗的呼吸；今晚門邊也有一種很淺的呼吸，一下一下對上她的。"
        "牠不知道該怎麼辦，只是把自己放在房門那條線上。"

    "天快亮時，她又醒了一次。房門線上的影子換了方向，[dog_label]的下巴從左腳挪到右腳，仍沒有離開。"
    show yuan sick_bed at char_right
    with Dissolve(0.4)
    "予安把手伸到床沿，沒有碰牠，只讓指尖垂在牠聞得到的位置。"
    hide yuan
    show dog nose_tip at dog_near_to_yuan
    with Dissolve(0.8)
    pause 0.6
    "一個濕涼的鼻尖短短靠近，又退回去。她在那個幾乎不能算接觸的瞬間，再次睡著。"
    show dog guard_door at dog_sick_mid
    with Dissolve(0.6)
    "早上，她傳訊息請假。主管只回「好，先休息」......一句話，比昨晚任何安慰都乾脆。她原本準備了一長段解釋，最後沒有送出。"
    if flags.get("ch2_seed_yuan_family_unread", False):
        "通知列往下滑時，家人那則未讀還停在原位。她沒有點開。"
    "予安忽然笑了一下。牠不會量體溫，也不會拿藥；門邊那團影子卻一直沒離開......履歷表上不會寫，但確實是全勤。"
    "耳鳴已經退遠。房間裡剩下兩種不整齊的呼吸，一個在床上，一個在門邊，慢慢找到彼此都能跟上的速度。"

    scene bg office_night
    with Dissolve(1.5)
    show yuan headphones at char_center
    with dissolve

    "退燒後的第一個上班日，她點進手機相簿：照片裡，[dog_label]睡在房門邊，一隻耳朵翻著。"
    "她沒有貼動態，只看了三秒，便把手機扣回桌上......這種照片，社群不需要，她自己需要。"
    "那張模糊照片，為什麼比退燒證明更像她真的撐過昨晚......她還不知道該怎麼解釋。"
    thought "我一直以為是我在照顧牠。那晚，門邊先沒有空。"
    "下班時，她繞進生活用品店，買了一條最普通的牽繩。"
    "她把牽繩放進提袋時，忽然想起房門線上那一雙還沒完全鬆開的耳朵。"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_08_corner_walk


## ------------------------------------------------------------
## Section 08：走到轉角就好
## 一件事：第一次正式牽繩外出。唯一動 trust 的選項組回到 Dist。
## flags 寫入：s08_waited／s08_forced_walk／s08_returned_early
## 演出四拍：進場（玄關胸背帶／門線）→ 關鍵（巷口機車＋三選一）
##          → 反應（返家玄關解帶／鞋邊睡）→ 離場鉤子（週一同事提議）
## BGM：calm／corner_walk → 驚嚇 tense 短 → 選項直接定 tender／calm（返家不重切）
## 鞋邊睡維持 tender；硬拖維持 calm
## ------------------------------------------------------------

label section_08_corner_walk:
    $ current_section = "s08"
    $ save_name = "Section 08｜走到轉角就好"
    $ trust = max(0, min(12, trust))
    if trust <= 3:
        $ play_bgm("calm", fade=2.5)
    else:
        $ play_bgm("corner_walk", fade=2.5)

    scene bg entrance_day
    with Dissolve(1.5)

    $ show_section_title("Section 08", "走到轉角就好")

    show yuan leash at char_right_s08
    show dog leash_wait at dog_entrance_far_s08
    with dissolve

    "週六上午，牽繩在玄關鞋櫃上躺了二十分鐘，比誰都有耐心。"
    "予安穿好鞋，又坐回地墊邊。[dog_label]隔著兩步看那條陌生的線，鼻尖靠近一下，立刻退開。"
    "她沒有拿胸背帶追著牠套，只把胸背帶和牽繩一起放到玄關地板，等牠聞完。"

    "金屬扣環碰到地墊邊緣，發出一聲很小的喀響。[dog_label]仍縮了一下，繞到鞋櫃另一側，從縫裡盯著那個不會自己移動的東西......牠顯然還不打算相信這點。"
    "予安把手收回膝上。她等到牠探頭，才用一根手指把胸背帶往前推一點；每推一次就停，讓牠自己補完剩下的距離。"
    "狗先聞布邊，再聞扣環，最後聞她碰過的地方。鼻尖在三種氣味之間來回，像確認這不是一個突然關上的圈套。"
    ya "我第一次用這個。你也是。"
    "語氣很平，沒有多加別的字......多說也沒用，牠聽的是語氣，不是字。"

    show dog leash_wait at dog_entrance_mid_s08
    with Dissolve(0.8)

    "等牠不再往後縮，她才蹲在側邊，讓牠自己把前腳踏進去。扣環喀一聲合上；她立刻鬆手，沒有把穿好當成出發命令......命令這種事，她今天不打算下。"
    show dog harness_bite at dog_entrance_mid_s08_to_yuan
    with Dissolve(0.6)
    "[dog_label]站在玄關原地，把左腳抬起又放下，接著扭頭去咬胸口那條陌生的布。予安沒有阻止，只用手背擋住扣環，免得牙齒卡住。"
    "過了半分鐘，牠停止啃咬。胸背帶沒有消失，門也沒有立刻打開......抗議無效之後，牠慢慢把四隻腳都放穩。"
    show dog leash_wait at dog_entrance_mid_s08
    with Dissolve(0.5)
    ya "走到轉角就好。"

    "她把手放上門把，先開一道縫。門外樓梯間的冷氣與燈管味鑽進來。[dog_label]的鼻子動了兩下，前腳踩出門檻半步，後腳仍留在地墊上......牠很清楚哪隻腳可以先出去試水溫。"
    "予安沒有用牽繩把那兩隻後腳拉過去。她側身讓出空間，門開大一點，又停住。"
    "第一次，牠縮回來。地墊還暖，外面還陌生。"
    pause 0.7
    "她把門再開一次。這回[dog_label]自己把後腳也帶出去......門裡一個世界，門外另一個，牠選了跟她同一側跨出去。"
    "玄關安靜下來。鞋櫃、空掛勾、地墊上她剛坐過的位置，都留在門後，等著一段不知道會怎麼收尾的散步。"

    scene bg alley_day
    with Dissolve(1.5)
    ## 巷口進場：予安走路；狗一開始在身後不願前進；停放空車
    show scooter parked at scooter_parked
    show yuan walk at char_right_walk
    show dog street_tense at dog_behind_walk
    with dissolve

    "大門推開的瞬間，外面的世界一下變得很密。早餐店的油煙、樓上曬過的衣服、排水溝、機車輪胎，全部擠在同一口呼吸裡......城市對一隻鼻子從來不是溫柔的地方。"
    pause 0.7
    "遠處有人拉鐵門，金屬聲沿著巷子刮過來。塑膠袋貼著地面滾了兩圈，卡在盆栽下。"
    "左側停著一台機車，座位空著，只有曬熱的塑膠與輪胎味......世界上最沒有威脅性的東西，此刻看起來仍像個陷阱。"
    "[dog_label]停在她身後半步，四隻腳像釘在地上。牽繩垂著，卻被那半步距離拉得筆直。"
    "予安把握把從手掌移到手腕，另一手只扶著繩身。她往前半步，停住，再等。"

    if trust <= 3:
        pause 0.6
        "[dog_label]貼著牆挪了半腳，又停。鼻子還沒決定先聞哪裡，呼吸已經又快又淺。"
        show dog street_tense at dog_mid_walk
        with Dissolve(1.2)
        "予安再往前一點。繩子緊了又鬆。牠跟了半步，又幾乎立刻想退回她腳後......外面對牠來說，還是太大了一號。"
    elif trust <= 6:
        pause 0.5
        show dog street_tense at dog_mid_walk
        with Dissolve(1.0)
        "過了一會兒，[dog_label]才自己挪出兩步。每走一步就停，右耳轉向她，確認她沒有忽然消失。"
        "牠走了兩步又停。予安也停，把手腕往前送一點，等繩子垂回鬆弧。"
        show dog leash_wait at dog_near_walk
        with Dissolve(1.0)
        "右耳轉向她之後，牠才再往前半個身位......信任這種東西，果然是靠公分累積的。"
    else:
        pause 0.4
        show dog leash_wait at dog_mid_walk
        with Dissolve(0.9)
        "[dog_label]先把鼻子伸向空著的機車，退半寸，又再探。牽繩一下鬆、一下緊。"
        show dog leash_wait at dog_near_walk
        with Dissolve(1.0)
        "牠慢慢跟到她側邊。牽繩仍繃著，卻不是一路往後退......已經算是進步。"

    "他們走過那台空著的機車。車殼還有曬熱的味道，狗伸長鼻子，沒敢靠近輪胎——新環境會怕車；這一退卻偏沉，像記得某種離遠。"
    "一個送餐員從後方快步經過，保溫箱擦過予安手肘。她下意識往旁邊讓，隨即發現牽繩也被帶緊。"
    ya "對不起。是我沒看到。"
    "她停下來，把繩子重新放鬆。[dog_label]沒有回頭，右耳卻短短轉向她。"
    "前方的樹影只有幾步，牠每走一步都先把重量壓到後腳，確定地面沒有追上來，才把前腳送出去......謹慎到近乎科學。"

    "予安沒有說「加油」。她怕連兩個字都會變成催促。"
    "一輛機車從轉角呼嘯切進來，排氣聲突然放大。"
    $ play_bgm("tense", fade=0.8)
    ## 轉角呼嘯機車：短暫疊在停放空車前方，再撤走（立繪 ×0.8）
    show scooter pass at scooter_pass
    show dog street_tense at dog_behind_walk
    with Dissolve(0.4)
    "狗整個往後扯，指甲在地面刮出短短一聲......剛才好不容易挪出來的距離，一瞬間退回她腳後。進度這種東西，從來不是永久保存。"
    "予安的手腕被猛地扯痛。她比狗還早半拍繃緊肩膀，又立刻強裝沒事；第一個反應仍是把繩子拉回來——力道才起來，便看見狗的腹部幾乎貼到地面。"
    pause 0.9
    $ dog_sfx("whimper", 0.28)
    hide scooter pass
    with Dissolve(0.5)
    "機車已經離開，聲音卻像還留在牠身上。胸背帶跟著急促呼吸一下下起伏，眼睛在轉角、家門與她之間來回——像在等一扇不會再打開的門。"
    "她看了一眼手機。才過六分鐘。計步數少得不像一次散步，卻已經裝滿牠今天能處理的聲音。"
    pause 0.6
    "樹影就在旁邊。轉角只剩幾公尺，近得讓人很想把「第一次成功」湊完整......但今天的重點，從來不是完整。"

    # ▷ 信任選擇（Dist）...... 本段唯一動 trust 的選項組
    # 驚嚇 tense 後由選項直接定下一首（勿先回開場再切，避免多一次換曲）
    menu:
        "走到樹下側身蹲著，等牠自己決定下一步":
            $ trust += 2
            $ dist += 1
            $ flags["s08_waited"] = True
            $ flags["s08_forced_walk"] = False
            $ flags["s08_returned_early"] = False
            show yuan leash at char_right_walk
            with Dissolve(0.6)
            "予安走到樹下側身蹲著，把視線移開，也把自己的呼吸放慢。"
            pause 0.8
            "狗先看機車離開的方向，再看她的鞋。牽繩鬆了一點，又一點。"
            "一片乾葉被風吹到牠腳邊。牠先退半步，等葉子停下，才低頭聞了聞。鼻尖碰到葉緣時，予安仍看著別處。"
            "她讓自己的手垂在膝旁，不拍腿、不拿零食......這次她決定什麼都不做，比做點什麼還難。"
            $ play_bgm("tender", fade=2.2)
            show dog leash_wait at dog_mid_walk
            with Dissolve(0.8)
            $ dog_sfx("soft")
            "過了一會兒，牠自己往前走了一公尺。"
            show dog leash_wait at dog_near_walk
            with Dissolve(1.0)
            "走到樹影中央，牠停下來甩了一次身體。胸背帶跟著晃動，從耳尖到尾巴的緊繃鬆開一點。"
            ya "好。我有跟上。"

        "既然都出門了，拉著牠把一圈走完":
            $ trust -= 2
            $ dist -= 1
            $ flags["s08_waited"] = False
            $ flags["s08_forced_walk"] = True
            $ flags["s08_returned_early"] = False
            show yuan walk at char_right_walk
            "予安把牽繩收短，往前走。"
            ya "一下就好，走完就回家。"
            show dog street_tense at dog_far_walk
            with Dissolve(0.7)
            $ dog_sfx("whimper")
            "牽繩繃成一條直線。[dog_label]被拉過樹影，四隻腳輪流追著胸口的力道。遇到轉彎，牠來不及聞便被帶往下一段。"
            "予安每走幾步就說一次「快到了」。同一句話重複到最後，連她自己都聽不出安撫，只剩完成......像在對自己交差。"
            "牠確實跟完了一圈，卻一路沒有再聞地面。完成的路線留在手機計步裡，數字很漂亮，別的什麼都沒留下。"
            "回到大門前，牠沒有立刻跨進去，只貼著牆喘氣。予安這才把牽繩放長，晚了，但仍讓最後那一步由牠自己走。"
            ## tense→calm 同檔只調音量；返家維持
            $ play_bgm("calm", fade=2.0)

        "今天先回家":
            $ trust += 1
            $ dist += 1
            $ flags["s08_waited"] = False
            $ flags["s08_forced_walk"] = False
            $ flags["s08_returned_early"] = True
            show yuan walk at char_right_walk
            "予安把牽繩留鬆，沿原路慢慢折返。"
            ya "好，今天到這裡。"
            $ play_bgm("tender", fade=2.0)
            "回家的每一步，都還是牠自己走的......沒走完的轉角，改天再說。"
            show dog leash_wait at dog_mid_walk
            with Dissolve(0.8)
            $ dog_sfx("soft")
            "經過剛才那台停著的機車時，[dog_label]仍繞開半個身位，卻肯停下來聞一次地面。"
            "予安也跟著停。回程因此比去程更久，但牽繩大多垂成一個鬆鬆的弧。"
            pause 0.6
            "抵達大門，狗先看裡面，再回頭看那個沒有走到的轉角。牠沒有再往轉角看很久，便跟她一起進門。"

    scene bg entrance_day
    with Dissolve(1.5)
    ## scene 會清掉巷口立繪；返家立刻重顯人＋狗（勿只留予安）
    if flags.get("s08_forced_walk", False):
        show yuan leash at char_right_s08
        show dog street_tense at dog_entrance_far_s08
    else:
        show yuan leash at char_right_s08
        show dog leash_wait at dog_entrance_mid_s08
    with Dissolve(0.5)

    show dog drink_bowl at dog_entrance_mid_s08
    with Dissolve(0.6)
    "[dog_label]一進門便衝向水碗，喝得很急。水沿著嘴角滴到玄關地墊。予安沒有立刻擦，只先坐下，把牽繩從手腕慢慢鬆開。"
    "手腕被繩帶磨出一條淡紅色。她用拇指按了按，才發現自己從出門到現在一直握得太緊......原來緊張的不只有狗。"
    "胸背帶的扣環在玄關解開時，[dog_label]全身抖了一下，把累積在毛裡的灰和緊張一起甩開。"
    "予安把胸背帶留在玄關地板，沒有立刻收進櫃子。"

    if flags.get("s08_forced_walk", False):
        show dog street_tense at dog_entrance_far_s08
        with Dissolve(0.8)
        pause 0.5
        "狗停在門邊，離她的鞋還有一段距離。予安把毛巾放在看得見的位置，沒有再叫牠過來。"
        "她把手機計步畫面關掉。那個完整的圓，今天先不給誰看。"
        pause 0.8
        ya "我走得太快了。"
        ## 已在 calm，不重播
        "狗仍沒有靠近，但喝水的間隔慢了一點......算是唯一願意讓步的地方。"
    else:
        ## 鞋邊睡：維持 tender（選項已換曲），不再切 warm
        show dog shoe_sleep at dog_entrance_mid_s08
        with Dissolve(1.0)
        pause 0.5
        $ dog_sfx("sigh")
        "狗喝完水，繞到她腳邊轉了半圈，最後靠著那雙剛走過外面的鞋趴下......鞋還停在玄關地墊上，比沙發還受歡迎。"
        pause 0.8
        "眼睛還睜著，身體卻先睡著了。外面還很大，鞋邊卻已經有溫度。"
        "予安原本想把鞋脫下來，腳跟動了一下又停住。她就維持那個不太舒服的角度，讓狗先把這場散步睡完。"
        "幾分鐘後，牠的呼吸從急促變得深長。每一次吐氣，都把下巴更完整地交給鞋面。"

    "那天下午，牽繩一直留在玄關地板。予安經過時會放慢腳步，[dog_label]醒來也只是抬眼，不再立刻躲開那條線。"
    "她沒有趁機再帶牠出門。今天的聲音與氣味，還需要時間在身體裡慢慢安靜。"

    scene bg living_day
    with Dissolve(1.0)
    ## 客廳空場：狗在玄關聞胸背帶（畫面外）；予安不入鏡
    hide yuan
    hide dog

    "睡醒後，狗自己走到玄關、胸背帶旁聞了一次。予安坐在沙發上看見了，沒有起身......有些事，不需要她在場也能發生。"

    pause 0.8
    scene bg office_night
    with Dissolve(1.0)
    show yuan headphones at char_right
    with dissolve

    if flags.get("s08_forced_walk", False):
        "週一，同事在她手機亮起時瞥見一張門邊的照片。畫面裡，[dog_label]離她的鞋還有一段距離，旁邊是沒有收起來的牽繩。"
    else:
        "週一，同事在她手機亮起時瞥見那張靠著鞋睡著的照片。"
    "「妳最近是不是很累？」對方停了一下，語氣沒有玩笑。"
    pause 0.6
    "「如果真的顧不來，我可以養。」"
    "予安看著螢幕裡那個小小的身影，沒有立刻回答......有些問題，答案比想像中難給。"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_09_almost_handoff


## ------------------------------------------------------------
## Section 09：差點交給別人
## 一件事：同事真誠提出接手，予安必須承認自己是否已經選過牠。
## 唯一硬分歧：留下（trust／Guard +2）或送走（trust／Guard -2）。
## flags 寫入：s09_stayed／gave_away／landmark_chose_reason_over_bond
## ------------------------------------------------------------

label section_09_almost_handoff:
    $ current_section = "s09"
    $ save_name = "Section 09｜差點交給別人"
    $ trust = max(0, min(12, trust))
    $ play_bgm("almost_gave", fade=2.5)

    scene bg office_night
    with Dissolve(1.4)

    $ show_section_title("Section 09", "差點交給別人")

    show yuan headphones at char_right
    show coworker stand at char_left
    with dissolve

    "同事又在茶水間問了一次。這次沒有笑著說，也沒有把狗講成什麼可以轉手的包裹。"
    coworker "我不是催妳。只是我以前養過，現在住的地方也比較大。妳如果真的太累，可以先讓我接手。"
    "飲水機恰好開始加熱，運轉聲把沉默填得剛好。予安盯著杯底那圈還沒化開的即溶咖啡，像在研究一道解不開的題。"
    coworker "我之前那隻活到十六歲。打針、換飼料、半夜跑醫院，我都碰過。"
    "她說得很平靜，不像在背履歷，更像把自己能扛的事一項項攤在桌上，讓人清點。"
    ya "妳家不是還有陽台嗎？"
    coworker "有，窗也裝好防護了。白天我媽在家，不會讓牠一直自己待著。"
    coworker "不過我自己下個月也會很忙。能幫的時候幫；忙不過來，我也會跟妳說。"
    "每個答案都比予安現在的生活更完整。找不到可以挑刺的地方，反而讓人更想點頭。"
    "予安點開手機備忘錄。工時、房租、醫療費、能不能準時回家......還有那張還沒填的報備表格。每一項都寫得很清楚，彷彿只要清單夠工整，心裡那些說不出理由的部分，也會乖乖閉嘴。"
    ya "我想一下。"

    scene bg living_night
    with Dissolve(1.1)
    hide coworker
    show yuan sofa at char_left
    with Dissolve(0.5)

    "她真的想了。第一晚，她把每個月可能多花的錢加總一遍，數字比想像中誠實。"
    "第二晚，加班通知在九點多跳出來，行事曆邊緣那塊代表趕工的色塊，也跟著亮了一下，準時得很諷刺。"
    show dog parallel at dog_far
    with Dissolve(0.6)
    "[dog_label]睡在門邊，聽見她拉開椅子就立刻抬頭。那雙眼睛沒有責怪的意思，卻讓清單變得比原本更難唸完。"
    "第三晚，她整理疫苗資料，順手把照片一張張滑過去：後門的紙箱、玄關的外套、靠著鞋睡著的那張臉。"
    if flags.get("s04_forced_photo", False):
        "還有一張沙發合照......她笑得很開，狗的眼睛卻直直望向能逃跑的方向。這張她沒刪。"
    "她沒有替照片加說明，只把檔案日期改成方便查找的格式。做完這些，效率高得像在幫人資整理離職交接......只是這次交接的是一段生活。"
    "最後，她按下送出：「週六見。」"

    scene bg living_day
    with Dissolve(1.2)
    hide dog
    ## 狗先、人後；transform 已翻轉予安，與狗對望（×0.8）
    show dog farewell at dog_farewell_near
    show yuan farewell at char_right_farewell
    with dissolve

    "週六出門前，她把水碗洗了兩次。牽繩捲好，疫苗資料放進紙袋，連平常老忘記補的濕紙巾，這次也記得塞了進去。"
    "東西準備得越齊全，房間看起來就越像有人正在搬家，只是箱子比較小。"
    "她把飼料分裝成七小袋，逐一寫上日期。寫到第四袋，筆尖停住，墨水在塑膠袋上暈開一小點，像是手比腦子先猶豫。"
    "舊外套也被折進提袋，摺得比平時整齊。"
    if flags.get("coat_bed", False):
        "鋪平過的那一面，還留著門邊那一夜的灰塵與牠的味道；袖口那幾道抓痕淺淺的，像簽名。"
    else:
        "只被當靠墊用過的那一角，氣味淡了些；但袖口那幾道抓痕，一筆都沒少。"
    "予安用拇指順過那幾道抓痕，最後還是沒把外套抽出來。牠習慣什麼，這種事無法寫進交接單，但她記得。"
    "臨走前，她在客廳地板蹲下來。沒先拿牽繩，只把手掌攤開......分不清是打招呼，還是道別，反正兩者的姿勢一樣。"

    scene bg entrance_day
    with Dissolve(1.0)
    show yuan leash at char_right_s09
    show dog leash_wait at dog_entrance_far_s09
    with Dissolve(0.6)

    if trust >= 5:
        show dog paper_bag at dog_entrance_far_s09
        with Dissolve(0.5)
        "[dog_label]跟到玄關，鼻尖碰了碰紙袋，又乖乖靠回她腳邊，像在確認行李還沒被誰動過。"
        "她移動紙袋，狗也跟著換位置。不是阻擋，只是很有技巧地把自己的肩膀，一直卡在她和袋子中間。"
        show dog leash_wait at dog_entrance_mid_s09
        with Dissolve(0.6)
        "予安蹲下，把胸背帶放到地墊上。牠聞了兩次，自己把前腳踏進去；扣環合上的那一聲喀，讓兩個都停頓了一秒。"
        "這次開門，不是散步，是去見另一個人。門把貼著掌心發涼......性質完全不同。"
    else:
        "[dog_label]停在門線附近，沒有靠近。牠只是盯著那個裝滿自己氣味的紙袋，像在看一份被別人先簽好的合約。"
        show dog paper_bag at dog_entrance_far_s09
        with Dissolve(0.5)
        "予安蹲下想替牠扣胸背帶，牠往鞋櫃邊退了一步。她沒有追，只等那雙眼睛不再只盯著出口，才重新伸手。"
        "胸背帶終於扣上。門把再次貼著掌心發涼......這趟出門，終點不是公園，是另一個人的客廳。"

    scene bg cafe_day
    with Dissolve(1.5)
    show coworker cafe at char_left_cafe
    show yuan cafe at char_right_cafe
    ## scene 會清掉玄關的狗；門口三人同框時狗必須一開始就在場
    if trust >= 5 or flags.get("s06_protected", False):
        show dog cafe_refuse at dog_cafe_near_guard
    else:
        show dog cafe_tense at dog_cafe_mid
    with dissolve

    "咖啡廳門口比照片裡窄得多。玻璃門每開一次，磨豆聲和陌生人的氣味就一起湧出來，毫不客氣。"
    "同事提早十分鐘到，手裡沒有玩具，也沒有零食。她說第一次見面別急著用東西把狗騙近......這個判斷，予安挑不出毛病。"
    "三個人......如果一隻狗也算數......在騎樓下維持著一種不太像交接的距離。沒有人催，時間反而過得特別清楚，一秒都跳不過去。"
    "店門上的風鈴響了三次。[dog_label]每次都抬頭確認，到第三次，才沒把整個身體往後縮。算是進步。"
    coworker "不用急。我先讓牠聞我。"
    "同事蹲下，側過身，把手留在膝上......教科書級的標準動作，語氣也放得很輕。"

    if trust >= 5 or flags.get("s06_protected", False):
        show dog cafe_refuse at dog_cafe_near_guard
        with Dissolve(0.8)
        $ dog_sfx("growl")
        "[dog_label]卻貼住予安的鞋，肩膀繃得筆直。牠沒有撲咬，只在同事伸手想接牽繩的那一刻，喉嚨裡滾出一聲很短、很低的警告......夠短，但誰都聽懂了。"
        "牠拒絕的不是那個人。牠只是把好不容易畫出來的安全範圍，一口氣縮回予安腳邊。"
    else:
        show dog cafe_tense at dog_cafe_mid
        with Dissolve(0.8)
        $ dog_sfx("murmur")
        "[dog_label]僵在離兩人都有點距離的地方。沒有低鳴，也沒躲進誰身後；牠只是把四隻腳，重新調成隨時能撤退的姿勢。"
        "予安忽然懂了，安靜不代表同意。有時只是牠還不相信，這兩個人裡，有誰會真的替牠停下腳步。"

    coworker "牠在找妳。"
    ya "可是妳比較有經驗。"
    coworker "也許。但牠認得的是妳。"
    ya "認得不一定代表我適合。"
    coworker "對。適合也不一定代表牠現在就能跟我走。"
    "同事把兩件事分開講，沒有替她選。予安原本期待一個聽起來很專業的答案，結果只聽見自己的呼吸聲，特別大聲。"
    "紙袋裡的疫苗資料被風吹得沙沙響。她伸手壓住，掌心剛好蓋在姓名欄上......那個她曾坐在桌邊，一筆一畫替牠填上去的名字。"
    "理智清單還在紙袋裡，一項都沒失效。只是那份清單回答的是誰比較方便，沒有一項回答，是誰一次又一次走回同一扇門。"

    "咖啡廳裡有人拉開椅子，木腳刮過地面，一聲刺耳。[dog_label]縮了一下，兩個女人同時停住動作，比狗還緊張。"
    "同事先把手收回去；予安蹲低半步，沒有碰牠。兩人都懂得怎麼不逼近，差別只在......狗先抬頭找的是誰。"
    "那雙眼睛沒有逼她做決定。牠只是把鼻尖依序對準她的鞋、紙袋，最後對準回家的方向，像在畫一條很誠實的路線。"
    "予安想起自己曾說過「今晚不算」，曾把門留一條縫，也曾走得太快。牠記得的，大概就是這些疊在一起的氣味與腳步聲。"
    thought "我也會累。加班、房租、半夜發燒......每一項都寫得進清單。送走會比較輕，這句話也是真的。"
    thought "如果留下，下次失手，我不能只說『我不會』就結束。"
    "紙袋的提把勒進掌心，勒出一條紅印。送走確實會輕一點；牽繩，卻還纏在她的手腕上，不肯配合。"

    menu:
        "把牽繩收回來，繼續照顧牠":
            $ trust += 2
            $ guard += 2
            $ flags["s09_stayed"] = True
            $ flags["gave_away"] = False
            ya "對不起，讓妳白跑一趟。"
            hide coworker
            show yuan leash_pass at char_right_cafe
            with Dissolve(0.5)
            "她的手在抖，還是把牽繩重新繞回自己手腕，一圈都沒少。"
            ya "我不是比較會。我只是……想繼續學。"
            show coworker cafe at char_left_cafe
            coworker "那就繼續。真的需要幫忙，再找我。"
            "同事站起來，沒有生氣，也沒替這個決定鼓掌。她只把空著的手收進外套口袋，讓門口重新寬出一點空間。"
            show yuan cafe at char_right_cafe
            show dog cafe_refuse at dog_cafe_near_home
            with Dissolve(0.7)
            pause 0.5
            $ dog_sfx("soft")
            "[dog_label]的肩膀過了很久才鬆下來。牠沒有搖尾巴，只把鼻尖碰了碰她的鞋側，像在確認那雙鞋，依然朝著回家的方向。"
            "予安把疫苗資料從紙袋拿回來。紙張重量沒變，握在手裡卻明顯比剛才更難放手。"
            coworker "留下不代表什麼都得自己撐。妳可以問我，也可以找別人幫忙。"
            ya "我可能真的會問很多。"
            coworker "那就問。"
            "她把外套重新披回手臂，袖口的抓痕朝外......這次她沒打算藏起來。"
            "回程走到同一個轉角，[dog_label]停下聞了好一會兒。予安沒催，只讓牽繩鬆成一道能呼吸的弧線。"
            $ play_bgm("tender", fade=2.4)

        "照原先的安排，把牽繩交給同事":
            $ entry_trust = trust
            $ trust -= 2
            $ guard -= 2
            $ flags["s09_stayed"] = False
            $ flags["gave_away"] = True
            # Landmark 依「送走前」信任判斷，避免先扣 2 後漏記。
            if entry_trust >= 7:
                $ flags["landmark_chose_reason_over_bond"] = True
            else:
                $ flags["landmark_chose_reason_over_bond"] = False
            "予安把紙袋遞過去，再把牽繩握把一圈一圈從手腕鬆開。最後一圈卡在袖口，她多停了一秒，才把它放進同事手裡。"
            hide coworker
            show yuan leash_pass at char_right_cafe
            with Dissolve(0.5)
            ya "牠怕突然的機車聲。喝水很急。睡覺的時候，門不要全關。"
            show coworker cafe at char_left_cafe
            coworker "好。我會慢慢來。"
            if flags.get("landmark_chose_reason_over_bond", False):
                "紙袋交出去的那一秒，予安忽然想起那張靠著鞋睡著的臉......關係最好的時候，理由永遠也最完整。這才是最諷刺的地方。"
                thought "不是因為不愛。是因為太清楚自己會累。"
            if entry_trust >= 5:
                show dog cafe_refuse at dog_cafe_mid
                with Dissolve(0.7)
                pause 0.5
                "[dog_label]往她鞋邊靠了靠，牽繩卻從另一隻手傳來方向。牠低低鳴了一聲，沒人把那當成挽留，也沒人拿來責怪誰。"
            else:
                show dog cafe_tense at dog_cafe_mid
                with Dissolve(0.7)
                pause 0.5
                "[dog_label]沒有跟上任何一邊。兩邊都等了一會兒，同事才用鬆著的牽繩，帶牠慢慢走離玻璃門。"
            show yuan cafe at char_right_cafe
            with Dissolve(0.4)
            "予安站在原地，把已經交代過的事又在心裡默背一次。這個選擇有理由，也仍然會痛......兩件事，可以同時是真的，人生偏偏就這麼不方便。"
            "同事沒有立刻轉身走。她先讓狗在原地聞紙袋，再把牽繩放到最長，把選第一步的權利，留給牠自己。"
            coworker "我到家會傳訊息。今晚如果牠不吃，我也會跟妳說。"
            ya "好。門……記得留一點縫。"
            coworker "我記得。"
            "予安點頭。她沒有要求再抱一下，因為最後一次接觸不該只服務自己的捨不得。"
            "玻璃門映出她空著的手。直到同事和狗走過轉角，她才發現紙袋早已不在自己手上，手指卻還維持著提東西的彎度，忘了通知自己。"
            $ play_bgm("ending_handover", fade=2.5)

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_10_share_the_key


## ------------------------------------------------------------
## Section 10：把鑰匙分給心跳
## 不再修改 trust；依 S09 決定與既有 trust／s08_forced_walk 分流 A～D。
## ------------------------------------------------------------

label section_10_share_the_key:
    $ current_section = "s10"
    $ save_name = "Section 10｜把鑰匙分給心跳"

    if flags.get("gave_away", False):
        $ play_bgm("ending_handover", fade=2.0)
    elif trust >= 10 and not flags.get("s08_forced_walk", False):
        $ play_bgm("ending_back", fade=2.0)
    elif trust >= 4:
        $ play_bgm("ending_learning", fade=2.0)
    else:
        $ play_bgm("ending_thin_ice", fade=2.0)

    $ show_section_title("Section 10", "把鑰匙分給心跳")

    if flags.get("gave_away", False):
        scene bg alley_night
        with Dissolve(1.5)
        show yuan commute at char_center
        with dissolve

        "從咖啡廳走回公寓，經過他們第一次練習散步的那個轉角。樹影還在原來的位置，地上卻少了一條牽繩，提醒她該停下來。"
        "她走得比平常快。到家門口才意識到，今天完全不需要先確認腳邊，有沒有那個小小的重量跟著。"

        scene bg entrance_night
        with Dissolve(1.0)
        show yuan commute at char_right
        with Dissolve(0.4)

        "鑰匙插進鎖孔，門開得異常順。屋裡沒有水碗被撞得移位，也沒有爪子聽見門聲，從地板上蹦起來。"
        "予安把鞋脫好，照習慣留出靠牆那一小塊空間。做完才想起，現在沒有誰，需要從那裡繞過她。"
        "玄關的燈亮得太乾淨。以前她會先側身，讓出狗轉身要用的那道弧線；今晚那道弧空著，她反而站得渾身不對。"

        scene bg kitchen_night
        with Dissolve(0.9)
        show yuan commute at char_right
        with Dissolve(0.3)

        "她先去洗水碗。水龍頭開到一半，手停在半空。碗其實是乾淨的，早上才洗過兩次；她只是還沒準備好，把它收進櫥子。"

        scene bg living_night
        with Dissolve(1.0)
        show yuan commute at char_right
        with Dissolve(0.3)

        "牆上的掛勾原本留給牽繩。現在左邊只掛著鑰匙，右邊空得很誠實，黏膠的透明邊在燈下反光，格外顯眼。"
        "她把鑰匙取下又掛回去，金屬碰牆的聲音，比平常清楚了不只一點。"
        thought "原來少一個心跳，不是完全沒有聲音。"
        "手機還是沒有訊息。她告訴自己，抵達新家總需要時間；告訴自己第二次，她才承認，自己其實在等一張不是由她拍下來的、安全證明。"
        "她把外套掛好，袖口那道舊抓痕朝外。房間裡沒有誰會再聞它，她卻還是把抓痕，留在看得見的那一面。"
        if flags.get("coat_bed", False):
            "掛上去的那一刻，門邊那一夜的味道，還淡淡留著，捨不得散。"
        jump ending_ch1_handed_over
    else:
        scene bg street_night
        with Dissolve(1.5)
        show yuan commute at char_center
        with dissolve

        "回程經過生活用品店，予安在碗架前站了很久。第一個水碗其實還能用，她最後還是挑了一個尺寸相同、顏色不同的。"
        "店員問：「家裡養兩隻嗎？」她愣了半秒，搖頭。"
        ya "一隻。只是想多放一個。"
        "新的水碗被包進薄紙袋。提著走回家的路上，重量輕得幾乎沒感覺，卻比疫苗資料更像一個「不再是暫住」的決定。"
        "她也買了一排不用鑽牆的小掛勾。說明書寫承重兩公斤，掛鑰匙、牽繩都夠，也留了空間，給日後可能越來越多的東西。"
        $ flags["ch2_seed_hooks"] = True

        scene bg entrance_night
        with Dissolve(1.0)
        show yuan commute at char_right
        show dog parallel at dog_entrance_mid
        with Dissolve(0.5)

        "回到家，[dog_label]先在玄關聞了聞紙袋，再退半步，讓出她脫鞋的空間。"
        $ dog_sfx("soft")

        scene bg living_night
        with Dissolve(1.0)
        show yuan commute at char_right
        show dog parallel at dog_mid
        with Dissolve(0.4)

        "回到客廳，[dog_label]再退回熟悉的距離，看她把牆面擦乾，一臉監工的樣子。"
        "第一個掛勾貼歪了。予安撕下來重貼，黏膠因此弱了一點；第二次還是歪，她就決定不管了，讓它歪著。"
        ya "不是每件事都要對得很準。"
        "狗看著她和牆面來回較勁，耳朵一邊立著、一邊垂著，像在給分。"
        "她把鑰匙掛在左邊，牽繩掛在右邊。牽繩垂下來時，[dog_label]往後退了半步；等它徹底不動，才慢慢靠近聞了一次，確認是無害物品。"
        $ dog_sfx("sigh")

        scene bg kitchen_night
        with Dissolve(0.9)
        show yuan commute at char_right
        show dog kitchen_door at dog_mid
        with Dissolve(0.4)

        "新的水碗被放到舊碗旁邊。一個裝水，一個暫時空著。予安沒急著決定它以後要裝什麼，先讓「並排」這件事成立就好。"

        scene bg living_night
        with Dissolve(0.9)
        show yuan sofa at char_left
        show dog parallel at dog_mid
        with Dissolve(0.4)

        if flags.get("delayed_entry", False):
            "牠現在睡在客廳地板中央，不再只肯貼著玄關那一小塊磁磚。"
        if flags.get("s08_forced_walk", False):
            "牽繩垂著的那道弧度，讓她想起那天把一圈走完之後，離鞋還隔著一段距離的睡姿......計步器上的圓畫完了，身體的圓卻還沒閉上。"
            thought "原來那天走得太快，會一路走到今晚的距離。"
        "窗外的風把招牌吹得輕輕響。幾秒後，屋裡的燈忽然滅了。冰箱停止嗡嗡，客廳只剩窗外漏進來那一點灰藍，安靜得有點失禮。"
        "予安摸到手機，打開手電筒，沒把光直接照向狗。她先照地板，再把光圈收回自己腳邊，很有分寸。"
        if trust >= 10 and not flags.get("s08_forced_walk", False):
            jump ending_ch1_back_to_back
        elif trust >= 4:
            jump ending_ch1_chosen_learning
        else:
            jump ending_ch1_thin_ice


label ending_ch1_back_to_back:
    $ save_name = "結局 A｜背靠"
    $ flags["ch1_ending"] = "back_to_back"
    $ flags["gave_away"] = False
    $ process_ending_unlock("A", trust)
    $ record_trust_trajectory()

    "[dog_label]在黑暗裡抬起頭，先看窗外，再看地板上那圈光。牠沒有衝向門，也沒鑽進桌底，只把鼻子伸進光圈邊緣聞了一下，像在確認警報等級。"
    "予安坐到地板上。手機放在膝邊，光從下方照亮牆上的鑰匙與牽繩，兩道影子疊在一起，難得合拍。"
    $ play_bgm("hopeful", fade=2.2)
    ya "我們再試一年。"
    thought "一年後，再說下一年。"
    "她沒有伸手叫牠過來，只把背靠上沙發，讓自己變成房間裡，唯一不會突然移動的東西。"
    show dog drink_bowl at dog_mid
    with Dissolve(0.7)
    "[dog_label]先走到水碗旁。新碗反射了一點手電筒的光，牠聞過邊緣，喝了兩口，再沿著牆走回來，路線精準。"
    show dog halfstep at dog_near
    with Dissolve(0.9)
    pause 0.6
    "走到予安腿邊時，牠停了很久，久到她幾乎以為牠會回頭選那塊安全的、兩步遠的地板。"
    show dog back_sleep at dog_near
    with Dissolve(1.0)
    pause 0.5
    "[dog_label]在伸手可及的地方轉了一圈，最後背對她躺下。耳朵鬆著，最沒有防備的那一側，朝向整個房間。"
    "她沒有立刻伸手。只把掌心懸在兩個呼吸之間，等牠自己先睡沉。"
    "停電讓所有電器都安靜下來。予安第一次聽清楚牠睡著後的呼吸：吸氣短一點，吐氣長一點，偶爾鼻尖碰到地板，發出很小的聲音。"
    "她把外套從沙發拉下來，蓋在自己腿上。衣角離狗的背只剩半掌寬，她還是沒有跨過那條線。"
    "過了一會兒，[dog_label]在夢裡動了一下，背脊碰上衣角。牠沒有醒，也沒有把身體移開，算是默許。"
    "予安看著牆上那排歪了一點的掛勾，沒有拍照。有些畫面不需要先證明給誰看，才算真的發生過。"
    "電力恢復時，冰箱重新嗡了一聲。狗的耳朵動了動，背，依然朝著她。"
    "那一晚，她在地板上睡得腰有點痛。醒來時，手掌還停在原處，沒有趁牠睡著偷摸一把。"
    "隔天鬧鐘響起，她伸手拿起鑰匙。"
    "牽繩被鑰匙帶得輕輕晃。[dog_label]睜開眼，從地板看她穿鞋，卻沒有把身體挪回門邊守著。"
    ya "晚上見。"
    "狗抬了一下耳朵，沒有起身確認。門會關，也會再打開......這件事，牠此刻決定交給她處理。"
    "傍晚，鑰匙聲再次落在門外。[dog_label]仍趴在原位，只用尾巴輕輕碰了一下地板，算是打卡。"
    "予安進門後先把鑰匙掛好。她沒有叫牠迎接；被相信會回來，已經是今天最安靜、也最貴重的歡迎。"
    ## 節拍動畫 → 標題卡 → 解鎖提示 → aftercare
    call ending_coda_finish("A", "結局 A｜背靠", "背靠很暖。門會關，也會再打開。")
    return


label ending_ch1_chosen_learning:
    $ save_name = "結局 B｜選定但還在學"
    $ flags["ch1_ending"] = "chosen_learning"
    $ flags["gave_away"] = False
    $ process_ending_unlock("B", trust)
    $ record_trust_trajectory()

    "黑暗裡，[dog_label]先退到沙發另一側。手機的手電筒亮起時，牠瞇了一下眼，視線緊緊跟著那圈移動的光，像盯哨。"
    "予安把手機平放到地板，沒拿光去追牠。她在離狗兩步的位置坐下，跟他們第一次共享客廳時，一樣的距離。"
    ## 與結局 A 對稱：承諾「再試一年」切 hopeful（first-light）
    $ play_bgm("hopeful", fade=2.2)
    ya "我們再試一年。"
    "這句話不像是在承諾永遠，更像先把明天預留一個座位。"
    "狗站著聽了一會兒。牠先去聞新水碗，金屬邊被鼻尖碰出輕響，退了半步，又湊回去聞第二次，謹慎得像在驗貨。"
    "予安笑了一下，沒有說「你看，沒什麼好怕」。對牠來說，光是敢靠近第二次，已經很忙了。"
    "她把外套鋪在沙發旁。不是圈出一塊非睡不可的地方，只是讓地板多一處，聞起來還算熟悉的位置。"
    show dog check_sleep at dog_mid
    with Dissolve(1.0)
    if flags.get("s08_forced_walk", False):
        "[dog_label]在沙發旁睡下，距離比以前近，卻仍留著半步的餘地。牠背過身一會兒，又睜眼回頭，確認她還坐在原處......像那天把一圈路走完之後，還在等自己的身體跟上腳步。"
        thought "那天我把路走完了。今晚牠把背轉過來，又轉回去看我。"
    else:
        "[dog_label]在沙發旁睡下，距離比以前近了。牠背過身一會兒，又睜眼回頭，確認她確實還坐在原處。"
    ya "我在。"
    "牠重新把下巴放回前腳。信任從來不是一次到位，今晚只是少確認了一回。"
    "窗外有車燈掃過天花板。狗又抬頭，予安沒有立刻安撫，只是留在原位，讓同一個人、同一個氣味、同一塊地板，替她把答案說出來。"
    "確認完門沒有開、她也沒有消失，牠第三次把頭放下。這次眼睛閉得，比前兩次都快。"
    "電力恢復後，電視待機燈亮起一個小紅點。[dog_label]看了一眼，沒有換回靠門那個舊位置。"
    "予安替自己倒水，也替新碗添了一點。兩個碗並排時發出輕響，狗的耳朵動了一下，身體仍留在外套邊，沒被聲音收買。"
    "她在沙發上睡著前，看見牠又回頭一次。她沒有覺得前功盡棄，只是低聲又說了一遍：「我在。」"
    "後半夜，確認變成偶爾才做的事。每一次間隔，都比前一次拖得更長一點。"
    "隔天鬧鐘響起。予安拿起鑰匙，牽繩在旁邊輕輕晃了一下。"
    "[dog_label]站起來跟到玄關，在門線前停住。予安穿鞋時，牠看了門外一眼，又轉頭看她。"
    ya "晚上見。"
    "狗看著她，沒有跟到門外。這已經算是一種選定；剩下的部分，他們可以慢慢學。"
    "傍晚，她開門時，[dog_label]先在原地確認了兩秒，才慢慢走到玄關一半。"
    "予安蹲下，卻沒有伸手。剩下那一半距離，不需要今晚就走完。"
    call ending_coda_finish("B", "結局 B｜選定但還在學", "選定了，卻還在把身體學回來。")
    return


label ending_ch1_handed_over:
    $ save_name = "結局 C｜送走之後"
    $ flags["ch1_ending"] = "handed_over"
    $ flags["gave_away"] = True
    $ process_ending_unlock("C", trust)
    $ record_trust_trajectory()

    "夜裡短暫停電。冰箱的嗡嗡忽然停下，房間裡連一個能填補空白的聲音，都沒有了。"
    "予安打開手機手電筒，習慣性先照地板，怕光直接落進一雙敏感的眼睛。光圈移出去半公尺，她才想起，這裡已經不用再避了。"
    "她把手機立在水杯旁。牆上只剩鑰匙，右邊那個空掛勾，投下一小段孤單的影子。"
    "新的水碗沒有買。原本那個還放在廚房門口，裡面的水，維持在早上出門前的高度，沒人動過。"
    "予安端起水碗走向水槽，走到一半又放回原處。她分不清這是在整理，還是太急著替這間屋子，宣布已經結束。"
    "手機亮起。同事傳來一張照片：[dog_label]趴在新家的門邊，水碗放得很遠，門留著一條縫。"
    coworker "牠有喝水。還在找能看見門的位置。我會等。"
    "照片裡的地板不是她家的顏色。狗的姿勢卻熟悉得不得了：背朝走廊，臉朝門，四隻腳收得隨時能站起來，隨時準備跑。"
    "她把照片放大，看見紙袋裡那件舊外套露出一角。同事沒把它洗掉，也沒急著換成比較新的墊子......這個細節，比任何保證都可靠。"
    if flags.get("landmark_chose_reason_over_bond", False):
        "關係最好的時候放手......照片裡那條門縫，反而比她家的空掛勾，更像一句沒說完的話。"
        thought "理由排得越整齊，胸口那塊越說不清楚。"
    "予安打了「牠晚上可能會叫」，又刪掉。打了「如果真的不行」，也刪掉。最後只送出一句「謝謝」，比原本想說的短得多。"
    "對話框上方很快顯示已讀。沒有更多保證，也沒有哪句話，能把適應期直接縮短。"
    "她坐在地板上，背靠沙發。以前這個高度會看見狗的耳朵或鼻尖；現在只看見手機的光，把灰塵照得清清楚楚。"
    ya "今天先這樣。"
    "聲音仍然很輕。不是說給誰聽的，卻也沒有因此變得沒有意義。"
    "電力恢復時，她終於把水碗裡的水倒掉，洗乾淨，放進櫥櫃最下層。門沒有關緊，照樣留著一條縫。"
    "她沒有再替這個選擇找名字。想念還在，理由也還在；兩件事並排放著，誰都沒有贏過誰。"
    "隔天鬧鐘響起，她伸手拿起鑰匙。"
    "右邊的空掛勾被鑰匙碰了一下，輕輕搖著。她伸手按住，等它徹底靜下來。"
    ya "晚上見。"
    "話說出口後，房間裡沒有誰回頭。她站了一秒，才把門關上。"
    "往後如果還想靠近，大概得隔著另一扇門，重新慢慢學一次。"
    "三天後，同事又傳來照片：[dog_label]睡在離新家房門兩步遠的地方，舊外套仍墊在身下，沒被換掉。"
    "予安回了一個「收到」。她沒有要求更多證明，只把那張照片，收進一個她再也不會更新的相簿。"
    call ending_coda_finish("C", "結局 C｜送走之後", "想念還在，理由也還在。")
    return


label ending_ch1_thin_ice:
    $ save_name = "結局 D｜薄冰同住"
    $ flags["ch1_ending"] = "thin_ice"
    $ flags["gave_away"] = False
    $ process_ending_unlock("D", trust)
    $ record_trust_trajectory()

    "黑暗落下時，[dog_label]立刻回到門邊。背貼著牆，頭朝出口，手機的光才亮起，眼睛就跟著縮了一下。"
    "予安把光轉向自己，不照牠。她在客廳中央停住......選擇留下，不代表這間屋子裡每一段距離，都自動變成她的。"
    "她留下了。還沒學會的事，今晚照樣攤在客廳地板上，一件都沒少。"
    ya "我們再試一年。"
    "她說得很輕，沒有要求房間裡的另一個心跳立刻相信。"
    "狗沒有靠近。牠聞到牆上新掛的牽繩時，鼻尖只動了一下，便把視線轉回門鎖，比較關心那個。"
    "予安把第二個水碗裝好，放在離第一個碗更遠的位置。兩條路都能喝到水，都不用經過她腳邊。"
    "她坐回沙發，手機光朝下。停電讓房間變得陌生，狗選擇最靠近出口的位置；她沒把這個選擇解讀成拒絕。"
    show dog door_edge at dog_far
    with Dissolve(1.0)
    "[dog_label]睡在靠門的位置，身體朝著出口，眼睛閉得很淺。牽繩掛好了，兩人之間仍隔著一段，沒辦法假裝不存在的距離。"
    "予安把手收回膝上。今晚不追。明天也不打算拿「已經留下」，去要求牠靠近。"
    "樓上有人拖動椅子，狗立刻睜眼。予安也抬頭，卻沒有走過去抱住牠。她只是把自己的呼吸放慢，留在原位不動。"
    ya "是樓上的聲音。"
    "牠聽不懂聲音的來源，但聲音結束後，她沒有靠近，門也沒有打開。過了很久，牠才重新把下巴放回前腳。"
    "電力恢復，冰箱啟動。狗又醒了一次。這回牠只是抬眼，沒有站起來，算是給了個台階。"
    "予安把新水碗往牆邊推近一點，再退回沙發。每個動作都讓牠看得清清楚楚，不趁轉身縮短距離耍花招。"
    "那一夜沒有背靠，也沒有突然的原諒。只有兩個睡得都不深的生命，隔著客廳，慢慢確認對方沒趁黑暗偷改規則。"
    "清晨，她醒來時，[dog_label]仍在門邊，身體卻不再完全貼著牆。牠替自己留的那道縫，比昨晚少了一點點。"
    "隔天鬧鐘響起，她伸手拿起鑰匙。"
    "她穿鞋時沒有叫狗的名字，只把牽繩扶穩，不讓它因鑰匙晃動而敲到牆。"
    ya "晚上見。"
    "狗沒有看她。耳朵卻在門闔上前動了一下。薄冰沒有忽然變厚，但他們，還都站在這一邊。"
    "傍晚回家，水碗少了一點水。[dog_label]仍守在門邊，身體卻沒有因鑰匙聲立刻站起來，反應慢了半拍。"
    "予安把鞋放好，退到牠看得見的位置。今天沒有靠近，只比昨天少驚動了一次，進度緩慢但存在。"
    call ending_coda_finish("D", "結局 D｜薄冰同住", "薄冰沒有忽然變厚，但他們都還站在這一邊。")
    return


## ------------------------------------------------------------
## 結局後：鼓勵重玩（gamer_30｜選擇要有可感知回聲）
## ------------------------------------------------------------

label ending_aftercare:
    $ sync_unlocked_ending_rewards()
    $ renpy.save_persistent()

    if flags.get("ch1_ending") == "chosen_learning":
        if flags.get("s08_forced_walk", False):
            "那天把整整一圈走完，今晚還是會回頭確認......選定了，身體卻還在慢慢學。"
        else:
            "這大概是很多人第一次留下時，會有的溫度......選定了，卻還在學。"
    elif flags.get("ch1_ending") == "back_to_back":
        "背靠很暖。若想看更接近日常養寵的溫度，結局 B〈選定但還在學〉也值得一看。"
        if secret_photo_unlocked("lap_sleep"):
            "有一段畫面，只有真正把背交給彼此之後才看得到......可在「結局一覽」打開紀念照片與結局靜幀。"
            "狗的日記、予安心境與朋友視角，也已寫進主選單「隱藏內容」。"
    elif flags.get("ch1_ending") == "handed_over":
        if flags.get("landmark_chose_reason_over_bond", False):
            "在關係最好的時候把牽繩交出去......那股酸，比失敗更難跟別人解釋清楚。"
        else:
            "送走不是被判失敗。不同的選擇會改變睡姿與那個空掛勾......想再看一次，留下之後會是什麼距離嗎？"
    else:
        "薄冰同住很誠實。若想看信任怎麼一點點長出來，結局 B 常被推薦當作第一次。"

    "不同的選擇，會改變狗的距離與睡姿。想再試另一條路嗎？"
    menu:
        "回主選單":
            $ renpy.save_persistent()
            return

        "查看已解鎖結局":
            $ sync_unlocked_ending_rewards()
            call screen ending_gallery
            jump ending_aftercare

        "查看隱藏內容":
            $ sync_unlocked_ending_rewards()
            call screen hidden_content_gallery
            jump ending_aftercare

        "從 Section 09 再試一次（留下或送走）":
            jump start_section_09

        "從頭開始":
            jump start
