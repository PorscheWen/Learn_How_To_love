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

    ## 主視覺：theme/title-main.png；缺圖退回深色 → 面板文字須用亮色
    add "lhtl_title_bg"
    add Solid("#17120F22")

    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (32, 24)
        xalign 0.5
        yalign 0.5
        xsize 420

        vbox:
            spacing 0
            xalign 0.5
            xfill True

            text "Learn How to Love":
                font CJK_FONT
                size 26
                color LHTL_TEXT_LIGHT
                xalign 0.5
                outlines [(2, "#17120F99", 0, 0)]

            text "Ch1 Trust｜學會靠近":
                font CJK_FONT
                size 14
                color LHTL_TEXT_SOFT
                xalign 0.5
                outlines [(1, "#17120F66", 0, 0)]

            null height 14

            text "遊玩":
                font CJK_FONT
                size 13
                color LHTL_TEXT_SOFT
                xalign 0.0

            null height 6

            textbutton "開始" style "menu_primary_button" action Start():
                xfill True
            null height 6
            textbutton "讀取進度" style "menu_button" action ShowMenu("load"):
                xfill True
            null height 6
            textbutton "章節選擇" style "menu_button" action ShowMenu("section_select"):
                xfill True

            null height 14

            text "收藏":
                font CJK_FONT
                size 13
                color LHTL_TEXT_SOFT
                xalign 0.0

            null height 6

            textbutton "結局一覽" style "menu_button" action ShowMenu("ending_gallery"):
                xfill True
            null height 6
            textbutton ("隱藏內容　新" if hidden_content_unread_count() > 0 else "隱藏內容") style "menu_button" action ShowMenu("hidden_content_gallery"):
                xfill True

            null height 16

            hbox:
                spacing 10
                xalign 0.5
                xfill True
                textbutton "設定" style "menu_back_button" action ShowMenu("preferences"):
                    xminimum 170
                textbutton "離開" style "menu_back_button" action Quit(confirm=False):
                    xminimum 170

    key "K_F8" action Function(dev_unlock_all_gallery)
    key "shift_K_u" action Function(dev_unlock_all_gallery)


screen ending_gallery():
    tag menu

    key "K_F8" action Function(dev_unlock_all_gallery)
    key "shift_K_u" action Function(dev_unlock_all_gallery)

    add "lhtl_menu_bg"
    add Solid("#17120F33")

    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (28, 20)
        xalign 0.05
        yalign 0.5
        xsize 760
        ysize 620

        side "t c b":
            xfill True
            yfill True
            spacing 10

            vbox:
                spacing 2
                xfill True
                text "結局一覽":
                    font CJK_FONT
                    size 24
                    color LHTL_TEXT_LIGHT
                    outlines [(2, "#17120F99", 0, 0)]
                text "點項目看大圖":
                    font CJK_FONT
                    size 13
                    color LHTL_TEXT_SOFT

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xfill True
                yfill True

                vbox:
                    spacing 8
                    xfill True

                    $ latest_run = latest_trajectory_summary()
                    if latest_run:
                        text "本輪旅程":
                            font CJK_FONT
                            size 14
                            color LHTL_TEXT_SOFT
                        frame:
                            background Solid("#F3E9D9CC")
                            padding (14, 10)
                            xfill True
                            vbox:
                                spacing 4
                                text latest_run[0]:
                                    font CJK_FONT
                                    size 16
                                    color "#4A3728"
                                text latest_run[1]:
                                    font CJK_FONT
                                    size 13
                                    color "#7A4E2E"
                        null height 4

                    text "結局":
                        font CJK_FONT
                        size 14
                        color LHTL_TEXT_SOFT

                    grid 2 2:
                        spacing 8
                        xfill True

                        textbutton "結局 A｜背靠" style "menu_list_button" action Function(open_gallery_image, "gallery/ending-a-back.png", "結局 A｜背靠"):
                            xsize 340
                        textbutton "結局 B｜選定但還在學" style "menu_list_button" action Function(open_gallery_image, "gallery/ending-b-learning.png", "結局 B｜選定但還在學"):
                            xsize 340
                        textbutton "結局 C｜送走之後" style "menu_list_button" action Function(open_gallery_image, "gallery/ending-c-handover.png", "結局 C｜送走之後"):
                            xsize 340
                        textbutton "結局 D｜薄冰同住" style "menu_list_button" action Function(open_gallery_image, "gallery/ending-d-thin-ice.png", "結局 D｜薄冰同住"):
                            xsize 340

                    null height 4

                    text "隱藏紀念照片":
                        font CJK_FONT
                        size 14
                        color LHTL_TEXT_SOFT

                    textbutton "紀念｜躺在大腿" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-lap-sleep.png", "紀念照片｜躺在大腿"):
                        xfill True
                    textbutton "紀念｜額頭輕碰" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-forehead-nudge.png", "紀念照片｜額頭輕碰"):
                        xfill True
                    textbutton "紀念｜擋在身後" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-behind-legs.png", "紀念照片｜擋在身後"):
                        xfill True
                    textbutton "紀念｜鞋邊小睡" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-shoe-sleep.png", "紀念照片｜鞋邊小睡"):
                        xfill True
                    textbutton "紀念｜指尖碰鼻" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-nose-touch.png", "紀念照片｜指尖碰鼻"):
                        xfill True
                    textbutton "紀念｜新水碗" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-water-bowl.png", "紀念照片｜新水碗"):
                        xfill True
                    textbutton "紀念｜背對背" style "menu_list_button" action Function(open_gallery_image, "gallery/secret-back-to-back.png", "紀念照片｜背對背"):
                        xfill True

            textbutton "返回" style "menu_back_button" action Return():
                xalign 0.5


## scene 預覽時的標題列（配合 gallery_pic_label）
screen gallery_pic_chrome(title=""):
    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (18, 10)
        xalign 0.5
        yalign 0.05
        text title:
            font CJK_FONT
            size 22
            color "#7A4E2E"

    text "點一下關閉":
        font CJK_FONT
        size 16
        color "#F3E9D9"
        xalign 0.5
        yalign 0.96


## 備援選單預覽（主路徑已改 open_gallery_image）
screen gallery_image_view(title="紀念照片", img_path="gallery/secret-lap-sleep.png"):
    tag menu

    add Solid("#17120F")

    add img_path:
        xalign 0.5
        yalign 0.52
        zoom 0.72

    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (18, 10)
        xalign 0.5
        yalign 0.05
        text title:
            font CJK_FONT
            size 22
            color "#7A4E2E"

    textbutton "關閉" style "menu_back_button" action ShowMenu("ending_gallery"):
        xalign 0.5
        yalign 0.96


## 舊名稱保留（轉到統一預覽參數）
screen ending_still_view(ending_id="A", title="", img_path="gallery/ending-a-back.png", img_name=None):
    tag menu
    add Solid("#17120F")
    add img_path:
        xalign 0.5
        yalign 0.52
        zoom 0.72
    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (18, 10)
        xalign 0.5
        yalign 0.05
        text (title or "結局靜幀"):
            font CJK_FONT
            size 22
            color "#7A4E2E"
    textbutton "關閉" style "menu_back_button" action ShowMenu("ending_gallery"):
        xalign 0.5
        yalign 0.96


screen secret_photo_view(photo="lap_sleep"):
    tag menu
    $ _meta = SECRET_PHOTO_META.get(photo) or SECRET_PHOTO_META["lap_sleep"]
    $ _title = _meta["title"]
    $ _path = _meta["path"]
    add Solid("#17120F")
    add _path:
        xalign 0.5
        yalign 0.52
        zoom 0.72
    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (18, 10)
        xalign 0.5
        yalign 0.05
        text _title:
            font CJK_FONT
            size 22
            color "#7A4E2E"
    textbutton "關閉" style "menu_back_button" action ShowMenu("ending_gallery"):
        xalign 0.5
        yalign 0.96


screen hidden_content_gallery():
    tag menu

    key "K_F8" action Function(dev_unlock_all_gallery)
    key "shift_K_u" action Function(dev_unlock_all_gallery)

    add "lhtl_menu_bg"
    add Solid("#17120F33")

    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (28, 20)
        xalign 0.05
        yalign 0.5
        xsize 760
        ysize 620

        side "t c b":
            xfill True
            yfill True
            spacing 10

            vbox:
                spacing 2
                xfill True
                text "隱藏內容":
                    font CJK_FONT
                    size 24
                    color LHTL_TEXT_LIGHT
                    outlines [(2, "#17120F99", 0, 0)]
                text "點項目讀全文":
                    font CJK_FONT
                    size 13
                    color LHTL_TEXT_SOFT

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xfill True
                yfill True

                vbox:
                    spacing 7
                    xfill True
                    for content_id in HIDDEN_CONTENT_ORDER:
                        $ entry = hidden_content_entry(content_id)
                        if entry is not None:
                            textbutton entry["label"] style "menu_list_button" action [Function(mark_hidden_content_viewed, content_id), Show("hidden_content_reader", content_id=content_id)]:
                                xfill True

            textbutton "返回" style "menu_back_button" action Return():
                xalign 0.5


screen hidden_content_reader(content_id=""):
    modal True
    zorder 210
    add Solid("#17120FEE")

    $ entry = hidden_content_entry(content_id) or {"label": "（空）", "body": ""}

    frame:
        ## 長文閱讀用實色米白底（玻璃底會讓深棕內文沉進深色背景）
        background Solid("#F3E9D9F2")
        padding (36, 24)
        xalign 0.5
        yalign 0.5
        xsize 860
        ysize 560

        side "t c b":
            xfill True
            yfill True
            spacing 12

            text entry["label"]:
                font CJK_FONT
                size 22
                color LHTL_ACCENT_DARK

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xfill True
                yfill True
                text entry["body"]:
                    font CJK_FONT
                    size 18
                    color LHTL_TEXT
                    line_spacing 8

            textbutton "關閉" style "menu_back_button":
                action Hide("hidden_content_reader")
                xalign 0.5


screen how_to_play():
    zorder 200
    modal True
    add Solid("#17120FF2")
    vbox:
        align (0.5, 0.46)
        spacing 22
        xmaximum 720
        text "怎麼玩" at title_slow_fade(0.0):
            xalign 0.5
            font CJK_FONT
            size 36
            color LHTL_TEXT_LIGHT
            kerning 2
        text "點畫面即可繼續。" at title_slow_fade(0.4):
            xalign 0.5
            font CJK_FONT
            size 22
            color LHTL_TEXT_SOFT
            text_align 0.5
        text "選項會改變牠跟妳的距離，也會改變後來怎麼睡。" at title_slow_fade(0.8):
            xalign 0.5
            font CJK_FONT
            size 22
            color LHTL_TEXT_SOFT
            text_align 0.5
        text "右上角可隨時存檔；遊戲也會自動保存。" at title_slow_fade(1.2):
            xalign 0.5
            font CJK_FONT
            size 22
            color LHTL_TEXT_SOFT
            text_align 0.5
    timer 2.2 action Show("section_title_hint")
    key "dismiss" action [Hide("section_title_hint"), Return()]
    button:
        background None
        xfill True
        yfill True
        action [Hide("section_title_hint"), Return()]

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
        ("start_section_06", "Section 06｜樓梯間的第三者", "當陌生人的手伸向小7，予安第一次發現，自己已經站進了「我們」這一邊。"),
        ("start_section_07", "Section 07｜她倒下的那天", "予安病得起不了身，小7不懂怎麼照顧人，只知道守在門口，試著等她回應。"),
        ("start_section_08", "Section 08｜走到轉角就好", "第一次出門只為抵達巷口；世界太吵時，予安得決定要拉著牠，還是一起停下。"),
        ("start_section_09", "Section 09｜差點交給別人", "預設留下可收集結局 A。同事提出接手；交繩前她得承認誰已經選過誰。"),
        ("start_section_10", "Section 10｜把鑰匙分給心跳", "鑰匙與牽繩掛在同一面牆上；夜深後，睡眠的距離替這段關係留下答案。"),
    ]

    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (24, 16)
        xalign 0.04
        yalign 0.5
        xsize 980
        ysize 640

        side "t c b":
            xfill True
            yfill True
            spacing 8

            vbox:
                spacing 4
                xfill True
                text "章節選擇":
                    font CJK_FONT
                    size 24
                    color LHTL_TEXT_LIGHT
                    outlines [(2, "#17120F99", 0, 0)]
                text "選擇章節會以該段預設狀態開始，不影響既有存檔。Section 09 預設較高信任，留下會走到結局 A。":
                    font CJK_FONT
                    size 13
                    color LHTL_TEXT_SOFT

            # 兩欄網格一次顯示 S01～S10；高度控在 side 中央區內，避免壓住返回
            grid 2 5:
                spacing 6
                xalign 0.0
                yalign 0.0

                for entry_label, entry_title, entry_summary in section_entries:
                    button:
                        background Solid(LHTL_MENU_ITEM)
                        hover_background Solid(LHTL_MENU_ITEM_HOVER)
                        padding (12, 5)
                        xsize 450
                        ysize 78
                        action Start(entry_label)

                        vbox:
                            spacing 2
                            text entry_title:
                                font CJK_FONT
                                size 16
                                color LHTL_TEXT
                            text entry_summary:
                                font CJK_FONT
                                size 11
                                color "#806C5B"

            textbutton "返回" style "menu_back_button" action If(main_menu, true=ShowMenu("main_menu"), false=Return()):
                xalign 0.5


screen game_menu(title, show_quit=False):
    tag menu

    ## 選單底圖：左欄面板，右側牆鉤／油畫透出
    add "lhtl_menu_bg"
    add Solid("#17120F22")

    ## side t/c/b：標題／內容／底部按鈕
    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (32, 22)
        xalign 0.05
        yalign 0.5
        xsize 900
        ysize 600

        side "t c b":
            xfill True
            yfill True
            spacing 12

            text title:
                font CJK_FONT
                size 26
                color LHTL_TEXT_LIGHT
                outlines [(2, "#17120F99", 0, 0)]

            frame:
                background None
                padding (0, 0)
                xfill True
                yfill True
                transclude

            ## 設定頁：返回＋離開並排；其餘選單只顯示返回
            if show_quit:
                hbox:
                    spacing 14
                    xalign 0.5
                    textbutton "返回" style "menu_back_button" action Return():
                        xminimum 160
                    textbutton "離開遊戲" style "menu_back_button" action Quit(confirm=False):
                        xminimum 160
            else:
                textbutton "返回" style "menu_back_button" action Return():
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
        spacing 12
        xalign 0.5
        yalign 0.5

        for slot in range(1, 7):
            button:
                background Solid(LHTL_MENU_ITEM)
                hover_background Solid(LHTL_MENU_ITEM_HOVER)
                xsize 260
                ysize 160
                padding (14, 10)
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

    use game_menu("設定", show_quit=True):
        ## 勿用 viewport+yfill 嵌在 game_menu 的 side 中央：高度會被算成 0，整頁空白
        ## 內容須壓在 side 中央區內（約 ≤450px），勿用 yalign 推位（會疊標題／返回）
        vbox:
            spacing 8
            xalign 0.5
            xfill True

            hbox:
                spacing 28
                xalign 0.5

                ## 左欄：閱讀／顯示
                vbox:
                    spacing 8
                    xsize 380

                    vbox:
                        spacing 4
                        text "文字速度":
                            font CJK_FONT
                            size 16
                            color LHTL_TEXT
                        hbox:
                            spacing 8
                            textbutton "慢" style "embed_pref_button" action Preference("text speed", 20)
                            textbutton "標準" style "embed_pref_button" action Preference("text speed", 30)
                            textbutton "快" style "embed_pref_button" action Preference("text speed", 50)

                    vbox:
                        spacing 4
                        text "自動前進等待":
                            font CJK_FONT
                            size 16
                            color LHTL_TEXT
                        bar value Preference("auto-forward time") style "lhtl_slider"

                    vbox:
                        spacing 4
                        text "顯示模式":
                            font CJK_FONT
                            size 16
                            color LHTL_TEXT
                        hbox:
                            spacing 8
                            textbutton "視窗" style "embed_pref_button" action Preference("display", "window")
                            textbutton "全螢幕" style "embed_pref_button" action Preference("display", "fullscreen")

                ## 右欄：聲音
                vbox:
                    spacing 8
                    xsize 380

                    vbox:
                        spacing 4
                        text "音樂音量":
                            font CJK_FONT
                            size 16
                            color LHTL_TEXT
                        bar value Preference("music volume") style "lhtl_slider"

                    vbox:
                        spacing 4
                        text "音效音量":
                            font CJK_FONT
                            size 16
                            color LHTL_TEXT
                        bar value Preference("sound volume") style "lhtl_slider"

                    textbutton "音樂靜音切換" style "embed_pref_button" action Preference("music mute", "toggle")

            ## 輔助需求：2×2 網格壓高度，避免擠到「返回」
            frame:
                background Solid("#F3E9D9EE")
                padding (14, 8)
                xsize 780
                xalign 0.5

                vbox:
                    spacing 6
                    xfill True

                    hbox:
                        spacing 12
                        xalign 0.5
                        text "輔助需求":
                            font CJK_FONT
                            size 18
                            color "#7A4E2E"
                        textbutton "開啟輔助組合" style "embed_pref_button" action Function(enable_assist_pack):
                            xminimum 140
                        textbutton "關閉輔助組合" style "embed_pref_button" action Function(disable_assist_pack):
                            xminimum 140

                    grid 2 2:
                        spacing 8
                        xalign 0.5

                        hbox:
                            spacing 8
                            text "大字體":
                                font CJK_FONT
                                size 16
                                color "#4A3728"
                                xminimum 72
                            textbutton "開" style "embed_pref_button" action Function(set_assist, "assist_large_text", True) selected persistent.assist_large_text:
                                xminimum 64
                            textbutton "關" style "embed_pref_button" action Function(set_assist, "assist_large_text", False) selected (not persistent.assist_large_text):
                                xminimum 64

                        hbox:
                            spacing 8
                            text "高對比":
                                font CJK_FONT
                                size 16
                                color "#4A3728"
                                xminimum 72
                            textbutton "開" style "embed_pref_button" action Function(set_assist, "assist_high_contrast", True) selected persistent.assist_high_contrast:
                                xminimum 64
                            textbutton "關" style "embed_pref_button" action Function(set_assist, "assist_high_contrast", False) selected (not persistent.assist_high_contrast):
                                xminimum 64

                        hbox:
                            spacing 8
                            text "休息提醒":
                                font CJK_FONT
                                size 16
                                color "#4A3728"
                                xminimum 72
                            textbutton "開" style "embed_pref_button" action Function(set_assist, "assist_rest_reminder", True) selected persistent.assist_rest_reminder:
                                xminimum 64
                            textbutton "關" style "embed_pref_button" action Function(set_assist, "assist_rest_reminder", False) selected (not persistent.assist_rest_reminder):
                                xminimum 64

                        hbox:
                            spacing 8
                            text "略過已讀":
                                font CJK_FONT
                                size 16
                                color "#4A3728"
                                xminimum 72
                            textbutton "開" style "embed_pref_button" action Function(set_assist, "assist_skip_seen", True) selected persistent.assist_skip_seen:
                                xminimum 64
                            textbutton "關" style "embed_pref_button" action Function(set_assist, "assist_skip_seen", False) selected (not persistent.assist_skip_seen):
                                xminimum 64

                    text "略過已讀開＝Ctrl 快轉已看過；建議年長／新手先開輔助組合。":
                        font CJK_FONT
                        size 12
                        color "#806C5B"
                        xalign 0.5


style lhtl_slider is slider:
    xsize 360
    ysize 22
    left_bar Solid("#B77A45")
    right_bar Solid("#E0D2BC")
    thumb Transform(Solid("#7A4E2E"), xysize=(10, 22))
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


## 開發用快捷鍵：F8／Shift+U → 全解鎖（不強制跳轉，避免沖掉目前畫面）
screen _dev_unlock_hotkey():
    zorder 2500
    key "K_F8" action Function(dev_unlock_all_gallery)
    key "shift_K_u" action Function(dev_unlock_all_gallery)
