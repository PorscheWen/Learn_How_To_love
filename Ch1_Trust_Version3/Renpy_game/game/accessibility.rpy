## ------------------------------------------------------------
## 輔助需求（對齊 gamer_60_retired：大字體／高對比／休息提醒／略過已讀）
## 設定頁可個別開關；變更後呼叫 apply_assist_prefs()
## ------------------------------------------------------------

default persistent.assist_large_text = False
default persistent.assist_high_contrast = False
default persistent.assist_rest_reminder = False
default persistent.assist_skip_seen = True


init python:
    ## 基準值（與 gui.rpy 對齊；開關關閉時還原）
    _ASSIST_BASE = {
        "text_size": 25,
        "name_text_size": 22,
        "interface_text_size": 20,
        "label_text_size": 30,
        "choice_button_text_size": 22,
        "textbox_height": 148,
        "menu_btn_yminimum": 46,
        "menu_btn_padding": (22, 11),
        "quick_btn_text_size": 15,
    }

    def assist_on(flag_name):
        return bool(getattr(persistent, flag_name, False))

    def apply_assist_prefs():
        """依 persistent 輔助開關重套字級／對比；必須回傳 None。"""
        large = bool(persistent.assist_large_text)
        hi = bool(persistent.assist_high_contrast)
        scale = 1.28 if large else 1.0

        gui.text_size = int(_ASSIST_BASE["text_size"] * scale)
        gui.name_text_size = int(_ASSIST_BASE["name_text_size"] * scale)
        gui.interface_text_size = int(_ASSIST_BASE["interface_text_size"] * scale)
        gui.label_text_size = int(_ASSIST_BASE["label_text_size"] * scale)
        gui.choice_button_text_size = int(_ASSIST_BASE["choice_button_text_size"] * scale)
        gui.textbox_height = int(_ASSIST_BASE["textbox_height"] * (1.2 if large else 1.0))

        ## 高對比：對話改近黑字＋更亮描邊；選項底更不透明
        if hi:
            style.say_dialogue.color = "#1A1008"
            style.say_dialogue.outlines = [(3, "#FFFFFFF2", 0, 0)]
            style.say_label.color = "#5C3018"
            style.say_label.outlines = [(3, "#FFFFFFF2", 0, 0)]
            style.choice_button.background = Solid("#FFF8EFFF")
            style.choice_button.hover_background = Solid("#F0D5B0FF")
            style.choice_button_text.color = "#1A1008"
            style.menu_button.background = Solid("#FFF8EFF0")
            style.menu_button.hover_background = Solid("#E8C9A0FF")
            style.menu_button_text.color = "#1A1008"
            style.embed_menu_button.background = Solid("#FFF8EFF0")
            style.embed_menu_button.hover_background = Solid("#E8C9A0FF")
            style.embed_menu_button_text.color = "#1A1008"
        else:
            style.say_dialogue.color = "#000000"
            style.say_dialogue.outlines = [(2, "#F7EFE4D9", 0, 0)]
            style.say_label.color = LHTL_ACCENT_DARK
            style.say_label.outlines = [(2, "#F7EFE4D9", 0, 0)]
            style.choice_button.background = Solid(LHTL_CHOICE)
            style.choice_button.hover_background = Solid(LHTL_CHOICE_HOVER)
            style.choice_button_text.color = LHTL_TEXT
            style.menu_button.background = Solid(LHTL_MENU_ITEM)
            style.menu_button.hover_background = Solid(LHTL_MENU_ITEM_HOVER)
            style.menu_button_text.color = LHTL_TEXT
            style.embed_menu_button.background = Solid(LHTL_MENU_ITEM)
            style.embed_menu_button.hover_background = Solid(LHTL_MENU_ITEM_HOVER)
            style.embed_menu_button_text.color = LHTL_TEXT

        ## 大字體：對話／選項／主選單變大；embed（設定／返回）維持原尺寸，避免擠爆 game_menu
        if large:
            style.menu_button.yminimum = 56
            style.menu_button.padding = (24, 14)
            style.menu_button_text.size = 22
            style.choice_button.padding = (28, 20)
            style.quick_button_text.size = 18
        else:
            style.menu_button.yminimum = _ASSIST_BASE["menu_btn_yminimum"]
            style.menu_button.padding = _ASSIST_BASE["menu_btn_padding"]
            style.menu_button_text.size = 20
            style.choice_button.padding = (28, 16)
            style.quick_button_text.size = _ASSIST_BASE["quick_btn_text_size"]

        style.embed_menu_button.yminimum = 44
        style.embed_menu_button.padding = (18, 10)
        style.embed_menu_button_text.size = 19

        ## 略過已讀：開＝允許 Ctrl 快轉（只跳已看過）；關＝停用略過，避免誤觸
        preferences.skip_unseen = False
        config.allow_skipping = bool(persistent.assist_skip_seen)

        style.rebuild()
        return None

    def toggle_assist(flag_name):
        """切換單一輔助旗標並立刻套用。"""
        cur = bool(getattr(persistent, flag_name, False))
        setattr(persistent, flag_name, not cur)
        renpy.save_persistent()
        apply_assist_prefs()
        state = "開" if getattr(persistent, flag_name) else "關"
        labels = {
            "assist_large_text": "大字體",
            "assist_high_contrast": "高對比",
            "assist_rest_reminder": "休息提醒",
            "assist_skip_seen": "略過已讀",
        }
        renpy.notify(labels.get(flag_name, flag_name) + "：" + state)
        return None

    def set_assist(flag_name, value):
        setattr(persistent, flag_name, bool(value))
        renpy.save_persistent()
        apply_assist_prefs()
        return None

    def enable_assist_pack():
        """一鍵開啟建議輔助組合（大字體＋高對比＋休息提醒＋略過已讀）。"""
        persistent.assist_large_text = True
        persistent.assist_high_contrast = True
        persistent.assist_rest_reminder = True
        persistent.assist_skip_seen = True
        renpy.save_persistent()
        apply_assist_prefs()
        renpy.notify("已開啟輔助組合（大字體／高對比／休息提醒／略過已讀）")
        return None

    def disable_assist_pack():
        persistent.assist_large_text = False
        persistent.assist_high_contrast = False
        persistent.assist_rest_reminder = False
        persistent.assist_skip_seen = True
        renpy.save_persistent()
        apply_assist_prefs()
        renpy.notify("已關閉輔助組合")
        return None


## 啟動時套用一次（讀取 persistent 後）
label after_load:
    $ apply_assist_prefs()
    return


init python:
    def _assist_boot():
        try:
            apply_assist_prefs()
        except Exception:
            pass

    if _assist_boot not in config.start_callbacks:
        config.start_callbacks.append(_assist_boot)


## 休息提醒：每 60 分鐘一次（僅遊戲中、開關開啟）
screen assist_rest_watch():
    zorder 5
    if persistent.assist_rest_reminder and not main_menu:
        timer 3600.0 repeat True action Show("assist_rest_dialog")


screen assist_rest_dialog():
    modal True
    zorder 900

    add Solid("#17120FCC")

    frame:
        background Solid("#F3E9D9")
        padding (36, 28)
        xalign 0.5
        yalign 0.5
        xmaximum 560

        vbox:
            spacing 16
            text "健康提醒":
                font CJK_FONT
                size 26
                color "#7A4E2E"
                xalign 0.5
            text "您已遊玩一段時間。\n建議適時休息，放鬆眼睛與脖子。":
                font CJK_FONT
                size 20
                color "#4A3728"
                text_align 0.5
                xalign 0.5
            hbox:
                spacing 14
                xalign 0.5
                textbutton "繼續遊玩" style "menu_button" action Hide("assist_rest_dialog"):
                    xminimum 160
                textbutton "現在休息" style "menu_button" action [Hide("assist_rest_dialog"), ShowMenu("preferences")]:
                    xminimum 160


init python:
    if "assist_rest_watch" not in config.always_shown_screens:
        config.always_shown_screens.append("assist_rest_watch")
