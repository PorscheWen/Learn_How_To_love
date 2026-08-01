## Week0 Day6｜小意外與道歉
## 來源：week0/day6_accident_and_apology.md ｜ agents/plot.md ｜ agents/audio.md

label d6_chewed_cord:
    $ story_day = 6
    $ smell_text = "塑膠、斷線、膠皮"
    $ play_bgm("tension_soft")
    scene bg living_day
    with Dissolve(0.5)
    show dog scare at dog_bottom
    with Dissolve(0.3)
    $ dog_sfx("whimper")

    narrator "加班回家。拖鞋一腳踢到什麼——充電線斷成兩截，膠皮開花，銅絲亮著。\n旁邊還有一隻拖鞋，鞋舌被嚼到變形，像被笑過的臉。"
    narrator "[dog_label]蹲在沙發腳邊。耳朵貼平，尾巴夾緊。嘴邊有一點白屑。"
    pudding "（嗚……）"
    narrator "空氣裡有塑膠味。小晴手心先熱，再涼。"
    xq "……這是我的線。"
    xq "這是——電。"
    jump d6_choice_scene


label d6_choice_scene:
    $ smell_text = "斷線、碎屑"
    scene bg living_day
    show dog scare at dog_bottom

    narrator "發現現場，第一個反應——"
    menu:
        "拍桌大罵，嚇牠":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "一聲拍擊，[dog_label]整團縮到牆角，短促悲鳴連發。\n尿墊邊濕了一小塊——嚇出來的。"
            xq "你知道這樣會怎樣嗎——！"
            narrator "話比腦子快。線還插在牆上。"
            $ add_trust(-2)
            $ show_trust_toast(-2)
            $ set_flag("yelled_at_chew", True)
            jump d6_choice_words
        "先把插頭拔掉，清開碎片":
            $ dog_sfx("murmur")
            narrator "她踩著碎屑跪下，手指發抖，還是先拔電。斷線丟進袋子，碎片撿乾淨。"
            narrator "[dog_label]仍縮著，但嗚嗚沒有被拍桌聲推高。"
            xq "先……先不要死。誰都不要。"
            $ set_flag("secured_cord_first", True)
            jump d6_choice_words


label d6_choice_words:
    $ smell_text = "塑膠、清潔後地板"
    $ play_bgm("calm")
    scene bg living_day
    show dog scare at dog_bottom
    if get_flag("yelled_at_chew"):
        narrator "安全還沒處理完。但話已經到嘴邊——你要對[dog_label]說什麼？"
    else:
        narrator "對[dog_label]說什麼？"

    menu:
        "「再這樣我就把你送走」":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "[dog_label]不懂句子，聽得懂語氣。身體更扁，眼睛亮得像要碎。"
            narrator "小晴說完就後悔。胸口像被自己踩了一腳。"
            xq "我不是……我不是那個意思。"
            narrator "太晚了。氣氛已經裂開。"
            $ add_trust(-2)
            $ show_trust_toast(-2)
            $ set_flag("said_abandon_threat", True)
            jump d6_kg_chew
        "「是我沒收好」":
            show dog shy at dog_bottom
            $ dog_sfx("soft")
            narrator "她蹲低，聲音啞。"
            xq "線是我亂放的。拖鞋也是。"
            xq "你不是壞。是我太累，沒收好。"
            narrator "[dog_label]鼻子動了動。嗚嗚還在，但沒有再往後退。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("owned_the_mess", True)
            jump d6_kg_chew


label d6_kg_chew:
    $ smell_text = "螢幕、斷線袋"
    $ play_bgm("calm")
    scene bg living_day
    show dog anxious at dog_bottom
    call kg_d6_why_chew from _call_kg_d6
    jump d6_tg_trade


label d6_tg_trade:
    $ smell_text = "橡膠玩具、碎膠皮"
    $ play_bgm("tender")
    scene bg living_day
    show dog shy at dog_bottom
    call tg_d6_trade_toy from _call_tg_d6
    jump d6_choice_after


label d6_choice_after:
    $ smell_text = "咬咬玩具、抽屜"
    scene bg living_day
    show dog anxious at dog_bottom

    narrator "善後——"
    menu:
        "只收東西，整晚不理牠":
            $ dog_sfx("murmur_b")
            narrator "線收進抽屜，拖鞋進垃圾桶。紙箱方向偶爾傳來嗚嗚，她裝成聽不見。"
            narrator "客廳很乾淨。也很冷。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("ignored_after_chew", True)
            jump d6_choice_night
        "拿出咬咬玩具，繼續陪牠把氣消掉":
            show dog shy at dog_bottom
            $ dog_sfx("yip")
            narrator "玩具被咬得喀喀響。小晴坐在可見距離，偶爾出聲。"
            xq "氣消了再靠近。我也不急。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("gave_chew_outlet", True)
            jump d6_choice_night


label d6_choice_night:
    $ smell_text = "延長線、毯子"
    $ play_bgm("warm")
    scene bg living_night
    with Dissolve(0.45)
    show dog anxious at dog_bottom

    narrator "晚上怎麼待？"
    menu:
        "把牠關進浴室當懲罰":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "磁磚回音把嗚嗚放大。門縫下伸出爪子刮刮刮。\n小晴坐在客廳，懲罰的是兩個人。"
            $ add_trust(-2)
            $ show_trust_toast(-2)
            $ set_flag("locked_in_bathroom", True)
            jump d6_day_end
        "同室相處，但把電線全部收高":
            show dog sleepy at dog_bottom
            $ dog_sfx("sigh")
            narrator "延長線捲好塞進盒子。桌緣清出安全帶。\n[dog_label]靠回毯子邊，咬著玩具，偶爾看她一眼。"
            xq "今天是我害的。明天把家收成你咬不到電的樣子。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("puppy_proofed_night", True)
            jump d6_day_end


label d6_day_end:
    $ smell_text = "橡膠玩具牙印、回收袋"
    $ play_bgm("warm_quiet")
    scene bg living_night
    show dog sleepy at dog_bottom
    $ dog_sfx("soft")

    narrator "斷線進了回收袋。新的咬咬玩具已經有牙印。\n[dog_label]睡在箱外一點點——還不敢太遠，也不再縮到最底。"
    xq "下次我先收好。"
    xq "你下次……也盡量咬對的那個。"
    narrator "她知道狗不懂「盡量」。但人需要說出口。"
    if get_flag("owned_the_mess") and get_flag("traded_toy_ok"):
        narrator "今天沒把關係搞斷。還在。"
    if get_flag("said_abandon_threat"):
        narrator "那句「送走」還掛在空氣裡。明天說出口的話，要更小心。"

    $ add_landmark("landmark_chew_accident")
    $ save_name = "第6天結束｜" + dog_label + "｜信任 " + str(trust)
    narrator "—— 第 6 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]\n\n紙箱以外——也許該有名字落地的地方。"
    jump d7_box_to_balcony
