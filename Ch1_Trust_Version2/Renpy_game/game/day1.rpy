## Week0 Day1｜雨天的紙箱
## 來源：week0/day1_rainy_cardboard.md ｜ agents/plot.md

label d1_street_rain:
    $ story_day = 1
    $ smell_text = "雨水、濕紙箱、微弱體溫"
    $ play_bgm("melancholy")
    scene bg street_night
    with Dissolve(0.5)
    show char hand_reach at char_center
    with Dissolve(0.3)

    narrator "傍晚的雨沒有要停的樣子。\n小晴撐著快翻面的傘，肩帶勒進肩膀——\n加班加到連便利商店關沒關都懶得想。"
    narrator "鞋跟踩進積水，濺起來的涼意讓她縮了一下脖子。\n\n巷口那隻溼透的紙箱，輕輕動了一下。"
    $ dog_sfx("murmur")
    xq "……誰亂丟垃圾啊。"
    narrator "她本想繞過去。\n紙箱又動了。這次更清楚——不是風。"
    hide char
    show dog box at dog_bottom
    with Dissolve(0.25)
    narrator "傘緣滴下水線。小晴蹲低，指尖碰到濕紙板，軟的。\n\n箱蓋掀開一條縫。\n\n裡面是一團發抖的毛。太小了，小到讓人不敢用力呼吸。\n一雙眼睛亮著，卻往後退，爪子刮過箱底，發出細細的刮紙聲。"
    $ dog_sfx("whimper")
    pudding "嗚……嗚嗚……"
    xq "欸、你……你怎麼會在這？"
    narrator "[dog_label]不回答。當然不會。\n只把身體縮得更緊，耳朵貼平，雨水沿著紙箱邊流進去。\n\n小晴喉嚨發乾。腦子裡沒有「收養」，只有一句很笨的——"
    xq "……這樣會冷死耶。"
    jump d1_choice_carry


label d1_choice_carry:
    $ smell_text = "雨水、濕紙箱、濕外套"
    scene bg street_night
    show dog box at dog_bottom

    narrator "怎麼帶[dog_label]離開雨裡？"
    menu:
        "直接伸手把幼犬抓出紙箱":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "手指剛扣住濕漉漉的側腹，[dog_label]像被電到，短促悲鳴拔高。\n爪子亂抓，雨水和泥一起糊上小晴袖口。"
            xq "抱歉抱歉——可是雨太大了啊……"
            narrator "[dog_label]在臂彎裡掙扎，身體僵硬，嗚嗚停不下來。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("grabbed_from_box", True)
            jump d1_carry_home
        "整箱連外套一起抱走":
            hide dog
            show char carry_box at char_center
            with Dissolve(0.25)
            $ dog_sfx("soft")
            narrator "她把外套罩住紙箱口，雨立刻打濕袖口。\n箱子晃一下，裡面傳來較輕的嗚嗚——\n還在怕，但沒有被硬抓出箱的那下尖叫。"
            xq "抱歉、抱歉，快到了……我也很慘好嗎。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("carried_whole_box", True)
            jump d1_carry_home


label d1_carry_home:
    $ smell_text = "雨水、濕毛、地板清潔劑"
    $ play_bgm("warm")
    scene bg living_night
    with Dissolve(0.5)
    show dog anxious at dog_bottom
    with Dissolve(0.3)
    $ dog_sfx("murmur_b")

    narrator "整段路她走得很快，又不敢跑。\n鑰匙轉了兩次才打開門。\n燈亮起的瞬間，窄小客廳像被突然叫醒。"
    narrator "紙箱放到地板中央。她自己也順勢坐下，\n雨水和疲憊一起往下掉。"
    xq "先……先查一下。我連你幾個月大都不知道。"
    jump d1_kg_first_aid_scene


label d1_kg_first_aid_scene:
    $ smell_text = "濕毛巾、手機螢幕熱度"
    scene bg living_night
    show dog anxious at dog_bottom
    call kg_d1_puppy_first_aid from _call_kg_d1
    jump d1_choice_clean


label d1_choice_clean:
    $ smell_text = "濕毛、舊毛巾"
    scene bg living_night
    show dog anxious at dog_bottom

    narrator "[dog_label]還濕著。你要怎麼清潔？"
    menu:
        "直接放水槽沖一沖":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "水流一響，[dog_label]尖叫似的嗚嗚炸開，\n後爪在金屬槽裡打滑。\n小晴手忙腳亂關水，袖子全濕。"
            if get_flag("knows_towel_first"):
                xq "不是——我不是要害你……明明剛看過……"
            else:
                xq "不是——我不是要害你……好像哪裡不對……"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("tried_sink_bath", True)
            $ set_flag("bathed", False)
            show dog wet at dog_bottom
            narrator "最後還是改用毛巾亂擦一通。\n電暖器拖過來又挪遠，怕太熱。"
            jump d1_search_food
        "先拿毛巾擦乾就好":
            show dog wet at dog_bottom
            $ dog_sfx("soft")
            narrator "毛巾靠近時，[dog_label]仍往後縮，後背輕撞箱壁。\n小晴手停半空，改成隔著布料按、吸、換面。"
            xq "我要碰你喔。不是要抓你……就擦一下。"
            $ dog_sfx("sigh")
            narrator "嗚嗚變短。水痕淡了。\n她把紙箱口對準暖風，又立刻挪遠一點。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("towel_dried", True)
            $ set_flag("bathed", False)
            jump d1_search_food


label d1_search_food:
    $ smell_text = "罐頭、便當、舊冰箱"
    scene bg living_night
    show dog hungry at dog_bottom

    narrator "冰箱冷光打在臉上：半盒便當、無糖茶、過期邊緣的優格。"
    xq "……也是，我自己都養不飽。"
    narrator "雨衣口袋裡有稍早被包裝騙到手的副食罐。\n她用熱水沖過淺盤，撬開罐頭，味道一下子填滿客廳。\n\n[dog_label]鼻子動了。警戒還在，肚子比驕傲誠實。"
    xq "你等等。我放遠一點。"
    jump d1_tg_space_feed_scene


label d1_tg_space_feed_scene:
    $ smell_text = "罐頭、濕毛巾"
    scene bg living_night
    show dog hungry at dog_bottom
    call tg_d1_space_feed from _call_tg_d1
    jump d1_choice_approach


label d1_choice_approach:
    $ smell_text = "罐頭、幼犬體溫"
    scene bg living_night
    if get_flag("gave_space"):
        show dog shy at dog_bottom
        narrator "[dog_label]在吃了。你現在……？"
        menu:
            "忍不住伸手想摸頭":
                show dog scare at dog_bottom
                $ dog_sfx("whimper_b")
                narrator "頂毛剛被碰到，[dog_label]像觸電，短促悲鳴，\n退到箱底最深處。\n眼睛還是亮的——亮得像害怕。"
                xq "對不起！我以為摸頭會比較好……"
                $ add_trust(-1)
                $ show_trust_toast(-1)
                $ set_flag("touched_too_soon", True)
                jump d1_choice_sleep
            "繼續遠遠看著，不伸手":
                show dog shy at dog_bottom
                $ dog_sfx("soft_b")
                narrator "小晴只剩眼角在看。\n[dog_label]咀嚼兩下抬一次頭，漸漸連那一下也省了。"
                $ add_trust(1)
                $ show_trust_toast(1)
                jump d1_choice_sleep
    else:
        show dog hungry at dog_bottom
        narrator "牠還沒敢吃。你要怎麼辦？"
        menu:
            "忍不住伸手想摸頭安撫":
                show dog scare at dog_bottom
                $ dog_sfx("whimper_b")
                narrator "頂毛剛被碰到，[dog_label]像觸電，短促悲鳴，\n退到箱底最深處。\n眼睛還是亮的——亮得像害怕。"
                xq "對不起！我以為摸頭會比較好……"
                $ add_trust(-1)
                $ show_trust_toast(-1)
                $ set_flag("touched_too_soon", True)
                jump d1_choice_sleep
            "把食物再推近一點，自己退開":
                show dog shy at dog_bottom
                $ dog_sfx("soft_b")
                narrator "小晴把盤子再推半指，整個人往後坐。\n[dog_label]猶豫很久，才低頭開吃。"
                $ add_trust(1)
                $ show_trust_toast(1)
                $ set_flag("gave_space", True)
                $ set_flag("fed", True)
                jump d1_choice_sleep


label d1_choice_sleep:
    $ smell_text = "舊毛巾、夜燈、雨停後的屋簷"
    scene bg living_night
    with Dissolve(0.5)
    show dog sleepy at dog_bottom

    narrator "今晚要睡哪？"
    menu:
        "回房間關門睡":
            $ dog_sfx("whimper")
            narrator "門扣上的瞬間，紙箱方向傳來細細嗚嗚，\n一下、一下，像敲在門板上。\n小晴把臉埋進枕頭，告訴自己明天還要上班。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("slept_in_living", False)
            narrator "門縫外的雨停了。嗚嗚沒停很久——\n但距離，又遠了一點。"
            jump d1_night_box
        "今晚就待在客廳陪牠":
            hide dog
            show char sit_floor at char_center
            with Dissolve(0.25)
            $ dog_sfx("sigh")
            narrator "她沒回房。外套蓋在腿上，\n螢幕停在《第一次帶幼犬回家你需要知道的十件事》，\n看到第三件眼睛就糊了。\n\n紙箱裡呼吸聲極輕，偶爾一兩聲夢囈似的嗚。"
            xq "先活過今晚。我們……都是。"
            hide char
            show dog sleepy at dog_bottom
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("slept_in_living", True)
            jump d1_night_box


label d1_night_box:
    $ smell_text = "乾毛巾、雨停後的空氣"
    $ play_bgm("warm_quiet")
    scene bg living_night
    show dog sleepy at dog_bottom
    $ dog_sfx("soft")

    narrator "乾淨毛巾墊進紙箱，濕紙板抽掉一角。\n[dog_label]肚子微鼓，眼睛半閉，拖鞋聲一響仍會豎一下耳朵。"
    xq "我還不知道你叫什麼。"
    xq "……明天再說。"
    narrator "雨停了。屋簷偶爾滴水。"

    $ set_flag("bathed", False)
    $ set_flag("named", False)
    $ add_landmark("landmark_cardboard_rain")
    if get_flag("gave_space"):
        $ add_landmark("landmark_first_space")

    $ save_name = "第1天結束｜信任 " + str(trust)
    narrator "—— 第 1 天結束 ——\n信任：[trust]　知識分：[knowledge_score]\n\n窗外漸漸亮了。客廳裡，還有另一場「意外」等著。"
    jump d2_morning_mess
