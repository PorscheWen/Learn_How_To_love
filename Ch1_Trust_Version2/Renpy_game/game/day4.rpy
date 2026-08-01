## Week0 Day4｜半夜的哭聲
## 來源：week0/day4_midnight_whine.md ｜ agents/plot.md ｜ agents/audio.md

label d4_bedtime:
    $ story_day = 4
    $ smell_text = "小夜燈熱度、紙箱毛巾"
    $ play_bgm("night_thin")
    scene bg living_night
    with Dissolve(0.5)
    show dog anxious at dog_bottom
    with Dissolve(0.3)
    $ dog_sfx("murmur")

    narrator "加班訊息終於停了。小晴關掉客廳燈，紙箱和小夜燈留一盞。"
    narrator "[dog_label]眼睛在暗裡亮著。尾巴不動，耳朵卻跟著她的腳步轉。"
    xq "我也要睡了。真的。"
    if get_flag("slept_in_living"):
        narrator "她站在房門口，手按著門把。第一夜若陪過客廳，此刻距離感會更刺——\n像把好不容易近的半步又拉遠。"
    else:
        narrator "她站在房門口，手按著門把。"
    jump d4_choice_door


label d4_choice_door:
    $ smell_text = "門縫、紙箱"
    scene bg living_night
    show dog anxious at dog_bottom

    narrator "剛進房，怎麼關？"
    menu:
        "立刻關門，不說一句話":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "門扣上的聲音很輕，紙箱方向的嗚嗚卻立刻拔高。\n一下、一下，像敲在門板上。"
            narrator "小晴背靠門板，閉眼。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("slammed_door_silent", True)
            jump d4_whine_up
        "先輕聲說「我在」再關":
            $ dog_sfx("soft")
            xq "[dog_label]。我在隔壁。不是消失。"
            narrator "門仍關上。嗚嗚有，但短了一拍——像被那句話卡住半秒。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("said_im_here", True)
            jump d4_whine_up


label d4_whine_up:
    $ smell_text = "枕頭、深夜空氣"
    $ play_bgm("calm")
    scene bg living_night
    show dog scare at dog_bottom
    $ dog_sfx("whimper_b")

    narrator "十一點。十二點。嗚嗚沒停，只是變成間歇的、磨人的節奏。\n隔壁住戶走路聲經過一次，[dog_label]又尖了一下。"
    narrator "小晴盯著天花板。眼皮打架，神經卻醒著。"
    xq "……我明天還要開會啊。"
    jump d4_choice_response


label d4_choice_response:
    $ smell_text = "耳機線、門縫"
    scene bg living_night
    show dog scare at dog_bottom

    narrator "哭聲升級。你要怎麼辦？"
    menu:
        "塞上耳機，硬睡":
            narrator "音樂進來，狗聲變遠。她以為勝利了——\n直到醒來發現耳機掉一邊，另一邊臉頰濕的，不知是汗還是什麼。"
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "門外，[dog_label]嗓子已經啞了半截。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("headphones_night", True)
            jump d4_kg_separation
        "開門，坐在看得見的地方":
            show dog shy at dog_bottom
            $ dog_sfx("soft")
            narrator "門開一條縫。[dog_label]嗚嗚卡一下，前爪踩到箱邊，又縮回去。"
            narrator "小晴沒抱牠。只坐在地板上，外套蓋住腿。"
            xq "看得到就好。別叫了……求你。"
            narrator "嗚嗚降成偶爾一兩聲。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("opened_for_visible", True)
            jump d4_kg_separation


label d4_kg_separation:
    $ smell_text = "螢幕低光、枕頭"
    $ play_bgm("calm")
    scene bg living_night
    show dog anxious at dog_bottom
    call kg_d4_separation from _call_kg_d4
    jump d4_tg_visible_sleep


label d4_tg_visible_sleep:
    $ smell_text = "枕頭、毯子、紙箱口"
    $ play_bgm("tender")
    scene bg living_night
    show dog sleepy at dog_bottom
    call tg_d4_visible_sleep from _call_tg_d4
    jump d4_choice_comfort


label d4_choice_comfort:
    $ smell_text = "枕頭、同室空氣"
    scene bg living_night
    show dog shy at dog_bottom

    narrator "牠終於安靜一點。你要……？"
    menu:
        "整晚緊抱不放":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "[dog_label]先是僵，後來才鬆一點。小晴手臂發麻，凌晨三點兩人都沒真正睡著。\n牠習慣了溫度——也更怕溫度消失。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("hugged_all_night", True)
            jump d4_dawn
        "同室不同床，偶爾輕聲出聲":
            show dog sleepy at dog_bottom
            $ dog_sfx("sigh")
            narrator "她躺回枕頭，紙箱在視線裡。隔一段時間才說一句很短的話。"
            xq "還在。"
            xq "睡。"
            narrator "[dog_label]耳朵動動，嗚嗚不再連成線。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("same_room_apart", True)
            jump d4_dawn


label d4_dawn:
    $ smell_text = "陽光、啞嗓子、黑眼圈"
    $ play_bgm("warm")
    scene bg living_day
    with Dissolve(0.5)
    show dog sleepy at dog_bottom

    narrator "鬧鐘比人兇。陽光從窗簾縫刺進來。\n[dog_label]眼睛睜著，嗓子有點啞。小晴黑眼圈像印章。"
    narrator "兩人對看。誰都沒贏。"
    jump d4_choice_morning


label d4_choice_morning:
    $ smell_text = "空碗、晨光"
    scene bg living_day
    show dog anxious at dog_bottom

    narrator "天亮後，怎麼說？"
    menu:
        "你昨晚吵死了":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "聲音一沉，[dog_label]耳朵貼平，退半步。空碗邊的爪子縮回去。"
            xq "……我也知道你不是故意的。可是——算了。"
            narrator "話出了口，空氣涼了一截。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("blamed_morning", True)
            jump d4_day_end
        "「我們都好累。可是你有叫我」":
            show dog shy at dog_bottom
            $ dog_sfx("soft")
            narrator "她蹲下去，沒伸手。"
            xq "我聽到了。下次……我們練習短一點的分開。"
            narrator "[dog_label]鼻子動了動。嗚嗚很輕，像回應，又像只是啞了。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("morning_gentle", True)
            jump d4_day_end


label d4_day_end:
    $ smell_text = "飼料、門口十秒練習"
    $ play_bgm("warm_quiet")
    scene bg living_day
    with Dissolve(0.45)
    show dog sleepy at dog_bottom
    $ dog_sfx("sigh")

    narrator "白天兩人都昏沉。飼料碗見底又裝滿。\n傍晚，小晴練習：走到門口、說一句、回來——只有十秒。[dog_label]嗚嗚，但沒有昨晚那麼長。"
    if get_flag("slept_in_living"):
        narrator "又是客廳地板。這次至少是清醒的練習。"
    xq "十秒。我們先會十秒。"

    $ add_landmark("landmark_midnight_whine")
    if get_flag("visible_sleep_ok"):
        $ add_landmark("landmark_visible_circle")
    $ save_name = "第4天結束｜" + dog_label + "｜信任 " + str(trust)
    narrator "—— 第 4 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]\n\n明天，也許牠會再靠近半步。"
    jump d5_afternoon_light
