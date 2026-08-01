## Version2 — 精簡 UI（say／choice／主選單／快捷列）
## 字型安全：勿用 U+00B7 間隔點；間隔用 ｜

define V2_CHOICE_YALIGN = 0.40

screen say(who, what):
    style_prefix "say"
    zorder 100

    if smell_text:
        frame:
            xfill True
            ypos 0
            background Solid(LHTL_SMELL_BG)
            padding (16, 7)
            hbox:
                spacing 8
                text "＊" size gui.smell_text_size color LHTL_ACCENT
                text "氣味：" + smell_text size gui.smell_text_size color LHTL_TEXT_SOFT font "SourceHanSansLite.ttf"

    window:
        id "window"
        background lhtl_textbox_bg()
        yalign 1.0
        ysize gui.textbox_height
        xfill True
        padding (28, 14)

        vbox:
            spacing 6
            xfill True
            frame:
                background Solid(LHTL_TEXTBOX_EDGE)
                ysize 2
                xfill True
            if who is not None:
                text who id "who"
            else:
                null height 4
            ## 固定約三行；保留 \\n 跳行；過長可滾輪
            fixed:
                xfill True
                ysize gui.dialogue_text_height
                viewport:
                    xfill True
                    yfill True
                    mousewheel True
                    draggable True
                    scrollbars "vertical"
                    text what id "what":
                        xmaximum gui.dialogue_width
                        line_spacing gui.dialogue_line_spacing

screen choice(items):
    style_prefix "choice"
    zorder 110

    frame:
        xalign 0.5
        yalign V2_CHOICE_YALIGN
        yanchor 0.5
        background None
        padding (0, 0)

        vbox:
            spacing 18
            xalign 0.5
            for i in items:
                textbutton i.caption action i.action xalign 0.5

screen quick_menu():
    zorder 200
    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.98
            yalign 0.02
            spacing 8
            frame:
                background lhtl_panel(LHTL_QUICK_BG, LHTL_PANEL_EDGE)
                padding (10, 6)
                hbox:
                    spacing 10
                    textbutton "回溯" action Rollback()
                    textbutton "紀錄" action ShowMenu("history")
                    textbutton "節奏" action ShowMenu("text_speed")
                    textbutton "存檔" action ShowMenu("save")
                    textbutton "讀檔" action ShowMenu("load")
                    textbutton "章節" action Show("chapter_select")
                    textbutton "選單" action ShowMenu("preferences")

screen main_menu():
    tag menu
    add Solid(LHTL_BG)
    frame:
        background Solid("#18140F99")
        ysize 220
        ypos 0
        xfill True
    frame:
        background Solid(LHTL_ACCENT_GLOW)
        ysize 3
        ypos 218
        xfill True

    frame:
        xalign 0.5
        yalign 0.52
        background lhtl_panel()
        padding (56, 40)

        vbox:
            spacing 12
            text "Learn How to Love" size gui.title_text_size color LHTL_TEXT xalign 0.5 outlines [(1, "#00000066", 0, 1)]
            text "學會去愛" size gui.notify_text_size color LHTL_ACCENT xalign 0.5
            frame:
                background Solid(LHTL_ACCENT)
                ysize 2
                xsize 140
                xalign 0.5
            text "Ch1 Trust｜Week 0 · Day 1～7" size gui.interface_text_size color LHTL_TEXT_SOFT xalign 0.5
            null height 10
            textbutton "開始遊戲" action Start() xalign 0.5
            textbutton "選擇章節（Week／Day）" action Show("chapter_select") xalign 0.5
            textbutton "讀取進度" action ShowMenu("load") xalign 0.5
            textbutton "設定" action ShowMenu("preferences") xalign 0.5
            textbutton "離開" action Quit(confirm=True) xalign 0.5


## —— 章節：先選 Week，再選 Day ——
screen chapter_select():
    modal True
    zorder 400
    add Solid(LHTL_OVERLAY)

    key "K_ESCAPE" action Hide("chapter_select")

    frame:
        xalign 0.5
        yalign 0.5
        background lhtl_panel()
        padding (40, 28)
        xsize 600

        vbox:
            spacing 10
            xfill True

            text "選擇章節" size gui.label_text_size color LHTL_TEXT xalign 0.5
            text "先選 Week，再選 Day" size gui.notify_text_size color LHTL_TEXT_SOFT xalign 0.5

            frame:
                background Solid(LHTL_ACCENT_DIM)
                ysize 1
                xfill True

            ## Week 列（未開放也可點，下方會顯示提示）
            hbox:
                spacing 8
                xalign 0.5
                for wid, wtitle, wready in week_tab_rows():
                    if chapter_week_id == wid:
                        textbutton wtitle:
                            text_color LHTL_ACCENT
                            action SetChapterWeek(wid)
                    else:
                        textbutton wtitle:
                            text_color (LHTL_TEXT if wready else LHTL_TEXT_MUTED)
                            action SetChapterWeek(wid)

            text week_subtitle(chapter_week_id) size 16 color LHTL_TEXT_MUTED xalign 0.5 font "SourceHanSansLite.ttf"

            frame:
                background Solid(LHTL_ACCENT_DIM)
                ysize 1
                xfill True

            ## Day 列表（不用 viewport 嵌套 dict，避免空白）
            if not week_is_ready(chapter_week_id):
                null height 12
                text "此週尚未開放。" size 18 color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"
                null height 12
            elif not week_day_rows(chapter_week_id):
                null height 12
                text "此週尚無章節。" size 18 color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"
                null height 12
            else:
                vbox:
                    spacing 8
                    xfill True
                    for day_num, day_title, day_label, day_ready in week_day_rows(chapter_week_id):
                        if day_ready and day_label:
                            textbutton day_title:
                                xfill True
                                text_xalign 0.5
                                action StartChapterDay(day_num, day_label)
                        else:
                            textbutton day_title + "（尚未實作）":
                                xfill True
                                text_xalign 0.5
                                text_color LHTL_TEXT_SOFT
                                action NullAction()

            null height 6
            textbutton "關閉" action Hide("chapter_select") xalign 0.5


## —— 知識小遊戲 HUD ——
screen knowledge_hud():
    zorder 120
    frame:
        xalign 0.5
        ypos 24
        background lhtl_panel()
        padding (20, 10)
        text "[knowledge_hud_title]  [knowledge_correct_today]／5" size 20 color LHTL_ACCENT font "SourceHanSansLite.ttf"

## —— 信任小遊戲：等待條（不可點狗＝點失敗區）——
screen tg_space_feed_wait(seconds=4.0):
    modal True
    zorder 150

    frame:
        xalign 0.5
        yalign 0.22
        background lhtl_panel()
        padding (28, 18)
        vbox:
            spacing 10
            text "把空間留給[dog_label]……" size 22 color LHTL_TEXT xalign 0.5 font "SourceHanSansLite.ttf"
            text "倒數中，不要伸手。" size 18 color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"
            bar:
                value AnimatedValue(value=1.0, range=1.0, delay=seconds)
                xmaximum 360
                ysize 14
                xalign 0.5

    ## 點狗區域＝失敗（對齊 dog_bottom 偏下位置）
    button:
        xalign 0.5
        yalign 0.78
        xysize (480, 300)
        background Solid("#00000001")
        action Return("fail")
        text "（這裡是[dog_label]——別點）" size 16 color LHTL_TEXT_MUTED xalign 0.5 yalign 0.92 font "SourceHanSansLite.ttf"

    textbutton "忍住，繼續等":
        xalign 0.5
        yalign 0.94
        action NullAction()

    timer seconds action Return("success")


## —— 信任小遊戲：溫柔聲＋焦慮條 ——
screen tg_soft_voice_bar(level=0.7):
    zorder 120
    frame:
        xalign 0.5
        ypos 24
        background lhtl_panel()
        padding (20, 10)
        vbox:
            spacing 6
            text "焦慮" size 16 color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"
            bar:
                value level
                range 1.0
                xmaximum 280
                ysize 12
                xalign 0.5


## Ren'Py 預設選單殼（精簡）
screen save():
    tag menu
    use file_slots(_("存檔"))

screen load():
    tag menu
    use file_slots(_("讀檔"))

screen file_slots(title):
    default page = 1
    add Solid(LHTL_OVERLAY)
    frame:
        xalign 0.5
        yalign 0.5
        background lhtl_panel()
        padding (40, 28)
        vbox:
            spacing 12
            text title size 28 color LHTL_TEXT xalign 0.5
            for i in range(1, 7):
                $ slot = i + (page - 1) * 6
                button:
                    xfill True
                    action FileAction(slot)
                    frame:
                        background lhtl_panel(LHTL_PANEL_ALT, LHTL_PANEL_EDGE)
                        padding (12, 10)
                        hbox:
                            spacing 12
                            text FileTime(slot, empty=_("空欄位")) size 18 color LHTL_TEXT_SOFT
                            text FileSaveName(slot) size 18 color LHTL_TEXT_MUTED
            textbutton "返回" action Return() xalign 0.5

screen preferences():
    tag menu
    add Solid(LHTL_OVERLAY)
    frame:
        xalign 0.5
        yalign 0.5
        background lhtl_panel()
        padding (40, 28)
        xmaximum 560
        vbox:
            spacing 14
            text "設定" size 28 color LHTL_TEXT xalign 0.5

            text "字幕節奏：[text_speed_label()]" size 18 color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"
            hbox:
                spacing 10
                xalign 0.5
                for name, cps in TEXT_SPEED_PRESETS:
                    textbutton name:
                        selected (preferences.text_cps == cps)
                        action Function(apply_text_speed, cps)

            label _("細調文字速度")
            bar value Preference("text speed")

            label _("自動前進時間")
            bar value Preference("auto-forward time")

            label _("音樂音量")
            bar value Preference("music volume")
            label _("音效音量")
            bar value Preference("sound volume")
            textbutton "返回" action Return() xalign 0.5


screen text_speed():
    tag menu
    modal True
    zorder 300
    add Solid(LHTL_OVERLAY)

    frame:
        xalign 0.5
        yalign 0.5
        background lhtl_panel()
        padding (40, 32)
        xmaximum 520

        vbox:
            spacing 12
            text "字幕節奏" size gui.label_text_size color LHTL_TEXT xalign 0.5
            frame:
                background Solid(LHTL_ACCENT_DIM)
                ysize 1
                xsize 180
                xalign 0.5
            text "預設「適讀」：跟得上敘事、不必急著點" size gui.notify_text_size color LHTL_TEXT_MUTED xalign 0.5 font "SourceHanSansLite.ttf"
            text "目前：[text_speed_label()]" size gui.interface_text_size color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"

            hbox:
                spacing 10
                xalign 0.5
                for name, cps in TEXT_SPEED_PRESETS:
                    textbutton name:
                        selected (preferences.text_cps == cps)
                        action Function(apply_text_speed, cps)

            null height 8
            textbutton "關閉" action Return() xalign 0.5

screen history():
    tag menu
    predict False
    add Solid(LHTL_OVERLAY)
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 520
        background lhtl_panel()
        padding (28, 22)
        viewport:
            scrollbars "vertical"
            mousewheel True
            draggable True
            vbox:
                spacing 10
                for h in _history_list:
                    if h.who:
                        text h.who size 16 color LHTL_ACCENT
                    text h.what size 18 color LHTL_TEXT_SOFT
                if not _history_list:
                    text "尚無紀錄。" size 18 color LHTL_TEXT_MUTED
        textbutton "關閉" action Return() xalign 0.5

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid(LHTL_OVERLAY)
    frame:
        xalign 0.5
        yalign 0.5
        background lhtl_panel()
        padding (36, 28)
        vbox:
            spacing 16
            text message size 20 color LHTL_TEXT xalign 0.5
            hbox:
                spacing 24
                xalign 0.5
                textbutton "是" action yes_action
                textbutton "否" action no_action

screen notify(message):
    zorder 100
    text message:
        xpos 0.5
        xanchor 0.5
        ypos 0.08
        size 18
        color LHTL_ACCENT
        outlines [(1, "#00000088", 0, 1)]
    timer 2.25 action Hide("notify")

screen skip_indicator():
    zorder 100
    text "略過中……":
        xpos 0.5
        xanchor 0.5
        ypos 0.06
        size 16
        color LHTL_TEXT_MUTED

## —— Day2 隱藏知識｜5 選 4（狗不能吃的）——
screen kg_toxic_food_pick():
    modal True
    zorder 160
    key "game_menu" action NullAction()
    add Solid(LHTL_OVERLAY)

    frame:
        xalign 0.5
        yalign 0.42
        background lhtl_panel()
        padding (32, 26)
        xsize 520
        vbox:
            spacing 12
            xfill True
            text "隱藏知識｜哪些東西狗狗不能吃" size 22 color LHTL_ACCENT xalign 0.5 font "SourceHanSansLite.ttf"
            text "請點選 4 樣不能給狗吃的（已選 [toxic_food_pick_count()]／4）" size 17 color LHTL_TEXT_SOFT xalign 0.5 font "SourceHanSansLite.ttf"
            null height 4
            for key, food_name, _bad in TOXIC_FOOD_CHOICES:
                button:
                    xfill True
                    action Function(toggle_toxic_food, key)
                    padding (14, 10)
                    if toxic_food_is_picked(key):
                        background Solid(LHTL_ACCENT_DIM)
                        hover_background Solid(LHTL_ACCENT)
                        text ("✓ " + food_name) size 19 color LHTL_TEXT font "SourceHanSansLite.ttf"
                    else:
                        background Solid(LHTL_PANEL_ALT)
                        hover_background Solid(LHTL_PANEL_HOVER)
                        text food_name size 19 color LHTL_TEXT font "SourceHanSansLite.ttf"
            null height 6
            if toxic_food_pick_count() == 4:
                textbutton "確認這 4 樣":
                    xalign 0.5
                    action Return("submit")
            else:
                text "選滿 4 樣才能確認" size 16 color LHTL_TEXT_MUTED xalign 0.5 font "SourceHanSansLite.ttf"


## —— 寵物店取名 ——
screen dog_name_input():
    modal True
    zorder 200
    key "game_menu" action NullAction()
    key "K_RETURN" action [Function(confirm_dog_name), Return()]
    key "K_KP_ENTER" action [Function(confirm_dog_name), Return()]
    add Solid(LHTL_OVERLAY)
    frame:
        xalign 0.5
        yalign 0.5
        background lhtl_panel()
        padding (40, 36)
        xsize 420
        vbox:
            spacing 14
            xfill True
            text "替小狗狗取名字吧" size gui.label_text_size color LHTL_TEXT xalign 0.5
            frame:
                background Solid(LHTL_ACCENT_DIM)
                ysize 1
                xsize 140
                xalign 0.5
            text "最多 10 個字（空白＝布丁）" size gui.notify_text_size color LHTL_TEXT_MUTED xalign 0.5
            frame:
                xalign 0.5
                xsize 280
                background Solid(LHTL_PANEL_ALT)
                padding (12, 10)
                input:
                    value VariableInputValue("dog_name")
                    length 10
                    xalign 0.5
                    xsize 256
                    color LHTL_TEXT
                    copypaste True
            textbutton "確定" action [Function(confirm_dog_name), Return()] xalign 0.5
