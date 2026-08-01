## Week0 Day2｜混亂的客廳
## 來源：week0/day2_messy_living_room.md ｜ agents/plot.md

label d2_morning_mess:
    $ story_day = 2
    $ smell_text = "便便、濕毛巾、雨後的悶"
    $ play_bgm("calm")
    scene bg living_day
    with Dissolve(0.5)
    show dog scare at dog_bottom
    with Dissolve(0.3)
    $ dog_sfx("whimper")

    narrator "鬧鐘還沒響。先響的是腳底——軟的、涼的、黏的。"
    narrator "小晴整個人僵在走廊口。客廳地板中央，\n一坨小小的、鐵證如山那種：\n昨晚那罐副食，成功走完消化系統。"
    show dog anxious at dog_bottom
    $ dog_sfx("murmur")
    narrator "紙箱口露出一顆毛茸茸的頭。\n耳朵貼平，尾巴緊貼後腿，眼睛亮得像在等她發飆。"
    pudding "嗚……"
    xq "……啊。"
    narrator "她站了大概五秒。\n便當盒氣味還在空氣裡，混著濕毛巾和雨後的悶。"
    xq "好。好。先……先別哭。是我要哭。"
    jump d2_choice_react


label d2_choice_react:
    $ smell_text = "便便、紙箱、焦慮"
    scene bg living_day
    show dog anxious at dog_bottom

    narrator "地上那坨。你第一個反應是？"
    menu:
        "提高音量「你怎麼可以」":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "聲音一抬，[dog_label]整團縮進箱底，短促嗚嗚連成串。\n爪子刮紙板，像要把自己刮進縫裡。"
            xq "不是——我是說——算了。"
            narrator "她自己也愣住。喉嚨還熱著，手卻已經發軟。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("yelled_at_mess", True)
            jump d2_kg_potty_scene
        "先深呼吸再走近":
            show dog anxious at dog_bottom
            $ dog_sfx("soft")
            narrator "她數到三，蹲下來，聲音壓回平常的高度。"
            xq "……好啦。我知道你不是故意的。"
            xq "我也沒教過你啊。"
            narrator "[dog_label]耳朵動了一下。嗚嗚還在，但沒有再往後退。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("calm_after_mess", True)
            jump d2_kg_potty_scene


label d2_kg_potty_scene:
    $ smell_text = "手機熱度、清潔劑櫃"
    scene bg living_day
    show dog anxious at dog_bottom
    call kg_d2_potty_myths from _call_kg_d2
    jump d2_choice_clean


label d2_choice_clean:
    $ smell_text = "清潔劑、溫水、開窗風"
    scene bg living_day
    show dog anxious at dog_bottom

    narrator "怎麼清這一地？"
    menu:
        "用很香的清潔劑猛噴":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "檸檬味炸開。[dog_label]打了個噴嚏，嗚嗚變尖，\n鼻子往紙箱深處埋。\n\n小晴眼睛也被嗆到，乾咳兩聲。"
            xq "奇怪……文章說不要這樣耶。"
            narrator "她改用清水抹布亂擦一通，窗也沒開。\n味道卡在鼻腔裡，誰都不舒服。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("harsh_cleaner", True)
            jump d2_tg_soft_voice_scene
        "溫水＋中性清潔、開窗":
            show dog anxious at dog_bottom
            $ dog_sfx("sigh")
            narrator "風進來，味道淡了。\n[dog_label]鼻子動了動，仍警戒，但嗚嗚變短。"
            xq "好了、好了。這裡沒有怪物。"
            $ play_bgm("warm")
            narrator "她把濕紙丟進垃圾袋，手洗了兩遍，\n才敢再看紙箱一眼。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("gentle_clean", True)
            jump d2_tg_soft_voice_scene


label d2_tg_soft_voice_scene:
    $ smell_text = "溫水、乾毛巾"
    $ play_bgm("tender")
    scene bg living_day
    show dog anxious at dog_bottom
    call tg_d2_soft_voice from _call_tg_d2
    jump d2_choice_pad


label d2_choice_pad:
    $ smell_text = "尿墊塑膠味、乾毛巾"
    scene bg living_day
    if get_flag("soft_voice_ok"):
        show dog shy at dog_bottom
    else:
        show dog anxious at dog_bottom

    narrator "尿墊鋪好了。怎麼讓[dog_label]知道「這裡」？"
    menu:
        "硬把[dog_label]按在墊上":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "身體一被固定，[dog_label]尖叫似的嗚嗚炸開，四肢亂蹬。\n墊子皺成一團。"
            xq "文章說要「引導」——可是你一直跑啊！"
            narrator "她鬆手。[dog_label]彈回紙箱，整個人也坐倒在地。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("forced_onto_pad", True)
            jump d2_choice_leave
        "帶[dog_label]嗅墊邊，人退開":
            show dog shy at dog_bottom
            $ dog_sfx("soft")
            narrator "她把墊子固定在牆角——離紙箱不遠、離沙發有一點距離。\n用毛巾邊輕輕引[dog_label]靠過來。鼻子碰到墊面，抽了兩下。"
            xq "這裡。以後……大概這裡。"
            narrator "她退到沙發腳邊坐下。\n[dog_label]在墊邊站了一會兒，沒有立刻用，但也沒逃回箱底。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("pad_introduced_gently", True)
            jump d2_choice_leave


label d2_choice_leave:
    $ smell_text = "鑰匙、尿墊、茶几灰塵"
    scene bg living_day
    show dog anxious at dog_bottom

    narrator "今天還要上班。你要怎麼辦？（信任不變）"
    menu:
        "硬撐上班":
            narrator "她把水碗放遠一點、尿墊攤平，\n紙箱口對準不會被風直吹的方位。鑰匙在手上轉了兩圈。"
            xq "我很快回來。真的。大概。"
            narrator "門關上。走廊裡她已經開始想便便的事。"
            $ set_flag("took_half_day", False)
            $ set_flag("rushed_day", True)
            jump d2_naming_petshop
        "請半天在家觀察":
            narrator "訊息打了又刪，最後還是送出。主管已讀不回。\n她把筆電放在茶几上，聲音調到最小。"
            xq "今天我們……就混一天。"
            narrator "[dog_label]在墊邊打了個盹，耳朵仍會豎一下。"
            $ set_flag("took_half_day", True)
            $ set_flag("rushed_day", False)
            jump d2_home_hidden_kg


label d2_home_hidden_kg:
    ## 請假在家：不直接去寵物店 → 隱藏知識（狗不能吃什麼）
    $ smell_text = "便當殘渣、手機熱度、茶几灰塵"
    $ play_bgm("calm")
    scene bg living_day
    show dog shy at dog_bottom
    with Dissolve(0.3)

    narrator "午後光斜進來。筆電開著，她卻盯著茶几上那點便當邊角料。"
    narrator "[dog_label]鼻子動了動，好像在問：那是給我的嗎？"
    xq "等等……你不能亂吃吧。"
    call kg_d2_toxic_foods from _call_kg_d2_toxic
    jump d2_naming_home


label d2_naming_home:
    ## 請假支線：在家取名（不去寵物店）
    $ smell_text = "尿墊、舊毛巾、午後陽光"
    $ play_bgm("tender")
    scene bg living_day
    show dog shy at dog_bottom

    narrator "紙箱裡的毛團打了個呵欠，舌頭小小一截。\n小晴盯著牠看了很久。叫「小狗狗」太隨便，叫「你」太遠。"
    xq "……你該有個名字。"

    $ dog_name = ""
    call screen dog_name_input

    $ dog_sfx("yip")
    narrator "她把名字在嘴裡滾了一遍。[dog_label]。\n不一定聽得懂，但總要有個開頭。"
    xq "[dog_label]。好。先這樣。不喜歡再改。"
    jump d2_day_end


label d2_naming_petshop:
    ## 上班支線：下班路上去寵物店取名
    $ smell_text = "飼料袋、塑膠包裝、消毒水"
    $ play_bgm("tender")
    scene bg petshop_day
    with Dissolve(0.45)
    hide dog

    narrator "下班路上她拐進巷口寵物店。副食快見底——\n還有一件她一路逃避的事。"
    show char shop_cashier at char_center
    with Dissolve(0.3)
    narrator "結帳時，櫃檯的妹妹隨口問："
    shop_cashier "小朋友叫什麼名字呀？"
    xq "……啊？"
    narrator "她這才發現——還沒正式取名。\n塑膠袋勒進手指，櫃檯燈光有點刺眼。"

    $ dog_name = ""
    call screen dog_name_input

    hide char
    $ dog_sfx("yip")
    narrator "她把名字在嘴裡滾了一遍。[dog_label]。\n不一定聽得懂，但總要有個開頭。"
    xq "[dog_label]。好。先這樣。不喜歡再改。"
    jump d2_day_end


label d2_day_end:
    $ smell_text = "尿墊、舊毛巾、夜燈"
    $ play_bgm("warm")
    scene bg living_night
    with Dissolve(0.5)
    show dog sleepy at dog_bottom
    $ dog_sfx("sigh")

    if get_flag("took_half_day"):
        narrator "尿墊角落有一小塊新的濕痕——至少在對的方向。\n[dog_label]肚子貼著乾毛巾，呼吸比昨晚穩一點。"
        xq "今天好亂。"
        xq "可是你還在。我也還在。"
        if get_flag("calm_after_mess"):
            narrator "距離，比清晨近了半步。"
        narrator "窗外車聲遠近。客廳終於安靜到能聽見彼此的呼吸。"
    else:
        narrator "提袋放在玄關。尿墊角落有一小塊新的濕痕——至少在對的方向。\n[dog_label]肚子貼著乾毛巾，呼吸比昨晚穩一點。"
        xq "今天好亂。"
        xq "可是你還在。我也還在。"
        if get_flag("calm_after_mess"):
            narrator "距離，比清晨近了半步。"
        narrator "窗外車聲遠近。客廳終於安靜到能聽見彼此的呼吸。"

    $ add_landmark("landmark_messy_morning")
    if get_flag("pad_introduced_gently"):
        $ add_landmark("landmark_first_pad")
    if get_flag("knows_toxic_foods"):
        $ add_landmark("landmark_toxic_foods")

    $ save_name = "第2天結束｜" + dog_label + "｜信任 " + str(trust)
    if get_flag("took_half_day"):
        narrator "—— 第 2 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]\n\n飼料還沒補。明天，大概得出門一趟。"
    else:
        narrator "—— 第 2 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]\n\n飼料補上了。明天，大概還會再出門一趟。"
    jump d3_empty_can
