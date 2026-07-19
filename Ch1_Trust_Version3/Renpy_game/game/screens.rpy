## Version3 精簡繁中 UI

screen say(who, what):
    style_prefix "say"
    zorder 100

    window:
        id "window"

        vbox:
            spacing 8
            if who is not None:
                text who id "who"
            text what id "what":
                xmaximum gui.dialogue_width

    use quick_menu


screen choice(items):
    style_prefix "choice"
    zorder 110

    frame:
        background Solid("#17120F88")
        xfill True
        yfill True

        vbox:
            spacing 18
            xalign 0.5
            yalign 0.47

            for i in items:
                textbutton i.caption action i.action


## renpy.input() 必需的內建畫面（S05 幫小7取名會用到）
screen input(prompt):
    style_prefix "input"
    zorder 120
    modal True

    add Solid("#17120F88")

    frame:
        background Solid(LHTL_PANEL)
        padding (42, 30)
        xalign 0.5
        yalign 0.45
        xminimum 560

        vbox:
            spacing 18
            xalign 0.5

            text prompt:
                font CJK_FONT
                size 23
                color LHTL_TEXT
                xalign 0.5

            input id "input":
                font CJK_FONT
                size 26
                color LHTL_ACCENT_DARK
                xalign 0.5

            text "輸入後按 Enter 確認":
                font CJK_FONT
                size 15
                color "#806C5B"
                xalign 0.5


screen quick_menu():
    zorder 200

    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.98
            yalign 0.025
            spacing 7

            textbutton "回溯" action Rollback()
            textbutton "紀錄" action ShowMenu("history")
            textbutton "存檔" action ShowMenu("save")
            textbutton "讀檔" action ShowMenu("load")
            textbutton "設定" action ShowMenu("preferences")


screen main_menu():
    tag menu

    ## 主視覺：assets/theme/title-main.png 存在時使用（MJ 產出），否則退回純色
    add optional_background("theme/title-main.png", "#17120F")
    add Solid("#B77A4518")

    frame:
        background Solid("#F3E9D9EE")
        padding (64, 44)
        xalign 0.5
        yalign 0.52

        vbox:
            spacing 14
            xalign 0.5

            text "Learn How to Love":
                font CJK_FONT
                size gui.title_text_size
                color LHTL_TEXT
                xalign 0.5

            text "Ch1 Trust｜學會靠近":
                font CJK_FONT
                size 22
                color LHTL_ACCENT_DARK
                xalign 0.5

            text "Section 01–10｜從相遇到把背交給彼此":
                font CJK_FONT
                size 17
                color "#806C5B"
                xalign 0.5

            null height 12
            textbutton "開始" style "menu_button" action Start()
            textbutton "章節選擇" style "menu_button" action ShowMenu("section_select")
            textbutton "讀取進度" style "menu_button" action ShowMenu("load")
            textbutton "設定" style "menu_button" action ShowMenu("preferences")
            textbutton "離開" style "menu_button" action Quit(confirm=False)


screen section_select():
    tag menu

    ## 選單底圖：牆鉤上的鑰匙與牽繩（theme/menu-bg.png），缺檔退回深棕
    add optional_background("theme/menu-bg.png", "#17120F")
    add Solid("#17120F26")

    default section_entries = [
        ("start_section_01", "Section 01｜螢幕光比月亮亮", "予安習慣獨自度過加班的夜，直到店員提起後門那隻沒力氣的小狗。"),
        ("start_section_02", "Section 02｜後門那一瞥", "她終於轉進後門，看見小7，也第一次試著在害怕面前放慢腳步。"),
        ("start_section_03", "Section 03｜樓梯間的臨時國界", "一句「今晚不算數」把牠留在樓梯間；她上樓之後，卻還是回頭了。"),
        ("start_section_04", "Section 04｜共享同一種安靜", "沙發與地板隔著兩步，他們不急著靠近，只練習在同一份安靜裡留下。"),
        ("start_section_05", "Section 05｜你的聲音有兩種", "戴上耳機後，予安的聲音變得又快又尖；小7開始分辨，哪一種聲音會為牠慢下來。"),
        ("start_section_06", "Section 06｜走廊上的第三者", "當陌生人的手伸向小7，予安第一次發現，自己已經站進了「我們」這一邊。"),
        ("start_section_07", "Section 07｜她倒下的那天", "予安病得起不了身，小7不懂怎麼照顧人，只知道守在門口，試著等她回應。"),
        ("start_section_08", "Section 08｜走到轉角就好", "第一次出門只為抵達巷口；世界太吵時，予安得決定要拉著牠，還是一起停下。"),
        ("start_section_09", "Section 09｜差點交給別人", "同事真誠提出接手；在牽繩交出去以前，予安必須承認誰已經選過誰。"),
        ("start_section_10", "Section 10｜把鑰匙分給心跳", "鑰匙與牽繩掛在同一面牆上；夜深後，睡眠的距離替這段關係留下答案。"),
    ]

    frame:
        background Solid("#F3E9D9EE")
        padding (34, 18)
        xalign 0.5
        yalign 0.5
        xsize 1210

        vbox:
            spacing 10
            xfill True

            hbox:
                xfill True
                text "章節選擇":
                    font CJK_FONT
                    size gui.label_text_size
                    color LHTL_TEXT
                null width 1 xfill True
                textbutton "返回" style "menu_button" action ShowMenu("main_menu")

            text "選擇章節會以該段的預設狀態開始，不影響既有存檔。":
                font CJK_FONT
                size 16
                color "#806C5B"

            # 兩欄網格一次顯示 S01～S10，不需捲動。
            grid 2 5:
                spacing 8
                xalign 0.5

                for entry_label, entry_title, entry_summary in section_entries:
                    button:
                        background Solid("#E8D9C5")
                        hover_background Solid("#D9BE9D")
                        padding (18, 8)
                        xsize 560
                        ysize 96
                        action Start(entry_label)

                        vbox:
                            spacing 4
                            text entry_title:
                                font CJK_FONT
                                size 19
                                color LHTL_TEXT
                            text entry_summary:
                                font CJK_FONT
                                size 14
                                color "#806C5B"


screen game_menu(title):
    tag menu

    add optional_background("theme/menu-bg.png", "#17120F")
    add Solid("#17120F26")

    ## 面板靠左，讓右側牆鉤（鑰匙＋牽繩）主題視覺露出
    frame:
        background Solid("#F3E9D9EE")
        padding (46, 32)
        xalign 0.06
        yalign 0.5
        xsize 1060
        ysize 610

        vbox:
            spacing 18
            xfill True

            hbox:
                xfill True
                text title:
                    font CJK_FONT
                    size gui.label_text_size
                    color LHTL_TEXT
                null width 1 xfill True
                textbutton "返回" style "menu_button" action Return()

            transclude


screen save():
    tag menu
    use game_menu("存檔"):
        use file_slots


screen load():
    tag menu
    use game_menu("讀檔"):
        use file_slots


screen file_slots():
    grid 3 2:
        spacing 18
        xalign 0.5
        yalign 0.5

        for slot in range(1, 7):
            button:
                background Solid("#E8D9C5")
                hover_background Solid("#D9BE9D")
                xsize 290
                ysize 180
                padding (18, 14)
                action FileAction(slot)

                vbox:
                    spacing 9
                    text "存檔 [slot]":
                        font CJK_FONT
                        size 21
                        color LHTL_TEXT
                    text FileTime(slot, format="%Y-%m-%d  %H:%M", empty="空白"):
                        font CJK_FONT
                        size 16
                        color "#806C5B"
                    if FileSaveName(slot):
                        vbox:
                            spacing 3
                            text "章節":
                                font CJK_FONT
                                size 13
                                color LHTL_ACCENT_DARK
                            text FileSaveName(slot):
                                font CJK_FONT
                                size 15
                                color "#806C5B"


screen preferences():
    tag menu

    use game_menu("設定"):
        hbox:
            spacing 60
            xalign 0.5
            yalign 0.40

            ## 左欄：閱讀
            vbox:
                spacing 24
                xsize 430

                vbox:
                    spacing 12
                    text "文字速度":
                        font CJK_FONT
                        size 22
                        color LHTL_TEXT
                    hbox:
                        spacing 10
                        textbutton "慢" style "pref_button" action Preference("text speed", 20)
                        textbutton "標準" style "pref_button" action Preference("text speed", 30)
                        textbutton "快" style "pref_button" action Preference("text speed", 50)

                vbox:
                    spacing 12
                    text "自動前進等待":
                        font CJK_FONT
                        size 22
                        color LHTL_TEXT
                    bar value Preference("auto-forward time") style "lhtl_slider"

                vbox:
                    spacing 12
                    text "顯示模式":
                        font CJK_FONT
                        size 22
                        color LHTL_TEXT
                    hbox:
                        spacing 10
                        textbutton "視窗" style "pref_button" action Preference("display", "window")
                        textbutton "全螢幕" style "pref_button" action Preference("display", "fullscreen")

            ## 右欄：聲音
            vbox:
                spacing 24
                xsize 430

                vbox:
                    spacing 12
                    text "音樂音量":
                        font CJK_FONT
                        size 22
                        color LHTL_TEXT
                    bar value Preference("music volume") style "lhtl_slider"

                vbox:
                    spacing 12
                    text "音效音量":
                        font CJK_FONT
                        size 22
                        color LHTL_TEXT
                    bar value Preference("sound volume") style "lhtl_slider"

                textbutton "音樂靜音切換" style "pref_button" action Preference("music mute", "toggle")

                null height 6
                textbutton "返回主選單" style "pref_button" action MainMenu()


style lhtl_slider is slider:
    xsize 380
    ysize 24
    left_bar Solid("#B77A45")
    right_bar Solid("#E0D2BC")
    thumb Transform(Solid("#7A4E2E"), xysize=(10, 24))
    thumb_offset 5


style pref_button is menu_button:
    xminimum 120
    padding (20, 10)

style pref_button_text is menu_button_text:
    size 19


screen history():
    tag menu

    use game_menu("對話紀錄"):
        viewport:
            mousewheel True
            draggable True
            scrollbars "vertical"
            xfill True
            yfill True

            vbox:
                spacing 16
                xfill True

                for h in _history_list:
                    vbox:
                        spacing 4
                        if h.who:
                            text h.who:
                                font CJK_FONT
                                size 19
                                color LHTL_ACCENT_DARK
                        text h.what:
                            font CJK_FONT
                            size 20
                            color LHTL_TEXT
                            xmaximum 920


screen confirm(message, yes_action, no_action):
    modal True
    zorder 300
    add Solid("#17120FCC")

    frame:
        background Solid(LHTL_PANEL)
        padding (42, 32)
        xalign 0.5
        yalign 0.5

        vbox:
            spacing 22
            text message:
                font CJK_FONT
                size 22
                color LHTL_TEXT
                xalign 0.5
            hbox:
                spacing 16
                xalign 0.5
                textbutton "確定" style "menu_button" action yes_action
                textbutton "取消" style "menu_button" action no_action


screen notify(message):
    zorder 400
    frame at notify_appear:
        background Solid("#2E241FDD")
        padding (18, 10)
        xalign 0.98
        yalign 0.10
        text message:
            font CJK_FONT
            size 17
            color LHTL_TEXT_LIGHT
    timer 3.0 action Hide("notify")


transform notify_appear:
    alpha 0.0
    linear 0.2 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0


screen skip_indicator():
    zorder 100
    text "略過中":
        font CJK_FONT
        size 17
        color LHTL_TEXT_LIGHT
        xalign 0.98
        yalign 0.10
