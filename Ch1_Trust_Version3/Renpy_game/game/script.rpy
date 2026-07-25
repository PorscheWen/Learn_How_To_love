## Version3｜Ch1 Trust
## Section 01：螢幕光比月亮亮
## Section 02：後門那一瞥
## Section 03：大門的臨時國界
## Section 04：共享同一種安靜
## Section 05：你的聲音有兩種
## Section 06：走廊上的第三者
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


init python:
    def optional_displayable(path, fallback):
        """正式資產存在時使用；否則回傳 fallback。"""
        if renpy.loadable(path):
            return path
        return fallback

    # 立繪來源高度混雜（1536／2048），先歸一化再交給 char_*／dog_* transform。
    # 畫面定位：腳底落在字幕框上方（約 ypos 0.85），水平靠中；transform zoom 為基線 ×1。
    CHAR_REF_H = 1280.0   # char_right zoom 0.50 → 畫面高約 640px
    DOG_REF_H = 1536.0    # dog_near zoom 0.34 → 歸一化後再乘距離 zoom

    def scaled_sprite(path, fallback, ref_h):
        if renpy.loadable(path):
            w, h = renpy.image_size(Image(path))
            return Transform(path, zoom=ref_h / float(h))
        if isinstance(fallback, str) and renpy.loadable(fallback):
            return scaled_sprite(fallback, Solid("#00000000"), ref_h)
        return fallback

    def char_sprite(path, fallback=Solid("#00000000")):
        return scaled_sprite(path, fallback, CHAR_REF_H)

    # 兩批狗圖留白差異大：高畫布（1024x1536）狗身只佔 42～47%，
    # 方形畫布（1024x1024）狗身佔 83～98%，同 transform 會放大近一倍。
    # 以 S02 高畫布那批為基準，依「站姿≈0.45、臥姿≈0.34」的內容高度修正。
    DOG_POSE_SCALE = {
        "dog/dog-halfstep.png": 0.46,
        "dog/dog-stair-watch.png": 0.46,
        "dog/dog-leash-wait.png": 0.49,
        "dog/dog-kitchen-door.png": 0.49,
        "dog/dog-guard-door.png": 0.52,
        "dog/dog-behind-legs.png": 0.48,
        "dog/dog-sniff-wire.png": 0.52,
        "dog/dog-parallel.png": 0.40,
        "dog/dog-shoe-sleep.png": 0.41,
        "dog/dog-back-sleep.png": 0.39,
        "dog/dog-check-sleep.png": 0.35,
        "dog/dog-door-edge.png": 0.36,
        "dog/dog-door-sleep.png": 0.37,
    }

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
        """依 audio.md 掛載 BGM。別名可帶音量（tense = calm @0.88）。"""
        aliases = {
            "blank_night": ("audio/calm.ogg", 1.0),
            "calm": ("audio/calm.ogg", 1.0),
            "warm": ("audio/warm.ogg", 1.0),
            "tender": ("audio/tender.ogg", 1.0),
            "melancholy": ("audio/melancholy.ogg", 1.0),
            "night": ("audio/calm.ogg", 0.93),
            "stair_border": ("audio/calm.ogg", 1.0),
            "gate_border": ("audio/calm.ogg", 1.0),
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
        store._current_bgm = profile
        playing = renpy.music.get_playing(channel="music")
        if playing != filename:
            renpy.music.play(
                filename,
                channel="music",
                loop=True,
                fadein=fade,
                if_changed=True,
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
        if photo_id == "lap_sleep":
            if ending_unlocked("A"):
                return True
            ## 相容舊 id back_to_back
            return "lap_sleep" in unlocked or "back_to_back" in unlocked
        return photo_id in unlocked


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
## 結局 A 隱藏紀念照（中型幼犬躺大腿特寫）；僅 gallery／aftercare 顯示
image gallery secret_lap_sleep = optional_background(
    "gallery/secret-lap-sleep.png", "#211913"
)
image bg backdoor_night = optional_background(
    "bg/bg-backdoor-night.png", "#131A22"
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
image bg corridor_day = optional_background(
    "bg/bg-corridor-day.png", "#A99B8B"
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
image yuan commute = char_sprite("char/char-yuan-commute.png")
image clerk stand = char_sprite("char/char-clerk.png")
image yuan block = char_sprite(
    "char/char-yuan-block.png", "char/char-yuan-commute.png"
)
image neighbor stand = char_sprite("char/char-neighbor.png")
image yuan leash = char_sprite(
    "char/char-yuan-leash.png", "char/char-yuan-commute.png"
)
image coworker stand = char_sprite(
    "char/char-coworker.png", "char/char-neighbor.png"
)

image dog anxious = dog_sprite("dog/dog-anxious.png")
image dog halfstep = dog_sprite("dog/dog-halfstep.png")
image dog stair_watch = dog_sprite(
    "dog/dog-stair-watch.png", "dog/dog-anxious.png"
)
image dog door_sleep = dog_sprite(
    "dog/dog-door-sleep.png", "dog/dog-anxious.png"
)
image dog parallel = dog_sprite(
    "dog/dog-parallel.png", "dog/dog-halfstep.png"
)
image dog kitchen_door = dog_sprite(
    "dog/dog-kitchen-door.png", "dog/dog-halfstep.png"
)
image dog ear_flat = dog_sprite(
    "dog/dog-ear-flat.png", "dog/dog-anxious.png"
)
image dog sniff_wire = dog_sprite(
    "dog/dog-sniff-wire.png", "dog/dog-halfstep.png"
)
image dog behind_legs = dog_sprite(
    "dog/dog-behind-legs.png", "dog/dog-anxious.png"
)
image dog forehead_nudge = dog_sprite(
    "dog/dog-forehead-nudge.png", "dog/dog-halfstep.png"
)
image dog guard_door = dog_sprite(
    "dog/dog-guard-door.png", "dog/dog-door-sleep.png"
)
image dog street_tense = dog_sprite(
    "dog/dog-street-tense.png", "dog/dog-anxious.png"
)
image dog leash_wait = dog_sprite(
    "dog/dog-leash-wait.png", "dog/dog-halfstep.png"
)
image dog shoe_sleep = dog_sprite(
    "dog/dog-shoe-sleep.png", "dog/dog-parallel.png"
)
image dog refuse_stranger = dog_sprite(
    "dog/dog-refuse-stranger.png", "dog/dog-ear-flat.png"
)
image dog back_sleep = dog_sprite(
    "dog/dog-back-sleep.png", "dog/dog-shoe-sleep.png"
)
image dog check_sleep = dog_sprite(
    "dog/dog-check-sleep.png", "dog/dog-parallel.png"
)
image dog door_edge = dog_sprite(
    "dog/dog-door-edge.png", "dog/dog-door-sleep.png"
)


# 腳底錨在字幕框上緣附近（720×108 → y≈0.85），水平靠中；zoom 為基線 ×1。
transform char_center:
    xalign 0.50
    yanchor 1.0
    ypos 0.85
    zoom 0.52

transform char_right:
    xalign 0.70
    yanchor 1.0
    ypos 0.85
    zoom 0.50

transform char_left:
    xalign 0.30
    yanchor 1.0
    ypos 0.85
    zoom 0.50

# 狗的距離＝畫面上的信任條：near／far 之間用移動表達，不顯示數字。
transform dog_far:
    xalign 0.58
    yanchor 1.0
    ypos 0.85
    zoom 0.26

transform dog_mid:
    xalign 0.50
    yanchor 1.0
    ypos 0.85
    zoom 0.30

transform dog_near:
    xalign 0.44
    yanchor 1.0
    ypos 0.85
    zoom 0.34

# 人＋狗同框：人在右（char_right≈0.70），狗在人左側／腿後，勿貼到左側陌生人身上。
transform dog_far_pair:
    xalign 0.48
    yanchor 1.0
    ypos 0.85
    zoom 0.22

transform dog_mid_pair:
    xalign 0.54
    yanchor 1.0
    ypos 0.85
    zoom 0.24

transform dog_near_pair:
    xalign 0.60
    yanchor 1.0
    ypos 0.85
    zoom 0.26

# 玄關：地墊在門前偏中，避免狗貼進門板。
transform dog_entrance_far:
    xalign 0.50
    yanchor 1.0
    ypos 0.86
    zoom 0.24

transform dog_entrance_mid:
    xalign 0.52
    yanchor 1.0
    ypos 0.86
    zoom 0.27

# S08 巷口散步：仍拉開一人一狗，整體靠中、腳底清字幕。
transform char_right_walk:
    xalign 0.70
    yanchor 1.0
    ypos 0.85
    zoom 0.42

transform dog_far_walk:
    xalign 0.28
    yanchor 1.0
    ypos 0.85
    zoom 0.24

transform dog_mid_walk:
    xalign 0.38
    yanchor 1.0
    ypos 0.85
    zoom 0.27

transform dog_near_walk:
    xalign 0.46
    yanchor 1.0
    ypos 0.85
    zoom 0.30


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
    $ renpy.music.stop(channel="music", fadeout=0.4)
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
    $ trust = 7
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

    "週四深夜。予安關掉簡報最後一頁的動畫，游標在「儲存」上停了半秒——像怕點下去，就會有下一個檔案冒出來。"
    "辦公室只剩冷氣的風聲，輕輕的，像沒人記得關。她戴上耳機，白噪音，選了雨聲那一軌；其實外面沒有下雨。"

    "電梯往下跳，她數：十四、十三、十二。"
    thought "數字比想明天的會議安全。"

    scene bg convenience_night
    with dissolve

    show yuan commute at char_right
    show clerk stand at char_left
    with dissolve

    "便利商店門一開，冷氣撞上來。她走向微波櫃，便當盒上的透明膜起了一層霧。"

    clerk "小姐，要加水嗎？"
    ya "不用，謝謝。"

    "尾音收得乾淨——上班的聲音。"
    "她已經很久沒用另一種：句子講一半、會拖長、對著空氣自言自語的低聲。"
    "一個人住久了，低聲那一軌像很少播放的歌。"

    "微波「叮」的一聲。她正要結帳，店員把關東煮湯汁擦掉一滴，忽然像想起什麼。"

    clerk "對了，小7 今天好像沒力氣跑了。"
    ya "嗯？"

    clerk "後門那隻狗啊。我們都叫牠小7——老待在卸貨區。"
    clerk "瘦瘦的。前幾天還會晃到騎樓，今天丟垃圾，牠幾乎沒站起來。我跟店長講了，明天再看要不要叫人來。"

    ya "喔。"
    "標準的「喔」。不承諾、不追問、剛好夠禮貌。"

    hide clerk
    with dissolve

    scene bg street_night
    with dissolve

    show yuan commute at char_center
    with dissolve

    "她提袋出門。夜風從袖口鑽進去。巷口路燈把柏油路照成淺黃，機車一台一台睡死在格子裡。"
    "後門在另一側——卸貨區、壓扁紙箱、濕紙箱混隔夜油的氣味。"
    "這條路她走了兩年，轉角永遠只是轉角。"
    "腳在轉角前慢了半拍。只有半拍。"

    menu:
        "繞去看一眼":
            $ flags["peeked_backdoor"] = True
            "她告訴自己，只看一眼，不算答應什麼。"
            "她繞到轉角邊。卸貨區的燈壞了一盞，紙箱在陰影裡疊成模糊的形狀。深處像有什麼動了一下，也可能只是塑膠袋被風吹過。"
            "她沒有走近。站了兩秒，便轉回原路。"
            thought "便當會涼。"

        "照原路回家":
            $ flags["peeked_backdoor"] = False
            thought "便當會涼。便當真的會涼。"
            "她沒轉進去。步伐穩得像設定好的導航。"

    "耳機裡的雨還在下，她忽然覺得吵，把音量轉小。"
    "世界變大：遠處的狗叫、樓上電視、自己的呼吸。"

    scene bg living_night
    with dissolve

    show yuan commute at char_right
    with dissolve

    "公寓門「嘀」一聲。冰箱低沉的嗡嗡，像有人在廚房輕輕唸經。"
    "她坐在沙發邊緣吃便當，電視沒開，螢幕黑著比較省事。"

    "吃到一半，手機亮起。備忘錄的搜尋建議浮出一筆三個月前的舊項目：「週六十點，動保處——帶租約影本。」"
    "日期已經灰掉，後面沒有完成的勾。她盯了兩秒，把通知往旁邊滑掉。"
    "店員那句「幾乎沒站起來」卻還掛在耳朵邊，像沒撕乾淨的標價貼紙。"

    "她打開冰箱。"
    "門上的冷光落在腳邊。她盯著那塊空地，忽然想到：如果真把什麼帶回來，牠會待在哪裡？"
    "念頭才成形，她便把冰箱門關上。冷氣的嗡聲停了一瞬，整間屋子顯得更安靜。"
    thought "我連自己都常常忘記吃晚餐。"

    "手機搜尋框裡，她打了「路邊 小狗 沒力氣」。建議結果跳出脫水、失溫、通報電話。"
    "她沒有點進去。手指停在刪除鍵上，一個字一個字退回空白，像沒有搜尋過就不必負責。"
    "幾秒後，她又把通報電話抄在那筆舊備忘下面。只抄號碼，沒有寫用途，也沒有改掉過期的日期。"

    ya "不要。"
    "聲音很輕，像怕被自己聽見。"

    "上床前，手機最後亮一次：明天十點開會、週五要交的檔。"
    "她點開備忘，打了幾個字又刪掉。刪掉的是：「明天如果還在——」"

    thought "還在什麼。"

    hide yuan
    with dissolve

    "意識往下沉。腳步聲在想像裡又走一遍：便利商店、微波的叮、那個「喔」、沒有走近的轉角。"
    "予安睡著了。窗外月亮大概還在，只是今晚螢幕光先贏了。"
    "而那隻她沒有去看的狗，是否還趴在後門陰影裡——這個問題，被她很成功、也很短暫地，留在了夢的外面。"

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

    # —— 進場畫面 ——
    scene bg convenience_night
    with Dissolve(1.2)

    $ show_section_title("Section 02", "後門那一瞥")

    "週五傍晚。予安還是最後一批關螢幕的人。簡報交出去了，身體卻像還欠一份存檔。"
    "耳機掛在脖子上，這次沒開白噪音——外面有真的風。"

    show clerk stand at char_left
    with dissolve

    clerk "小姐，小7 還在。"
    "說得很快，像怕自己太關心。"
    clerk "後門那隻。店長說動保明天才排得到。你要是……算了，當我沒說。"

    ya "喔。"
    "比昨晚短半拍。"

    hide clerk
    with dissolve

    "她提便當到巷口。轉角在左邊——兩年來從不轉進去的那個轉角。"

    if flags["peeked_backdoor"]:
        "昨晚繞過去看過一眼。此刻腳步比較穩，像赴一個沒說出口的約。"
    else:
        "昨晚沒有繞過去。轉角突然變得很近，近得像地板自己往前送了一步。"

    "她轉進去了。"

    scene bg backdoor_night
    with Dissolve(1.5)

    "卸貨區比想像窄。機車棚陰影把地面切成深淺。垃圾桶邊壓扁的紙箱翹著邊角。"
    "氣味是濕紙箱混隔夜油，還有一點點體溫味，淡到幾乎像錯覺。"

    "然後她看見了。"

    show dog anxious at dog_far
    with Dissolve(1.2)
    pause 0.7

    "不是那種擺出來給人看的棄養。沒有綁絲帶、沒有紙條、沒有「請好心人收留」。"
    "一隻瘦的混種幼犬趴在紙箱邊。毛質略硬亂，毛色偏蜂蜜褐，耳尖較深，胸口一塊髒掉的奶油白。短腿、偏瘦，肋骨在呼吸裡一下一下顯出來。"

    "予安停在兩步外。手還提著便當袋，指節沒有收緊，也沒有伸出去。"
    "狗的鼻子動了。便當袋、鞋底、她垂在身側的手指。鼻尖往前一點，又縮回紙箱陰影。"
    "眼睛圓、深褐、亮得不太公平——在這種地方，不該有這麼亮的東西。"

    "她先眨眼。"
    "狗先看開。耳尖微微一顫，視線落到水泥縫。"
    pause 0.9
    "那半秒裡，世界很安靜。安靜到她聽見自己吞口水的聲音。"

    # —— 關鍵動作（距離 Dist）— 本段唯一動 trust 的選項組 ——
    menu:
        "蹲下，側身等待（不伸手）":
            $ trust += 1
            $ dist += 1
            $ flags["dist_ok"] = True
            $ flags["s02_conscience_return"] = False
            "予安把便當袋放到地上，慢慢蹲下。膝蓋輕響一聲。她側著身，讓自己看起來小一點。"
            show dog anxious at dog_far
            with Dissolve(0.4)
            "狗往後縮半步，屁股碰紙箱，沙沙響。前爪扒住箱緣，像隨時要鑽回去。"
            "她沒追。掌心朝上，停在膝蓋外，什麼都沒伸。"
            ya "嚇到了嗎。"
            "開會時那種尖銳的語氣收不回來，獨處時放軟的低聲還不熟，擠出來只有這一句。"
            "她掀開便當蓋，用筷子挑出一點白飯，放在掌心外的地上——離自己遠，離狗近。手收回來，停在空氣裡。"
            pause 0.6
            $ play_bgm("tender", fade=2.5)
            show dog halfstep at dog_mid
            with Dissolve(1.0)
            $ dog_sfx("soft")
            "狗靠近。停。再靠近。舌尖點了一下米粒，又點一下。每吞一口就抬眼看她。"
            "她的手指動了一下，又收回袖口。"
            thought "我可以什麼都不做。"

        "直接伸手抱／抓":
            $ trust -= 1
            $ dist -= 1
            $ flags["dist_ok"] = False
            $ flags["s02_conscience_return"] = False
            "她沒等。手臂伸過去。"
            pause 0.4
            show dog ear_flat at dog_far
            with Dissolve(0.3)
            $ dog_sfx("whimper")
            "狗整隻縮成一團，喉嚨裡擠出一聲短促的嗚。爪子在她袖口抓出淺痕。"
            "懷裡那團溫度硬得像一塊石頭，掙得她差點抓不住。"
            "她只好先放回紙箱邊。"
            show dog anxious at dog_far
            with Dissolve(0.6)
            "狗貼著紙箱，肩膀一下一下抖。耳朵貼平，鼻尖轉向陰影，不看她。"
            thought "抱到了。可是好像哪裡不對。"

        "拍腿趕開，轉身就走":
            $ trust -= 1
            $ dist -= 1
            $ flags["dist_ok"] = False
            $ flags["s02_conscience_return"] = True
            "她拍了拍腿，發出趕貓趕狗的嘖聲。"
            show dog ear_flat at dog_far
            with Dissolve(0.4)
            $ dog_sfx("murmur")
            "狗縮回紙箱深處，只剩尾巴尖露在外面。紙箱邊角輕輕顫了一下。"
            hide dog
            with Dissolve(0.5)
            "她轉身。走了五步。"
            pause 0.8
            "第六步停住。"
            thought "牠幾乎沒站起來——店員是這樣說的。"
            $ trust += 1
            "她轉回去。"
            show dog anxious at dog_far
            with Dissolve(0.8)
            "狗還在原地，眼睛在陰影裡亮著，像在等一個重播。"
            "這次她蹲下來，什麼都不做。膝蓋輕響，手貼在自己腿側。"
            $ play_bgm("tender", fade=2.5)
            show dog halfstep at dog_mid
            with Dissolve(1.0)
            "很久，狗的鼻子重新伸出來一點。停在紙箱邊，不再後退，也不再靠近。"

    # —— 反應鏡頭 ——
    "「動保明天才來。」她對狗說，也對自己說。「明天。」"
    "明天兩個字在巷子裡彈了一下，就消了。"

    if flags["dist_ok"]:
        show dog halfstep at dog_mid
        with Dissolve(0.6)
        "狗往前半步，停在「既不碰你、也不放你走」的距離。尾巴不搖，輕貼腿側。"
        pause 0.6
        "予安站起來，往後退一步——測試。"
        "狗跟著往前半步，停在她舊鞋印的位置。"
        "她再退。狗不再跟，只盯著腳踝，像怕腳踝長出另一雙鞋。"
    elif flags.get("s02_conscience_return", False):
        show dog halfstep at dog_mid
        with Dissolve(0.6)
        "狗留在紙箱邊，鼻尖卻沒有再縮回陰影。那半步很小，像只肯把回頭這件事記下一半。"
        pause 0.6
        "予安站起來，往後退一步。"
        "狗沒跟，只抬起鼻尖追著她的鞋印。距離還在，但不再像一道關上的門。"
    else:
        show dog anxious at dog_far
        with Dissolve(0.6)
        "狗往前一點，又縮回去，停在「既不碰你、也不放你走」的距離外緣。"
        pause 0.6
        "予安站起來，往後退一步。"
        "狗沒跟。只把下巴壓低，盯著她的鞋尖，肩膀還緊。"

    "店員從騎樓探頭：「小姐？要不要我幫你打給——」"
    ya "我知道了。我……先處理。"
    "語氣比較低、比較慢。不是客服音，像對自己下指令。"

    # ▷ 路徑選擇（風味為主；少動 trust）
    menu:
        "留地址，等動保明天":
            $ flags["called_shelter"] = True
            "她跟店員留了電話和地址，說如果明天動保來得早，先通知她。"
            "說完才發現，自己已經把「這件事」變成「我的事」。"

        "先帶去夜間急診":
            $ flags["vet_first"] = True
            "她查了最近的夜間動物醫院。掛號費比一個便當貴四倍。"
            "指尖在螢幕上停了一秒，按下「導航開始」。"
            if flags["dist_ok"]:
                $ trust += 1

        "先帶到公寓大門過一夜":
            $ flags["gate_night"] = True
            "只是大門口。不是家裡。她先跟自己談好條件。"
            if flags["dist_ok"]:
                $ trust += 1

    if not flags["dist_ok"] and not flags.get("s02_conscience_return", False):
        $ play_bgm("melancholy", fade=2.0)

    "予安看著那隻狗。狗看著便當袋，又看她的臉，最後看向巷口——車燈一掃而過，像有人用很大的手在翻書。"
    ya "今晚不算數。"
    "聲音輕得像怕被巷子聽見。"

    "她把空便當盒收進袋子，留一點水在瓶蓋裡推過去。"
    if flags["dist_ok"]:
        show dog halfstep at dog_mid
        with Dissolve(0.5)
        "狗嗅了嗅，喝了兩口。水聲很小，舌尖一下一下點著瓶蓋邊緣。"
    elif flags.get("s02_conscience_return", False):
        show dog halfstep at dog_mid
        with Dissolve(0.5)
        "狗停在紙箱邊喝了兩口，身體沒有靠近，鼻尖卻一直朝著她。"
    else:
        show dog anxious at dog_far
        with Dissolve(0.5)
        "狗先看她的手，才湊近瓶蓋，喝了兩口。每喝一口就抬眼確認一次。"
    pause 0.7
    "胸口某處鬆了一下——不是整個人鬆下來，只是「至少今晚牠還喝得動」那種小小的鬆一口氣。"

    # —— 離場鉤子 ——
    ya "我抱你一下。只是抱。很快。"
    "她事先預告，像對同事預告會議延遲。"

    if flags["dist_ok"]:
        show dog halfstep at dog_near
        with Dissolve(0.8)
        "她沒從正面撲。側身，手臂穿過胸腹下方，用力平均，像搬一份怕散的文件。"
        "狗僵住，短促嗚了一聲，爪子在她袖口抓出淺痕。她痛得吸氣，卻沒鬆手，也沒罵。"
    else:
        show dog anxious at dog_mid
        with Dissolve(0.8)
        "這次她放慢很多。手從側邊伸，停一下，再托住。"
        "狗還是僵住，嗚了一聲，抓痕疊在剛才那道旁邊。"
        "她痛得吸氣，卻沒鬆手，也沒罵。"

    ya "抱歉。我也不會。我們……先離開這裡。"
    "第一次，低聲聽起來比較像她自己。"

    hide dog
    with dissolve

    "機車棚燈管閃了一下。紙箱空了。陰影少了一塊活的東西。"

    scene bg street_night
    with Dissolve(1.5)

    $ play_bgm("warm", fade=3.0)

    "走向公寓的路上，狗的心臟隔著她的手臂跳得很快。她的心臟也是。"
    pause 0.6
    "兩個節奏疊在一起，亂，但沒有停下。"

    scene bg living_night
    with Dissolve(1.5)

    "電梯門要關時，她用肩膀擋住。狗的鼻子埋進她外套褶裡，嗅加班、關東煮、與一點點害怕的味道。"

    "予安低頭看牠。"
    ya "我叫予安。"
    thought "然後覺得可笑——狗又不辦證件。"
    ya "他們叫你小7……你要不要換一個，再說。"

    "門關上。樓層燈一格一格往上跳。"
    "她沒有數。第一次，她忘了數。"

    pause 0.8
    centered "{size=30}{color=#F7EFE4}今晚不算數。{/color}{/size}"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_03_gate_temp_border


## ------------------------------------------------------------
## Section 03：大門的臨時國界
## 一件事：門內／門外兩個世界——關上大門→開門歸來→夜裡見牠睡著、不忍心帶回門內直到天明。
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
        "從夜間急診回來時，已經過了午夜。醫生說牠只是餓、脫水，還有一身需要慢慢養回來的疲倦。"
        "予安抱著牠站在公寓大門前，藥袋輕輕敲著手腕。診所的白光退了，眼前只剩鐵門、門牌，與門縫底下那條細光。"
    elif flags.get("called_shelter", False):
        "她把留給動保的電話再確認一次，然後把手機收回口袋。明天有人會來——理論上，事情已經排進正確的流程。"
        "可今晚還沒結束。她站在公寓大門前，把狗放在門邊轉角——門外這一側。"
    else:
        "她站在公寓大門前，把狗放在門邊轉角——門外這一側。"

    "騎樓地面涼，大門感應燈嗡地亮了一下。門裡是上樓回家的路；門外是這塊臨時的地。"
    "狗的鼻子急促地動。機車廢氣、陌生人的鞋、油煙與鐵門的金屬味，全擠在同一個轉角。肩膀繃緊，尾巴夾著——把自己收小，好少佔一點陌生。"
    thought "帶進去，就像要養了。不帶進去，牠今晚睡在大門外面。"
    ya "今晚不算數。"
    "她又說一次，像對合約蓋章。聲音卻比預期更乾。"

    menu:
        "脫下外套，鋪成一塊臨時墊子":
            $ flags["coat_bed"] = True
            "她脫下外套鋪平，紙盤裡倒了半瓶水。"
            "狗縮在外套邊，先嗅衣領再嗅袖口。氣味熟一點，身體才敢放下半寸；耳朵仍朝向巷口。"

        "把外套折好，留一小塊能靠著的地方":
            $ flags["coat_bed"] = False
            "她把外套折成靠墊，擺在門邊牆角，紙盤裡倒了半瓶水。"
            "狗沒有趴上去，只讓肩膀貼著衣角——先借一點溫度，不借整件事。"

    show dog stair_watch at dog_far
    with Dissolve(1.0)

    $ dog_sfx("murmur")
    "牠只看著那扇大門，像在記住一條會開合的邊界：門裡一個世界，門外另一個。"
    "對面騎樓燈亮了一下，又滅。狗的爪子在磁磚上刮出短響。"
    "她把手伸向大門門把，又縮回來。指尖發涼。"

    # 進門：門外大門 → 玄關關門 → 客廳。狗留在門外，先藏立繪。
    hide dog
    scene bg entrance_night
    with Dissolve(1.0)

    "予安推開大門，跨過門檻，把門關上。門板合上的聲音很輕，卻把兩個世界切開。"
    "玄關全是她的氣味。門外那一小團蜂蜜褐，忽然失去唯一熟悉的來源。"

    scene bg living_night
    with Dissolve(1.0)

    "洗澡水開得很熱。熱水沖在肩上，心口那一塊卻沒熱起來。"
    thought "明天送走。明天讓日子恢復成只剩冰箱的夜晚。"
    "說出口的「明天」很短，像在趕時間，也像在躲。"
    "水聲裡，她好像聽見爪子又刮了一下。也可能只是水管。"

    scene bg entrance_night
    with Dissolve(0.9)

    "她擦乾頭髮，站在玄關通向大門那一側。門外沒有聲音——最好，也最糟。"
    thought "最好的意思是：牠還在。還是：牠已經走了。"
    "兩個答案她都不想要。她把手放上大門門把——門把是兩個世界之間唯一還熱的東西。"

    # ▷ 信任選擇（距離 Dist）— 本段唯一動 trust 的選項組
    menu:
        "開門蹲在兩步外，輕聲說「我還在」，再補水":
            $ trust += 2
            $ dist += 1
            $ flags["s03_returned"] = True
            $ flags["s03_ignored"] = False
            $ flags["s03_choice"] = "return"
            scene bg gate_night
            with Dissolve(1.0)
            show dog stair_watch at dog_far
            with Dissolve(0.6)
            "她還是開了大門。狗還在。窩更靠牆，更能看見鐵門打開的角度。外套被拖歪一角。"
            "門一開，牠先退半步，耳朵貼平。予安停在兩步外蹲下——膝蓋響了一下，狗的肩膀又緊半寸。"
            ya "我還在。明天……再說。"
            "聲音放軟，不是開會時那種尖銳。狗不懂句子，只聽見語氣裡那一點趕時間的急促被拉長。鼻子伸向鞋尖，停在半公分外。"
            "她補了一點水。指尖碰到紙盤時，自己也在抖。"
            hide dog
            scene bg entrance_night
            with Dissolve(0.9)
            "她把大門關上。玄關變回她的世界；門外，仍是牠的。"
            $ play_bgm("tender", fade=2.2)

        "開門用腳把牠趕進角落，提高音量說「別擋路」":
            $ trust -= 2
            $ dist -= 1
            $ flags["s03_returned"] = False
            $ flags["s03_ignored"] = False
            $ flags["s03_choice"] = "shoo"
            scene bg gate_night
            with Dissolve(1.0)
            show dog stair_watch at dog_far
            with Dissolve(0.6)
            "她開了大門。煩躁來得比心疼快——鞋尖把衣角推回牆邊，也把狗逼得更裡面。"
            ya "別擋路。"
            "音量碰上鐵門與騎樓壁，彈回來更硬。狗貼住牆，耳朵壓平，把這個聲音記進身體。"
            hide dog
            scene bg entrance_night
            with Dissolve(0.9)
            "她把大門關上。玄關燈嗡嗡，門裡的安靜卻變得刺耳。"

        "只看一眼就關門，整晚不再開門":
            $ trust -= 1
            $ dist -= 1
            $ flags["s03_returned"] = False
            $ flags["s03_ignored"] = True
            $ flags["s03_choice"] = "ignore"
            scene bg gate_night
            with Dissolve(0.8)
            show dog stair_watch at dog_far
            with Dissolve(0.5)
            "她把大門開一道縫，看見水盤還有水，便告訴自己這樣就夠了。"
            "狗抬眼確認人還在不在。她沒有走近，也沒有說話。"
            hide dog
            scene bg entrance_night
            with Dissolve(1.0)
            "大門關上後，她背靠門板，數自己的呼吸，假裝沒聽見那一側忽然變空的安靜。"

    # 夜裡睡不著 → 大門門把 → 門外睡覺的狗 → 不忍心帶回門內。
    hide dog
    scene bg living_night
    with Dissolve(1.0)

    "夜裡，大門外傳來爪子急促刮過磁磚的聲音，隨即縮回牆角。"
    "予安坐起來。不是狗叫——是爪子，短、急。騎樓地面很涼，門裡卻很暖。"
    "她躺回去，又坐起來。手機螢幕亮了一下，她沒有打開任何搜尋。"

    scene bg entrance_night
    with Dissolve(0.9)

    "她穿上拖鞋，沒開大燈，把手放上大門門把。掌心出汗，門把反而變涼。"

    scene bg gate_night
    with Dissolve(1.0)

    hide dog
    show dog door_sleep at dog_far
    with Dissolve(1.2)

    if flags.get("s03_ignored", False):
        "門一開，狗睡在轉角更遠的牆邊。背朝巷口，臉仍朝公寓大門，四隻腳收得很緊。"
    elif flags.get("s03_choice") == "shoo":
        "門一開，狗睡在被趕進的那個角落。身體縮成一小團，耳朵還壓著。"
    else:
        "門一開，狗睡在外套邊。背朝巷口，臉朝大門能打開的角度，呼吸淺而短。"

    "予安蹲在兩步外——一腳還在門裡的暖，一腳踩在門外的涼。"
    "她忽然覺得「今晚不算數」這句話很醜。"
    ya "今晚……算了。"
    "她不忍心看牠被關在門的這一側，獨自把陌生睡成這樣。"

    # ▷ 閘門 G1（進門權）— 一定帶回門內；差別只在進門後的距離質地。
    menu:
        "輕輕引牠進屋，讓牠待在看得見的地方":
            $ flags["entered_home"] = True
            $ flags["delayed_entry"] = False
            "予安把外套連同那一小團一起抱起來。狗在臂彎裡僵了一下，隨後才發現沒有被扔下。"
            scene bg entrance_night
            with Dissolve(1.0)
            if trust >= 2 or flags.get("s03_returned", False):
                show dog door_sleep at dog_entrance_mid
                with Dissolve(0.7)
                "跨過門檻。牠的鼻子貼著袖口，確認門裡的氣味：咖啡、洗衣精、她。"
            else:
                show dog door_sleep at dog_entrance_far
                with Dissolve(0.7)
                "跨過門檻時，牠的身體一直繃著。直到門關上，下巴才放下半公分。"
            "她把門關好，燈只留這一盞。"
            scene bg living_night
            with Dissolve(1.2)
            show dog door_sleep at dog_mid
            with Dissolve(0.8)
            "外套鋪進客廳地板，離沙發兩步。狗轉了一圈，背朝門、臉朝她躺下——仍怕，但怕得比較近。"

        "帶進來，但先只放到玄關——明天再算":
            $ flags["entered_home"] = True
            $ flags["delayed_entry"] = True
            "她還是把大門開大，把牠帶進門裡。手在抖——這一步比「明天送走」更難收回。"
            thought "先進玄關就好。不要整間屋子。"
            scene bg entrance_night
            with Dissolve(1.2)
            show dog door_sleep at dog_entrance_far
            with Dissolve(0.8)
            "玄關地墊成了新的臨時國界——已在門內，卻還貼著門。狗趴在鞋邊，鼻子朝客廳探了一下，又縮回。"
            "予安坐在牠看得見的地方，把今晚縮成門檻到鞋櫃這一段。"

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

    if flags.get("delayed_entry", False):
        scene bg entrance_day
        with Dissolve(1.4)
        show dog door_sleep at dog_entrance_far
        with Dissolve(0.6)
        "清晨。窗光先到玄關地墊。狗仍在那一小塊，看她，又看客廳深處。"
    else:
        scene bg living_day
        with Dissolve(1.4)
        show dog door_sleep at dog_mid
        with Dissolve(0.6)
        "清晨。窗光先到地板。狗還在那兩步遠——恐懼會醒來，但人不曾消失。"

    ya "……早。"
    "狗不回答。可牠還在門裡——這比任何句子都清楚。"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_04_shared_quiet


## ------------------------------------------------------------
## Section 04：共享同一種安靜
## 一件事：沙發與地板平行存在。唯一動 trust 的選項組為相處方式。
## flags 寫入：s04_parallel／s04_forced_photo／bathroom_closed
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
        "昨晚牠只肯待在玄關那一小塊。天亮後，地墊上的光移了一格。"
        scene bg living_day
        with Dissolve(1.0)
        "牠才慢慢把前腳挪進客廳更深的地板。"
        "予安沒有關門，只把門縫留成一條細光——像把「算不算數」先留著。"
    else:
        "門開著。狗已經在客廳裡過了一夜。沒有儀式。"

    "沒有新買的碗、沒有訓練課程，也沒有「從今天起我們是家人」的台詞。"
    "只有予安的客廳、昨天的馬克杯、黑著的電視，以及離沙發兩步遠的一塊地板。"

    if trust >= 2 or flags.get("entered_home", False):
        show dog parallel at dog_mid
        with Dissolve(1.0)
        "她坐上沙發，拿出手機。狗選了那塊地板——能看見她，也能看見門。"
    else:
        show dog anxious at dog_far
        with Dissolve(1.0)
        "她坐上沙發，拿出手機。狗先在門邊僵了一會兒，最後才選了靠牆的地板——離她更遠，但仍看得見門。"

    "冷氣一聲喀地啟動。狗的耳朵豎起半秒，又慢慢放下——不是看她，是先聽屋子會不會再響。"
    "電視忽然自己亮了一下，大概是遙控器被壓到。音量大得像有人把整間辦公室搬進了客廳。"
    "狗耳朵貼平，下巴離地一公分。"

    "予安把音量轉小。再小。幾乎只剩字幕。"
    "過了一會兒，狗的下巴貼上地板。"

    "手機自動播到下一段短影片，笑聲忽然炸開。她慌忙按停，聲音斷在一半。"
    "狗沒有立刻趴回去。牠先看電視，再看手機，最後看她的手——像在分辨屋子裡哪些東西會突然變大聲。"
    "予安把手機倒扣在沙發上。手掌離開時，塑膠殼和布面碰出很輕的一聲。"
    ya "今天已經夠多了，對吧。"
    "狗的耳朵朝她轉了一下。沒有靠近，但也沒有換到更遠的地方。"
    thought "原來信任有時不是靠近，是一起耗著，誰都不逼誰。"
    "她把原本要說的「過來」咬掉，改成把雙腳往後收，留出一條從地板通往門口的空路。"

    # ▷ 信任選擇（距離 Dist）— 本段唯一動 trust 的選項組
    menu:
        "繼續各坐各的；牠在看得見的地方就好":
            $ trust += 2
            $ dist += 1
            $ flags["s04_parallel"] = True
            $ flags["s04_forced_photo"] = False
            $ flags["bathroom_closed"] = False
            "予安把手機螢幕亮度調暗。螢光比窗外的光還搶，她忽然不想贏。"
            ya "你就待在那。我也待在這。"
            "句子不完整，語氣很低。狗不回答，尾巴輕輕貼著腿側。"
            show dog parallel at dog_mid
            with Dissolve(0.8)
            "幾分鐘後，牠的耳朵鬆下來，下巴完整貼住地板。安靜沒有被誰搶走。"

        "把牠硬抱上沙發，先合照一下":
            $ trust -= 2
            $ dist -= 1
            $ flags["s04_parallel"] = False
            $ flags["s04_forced_photo"] = True
            $ flags["bathroom_closed"] = False
            $ play_bgm("tense", fade=1.8)
            "她忽然覺得這個畫面應該被留下。手臂從狗胸前穿過，把牠抱上沙發。"
            "相機還沒對焦，懷裡的身體先僵住。爪子急著找地，尾巴夾在腹下。"
            hide dog
            show dog anxious at dog_far
            with Dissolve(0.7)
            "予安按下快門，又立刻把牠放回地板。照片裡她在笑，狗的眼睛卻只看著逃跑的方向。"
            "她沒有刪照片，也沒有再拍第二張。"

        "把牠關進浴室；那裡比較好清理":
            $ trust -= 2
            $ dist -= 1
            $ flags["s04_parallel"] = False
            $ flags["s04_forced_photo"] = False
            $ flags["bathroom_closed"] = True
            $ play_bgm("tense", fade=1.8)
            "她把紙盤和舊毛巾移進浴室，門關到只剩最後一條光。"
            "門後傳來一聲很低的鼻音，接著什麼都沒有。"
            "十分鐘後，予安發現自己根本沒看手機。她一直在聽那扇門有沒有聲音。"
            "她重新打開門，退到走廊另一端。"
            show dog anxious at dog_far
            with Dissolve(0.8)
            "狗沒有立刻出來。等牠終於走回客廳，選的是比原來更遠、也更靠近出口的地方。"

    "時間從上午走到傍晚。予安回完兩封工作訊息，洗掉昨天的馬克杯，又坐回沙發。"
    if flags.get("s04_parallel", False):
        "狗抬眼看她幾次，沒有起身。她把這當成安靜成立，不是邀請。"
    else:
        "狗抬眼時先找出口。她回到原位後，牠才把下巴放下。"
    "窗光移過地板一塊又一塊。她去倒水之前，地板上那團蜂蜜褐一直留在原位。"

    "傍晚，她口渴，起身去廚房倒水。腳步剛離沙發，地板上那團蜂蜜褐也跟著動了。"

    hide dog
    show dog kitchen_door at dog_mid
    with Dissolve(1.0)

    "不是撲上來。牠只跟到廚房門口，在門檻外停住。"
    "只到門口。不進來。"
    "水龍頭的水聲停住時，牠的耳朵還朝向廚房——人在裡面，牠就留在線外。"

    "予安在水槽邊站住。手裡的杯子涼涼的。"
    "她看著那雙停在門線上的前腳。牠沒有往出口退；牠是因為她離開沙發，才第一次選擇跟上來。"
    "她沒有叫牠再走一步，也沒有關廚房門。"

    $ play_bgm("warm", fade=2.2)

    "倒完水，她走回沙發。狗又回到地板原位。下巴貼地。安靜重新合上。"
    "手機亮起會議提醒：明天早會，鏡頭可開可關。予安看了一眼耳機——那條會讓聲音變得尖銳的線，靜靜掛在椅背上。"
    "狗的耳朵朝耳機方向動了一下，又放下。"

    thought "明天，會不會有兩種聲音。"
    "今晚，先只要一種——小的、慢的、夠兩個人耗著的那種。"
    "她把耳機線捲好，放進椅背看不見的地方。明天再開也不遲。"

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

    "早上八點五十七分。予安把筆電墊高，確認鏡頭只拍到書櫃和半張乾淨的牆。"
    "耳機一戴上，她的肩膀也跟著坐直。"

    show yuan headphones at char_right
    with dissolve

    if flags.get("s04_parallel", False) or trust >= 4:
        show dog parallel at dog_mid
        with Dissolve(0.8)
        "[dog_label]趴在離椅子兩步遠的地板，下巴靠近椅腳。牠已經知道，待在看得見的地方不一定會被趕走。"
    else:
        show dog anxious at dog_far
        with Dissolve(0.8)
        "[dog_label]仍留在靠門的位置。牠不看螢幕，只用耳朵聽她在房間裡走動。"

    "九點整，會議開始。"
    ya "早，檔案我昨晚補好了。第三頁的數字，我等一下再確認。"
    "予安的聲音俐落、清楚，每句話都有句點。"
    "狗抬起頭。那是同一個人，卻像從耳機線另一端借來了比較尖銳的聲音。"

    "同事問了一句進度。予安一邊回答，一邊用腳把滑落的充電線勾回桌下。"
    "[dog_label]的鼻尖跟著那條線移動，前腳才往前，螢幕裡又有人同時開口。三種聲音疊在一起，牠立刻把腳收回去。"
    "予安看見了，卻不能停。她對鏡頭點頭、記下修改項目，右手仍懸在桌邊，掌心朝下，像想把房間裡過快的節奏壓低。"
    thought "牠不知道哪一句不是在對牠說。"

    "同事臨時請她開鏡頭。她按下按鈕，螢幕裡出現自己，也出現一截從椅腳旁探出的蜂蜜色耳朵。"
    "[dog_label]嗅到垂下來的耳機線，往前半步。鼻尖碰了一下，線輕輕晃動。"
    "予安伸手去擋，牠以為那是邀請，前腳搭上椅緣。"
    "耳機插頭被扯鬆一點，兩端的聲音瞬間疊成一記尖銳回授。"
    "[dog_label]整個縮了一下，前腳卻卡在椅緣，退也不是、靠近也不是。"
    "螢幕裡，主管叫了她的名字。"
    ya "有，我在。"
    "她回答得太快。麥克風還開著，狗正抬頭看她——下一句會落在哪一邊，沒有時間慢慢準備。"

    # ▷ 信任選擇（Tone）— 本段唯一動 trust 的選項組
    menu:
        "先關麥克風、拿下耳機，再輕聲把牠抱下來":
            $ trust += 2
            $ tone += 1
            $ flags["s05_soft_voice"] = True
            $ flags["s05_sharp_voice"] = False
            $ flags["s05_repaired"] = False
            "予安先按下靜音。耳機拿下來時，房間忽然變大，冷氣聲、狗的呼吸、自己的心跳都回來了。"
            ya "等一下喔。我不是在兇你。"
            "她的手臂從胸腹下方托住牠，慢慢放回地板，沒有順手推開。"
            "狗站在原地看她。耳朵先貼著，過了一會兒才鬆開一點。"
            show dog parallel at dog_mid
            with Dissolve(0.8)

        "不關麥克風，用開會的聲音說「下去」":
            $ trust -= 2
            $ tone -= 1
            $ flags["s05_soft_voice"] = False
            $ flags["s05_sharp_voice"] = True
            $ flags["s05_repaired"] = False
            ya "下去。"
            "兩個字又快又直，連同事那端都安靜了半秒。"
            "狗的耳朵立刻貼平，前腳從椅緣滑下，退回靠門的位置。"
            hide dog
            show dog ear_flat at dog_far
            with Dissolve(0.7)
            $ dog_sfx("whimper")
            thought "我只是要牠下去。可是牠聽見的，好像不只這樣。"

        "先急著把牠抱開，會後再蹲下來道歉":
            $ trust -= 1
            $ tone -= 1
            $ flags["s05_soft_voice"] = False
            $ flags["s05_sharp_voice"] = False
            $ flags["s05_repaired"] = True
            "她怕同事看見，手臂先一步把狗抱離椅邊。力道比自己預想得急。"
            "狗落地後退了一步，耳朵壓低。予安已經把麥克風打開，只能先把那句抱歉留著。"
            hide dog
            show dog ear_flat at dog_far
            with Dissolve(0.7)

    "會議繼續。四十分鐘後，她闔上筆電，拿下耳機。"

    "耳罩離開後，她才發現自己咬緊了牙。椅子往後時，[dog_label]的爪子縮了一下；她立刻停住。"
    ya "好了。現在這句是對你說的。"

    if flags.get("s05_repaired", False):
        "她蹲到兩步外，把手放在膝上。"
        ya "剛才太急了，對不起。"
        $ trust += 1
        $ tone += 1
        "狗沒有馬上靠近。等那句話留在原地，牠才往前挪了半步。"
    elif flags.get("s05_sharp_voice", False):
        ya "剛剛……太大聲了。"
        "狗仍停在門邊，耳朵轉向她，沒有完全別開。"
    else:
        "狗等到耳機不再傳出人的聲音，才慢慢抬起頭。"

    $ play_bgm("tender", fade=2.2)

    hide dog
    show dog sniff_wire at dog_mid
    with Dissolve(1.0)

    "[dog_label]走到桌邊，鼻尖碰了碰垂下來的耳機線——像在確認：那種尖銳的聲音關了嗎。"
    "予安把耳機放到桌上，將線收好。"
    ya "關了。"
    "她把鬆掉的插頭完整拔下。喀的一聲很輕，卻是這場早會裡，第一個沒有從耳機裡折回來的聲音。"

    "狗又從桌腳縫裡聞一次，直到耳機真的不再冒出人的聲音。"
    "會議筆記最後一頁，多了一行不是工作的字：「先拿下耳機。」她盯著那五個字，沒有劃掉。"
    "忙起來的自己，需要一些比記憶更可靠的提醒。"

    "她打開手機裡的動物醫院資料。姓名欄還空著，游標一閃一閃。"
    menu:
        "保留超商叫牠的名字「小7」":
            $ dog_label = "小7"
            "予安在姓名欄填上「小7」。這個名字從後門一路跟來，短短的，卻已經有人回頭看。"

        "替牠換一個新名字":
            $ proposed_name = renpy.input("想怎麼叫牠？", default=dog_label, length=12).strip()
            if proposed_name:
                $ dog_label = proposed_name
            "予安把「[dog_label]」念得很輕。狗未必懂名字，耳朵卻朝她動了一下。"

    "門外傳來電梯開門聲。有人拖著紙箱經過，腳步停在她門前。"
    neighbor "妳有養狗喔？"
    "狗的身體比她更早聽懂陌生。"

    $ trust = max(0, min(12, trust))
    $ renpy.block_rollback()
    jump section_06_corridor_third_person


## ------------------------------------------------------------
## Section 06：走廊上的第三者
## 一件事：陌生人伸手時予安站在哪裡。唯一動 trust 的選項組為 Guard。
## flags 寫入：s06_protected／s06_allowed_touch／s06_sent_inside
## ------------------------------------------------------------

label section_06_corridor_third_person:
    $ current_section = "s06"
    $ save_name = "Section 06｜走廊上的第三者"
    $ trust = max(0, min(12, trust))
    $ play_bgm("guard_corridor", fade=2.5)

    scene bg corridor_day
    with Dissolve(1.5)

    $ show_section_title("Section 06", "走廊上的第三者")

    "門外的人是隔壁新搬來的鄰居。紙箱疊在推車上，最上面那箱歪了一角。"

    show neighbor stand at char_left
    show yuan commute at char_right
    with dissolve

    neighbor "好可愛。妳新養的喔？"
    "予安還沒想好該怎麼回答。[dog_label]先往後退，肩膀碰到門框。"
    neighbor "我摸一下，牠應該不會咬吧？"
    "鄰居往前一步，手已經伸了出來。"

    if tone >= 1 or flags.get("s05_soft_voice", False):
        show dog behind_legs at dog_near_pair
        with Dissolve(0.8)
        "狗的耳朵貼低，躲到予安的小腿後。鼻尖靠近褲管，沒有碰。"
    else:
        show dog anxious at dog_far_pair
        with Dissolve(0.8)
        "狗貼著牆，耳朵壓低。牠沒有躲到予安身後，只替自己留著一條能退回屋裡的路。"

    "推車上的紙箱忽然往旁邊滑了一寸。鄰居回頭扶住，鞋尖也跟著往前。"
    "[dog_label]的鼻子急促動了兩下：膠帶、陌生洗衣精，還有一隻停在頭頂上方的手。"
    "予安原本扶著門。她只要往後退，門就會替她把場面關掉；只要笑一下說「沒關係」，尷尬也會比較快過去。"
    "可是狗的後腳已經抵住門檻。再退，就只剩屋內那條看不見外面的路。"
    neighbor "牠是不是很膽小？我家的狗以前摸兩次就熟了。"
    neighbor "我不會突然摸啦，先讓牠聞一下就好。"
    "推車輪子卡進磁磚縫，前後推了兩下——喀、喀。每響一次，[dog_label]的肩膀便往她腿後再縮一點。予安感覺得到那點重量，隔著褲管輕輕發抖。"
    "話沒有惡意。正因為沒有惡意，拒絕更難說出口。"
    thought "要保護牠，不一定要先證明別人做錯了。"
    "牠先看的從來不是手，而是那隻手會不會停。"

    # ▷ 信任選擇（Guard）— 本段唯一動 trust 的選項組
    menu:
        "往前半步擋住，說「牠還在適應，先不要摸」":
            $ trust += 2
            $ guard += 1
            $ flags["s06_protected"] = True
            $ flags["s06_allowed_touch"] = False
            $ flags["s06_sent_inside"] = False
            hide yuan
            show yuan block at char_right
            with Dissolve(0.6)
            "予安往前半步，剛好把那隻手和狗隔開。"
            ya "不好意思，牠還在適應。今天先不要摸牠。"
            neighbor "喔，好啊。我只是看牠很可愛。"
            ya "我知道，謝謝妳。"
            "走廊只安靜了兩秒，鄰居便把手收了回去。"
            show dog behind_legs at dog_near_pair
            with Dissolve(0.6)

        "怕場面尷尬，讓鄰居摸一下":
            $ trust -= 2
            $ guard -= 1
            $ flags["s06_protected"] = False
            $ flags["s06_allowed_touch"] = True
            $ flags["s06_sent_inside"] = False
            ya "可以吧……輕一點就好。"
            "手掌落下時，狗整個僵住。尾巴貼緊腹側，眼睛只看著門內。"
            hide dog
            show dog ear_flat at dog_far_pair
            with Dissolve(0.7)
            neighbor "牠好乖喔。"
            "予安第一次覺得「乖」有時只是沒有地方可以退。"

        "先把牠抱回屋裡，避免惹麻煩":
            $ trust -= 1
            $ guard -= 1
            $ flags["s06_protected"] = False
            $ flags["s06_allowed_touch"] = False
            $ flags["s06_sent_inside"] = True
            "予安彎身把狗抱起來。動作不重，卻快得像先把一件麻煩收好。"
            ya "不好意思，牠怕生。"
            hide dog
            with dissolve
            "門關上了。事情確實簡單了，牠卻沒有看見她站在哪一邊。"

    neighbor "可是這棟可以養嗎？"

    if flags.get("s06_protected", False):
        "予安低頭，看見[dog_label]仍停在她腿後。"
    else:
        "予安看向門內。"

    ya "我會去跟管理室確認。"
    "她停了一下。"
    ya "我們還在適應。"
    "「我們」兩個字比她預想得自然。說完才發現，已經收不回去了。"

    neighbor "好啦，那我先不吵牠。下次遠遠打招呼。"
    "予安點頭。拒絕沒有讓走廊裂開。她低頭看狗——牠只知道那隻伸來的手最後停住了。"

    "電梯門關上。予安退回屋內，沒有急著把門甩上。"

    scene bg living_day
    with Dissolve(1.2)

    hide neighbor
    hide yuan
    show yuan commute at char_right

    if flags.get("s06_sent_inside", False):
        "狗在鞋櫃旁等著。予安把門留開，退到兩步外，等牠自己決定要不要靠近。"
    else:
        "她等[dog_label]自己跨過門線，才把走廊的聲音關在外面。"

    $ play_bgm("tender", fade=2.2)

    if flags.get("s06_protected", False) or trust >= 5:
        show dog forehead_nudge at dog_near_pair
        with Dissolve(1.0)
        $ dog_sfx("soft")
        "[dog_label]往前半步，用額頭很輕地碰了一下她的小腿。不是撲，也不是討摸。碰完就退開，像把一句很短的話放在那裡。"
        ya "……不客氣。"
        "她說完才覺得自己有點好笑。可這一次，她沒有把話吞回去。"
    else:
        show dog halfstep at dog_far_pair
        with Dissolve(1.0)
        "狗往前走了半步，鼻尖停在褲管外一點點，最後沒有碰上。予安沒有追，只讓那段距離留到下一次。"

    "走廊外又傳來推車輪子壓過磁磚縫的聲音。[dog_label]抬頭，身體先朝門的方向繃了一下。"
    "予安沒有立刻說「沒事」。她先走到門邊，確認門鎖好，再回到牠看得見的位置坐下。"
    "狗聽不懂緊張是什麼，只看見她的手沒有再伸過來。過了一會兒，牠把原本懸著的前腳放回地板。"
    "被保護之後，不一定馬上靠近；有時只是終於能把一隻腳放下來。"

    centered "{size=30}{color=#F7EFE4}原來「我們」，會先從站的位置長出來。{/color}{/size}"

    "她把這句話留給自己。"
    "玄關燈還亮著。[dog_label]在鞋櫃旁繞了一圈，最後選了能同時看見她與門的位置趴下。"
    "予安沒有關燈。今晚先讓走廊那一點餘波，慢慢散掉。"
    "她把鞋子擺整齊，動作比平常慢一點——怕再發出像推車輪那樣突然的聲響。"

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

    "凌晨兩點十三分，予安冷得自己醒過來。"
    "客廳的燈還亮著，鬧鐘在桌上震了第三次。她想伸手關掉，手臂卻重得像壓著一條濕毛巾。"
    "額頭燙，喉嚨乾，連吞口水都要先想一下。門外有爪子刮過地板。"

    if trust >= 5 or flags.get("s06_protected", False):
        show dog guard_door at dog_near
        with Dissolve(0.8)
        "[dog_label]走到床邊，鼻尖碰了一下垂落的被角，又把她忘在客廳的拖鞋咬到門邊。"
        "牠不知道拖鞋能做什麼，只記得她起床時總會穿上。"
    else:
        show dog anxious at dog_far
        with Dissolve(0.8)
        "[dog_label]沒有進房，只在門口來回兩趟，發出一聲短短的輕吠，又立刻安靜。"
        "像怕自己的聲音，也會被關在外面。"

    ya "現在幾點……"
    $ dog_sfx("bark")
    "狗又叫了一聲。不是催促，更像確認房間裡還有沒有回答。"

    "予安想撐起身體，手肘才離開床，視線便暗了一圈。她重新躺下，棉被被汗黏在膝後。"
    "床邊的水杯是空的，手機在客廳充電。她平常替所有東西安排位置，今晚每一樣都離她差一點。"
    "[dog_label]聽見床墊下沉，前腳往前半步，又因她突然咳嗽停住。"
    "牠低頭聞自己的腳，再聞門外，像把房間裡每一道能走的路重新排過一次。"
    ya "我知道你也不知道怎麼辦。"
    "這句話說完，她反而沒有那麼急著要求牠安靜。"
    "耳鳴忽然蓋過冷氣聲，尖銳地停在腦後。予安閉上眼，連門口的影子都被那道聲音沖淡。"
    "過了幾秒，[dog_label]短短叫了一聲。那聲音不大，卻從耳鳴裡穿進來，讓她重新找到房門的方向。"
    "她想回應，喉嚨只剩乾痛；想伸手，手臂仍沉在床沿。這一次，她得先決定要把哪一種聲音送回去。"

    # ▷ 信任選擇（Tone）— 本段唯一動 trust 的選項組
    menu:
        "摸摸牠的背，低聲說「我還在」":
            $ trust += 2
            $ tone += 1
            $ flags["s07_reassured"] = True
            $ flags["s07_shut_out"] = False
            $ flags["s07_door_ajar"] = False
            "予安把手移到床沿，指尖很輕地碰了碰狗背。"
            ya "我還在。只是有點不舒服。"
            "[dog_label]聽不懂後半句，卻聽見那個熟悉的低聲。牠沒有再叫，只把身體放回門線上。"
            $ play_bgm("tender", fade=2.2)

        "煩躁地說「吵死了」，把牠關到客廳":
            $ trust -= 2
            $ tone -= 1
            $ flags["s07_reassured"] = False
            $ flags["s07_shut_out"] = True
            $ flags["s07_door_ajar"] = False
            ya "吵死了……讓我睡一下。"
            $ play_bgm("tense", fade=1.2)
            "門闔上的聲音不大。外面的爪步停了，過了一會兒，才慢慢退到沙發旁。"
            hide dog
            show dog ear_flat at dog_far
            with Dissolve(0.7)

        "說「等一下，我不舒服」，把門留一條縫":
            $ flags["s07_reassured"] = False
            $ flags["s07_shut_out"] = False
            $ flags["s07_door_ajar"] = True
            ya "等一下。我不舒服，不是在兇你。"
            "她把門留了一條縫。狗停在縫外，沒有靠近，也沒有離開。"
            show dog guard_door at dog_mid
            with Dissolve(0.7)

    "予安扶著牆去倒水。杯子碰到流理台，比平常更響。水柱濺到手背，她花了兩次才轉緊水龍頭。"
    ya "沒關係。你待在那裡就好。"

    if flags.get("s07_shut_out", False):
        "她回房前重新把門打開。[dog_label]仍在沙發旁，抬眼確認了一次，沒有跟過來。"
        "予安把一條乾毛巾放在門邊，留給下一次靠近。"
    else:
        show dog guard_door at dog_mid
        with Dissolve(0.6)
        "[dog_label]跟到房門口便停下。牠趴在那條線上，頭朝客廳，耳朵卻留一隻向著她。"
        ya "謝啦。"
        "以前都是她確認狗有沒有呼吸；今晚第一次，有另一個心跳在確認她。"
        "不是救援。只是一隻幼犬不知道該怎麼辦，所以把自己放在最靠近問題的地方。"

    "天快亮時，她又醒了一次。房門線上的影子換了方向，[dog_label]的下巴從左腳挪到右腳，仍沒有離開。"
    "予安把手伸到床沿，沒有碰牠，只讓指尖垂在牠聞得到的位置。"
    "一個濕涼的鼻尖短短靠近，又退回去。她在那個幾乎不能算接觸的瞬間，再次睡著。"
    "早上，她傳訊息請假。主管只回「好，先休息」。她原本準備了一長段解釋，最後沒有送出。"
    "予安忽然笑了一下。牠不會替她量體溫，也不會拿藥；牠只會重複確認。可人在最沒有力氣的時候，被確認還在，已經足夠。"
    "耳鳴已經退遠。房間裡剩下兩種不整齊的呼吸，一個在床上，一個在門邊，慢慢找到彼此都能跟上的速度。"

    scene bg office_night
    with Dissolve(1.5)
    show yuan headphones at char_center
    with dissolve

    "退燒後的第一個上班日，她點進手機相簿：照片裡，[dog_label]睡在房門邊，一隻耳朵翻著。"
    "她沒有貼動態，只看了三秒，便把手機扣回桌上。"
    "那張模糊照片，為什麼比退燒證明更像她真的撐過昨晚——她還不知道該怎麼解釋。"
    "下班時，繞進生活用品店，買了一條最普通的牽繩。"
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
## BGM：calm／corner_walk → 驚嚇 tense 短 → 分支 tender／tense
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

    show yuan leash at char_right
    show dog leash_wait at dog_entrance_far
    with dissolve

    "週六上午，牽繩在玄關鞋櫃上躺了二十分鐘。"
    "予安穿好鞋，又坐回地墊邊。[dog_label]隔著兩步看那條陌生的線，鼻尖靠近一下，立刻退開。"
    "她沒有拿胸背帶追著牠套，只把胸背帶和牽繩一起放到玄關地板，等牠聞完。"

    "金屬扣環碰到地墊邊緣，發出一聲很小的喀響。[dog_label]仍縮了一下，繞到鞋櫃另一側，從縫裡盯著那個不會自己移動的東西。"
    "予安把手收回膝上。她等到牠探頭，才用一根手指把胸背帶往前推一點；每推一次就停，讓牠自己補完剩下的距離。"
    "狗先聞布邊，再聞扣環，最後聞她碰過的地方。鼻尖在三種氣味之間來回，像確認這不是一個突然關上的圈套。"
    ya "我第一次用這個。你也是。"
    "她把這句話說成平等的承認。沒有「很簡單」，也沒有「別怕」。"

    show dog leash_wait at dog_entrance_mid
    with Dissolve(0.8)

    "等牠不再往後縮，她才蹲在側邊，讓牠自己把前腳踏進去。扣環喀一聲合上；她立刻鬆手，沒有把穿好當成出發命令。"
    "[dog_label]站在玄關原地，把左腳抬起又放下，接著扭頭去咬胸口那條陌生的布。予安沒有阻止，只用手背擋住扣環，免得牙齒卡住。"
    "過了半分鐘，牠停止啃咬。胸背帶沒有消失，門也沒有立刻打開。牠慢慢把四隻腳都放穩。"
    ya "走到轉角就好。"

    "她把手放上門把，先開一道縫。門外走廊的冷氣與燈管味鑽進來。[dog_label]的鼻子動了兩下，前腳踩出門檻半步，後腳仍留在地墊上。"
    "予安沒有用牽繩把那兩隻後腳拉過去。她側身讓出空間，門開大一點，又停住。"
    "第一次，牠縮回來。地墊還暖，外面還陌生。"
    pause 0.7
    "她把門再開一次。這回[dog_label]自己把後腳也帶出去——門裡一個世界，門外另一個，牠選了跟她同一側跨出去。"
    "玄關安靜下來。鞋櫃、空掛勾、地墊上她剛坐過的位置，都留在門後。"

    scene bg alley_day
    with Dissolve(1.5)
    show yuan leash at char_right_walk

    "大門推開的瞬間，外面的世界一下變得很密。早餐店的油煙、樓上曬過的衣服、排水溝、機車輪胎，全部擠在同一口呼吸裡。"
    pause 0.7
    "遠處有人拉鐵門，金屬聲沿著巷子刮過來。塑膠袋貼著地面滾了兩圈，卡在盆栽下。"
    "[dog_label]的鼻子來不及決定先聞哪裡，呼吸變得又快又淺。牽繩不是被牠往前拉緊，而是被整個身體往後墜住。"
    "予安把握把從手掌移到手腕，另一手只扶著繩身，不把張力一路傳回牠胸口。"

    if trust <= 3:
        show dog street_tense at dog_far_walk
        with Dissolve(0.7)
        "[dog_label]一出門便貼著牆，四隻腳像各自忘了下一步。"
    elif trust <= 6:
        show dog leash_wait at dog_mid_walk
        with Dissolve(0.7)
        "[dog_label]走到巷子一半，每幾步便回頭確認。牽繩一下鬆、一下緊。"
        "牠走了兩步又停。予安也停，把手腕往前送一點，等繩子垂回鬆弧。"
        "右耳轉向她之後，牠才再走兩步。這段路不是一次走完，是停下、確認，再重新開始。"
    else:
        show dog leash_wait at dog_near_walk
        with Dissolve(0.7)
        "[dog_label]跟到接近轉角的位置。牽繩仍繃著，卻不是一路往後退。"

    "他們走過第一台停著的機車。車殼還有曬熱的味道，狗伸長鼻子，沒敢靠近輪胎。"
    "一個送餐員從後方快步經過，保溫箱擦過予安手肘。她下意識往旁邊讓，隨即發現牽繩也被帶緊。"
    ya "對不起。是我沒看到。"
    "她停下來，把繩子重新放鬆。[dog_label]沒有回頭，右耳卻短短轉向她。"
    "前方的樹影只有幾步，牠每走一步都先把重量壓到後腳，確定地面沒有追上來，才把前腳送出去。"

    "予安沒有說「加油」。她怕那兩個字也變成催促。"
    "一輛機車從轉角切進來，排氣聲突然放大。"
    $ play_bgm("tense", fade=0.8)
    show dog street_tense at dog_far_walk
    with Dissolve(0.4)
    "狗整個往後扯，指甲在地面刮出短短一聲。"
    "予安的手腕被猛地扯痛。她也嚇了一跳，第一個反應是把繩子拉回來；力道才起來，她便看見狗的腹部幾乎貼到地面。"
    pause 0.9
    $ dog_sfx("whimper", 0.28)
    "機車已經離開，聲音卻像還留在牠身上。胸背帶跟著急促呼吸一下下起伏，眼睛在轉角、家門與她之間來回。"
    "她看了一眼手機。才過六分鐘。計步數少得不像一次散步，卻已經裝滿牠今天能處理的聲音。"
    pause 0.6
    "樹影就在旁邊。轉角只剩幾公尺，近得讓人很想把「第一次成功」湊完整。"

    # ▷ 信任選擇（Dist）— 本段唯一動 trust 的選項組
    menu:
        "走到樹下側身蹲著，等牠自己決定下一步":
            $ trust += 2
            $ dist += 1
            $ flags["s08_waited"] = True
            $ flags["s08_forced_walk"] = False
            $ flags["s08_returned_early"] = False
            "予安走到樹下側身蹲著，把視線移開，也把自己的呼吸放慢。"
            pause 0.8
            "狗先看機車離開的方向，再看她的鞋。牽繩鬆了一點，又一點。"
            "一片乾葉被風吹到牠腳邊。牠先退半步，等葉子停下，才低頭聞了聞。鼻尖碰到葉緣時，予安仍看著別處。"
            "她讓自己的手垂在膝旁，不拍腿、不拿零食，也不把那次嗅聞變成需要稱讚的表演。"
            $ play_bgm("tender", fade=2.2)
            show dog leash_wait at dog_mid_walk
            with Dissolve(0.8)
            "過了一會兒，牠自己往前走了一公尺。沒有抵達任何值得拍照的地方，卻是牠決定的那一步。"
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
            "予安把牽繩收短，往前走。"
            ya "一下就好，走完就回家。"
            show dog street_tense at dog_far_walk
            with Dissolve(0.7)
            "牽繩繃成一條直線。[dog_label]被拉過樹影，四隻腳輪流追著胸口的力道。遇到轉彎，牠來不及聞便被帶往下一段。"
            "予安每走幾步就說一次「快到了」。同一句話重複到最後，連她自己都聽不出安撫，只剩完成。"
            "牠確實跟完了一圈，卻一路沒有再聞地面。完成的路線留在手機計步裡，沒有留進牠的身體。"
            "回到大門前，牠沒有立刻跨進去，只貼著牆喘氣。予安這才把牽繩放長，晚了，但仍讓最後那一步由牠自己走。"
            $ play_bgm("tense", fade=1.5)

        "今天先回家，不把提早結束當成失敗":
            $ trust += 1
            $ dist += 1
            $ flags["s08_waited"] = False
            $ flags["s08_forced_walk"] = False
            $ flags["s08_returned_early"] = True
            "予安把牽繩留鬆，沿原路慢慢折返。"
            ya "好，今天到這裡。"
            $ play_bgm("tender", fade=2.0)
            "她沒有用「失敗」替這段路命名。回家的每一步，都還是牠自己走的。"
            show dog leash_wait at dog_mid_walk
            with Dissolve(0.8)
            "經過剛才那台停著的機車時，[dog_label]仍繞開半個身位，卻肯停下來聞一次地面。"
            "予安也跟著停。回程因此比去程更久，但牽繩大多垂成一個鬆鬆的弧。"
            pause 0.6
            "抵達大門，狗先看裡面，再回頭看那個沒有走到的轉角。牠沒有補完路線，只把今天能帶回家的部分帶回去。"

    scene bg entrance_day
    with Dissolve(1.5)
    hide yuan
    show yuan leash at char_right
    with Dissolve(0.5)

    "[dog_label]一進門便衝向水碗，喝得很急。水沿著嘴角滴到玄關地墊。予安沒有立刻擦，只先坐下，把牽繩從手腕慢慢鬆開。"
    "手腕被繩帶磨出一條淡紅色。她用拇指按了按，才發現自己從出門到現在一直握得太緊。"
    "胸背帶的扣環在玄關解開時，[dog_label]全身抖了一下，把累積在毛裡的灰和緊張一起甩開。"
    "予安把胸背帶留在玄關地板，沒有立刻收進櫃子。下一次，它不該又從一個突然出現的陌生東西開始。"

    if flags.get("s08_forced_walk", False):
        show dog street_tense at dog_entrance_far
        with Dissolve(0.8)
        "狗停在門邊，離她的鞋還有一段距離。予安把毛巾放在看得見的位置，沒有再叫牠過來。"
        "她把手機計步畫面關掉。那個完整的圓不再值得給誰看，至少今天不是。"
        pause 0.8
        ya "我走得太快了。"
        $ play_bgm("calm", fade=2.5)
        "狗仍沒有靠近，但喝水的間隔慢了一點。"
    else:
        $ play_bgm("warm", fade=2.5)
        show dog shoe_sleep at dog_entrance_mid
        with Dissolve(1.0)
        "狗喝完水，繞到她腳邊轉了半圈，最後靠著那雙剛走過外面的鞋趴下——鞋還停在玄關地墊上。"
        pause 0.8
        "眼睛還睜著，身體卻先睡著了。外面很大；回來的路，現在有了形狀。"
        "予安原本想把鞋脫下來，腳跟動了一下又停住。她就維持那個不太舒服的角度，讓狗先把這場散步睡完。"
        "幾分鐘後，牠的呼吸從急促變得深長。每一次吐氣，都把下巴更完整地交給鞋面。"

    "那天下午，牽繩一直留在玄關地板。予安經過時會放慢腳步，[dog_label]醒來也只是抬眼，不再立刻躲開那條線。"
    "她沒有趁機再帶牠出門。第一次的終點不是多走一趟，而是讓今天的聲音、氣味和回家的路在身體裡慢慢安靜。"

    scene bg living_day
    with Dissolve(1.0)
    hide yuan

    "睡醒後，狗自己走到玄關、胸背帶旁聞了一次。予安坐在沙發上看見了，沒有起身。那個沒有被追著完成的動作，被完整留給牠。"

    pause 0.8
    if flags.get("s08_forced_walk", False):
        "週一，同事在她手機亮起時瞥見一張門邊的照片。畫面裡，[dog_label]離她的鞋還有一段距離，旁邊是沒有收起來的牽繩。"
    else:
        "週一，同事在她手機亮起時瞥見那張靠著鞋睡著的照片。"
    "「妳最近是不是很累？」對方停了一下，語氣沒有玩笑。"
    pause 0.6
    "「如果真的顧不來，我可以養。」"
    "予安看著螢幕裡那團蜂蜜色，沒有立刻回答。"

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

    "同事是在茶水間又問了一次。沒有半句玩笑，也沒有把狗說成一件可以轉送的東西。"
    coworker "我不是催妳。只是我以前養過，現在住的地方也比較大。妳如果真的太累，可以先讓我接手。"
    "飲水機剛好開始加熱，低低的運轉聲填進兩人中間。予安盯著杯底那圈還沒融開的即溶咖啡。"
    coworker "我之前那隻活到十六歲。打針、換飼料、半夜跑醫院，我都碰過。"
    "她說得平靜，不像在列履歷，只是把能承擔的事情一項一項放到桌面上。"
    ya "妳家不是還有陽台嗎？"
    coworker "有，窗也裝好防護了。白天我媽在家，不會讓牠一直自己待著。"
    "每一個回答都比予安現在的生活更完整。她找不到可以挑錯的地方，也因此更容易點頭。"
    "予安點開手機備忘錄。工時、房租、醫療費、能不能準時回家。每一項都寫得清楚，像只要把理由排整齊，心裡那塊沒有欄位的地方就會安靜。"
    ya "我想一下。"

    "她真的想了。第一晚，她把每個月可能多出的花費加總，數字比想像中大。"
    "第二晚，加班通知在九點多跳出來。[dog_label]睡在門邊，聽見她拉開椅子便立刻抬頭。那雙眼睛沒有責怪，反而讓清單更難看完。"
    "第三晚，她整理疫苗資料。照片一張張滑過：後門的紙箱、大門口的外套、靠著鞋睡著的臉。"
    "她沒有替照片加說明，只把檔案日期改成容易找到的格式。做完這些，像是已經把某段生活打包得足夠讓別人接手。"
    "最後，她傳出一句：「週六見。」"

    scene bg living_day
    with Dissolve(1.2)
    hide coworker
    show yuan leash at char_right
    show dog leash_wait at dog_mid
    with dissolve

    "週六出門前，她把水碗洗了兩次。牽繩捲好，疫苗資料放進紙袋，連平常忘記補的濕紙巾都塞進去。"
    "東西準備得越齊全，房間裡就越像有人正在搬走。"
    "她把飼料分裝成七小袋，在每袋寫上日期。寫到第四袋時，筆尖停住，墨水在塑膠袋上暈成一小點。"
    "舊外套也被折進提袋。那件衣服早該送洗，袖口還留著第一次抱牠時抓出的淺痕。"
    "予安用拇指摸過那幾道線，最後沒有把外套拿出來。知道牠習慣什麼，也是交接資料的一部分。"

    scene bg entrance_day
    with Dissolve(1.0)
    show yuan leash at char_right
    show dog leash_wait at dog_entrance_far
    with Dissolve(0.6)

    if trust >= 5:
        "[dog_label]跟著她走到玄關，鼻尖碰了碰紙袋，又靠回她腳邊。"
        "她移動紙袋，狗也跟著換位置。不是阻擋，只是讓自己的肩膀一直貼在她和袋子之間。"
        show dog leash_wait at dog_entrance_mid
        with Dissolve(0.6)
        "予安蹲下，把胸背帶放到地墊上。牠聞了兩次，自己把前腳踏進去；扣環合上時，兩人都停了一秒。"
        "門把在掌心發涼——這次開門，不是散步，是去見另一個人。"
    else:
        "[dog_label]停在門線附近，沒有靠近。牠只看著那個裝滿自己氣味的紙袋。"
        "予安蹲下想替牠扣胸背帶，牠往鞋櫃邊退。她停住，等那雙眼睛不再只盯著出口，才重新伸手。"
        "胸背帶終於扣上。門把在掌心發涼——這次開門，不是散步，是去見另一個人。"

    scene bg cafe_day
    with Dissolve(1.5)
    show coworker stand at char_left
    show yuan leash at char_right
    with dissolve

    "咖啡廳門口比照片裡窄。玻璃門每開一次，磨豆聲和陌生人的氣味便一起湧出來。"
    "同事提早十分鐘到，手裡沒有玩具，也沒有零食。她說第一次見面先不要用東西把狗騙近，予安知道這個做法是對的。"
    "三個人——如果一隻狗也算一個人——在騎樓下維持著不太像交接的距離。沒有人催，時間反而更清楚。"
    "店門上的風鈴響了三次。[dog_label]每次都抬頭，第三次才沒有整個身體往後縮。"
    coworker "不用急。我先讓牠聞我。"
    "同事蹲下，側過身，把手留在膝上。動作沒有錯，語氣也很輕。"

    if trust >= 5 or flags.get("s06_protected", False):
        show dog refuse_stranger at dog_near_pair
        with Dissolve(0.8)
        $ dog_sfx("growl")
        "[dog_label]卻貼住予安的鞋，肩膀繃緊。牠沒有撲咬，只在同事伸手想接牽繩時，喉嚨裡滾出一聲很低、很短的警告。"
        "牠拒絕的不是那個人。牠只是把已經認得的外圍，縮回予安腳邊。"
    else:
        show dog street_tense at dog_mid_pair
        with Dissolve(0.8)
        "[dog_label]僵在離兩人都有一點距離的位置。沒有低鳴，也沒有躲進誰身後；牠只是再次把四隻腳準備成隨時能退的樣子。"
        "予安忽然明白，安靜不一定是同意。有時只是牠還不相信，任何一邊會替牠停下來。"

    coworker "牠在找妳。"
    ya "可是妳比較有經驗。"
    coworker "也許。但牠認得的是妳。"
    ya "認得不一定代表我適合。"
    coworker "對。適合也不一定代表牠現在就能跟我走。"
    "同事把兩件事分開說，沒有替她選。予安原本希望聽見一個專業答案，卻只得到一段需要自己承認的沉默。"
    "紙袋裡的疫苗資料被風吹得沙沙響。她伸手壓住，掌心剛好蓋在姓名欄上——那個她曾坐在桌邊，慢慢替牠填進去的名字。"
    "理智清單還在紙袋裡，一項都沒有失效。只是清單回答的是誰比較方便，沒有回答誰已經一次又一次回到同一扇門。"

    "咖啡廳裡有人拉開椅子，木腳刮過地面。[dog_label]縮了一下，兩個女人同時停住動作。"
    "同事先把手收回去；予安則蹲低半步，沒有碰牠。兩個人都知道怎麼不逼近，差別只在狗先抬頭找了誰。"
    "那雙眼睛沒有說「留下我」。牠不會替任何人做道德判斷，只把此刻能辨認的氣味、聲音和回家方向放在一起。"
    "予安想起自己曾說「今晚不算數」，曾把門留縫，也曾走得太快。被認得的不是一個總做對的人，而是一個所有好壞都已經發生過的人。"
    thought "如果留下，我不能再用『我不會』當作每一次傷害的結尾。"
    "她也明白，送走不代表不愛；留下更不等於從此有能力。真正卡在手裡的，是她願不願意承認這段關係已經需要一個由自己做出的答案。"

    menu:
        "把牽繩收回來，承認「我想繼續照顧牠」":
            $ trust += 2
            $ guard += 2
            $ flags["s09_stayed"] = True
            $ flags["gave_away"] = False
            ya "對不起，讓妳白跑一趟。"
            "她的手在抖，還是把牽繩重新繞回自己手腕。"
            ya "我不是比較會。我只是……想繼續學。"
            coworker "那就繼續。真的需要幫忙，再找我。"
            "同事站起來，沒有生氣，也沒有替這個決定鼓掌。她只把空著的手收回外套口袋，讓門口重新寬了一點。"
            show dog refuse_stranger at dog_near_pair
            with Dissolve(0.7)
            "[dog_label]的肩膀過了很久才鬆。牠沒有搖尾巴，只把鼻尖碰到她鞋側，像確認那雙鞋仍朝著回家的方向。"
            "予安把疫苗資料從紙袋拿回來。紙張沒有變重，握在手裡卻不像剛才那麼容易交出去。"
            coworker "留下不代表什麼都得自己撐。妳可以問我，也可以找別人幫忙。"
            ya "我可能真的會問很多。"
            coworker "那就問。"
            "予安第一次把「需要幫忙」和「不適合照顧」拆成兩件事。她把外套重新披回手臂，袖口的抓痕朝外。"
            "回程走到同一個轉角，[dog_label]停下聞了一會兒。予安沒有催，只把牽繩留成一個能呼吸的弧。"
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
            "予安把紙袋遞過去，再把牽繩握把一圈一圈從手腕鬆開。最後一圈卡在袖口，她停了一秒，才把它交到同事手裡。"
            ya "牠怕突然的機車聲。喝水很急。睡覺的時候，門不要全關。"
            coworker "好。我會慢慢來。"
            if entry_trust >= 5:
                show dog refuse_stranger at dog_mid_pair
                with Dissolve(0.7)
                "[dog_label]往她鞋邊靠，牽繩卻從另一隻手傳來方向。牠低低鳴了一聲，沒有被寫成挽留，也沒有被誰責怪。"
            else:
                show dog street_tense at dog_mid_pair
                with Dissolve(0.7)
                "[dog_label]沒有跟上任何人。兩邊都等了一會兒，同事才用鬆著的牽繩，帶牠慢慢離開玻璃門。"
            "予安站在原地，把所有已經交代過的事又在心裡重複一次。這個選擇有理由，也仍然會痛；兩件事可以同時是真的。"
            "同事沒有立刻轉身走。她先讓狗在原地聞紙袋，再把牽繩放到最長，等牠自己選第一步。"
            coworker "我到家會傳訊息。今晚如果牠不吃，我也會跟妳說。"
            ya "好。門……記得留一點縫。"
            coworker "我記得。"
            "予安點頭。她沒有要求再抱一下，因為最後一次接觸不該只服務自己的捨不得。"
            "玻璃門映出她空著的手。直到同事和狗走過轉角，她才發現紙袋已經不在自己手上，手指仍維持著提東西的彎度。"
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

    scene bg living_night
    with Dissolve(1.5)

    $ show_section_title("Section 10", "把鑰匙分給心跳")

    if flags.get("gave_away", False):
        "從咖啡廳走回公寓，予安經過他們第一次練習散步的轉角。樹影還在原來的位置，地上卻沒有一條牽繩提醒她停下。"
        "她走得比平常快。到家門口才發現，今天不需要先看腳邊有沒有一團蜂蜜色跟著。"
        "鑰匙插進鎖孔，門開得很順。屋裡沒有水碗被推動，也沒有爪子因為門聲從地板上站起來。"
        "予安把鞋脫好，照習慣留出靠牆那一小塊位置。做完才想起，已經沒有誰需要從那裡繞過她。"
        "她先去洗水碗。水龍頭開到一半，手停在空中。碗是乾淨的，早上才洗過兩次；她只是還沒準備好把它收起來。"
        "牆上的掛勾原本預留給牽繩。現在只有鑰匙掛在左邊，右邊空著，黏膠的透明邊在燈下反光。"
        "她把鑰匙取下又掛回去，金屬碰牆的聲音比平常清楚。"
        thought "原來少一個心跳，不是完全沒有聲音。"
        "手機仍沒有訊息。她告訴自己，抵達新家需要時間；告訴第二次時，才承認自己其實在等一個不是由她拍下來的安全證明。"
        jump ending_ch1_handed_over
    else:
        "回程經過生活用品店，予安站在碗架前很久。第一個水碗其實還能用，她最後仍拿了一個同樣大小、不同顏色的。"
        "店員問：「家裡有兩隻嗎？」她愣了一下，搖頭。"
        ya "一隻。只是想多放一個。"
        "新的水碗被包進薄紙袋。她提著它走回家，重量很輕，卻比疫苗資料更像一個不能再假裝只是暫住的決定。"
        "她也買了一排不需要鑽牆的小掛勾。說明書寫著承重兩公斤，足夠掛鑰匙、牽繩，以及日後可能越來越多的東西。"
        "回到客廳，[dog_label]先聞紙袋，再退到熟悉的距離，看她把牆面擦乾。"
        "第一個掛勾貼歪了。予安撕下來重貼，黏膠失去一點力；第二次仍歪，她便決定留下。"
        ya "不是每件事都要對得很準。"
        "狗看著她和牆面來回較勁，耳朵一邊高、一邊低。"
        "她把鑰匙掛在左邊，牽繩掛在右邊。牽繩垂下來時，[dog_label]往後半步；等它安靜不動，才慢慢靠近聞了一次。"
        "新的水碗被放在舊碗旁邊。一個裝水，一個暫時空著。予安沒有急著決定它以後要裝什麼，只讓並排這件事先成立。"
        "窗外的風把招牌吹得輕響。幾秒後，屋裡的燈忽然滅了。冰箱停止嗡嗡，客廳只剩窗外漏進來的一點灰藍。"
        "予安摸到手機，打開手電筒，沒有把光直接照向狗。她先照地板，再把光圈停在自己腳邊。"
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
    $ unlock_ending("A")
    $ unlock_secret_photo("lap_sleep")

    "[dog_label]在黑暗裡抬起頭，先看窗外，再看地板上的光。牠沒有衝向門，也沒有鑽進桌底，只把鼻子伸進光圈邊緣聞了一下。"
    "予安坐到地板上。手機放在膝旁，光便從下方照亮牆上的鑰匙與牽繩，兩道影子靠在一起。"
    $ play_bgm("hopeful", fade=2.2)
    ya "我們再試一年。"
    thought "一年後，再說下一年。"
    "她沒有伸手叫牠過來，只把背靠上沙發，讓自己的位置成為房間裡不會突然移動的東西。"
    "[dog_label]先走到水碗旁。新的碗反了一點手電筒的光，牠聞過邊緣，喝了兩口，再沿著牆走回來。"
    "走到予安腿邊時，牠停了很久。她甚至以為牠會選擇原本那塊兩步遠的地板。"
    show dog back_sleep at dog_near
    with Dissolve(1.0)
    "[dog_label]在伸手可及的地方轉了一圈，最後背對她躺下。耳朵鬆著，最沒有防備的那一側朝向房間。"
    "她沒有立刻伸手。只把掌心放在兩個呼吸之間，等牠自己睡沉。"
    "停電讓所有電器都安靜下來。予安第一次聽清楚牠睡著後的呼吸：吸氣短一點，吐氣長一點，偶爾鼻尖碰到地板。"
    "她把外套從沙發拉下來，蓋在自己腿上。衣角離狗的背只有半掌寬，她仍沒有跨過去。"
    "過了一會兒，[dog_label]在夢裡動了一下，背脊碰上衣角。牠沒有醒，也沒有把身體移開。"
    "予安看著牆上那排歪了一點的掛勾，沒有拍照。這個畫面不用先證明給別人看，才能算真的發生。"
    "電力恢復時，冰箱重新嗡了一聲。狗的耳朵動了動，背仍朝著她。"
    "那一晚，她在地板上睡得腰有點痛。醒來時，手掌還停在原處，沒有趁牠睡著偷摸一下。"
    "隔天鬧鐘響起，她拿起鑰匙。"
    "牽繩被鑰匙帶得輕晃。[dog_label]睜開眼，從地板看她穿鞋，卻沒有把身體挪回門邊。"
    ya "晚上見。"
    "狗抬了一下耳朵，沒有起身確認。門會關，也會再打開——此刻，牠把這件事交給她。"
    "傍晚，鑰匙聲再次落在門外。[dog_label]仍趴在原位，只用尾巴輕輕碰了一下地板。"
    "予安進門後先把鑰匙掛好。她沒有叫牠迎接；被相信回得來，已經是今天最安靜的歡迎。"
    centered "{size=31}{color=#F7EFE4}結局 A｜背靠{/color}{/size}"
    jump ending_aftercare


label ending_ch1_chosen_learning:
    $ save_name = "結局 B｜選定但還在學"
    $ flags["ch1_ending"] = "chosen_learning"
    $ flags["gave_away"] = False
    $ unlock_ending("B")

    "黑暗裡，[dog_label]先退到沙發另一側。手機的手電筒亮起時，牠瞇了一下眼，視線緊跟著那圈移動的光。"
    "予安把手機平放到地板，不拿光追牠。她在離狗兩步的位置坐下，像他們第一次共享客廳時那樣。"
    ya "我們再試一年。"
    "這句話不像承諾永遠，更像把明天先留出一個位置。"
    "狗站著聽了一會兒。牠先去聞新水碗，金屬邊被鼻尖碰出輕響，牠退半步，又回去聞第二次。"
    "予安笑了一下，沒有說「你看，沒什麼好怕」。對牠來說，第二次靠近本身已經夠忙了。"
    "她把外套鋪在沙發旁。不是圈出必須睡的位置，只是讓地板多一塊熟悉的氣味。"
    show dog check_sleep at dog_mid
    with Dissolve(1.0)
    "[dog_label]在沙發旁睡下，距離比以前近。牠背過身一會兒，又睜眼回頭，確認她還坐在原處。"
    ya "我在。"
    "牠重新把下巴放回前腳。信任沒有一次完成，只是今晚少確認了一次。"
    "窗外有車燈掃過天花板。狗又抬頭，予安沒有立刻安撫，只留在原位，讓同一個人、同一個氣味與同一塊地板替她回答。"
    "確認完門沒有開、她也沒有消失，牠第三次把頭放下。這次眼睛閉得比前兩次快。"
    "電力恢復後，電視待機燈亮起一個小紅點。[dog_label]看了一眼，沒有換回靠門的位置。"
    "予安替自己倒水，也替新碗添了一點。兩個碗並排時發出輕響，狗的耳朵動了，身體仍留在外套邊。"
    "她在沙發上睡著前，看見牠又回頭一次。她沒有覺得前功盡棄，只低聲再說一遍：「我在。」"
    "後半夜，確認變成偶爾的事。每一次間隔都比前一次長一點。"
    "隔天鬧鐘響起。予安拿起鑰匙，牽繩在旁邊輕輕晃了一下。"
    "[dog_label]站起來跟到玄關，在門線前停住。予安穿鞋時，牠看了門外，又看她。"
    ya "晚上見。"
    "狗看著她，沒有跟到門外。這已經是一種選定；剩下的，他們可以慢慢學。"
    "傍晚，她開門時，[dog_label]先在原地確認兩秒，才走到玄關一半。"
    "予安蹲下但沒有伸手。那剩下的一半距離，不需要今晚就完成。"
    centered "{size=31}{color=#F7EFE4}結局 B｜選定但還在學{/color}{/size}"
    jump ending_aftercare


label ending_ch1_handed_over:
    $ save_name = "結局 C｜送走之後"
    $ flags["ch1_ending"] = "handed_over"
    $ flags["gave_away"] = True
    $ unlock_ending("C")

    "夜裡短暫停電。冰箱的嗡嗡忽然停下，房間連原本能填空的聲音都沒有了。"
    "予安打開手機手電筒，習慣性先照地板，怕光直接落進一雙敏感的眼睛。光圈移出去半公尺，她才想起不用再避。"
    "她把手機立在水杯旁。牆上只有鑰匙，右邊那個空掛勾投下一小段影子。"
    "新的水碗沒有買。原本那個仍放在廚房門口，裡面的水維持早上出門前的高度。"
    "予安端起來走向水槽，走到一半又放回原處。她不知道收起來是整理，還是太快替這間屋子決定已經結束。"
    "手機亮起。同事傳來一張照片：[dog_label]趴在新家的門邊，水碗放得很遠，門留著一條縫。"
    coworker "牠有喝水。還在找能看見門的位置。我會等。"
    "照片裡的地板不是她家的顏色。狗的姿勢卻很熟悉：背朝走廊，臉朝門，四隻腳收得隨時能站起來。"
    "她把照片放大，看見紙袋裡那件舊外套露出一角。同事沒有把它洗掉，也沒有急著換成比較新的墊子。"
    "予安打了「牠晚上可能會叫」，又刪掉。打了「如果真的不行」，也刪掉。最後只回一句「謝謝」。"
    "對話框上方很快顯示已讀。沒有更多保證，也沒有一句話能把適應縮短。"
    "她坐在地板上，背靠沙發。以前這個高度會看見狗的耳朵或鼻尖；現在只看見手機的光把灰塵照得很清楚。"
    ya "今天先這樣。"
    "聲音仍然很輕。不是說給誰聽，也沒有因此失去意義。"
    "電力恢復時，她終於把水碗裡的水倒掉，洗乾淨，放在櫥櫃最下面。門沒有關緊，留著一條縫。"
    "她沒有把選擇說成對，也沒有說成錯。只是記住：理由可以完整，想念也不會因此變得不合理。"
    "隔天鬧鐘響起，她拿起鑰匙。"
    "右邊的空掛勾被鑰匙碰了一下，輕輕搖著。她伸手按住，等它停下來。"
    ya "晚上見。"
    "話出口後，房間沒有誰回頭。她站了一秒，才關上門。"
    "這不是故事被判定失敗。只是往後的靠近，要隔著另一扇門重新學。"
    "三天後，同事又傳來照片：[dog_label]睡在離新家房門兩步遠的地方，舊外套仍墊在身下。"
    "予安回了一個「收到」。她沒有要求更多證明，只把那張照片收進一個不再由她更新的相簿。"
    centered "{size=31}{color=#F7EFE4}結局 C｜送走之後{/color}{/size}"
    jump ending_aftercare


label ending_ch1_thin_ice:
    $ save_name = "結局 D｜薄冰同住"
    $ flags["ch1_ending"] = "thin_ice"
    $ flags["gave_away"] = False
    $ unlock_ending("D")

    "黑暗落下時，[dog_label]立刻回到門邊。背貼著牆，頭朝出口，手機的光才亮起，眼睛便跟著縮了一下。"
    "予安把光轉向自己，不照牠。她在客廳中央停住，沒有因為已經選擇留下，就把這間屋子的每一段距離都算成自己的。"
    "留下不是信任已經完成，只是她決定不把還沒學會的事交給別人收尾。"
    ya "我們再試一年。"
    "她說得很輕，沒有要求房間裡的另一個心跳立刻相信。"
    "狗沒有靠近。牠聞到牆上新掛的牽繩時，鼻尖只動了一下，便把視線轉回門鎖。"
    "予安把第二個水碗裝好，放在離第一個碗更遠的位置。兩條路都能喝到水，不需要經過她腳邊。"
    "她坐回沙發，手機光朝下。停電讓房間變得陌生，狗選擇最靠近出口的位置；她沒有把這個選擇讀成拒絕。"
    show dog door_edge at dog_far
    with Dissolve(1.0)
    "[dog_label]睡在靠門的位置，身體朝著出口，眼睛閉得很淺。牽繩掛好了，彼此之間仍隔著一段不能假裝不存在的距離。"
    "予安把手收回膝上。今晚不追，明天也不拿留下當作牠欠她的答案。"
    "樓上有人拖動椅子，狗立刻睜眼。予安也抬頭，卻沒有走過去抱住牠。她只把自己的呼吸放慢，留在原位。"
    ya "是樓上的聲音。"
    "牠不懂來源解釋，但聲音結束後，她沒有靠近，門也沒有打開。過了很久，牠才重新把下巴放回前腳。"
    "電力恢復，冰箱啟動。狗又醒一次。這回牠只抬眼，沒有站起來。"
    "予安把新水碗往牆邊推近一點，再退回沙發。她做的每個動作都讓牠看完，不趁轉身時縮短距離。"
    "那一夜沒有背靠，也沒有突然的原諒。只有兩個都睡得不深的生命，隔著客廳，慢慢確認對方沒有趁黑暗改變規則。"
    "清晨，她醒來時，[dog_label]仍在門邊，身體卻不再完全貼著牆。牠替自己留的縫，比昨晚少了一點點。"
    "隔天鬧鐘響起，她拿起鑰匙。"
    "她穿鞋時沒有叫狗的名字，只把牽繩扶穩，不讓它因鑰匙晃動敲到牆。"
    ya "晚上見。"
    "狗沒有看她。耳朵卻在門闔上前動了一下。薄冰沒有忽然變厚，但他們都還站在這一邊。"
    "傍晚回家，水碗少了一點水。[dog_label]仍守在門邊，身體卻沒有因鑰匙聲立刻站起來。"
    "予安把鞋放好，退到牠看得見的位置。今天沒有靠近，只比昨天少驚動一次。"
    centered "{size=31}{color=#F7EFE4}結局 D｜薄冰同住{/color}{/size}"
    jump ending_aftercare


## ------------------------------------------------------------
## 結局後：鼓勵重玩（gamer_30｜選擇要有可感知回聲）
## ------------------------------------------------------------

label ending_aftercare:
    if flags.get("ch1_ending") == "chosen_learning":
        "這是許多人第一次會留下的溫度——選定了，卻還在學。"
    elif flags.get("ch1_ending") == "back_to_back":
        "背靠很暖。若想看更接近日常養寵的溫度，結局 B〈選定但還在學〉也很值得。"
        if secret_photo_unlocked("lap_sleep"):
            "有一段畫面，只有真正把背交給彼此之後才看得到——可在「結局一覽」打開紀念照片。"
    elif flags.get("ch1_ending") == "handed_over":
        "送走不是被判失敗。選擇會改變睡姿與空掛勾——想再看一次留下之後的距離嗎？"
    else:
        "薄冰同住很誠實。若想看信任長成什麼樣子，結局 B 常被推薦當第一次。"

    "選擇會改變狗的距離與睡姿。想再試另一條路嗎？"
    menu:
        "回主選單":
            return

        "查看已解鎖結局":
            call screen ending_gallery
            jump ending_aftercare

        "從 Section 09 再試一次（留下或送走）":
            jump start_section_09

        "從頭開始":
            jump start
