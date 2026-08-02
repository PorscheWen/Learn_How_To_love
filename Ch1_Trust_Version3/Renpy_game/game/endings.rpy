## ------------------------------------------------------------
## Ch1 結局節拍動畫｜標題卡｜解鎖提示
## 安靜的距離／睡姿 coda；可點擊或 Ctrl 略過 pause。
## ------------------------------------------------------------

# 距離緩動：遠 → 近（結局 A 靠近）
transform dog_coda_approach:
    xalign 0.58
    yanchor 1.0
    ypos 0.86
    zoom 0.26
    ease 2.8 xalign 0.50 zoom 0.30
    ease 2.6 xalign 0.42 zoom 0.34

# 選定仍學：中距 ↔ 略近（回頭確認感）
transform dog_coda_check:
    xalign 0.50
    yanchor 1.0
    ypos 0.86
    zoom 0.30
    ease 1.6 xalign 0.46 zoom 0.32
    pause 0.8
    ease 1.4 xalign 0.50 zoom 0.30
    pause 1.0
    ease 1.8 xalign 0.44 zoom 0.33

# 薄冰：門邊略鬆、仍遠
transform dog_coda_thin_ice:
    xalign 0.62
    yanchor 1.0
    ypos 0.86
    zoom 0.24
    ease 2.2 xalign 0.58 zoom 0.26
    pause 1.2
    ease 1.8 xalign 0.60 zoom 0.25


init python:
    def ending_unlock_lines(ending_id):
        """回傳本結局實際解鎖項目（與 process_ending_unlock 對齊）。"""
        eid = str(ending_id or "").upper()
        lines = ["結局靜幀｜可在「結局一覽」查看"]
        if eid == "A":
            lines.extend([
                "紀念照片｜躺在大腿",
                "紀念照片｜額頭輕碰",
                "紀念照片｜擋在身後",
                "紀念照片｜鞋邊小睡",
                "紀念照片｜指尖碰鼻",
                "紀念照片｜新水碗",
                "狗的日記｜她的背靠著我",
                "予安心境｜一百個清晨裡的信任",
                "朋友視角｜Kelly",
                "後續提示｜信任的地基",
            ])
        elif eid == "B":
            lines.extend([
                "狗的日記｜確認遊戲",
                "予安心境｜我們都還在學",
                "朋友視角｜Iris",
            ])
        elif eid == "C":
            lines.extend([
                "狗的日記｜新家的聲音",
                "予安心境｜愛不一定是擁有",
                "朋友視角｜David",
            ])
        elif eid == "D":
            lines.extend([
                "狗的日記｜薄冰上的確認",
                "予安心境｜薄冰上的堅持",
                "朋友視角｜Marcus",
            ])
        return lines

    def ending_coda_pause(seconds):
        """軟暫停：點擊或 Ctrl／略過可跳過。"""
        renpy.pause(float(seconds), hard=False)


## 節拍期間提示（非 modal，不擋 pause）
screen ending_skip_hint():
    zorder 250
    text "點擊或 Ctrl 可略過":
        font CJK_FONT
        size 16
        color "#8A7763"
        xalign 0.98
        yalign 0.94


## 結局標題卡（對齊 section_title 語氣）
screen ending_title_card(title, subtitle=""):
    zorder 200
    modal True
    add Solid("#17120FF2")
    vbox:
        align (0.5, 0.46)
        spacing 22
        text title at title_slow_fade(0.0):
            xalign 0.5
            font CJK_FONT
            size 34
            color LHTL_TEXT_LIGHT
            kerning 2
        if subtitle:
            text subtitle at title_slow_fade(0.9):
                xalign 0.5
                font CJK_FONT
                size 20
                color LHTL_TEXT_SOFT
                kerning 2
                textalign 0.5
                xmaximum 720
    timer 3.2 action Show("section_title_hint")
    key "dismiss" action Return()
    button:
        background None
        xfill True
        yfill True
        action Return()


## 隱藏內容解鎖提示（彩帶感用暖色邊框，不用狂歡特效）
transform ending_unlock_appear:
    alpha 0.0
    yoffset 18
    easein 0.55 alpha 1.0 yoffset 0
    on hide:
        linear 0.35 alpha 0.0


screen ending_unlock_notice(ending_id="A"):
    zorder 260
    modal True
    add Solid("#17120F99")

    frame at ending_unlock_appear:
        background Solid(LHTL_PANEL_GLASS)
        padding (36, 28)
        xalign 0.5
        yalign 0.48
        xmaximum 560

        vbox:
            spacing 14
            xfill True
            text "新隱藏內容已解鎖":
                font CJK_FONT
                size 24
                color LHTL_ACCENT_DARK
                xalign 0.5
            null height 4
            for line in ending_unlock_lines(ending_id):
                text "・  " + line:
                    font CJK_FONT
                    size 18
                    color LHTL_TEXT
            null height 6
            text "可在主選單「隱藏內容」「結局一覽」查看。":
                font CJK_FONT
                size 15
                color "#806C5B"
                xalign 0.5
                textalign 0.5
            null height 8
            textbutton "繼續" style "menu_button":
                action Return()
                xalign 0.5

    ## 自動繼續（可點提前）
    timer 4.5 action Return()
    key "dismiss" action Return()


label ending_show_title(title, subtitle=""):
    $ renpy.hide_screen("ending_skip_hint")
    $ renpy.hide_screen("section_title_hint")
    $ renpy.call_screen("ending_title_card", title=title, subtitle=subtitle)
    $ renpy.hide_screen("section_title_hint")
    with Dissolve(0.7)
    return


label ending_show_unlock(ending_id):
    $ renpy.call_screen("ending_unlock_notice", ending_id=ending_id)
    with Dissolve(0.4)
    return


## ========== 結局 A｜背靠：停電光圈 → 靠近 → 背對睡 ==========
label ending_beat_back_to_back:
    window hide
    show screen ending_skip_hint

    scene bg living_night
    with Dissolve(0.9)

    show dog anxious at dog_far
    with Dissolve(1.0)
    $ ending_coda_pause(1.1)

    show dog halfstep at dog_coda_approach
    with Dissolve(1.0)
    $ ending_coda_pause(5.6)

    show dog back_sleep at dog_near
    with Dissolve(1.4)
    $ dog_sfx("sigh")
    $ ending_coda_pause(2.4)

    ## 隔天感：切日景、狗仍近、不回門邊
    scene bg living_day
    show dog back_sleep at dog_near
    with Dissolve(1.2)
    $ ending_coda_pause(1.6)

    hide screen ending_skip_hint
    hide dog
    with Dissolve(0.8)
    window show
    return


## ========== 結局 B｜選定但還在學：近睡＋回頭確認 ==========
label ending_beat_chosen_learning:
    window hide
    show screen ending_skip_hint

    scene bg living_night
    with Dissolve(0.9)

    show dog parallel at dog_mid
    with Dissolve(1.0)
    $ ending_coda_pause(1.0)

    show dog check_sleep at dog_coda_check
    with Dissolve(1.2)
    $ dog_sfx("soft")
    $ ending_coda_pause(6.2)

    ## 玄關：跟到門線就停
    scene bg entrance_day
    show dog leash_wait at dog_mid
    with Dissolve(1.1)
    $ ending_coda_pause(1.4)

    show dog leash_wait at dog_far
    with Dissolve(0.9)
    $ ending_coda_pause(1.2)

    hide screen ending_skip_hint
    hide dog
    with Dissolve(0.8)
    window show
    return


## ========== 結局 C｜送走之後：空掛勾／空房間／照片感（狗不在場）==========
label ending_beat_handed_over:
    window hide
    show screen ending_skip_hint

    scene bg living_night
    with Dissolve(1.0)
    $ ending_coda_pause(1.4)

    ## 空房：無狗，略暗
    show expression Solid("#17120F55") as ending_dim
    with Dissolve(0.8)
    $ ending_coda_pause(1.2)

    ## 「同事傳來的照片」——文字框代替缺圖，避免狗誤入畫面
    show screen ending_c_photo_card
    $ ending_coda_pause(3.2)
    hide screen ending_c_photo_card
    with Dissolve(0.6)

    hide ending_dim
    with Dissolve(0.5)

    scene bg entrance_night
    with Dissolve(1.0)
    $ ending_coda_pause(1.5)

    hide screen ending_skip_hint
    with Dissolve(0.6)
    window show
    return


screen ending_c_photo_card():
    zorder 240
    frame:
        background Solid("#2E241FEE")
        padding (28, 22)
        xalign 0.5
        yalign 0.42
        xmaximum 480
        vbox:
            spacing 10
            text "同事傳來的照片":
                font CJK_FONT
                size 16
                color LHTL_TEXT_SOFT
                xalign 0.5
            text "門留著一條縫。舊外套還在。水碗放得很遠。":
                font CJK_FONT
                size 18
                color LHTL_TEXT_LIGHT
                textalign 0.5
                xalign 0.5


## ========== 結局 D｜薄冰同住：門邊淺睡、距離誠實 ==========
label ending_beat_thin_ice:
    window hide
    show screen ending_skip_hint

    scene bg living_night
    with Dissolve(0.9)

    show dog door_edge at dog_coda_thin_ice
    with Dissolve(1.2)
    $ dog_sfx("whimper")
    $ ending_coda_pause(5.4)

    ## 縫隙只少一點點：略近仍遠
    show dog door_edge at dog_far
    with Dissolve(1.0)
    $ ending_coda_pause(1.8)

    scene bg entrance_day
    show dog door_edge at dog_far
    with Dissolve(1.1)
    $ ending_coda_pause(1.4)

    hide screen ending_skip_hint
    hide dog
    with Dissolve(0.8)
    window show
    return


## 統一收束：節拍 → 標題 → 解鎖提示 → aftercare
## 以 jump 進 aftercare，避免 call 後 fall-through 掉進下一個結局 label。
label ending_coda_finish(ending_id, title, subtitle=""):
    if ending_id == "A":
        call ending_beat_back_to_back
    elif ending_id == "B":
        call ending_beat_chosen_learning
    elif ending_id == "C":
        call ending_beat_handed_over
    else:
        call ending_beat_thin_ice

    call ending_show_title(title, subtitle)
    $ sync_unlocked_ending_rewards()
    $ renpy.save_persistent()
    call ending_show_unlock(ending_id)

    ## aftercare 對白需要穩定底圖（勿停在日景／玄關 coda）
    scene bg living_night
    with Dissolve(0.7)
    jump ending_aftercare
