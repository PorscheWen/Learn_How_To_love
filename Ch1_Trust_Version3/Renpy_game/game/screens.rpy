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
            spacing 14

            ## 閱讀
            hbox:
                spacing 7
                textbutton "回溯" action Rollback()
                textbutton "紀錄" action ShowMenu("history")

            ## 進度
            hbox:
                spacing 7
                textbutton "存檔" action ShowMenu("save")
                textbutton "讀檔" action ShowMenu("load")

            ## 系統
            hbox:
                spacing 7
                textbutton "設定" action ShowMenu("preferences")


screen main_menu():
    tag menu

    ## 主視覺：theme/title-main.png；缺檔退回深棕
    add "lhtl_title_bg"
    add Solid("#B77A4518")

    frame:
        background Solid("#F3E9D9EE")
        padding (64, 44)
        xalign 0.5
        yalign 0.52

        vbox:
            spacing 10
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

            null height 14

            ## 遊玩
            textbutton "開始" style "menu_button" action Start()
            textbutton "讀取進度" style "menu_button" action ShowMenu("load")

            null height 8

            ## 章節／結局
            textbutton "章節選擇" style "menu_button" action ShowMenu("section_select")
            textbutton "結局一覽" style "menu_button" action ShowMenu("ending_gallery")
            textbutton "隱藏內容" style "menu_button" action ShowMenu("hidden_content_gallery")

            null height 8

            ## 系統
            textbutton "設定" style "menu_button" action ShowMenu("preferences")
            textbutton "離開" style "menu_button" action Quit(confirm=False)


screen ending_gallery():
    tag menu

    ## 選單底圖：theme/menu-bg.png；項目半透明嵌在牆面，右側牆鉤露出
    add "lhtl_menu_bg"

    ## 只顯示已解鎖標題；未解鎖不劇透內容。
    default ending_rows = [
        ("A", "結局 A｜背靠"),
        ("B", "結局 B｜選定但還在學"),
        ("C", "結局 C｜送走之後"),
        ("D", "結局 D｜薄冰同住"),
    ]

    frame:
        background Solid(LHTL_MENU_SHELL)
        padding (40, 28)
        xalign 0.06
        yalign 0.5
        xsize 760
        ysize 610

        side "t c b":
            xfill True
            spacing 12

            vbox:
                spacing 8
                xfill True
                text "結局一覽":
                    font CJK_FONT
                    size gui.label_text_size
                    color LHTL_TEXT_LIGHT
                text "達成後解鎖標題。未解鎖不顯示內容。":
                    font CJK_FONT
                    size 16
                    color LHTL_TEXT_SOFT

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xfill True
                ymaximum 420

                vbox:
                    spacing 10
                    xfill True
                    for ending_id, title in ending_rows:
                        if ending_unlocked(ending_id):
                            frame:
                                background Solid(LHTL_MENU_ITEM)
                                padding (18, 12)
                                xfill True
                                text "✓  " + title:
                                    font CJK_FONT
                                    size 22
                                    color LHTL_TEXT
                        else:
                            frame:
                                background Solid(LHTL_MENU_ITEM)
                                padding (18, 12)
                                xfill True
                                text "○  結局 " + ending_id + "｜尚未解鎖":
                                    font CJK_FONT
                                    size 22
                                    color "#806C5B"

                    text "已解鎖 " + str(len(persistent.unlocked_endings or [])) + "／4":
                        font CJK_FONT
                        size 16
                        color LHTL_TEXT_SOFT
                        xalign 1.0

                    null height 8

                    text "紀念照片":
                        font CJK_FONT
                        size 20
                        color LHTL_TEXT_LIGHT

                    if secret_photo_unlocked("lap_sleep"):
                        textbutton "✓  背靠｜中型幼犬躺在大腿特寫" style "embed_menu_button":
                            action Show("secret_photo_view", photo="lap_sleep")
                            xminimum 0
                            xfill True
                        text "真正把背交給彼此之後才看得到。":
                            font CJK_FONT
                            size 15
                            color LHTL_TEXT_SOFT
                    else:
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            text "○  ？？？｜尚未解鎖":
                                font CJK_FONT
                                size 22
                                color "#806C5B"
                        text "有一段畫面，只有真正把背交給彼此之後才看得到。":
                            font CJK_FONT
                            size 15
                            color LHTL_TEXT_SOFT

            textbutton "返回" style "embed_menu_button" action Return():
                xalign 0.5


screen secret_photo_view(photo="lap_sleep"):
    modal True
    zorder 200

    ## 點畫面空白可關閉（底層）
    button:
        background None
        xfill True
        yfill True
        action Hide("secret_photo_view")

    if photo == "lap_sleep":
        add "gallery secret_lap_sleep"
    else:
        add Solid("#17120F")

    frame:
        background Solid("#17120FCC")
        padding (20, 12)
        xalign 0.5
        yalign 0.06
        text "紀念照片｜躺在大腿":
            font CJK_FONT
            size 20
            color "#F7EFE4"

    textbutton "關閉":
        style "menu_button"
        action Hide("secret_photo_view")
        xalign 0.5
        yalign 0.94


screen hidden_content_gallery():
    tag menu

    ## 隱藏內容菜單：角色小傳、結局後故事、信任軌跡
    add "lhtl_menu_bg"

    frame:
        background Solid(LHTL_MENU_SHELL)
        padding (40, 28)
        xalign 0.06
        yalign 0.5
        xsize 760
        ysize 610

        side "t c b":
            xfill True
            spacing 12

            vbox:
                spacing 8
                xfill True
                text "隱藏內容｜角色小傳與結局後故事":
                    font CJK_FONT
                    size 22
                    color LHTL_TEXT_LIGHT
                text "完成各結局後，會解鎖該路線的角色心境回顧。":
                    font CJK_FONT
                    size 16
                    color LHTL_TEXT_SOFT

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xfill True
                ymaximum 420

                vbox:
                    spacing 10
                    xfill True

                    ## 結局 A 內容
                    if secret_content_unlocked("character_aftercare_a"):
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            vbox:
                                spacing 6
                                text "✓  結局 A｜背靠 — 角色小傳":
                                    font CJK_FONT
                                    size 19
                                    color LHTL_TEXT
                                text "信任的完整落地。她在辦公室反覆看著那張照片，想著 Ch2 會開始的日常……":
                                    font CJK_FONT
                                    size 15
                                    color LHTL_TEXT_SOFT
                    else:
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            text "○  結局 A｜背靠 — 尚未解鎖":
                                font CJK_FONT
                                size 19
                                color "#806C5B"

                    ## 結局 B 內容
                    if secret_content_unlocked("character_aftercare_b"):
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            vbox:
                                spacing 6
                                text "✓  結局 B｜選定但還在學 — 角色小傳":
                                    font CJK_FONT
                                    size 19
                                    color LHTL_TEXT
                                text "真實好結局的樣子。每一天都在選擇相信，不是完美，而是持續……":
                                    font CJK_FONT
                                    size 15
                                    color LHTL_TEXT_SOFT
                    else:
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            text "○  結局 B｜選定但還在學 — 尚未解鎖":
                                font CJK_FONT
                                size 19
                                color "#806C5B"

                    ## 結局 C 內容
                    if secret_content_unlocked("character_aftercare_c"):
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            vbox:
                                spacing 6
                                text "✓  結局 C｜送走之後 — 角色小傳":
                                    font CJK_FONT
                                    size 19
                                    color LHTL_TEXT
                                text "放手也是愛。她沒有失敗，只是誠實地承認「我還不夠」……":
                                    font CJK_FONT
                                    size 15
                                    color LHTL_TEXT_SOFT
                    else:
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            text "○  結局 C｜送走之後 — 尚未解鎖":
                                font CJK_FONT
                                size 19
                                color "#806C5B"

                    ## 結局 D 內容
                    if secret_content_unlocked("character_aftercare_d"):
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            vbox:
                                spacing 6
                                text "✓  結局 D｜薄冰同住 — 角色小傳":
                                    font CJK_FONT
                                    size 19
                                    color LHTL_TEXT
                                text "一夜一夜地去承擔風險。因為信任不是給完美者的……":
                                    font CJK_FONT
                                    size 15
                                    color LHTL_TEXT_SOFT
                    else:
                        frame:
                            background Solid(LHTL_MENU_ITEM)
                            padding (18, 12)
                            xfill True
                            text "○  結局 D｜薄冰同住 — 尚未解鎖":
                                font CJK_FONT
                                size 19
                                color "#806C5B"

                    null height 8

                    text "已解鎖隱藏內容 " + str(len([c for c in ["character_aftercare_a", "character_aftercare_b", "character_aftercare_c", "character_aftercare_d"] if secret_content_unlocked(c)])) + "／4":
                        font CJK_FONT
                        size 16
                        color LHTL_TEXT_SOFT
                        xalign 1.0

            textbutton "返回" style "embed_menu_button" action Return():
                xalign 0.5


screen section_select():
    tag menu

    ## 選單底圖：theme/menu-bg.png；章節卡半透明嵌牆，右側牆鉤露出
    add "lhtl_menu_bg"

    default section_entries = [
        ("start_section_01", "Section 01｜螢幕光比月亮亮", "予安習慣獨自度過加班的夜，直到店員提起後門那隻沒力氣的小狗。"),
        ("start_section_02", "Section 02｜後門那一瞥", "她終於轉進後門，看見小7，也第一次試著在害怕面前放慢腳步。"),
        ("start_section_03", "Section 03｜大門的臨時國界", "牠在大門外睡著；她不忍心，開門把牠帶回屋內直到天明。"),
        ("start_section_04", "Section 04｜共享同一種安靜", "沙發與地板隔著兩步，他們不急著靠近，只練習在同一份安靜裡留下。"),
        ("start_section_05", "Section 05｜你的聲音有兩種", "戴上耳機後，予安的聲音變得又快又尖；小7開始分辨，哪一種聲音會為牠慢下來。"),
        ("start_section_06", "Section 06｜走廊上的第三者", "當陌生人的手伸向小7，予安第一次發現，自己已經站進了「我們」這一邊。"),
        ("start_section_07", "Section 07｜她倒下的那天", "予安病得起不了身，小7不懂怎麼照顧人，只知道守在門口，試著等她回應。"),
        ("start_section_08", "Section 08｜走到轉角就好", "第一次出門只為抵達巷口；世界太吵時，予安得決定要拉著牠，還是一起停下。"),
        ("start_section_09", "Section 09｜差點交給別人", "同事真誠提出接手；在牽繩交出去以前，予安必須承認誰已經選過誰。"),
        ("start_section_10", "Section 10｜把鑰匙分給心跳", "鑰匙與牽繩掛在同一面牆上；夜深後，睡眠的距離替這段關係留下答案。"),
    ]

    frame:
        background Solid(LHTL_MENU_SHELL)
        padding (28, 16)
        xalign 0.04
        yalign 0.5
        xsize 980
        ysize 640

        side "t c b":
            xfill True
            spacing 10

            vbox:
                spacing 6
                xfill True
                text "章節選擇":
                    font CJK_FONT
                    size gui.label_text_size
                    color LHTL_TEXT_LIGHT
                text "選擇章節會以該段的預設狀態開始，不影響既有存檔。":
                    font CJK_FONT
                    size 16
                    color LHTL_TEXT_SOFT

            # 兩欄網格一次顯示 S01～S10；半透明卡嵌在牆面紋理上。
            grid 2 5:
                spacing 8
                xalign 0.0

                for entry_label, entry_title, entry_summary in section_entries:
                    button:
                        background Solid(LHTL_MENU_ITEM)
                        hover_background Solid(LHTL_MENU_ITEM_HOVER)
                        padding (14, 6)
                        xsize 450
                        ysize 86
                        action Start(entry_label)

                        vbox:
                            spacing 3
                            text entry_title:
                                font CJK_FONT
                                size 17
                                color LHTL_TEXT
                            text entry_summary:
                                font CJK_FONT
                                size 12
                                color "#806C5B"

            textbutton "返回" style "embed_menu_button" action ShowMenu("main_menu"):
                xalign 0.5


screen game_menu(title):
    tag menu

    ## 選單底圖：theme/menu-bg.png；半透明殼＋項目嵌牆，右側牆鉤露出
    add "lhtl_menu_bg"

    ## side t/c/b：標題／內容／返回各佔一區，避免返回被 yfill 擠出外框
    frame:
        background Solid(LHTL_MENU_SHELL)
        padding (40, 24)
        xalign 0.05
        yalign 0.5
        xsize 980
        ysize 610

        side "t c b":
            xfill True
            yfill True
            spacing 14

            text title:
                font CJK_FONT
                size gui.label_text_size
                color LHTL_TEXT_LIGHT

            frame:
                background None
                padding (0, 0)
                xfill True
                yfill True
                transclude

            textbutton "返回" style "embed_menu_button" action Return():
                xalign 0.5


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
        spacing 16
        xalign 0.5
        yalign 0.5

        for slot in range(1, 7):
            button:
                background Solid(LHTL_MENU_ITEM)
                hover_background Solid(LHTL_MENU_ITEM_HOVER)
                xsize 280
                ysize 180
                padding (16, 12)
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
        vbox:
            spacing 28
            xalign 0.5
            yalign 0.35

            hbox:
                spacing 60
                xalign 0.5

                ## 左欄：閱讀／顯示
                vbox:
                    spacing 24
                    xsize 430

                    vbox:
                        spacing 12
                        text "文字速度":
                            font CJK_FONT
                            size 22
                            color LHTL_TEXT_LIGHT
                        hbox:
                            spacing 10
                            textbutton "慢" style "embed_pref_button" action Preference("text speed", 20)
                            textbutton "標準" style "embed_pref_button" action Preference("text speed", 30)
                            textbutton "快" style "embed_pref_button" action Preference("text speed", 50)

                    vbox:
                        spacing 12
                        text "自動前進等待":
                            font CJK_FONT
                            size 22
                            color LHTL_TEXT_LIGHT
                        bar value Preference("auto-forward time") style "lhtl_slider"

                    vbox:
                        spacing 12
                        text "顯示模式":
                            font CJK_FONT
                            size 22
                            color LHTL_TEXT_LIGHT
                        hbox:
                            spacing 10
                            textbutton "視窗" style "embed_pref_button" action Preference("display", "window")
                            textbutton "全螢幕" style "embed_pref_button" action Preference("display", "fullscreen")

                ## 右欄：聲音
                vbox:
                    spacing 24
                    xsize 430

                    vbox:
                        spacing 12
                        text "音樂音量":
                            font CJK_FONT
                            size 22
                            color LHTL_TEXT_LIGHT
                        bar value Preference("music volume") style "lhtl_slider"

                    vbox:
                        spacing 12
                        text "音效音量":
                            font CJK_FONT
                            size 22
                            color LHTL_TEXT_LIGHT
                        bar value Preference("sound volume") style "lhtl_slider"

                    textbutton "音樂靜音切換" style "embed_pref_button" action Preference("music mute", "toggle")

            ## 系統
            textbutton "返回主選單" style "embed_pref_button" action MainMenu():
                xalign 0.5


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

style embed_pref_button is embed_menu_button:
    xminimum 120
    padding (20, 10)

style embed_pref_button_text is embed_menu_button_text:
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
                    frame:
                        background Solid(LHTL_MENU_ITEM)
                        padding (16, 10)
                        xfill True
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
                                xmaximum 860


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
