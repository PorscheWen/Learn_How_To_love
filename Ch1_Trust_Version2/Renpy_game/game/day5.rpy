## Week0 Day5｜牠肯靠近一點
## 來源：week0/day5_a_little_closer.md ｜ agents/plot.md ｜ agents/audio.md

label d5_afternoon_light:
    $ story_day = 5
    $ smell_text = "陽光塵、飼料、毯子"
    $ play_bgm("soft_growth")
    scene bg living_day
    with Dissolve(0.5)
    show dog shy at dog_bottom
    with Dissolve(0.3)

    narrator "週日。窗外有人在曬衣服，塑膠夾子喀喀響。\n小晴盤腿坐在地板滑手機，肩膀終於沒那麼緊。"
    narrator "[dog_label]在紙箱與尿墊之間走了一條熟悉的線。水碗見底，她起身去裝——\n回來時，發現毛團不在原位。"
    jump d5_approaches


label d5_approaches:
    $ smell_text = "褲管布料、皮膚溫熱"
    $ play_bgm("tender")
    scene bg living_day
    show dog shy at dog_bottom
    $ dog_sfx("soft")

    narrator "牠停在她腳邊。不是撲，是試探。\n鼻子碰到褲管布料，抽了兩下。耳朵半豎。尾巴貼著，尖端卻極輕顫了一下。"
    narrator "距離近到能聽見彼此呼吸。"
    xq "……[dog_label]？"
    if get_flag("gave_space"):
        narrator "像第一夜那半步，終於被還回來一點。"
    if get_flag("grabbed_from_box") or get_flag("touched_too_soon"):
        narrator "牠靠近時仍會閃一下肩膀，像記得手的速度。"
    $ dog_sfx("murmur")
    pudding "（嗚……）"
    jump d5_choice_react


label d5_choice_react:
    $ smell_text = "腳邊溫熱"
    scene bg living_day
    show dog shy at dog_bottom

    narrator "牠就在腳邊。你現在……？"
    menu:
        "一把抱起轉圈":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "身體離地的瞬間，[dog_label]短促悲鳴，四肢蹬空。尾巴夾緊。\n小晴高興的笑聲卡在一半。"
            xq "對不起！我太開心了——"
            narrator "放到地上後，牠退回紙箱，距離又拉開。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("hugged_too_fast", True)
            jump d5_kg_body
        "不動，讓牠自己靠過來":
            $ dog_sfx("soft_b")
            narrator "她連腳趾都不敢動。[dog_label]又靠近一點，側身輕輕貼上小腿——\n一觸即離，再貼一次，久一點。"
            narrator "溫度透過布料傳上來。很小，卻很清楚。"
            xq "……好。你決定。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("let_dog_choose_distance", True)
            jump d5_kg_body


label d5_kg_body:
    $ smell_text = "螢幕光、午後空氣"
    $ play_bgm("tender")
    scene bg living_day
    show dog shy at dog_bottom
    call kg_d5_body_language from _call_kg_d5
    jump d5_tg_sniff_pet


label d5_tg_sniff_pet:
    $ smell_text = "手掌、肩背毛"
    scene bg living_day
    show dog shy at dog_bottom
    call tg_d5_sniff_then_pet from _call_tg_d5
    jump d5_choice_touch


label d5_choice_touch:
    $ smell_text = "掌心溫度"
    scene bg living_day
    show dog shy at dog_bottom

    ## 信任小遊戲成功：已摸過背，勿重考部位
    if get_flag("sniff_then_pet_ok"):
        $ dog_sfx("soft")
        narrator "掌心還留著剛才那一下。[dog_label]沒退。\n她把手機扣遠一點——接下來，只想把這個距離留住。"
        $ set_flag("touched_back", True)
        jump d5_choice_ritual

    narrator "手伸出去之前——摸哪裡？"
    menu:
        "直接摸頭／臉":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            if get_flag("touched_too_soon"):
                narrator "回憶刺痛——一樣的閃躲。"
            narrator "頂毛一被壓，[dog_label]眨眼躲，耳朵貼平。不是攻擊，是拒絕。"
            xq "頭不行。好。頭不行。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("touched_head_again", True)
            jump d5_choice_ritual
        "輕摸背／肩":
            $ dog_sfx("soft")
            narrator "掌心貼在肩胛附近。[dog_label]身體沒僵。呼吸還在，甚至更慢一點。"
            xq "這裡。這裡比較好。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("touched_back", True)
            jump d5_choice_ritual


label d5_choice_ritual:
    $ smell_text = "舊毯子、毛球"
    $ play_bgm("warm")
    scene bg living_day
    show dog shy at dog_bottom

    narrator "接下來——你想留下什麼？"
    menu:
        "掏手機，開閃光燈拍照":
            show dog scare at dog_bottom
            $ dog_sfx("whimper")
            narrator "白光炸開。[dog_label]嚇得往後退，嗚嗚變尖，剛剛的靠近像被擦掉。"
            xq "啊——抱歉！我只是想留……"
            narrator "螢幕裡是一張模糊的、空的地板。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("flash_photo", True)
            jump d5_day_end
        "同一條毯子，安靜坐五分鐘":
            hide dog
            show char sit_floor at char_center
            with Dissolve(0.25)
            $ dog_sfx("sigh")
            narrator "毯子舊、有點毛球。兩人各佔一端，中間空一掌寬。\n手機扣在遠處。計時器響之前，[dog_label]又靠近了一點——頭靠上她膝蓋外側。"
            narrator "沒有主題音樂。只有呼吸。"
            xq "就這樣。不用更多。"
            hide char
            show dog sleepy at dog_bottom
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("blanket_five_min", True)
            jump d5_day_end


label d5_day_end:
    $ smell_text = "小腿邊溫熱、紙箱外空氣"
    $ play_bgm("warm_quiet")
    scene bg living_night
    with Dissolve(0.5)
    show dog sleepy at dog_bottom
    $ dog_sfx("soft")

    narrator "傍晚，紙箱還在，但[dog_label]有一半時間待在箱外。\n小腿邊留下一點溫熱——很小，卻記得住。"
    xq "你肯靠近一點了。"
    xq "我不會一次要全部。"
    if get_flag("sniff_then_pet_ok") and get_flag("blanket_five_min"):
        narrator "敢待著。比敢撲更難，也更安靜。"

    $ add_landmark("landmark_first_lean")
    $ save_name = "第5天結束｜" + dog_label + "｜信任 " + str(trust)
    narrator "—— 第 5 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]\n\n信任升高之後，日子也不會永遠這麼輕。"
    jump d6_chewed_cord
