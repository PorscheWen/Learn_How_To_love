## Week0 Day7｜紙箱以外的名字
## 來源：week0/day7_name_beyond_the_box.md ｜ agents/plot.md ｜ agents/audio.md

label d7_box_to_balcony:
    $ story_day = 7
    $ smell_text = "乾毛巾、陽台雜物、舊紙箱"
    $ play_bgm("warm")
    scene bg living_day
    with Dissolve(0.5)
    show dog shy at dog_bottom
    with Dissolve(0.3)
    $ dog_sfx("murmur")

    narrator "第七天早上。紙箱邊角還有雨天的水痕，已經乾成淺褐。\n小晴把乾毛巾、舊外套拿出來，箱子折平，塞進陽台雜物堆——不是丟掉，是騰出地板。"
    narrator "[dog_label]站在尿墊邊看著。鼻子抽動。箱子的氣味薄了。"
    xq "不是不要你。"
    xq "是這裡……該有你待的地方。不是路邊那種。"
    narrator "毯子鋪在牆角。比紙箱軟，也比較不像臨時。"
    jump d7_choice_list


label d7_choice_list:
    $ smell_text = "備忘錄、客廳日光"
    $ play_bgm("warm")
    scene bg living_day
    with Dissolve(0.4)
    show dog shy at dog_bottom

    narrator "責任清單攤開。疫苗、驅蟲、花費、誰照顧——"
    menu:
        "「好麻煩」，先擺著不做":
            narrator "每一行都像加班單。她把手機扣上。"
            xq "等等。我先把今天撐過去。"
            narrator "清單仍在備忘錄最上層，未勾。心口有點緊。"
            $ set_flag("checklist_deferred", True)
            jump d7_kg_checklist
        "逐項勾：疫苗／驅蟲／花費":
            narrator "她算了一下存款。眉頭皺了又鬆。"
            xq "貴。可是……比你不見要好算。"
            narrator "勾選聲一下一下。[dog_label]歪頭，不懂數字，只懂她坐得比較穩。"
            $ set_flag("checklist_started", True)
            jump d7_kg_checklist


label d7_kg_checklist:
    $ smell_text = "備忘錄墨水"
    scene bg living_day
    show dog shy at dog_bottom
    call kg_d7_care_checklist from _call_kg_d7
    jump d7_to_clinic


label d7_to_clinic:
    $ smell_text = "毛巾、戶外空氣、遠方犬吠"
    $ play_bgm("clinic_soft")
    scene bg treestreet_day
    with Dissolve(0.45)
    show dog anxious at dog_bottom
    $ dog_sfx("whimper")

    narrator "提袋裡是證件、紙巾、咬咬玩具。[dog_label]被毛巾半裹，嗚嗚斷續。\n樹蔭底下比較不刺眼。路上有狗叫聲從別的車傳來，牠縮得更緊。"
    if get_flag("checklist_deferred"):
        narrator "備忘錄還開著——空白勾選。她把手機塞進口袋，手心有點黏。"
    elif get_flag("checklist_started"):
        narrator "提袋側袋夾著剛勾過的清單。至少知道接下來要問醫生什麼。"
    xq "我們去看醫生。不是丟你。"
    narrator "她說了兩次。第二次比較像說給自己聽。"
    jump d7_choice_carrier


label d7_choice_carrier:
    $ smell_text = "提袋塑膠、毛巾、樹葉氣"
    scene bg treestreet_day
    show dog anxious at dog_bottom

    narrator "去醫院路上，怎麼帶？"
    menu:
        "硬塞進提籠，抱得太緊":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "[dog_label]尖叫似的嗚嗚，爪子亂抓。提籠門扣上的瞬間，信任像被擠扁。"
            xq "抱歉、抱歉，快到了——"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("forced_carrier", True)
            jump d7_tg_clinic
        "毛巾蓋著，輕聲說話":
            $ dog_sfx("soft")
            narrator "光線被遮掉一點。[dog_label]嗚嗚變短。小晴每走一段就重複同一句。"
            xq "我在。還在。快到了。"
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("towel_calm_trip", True)
            jump d7_tg_clinic


label d7_tg_clinic:
    $ smell_text = "消毒水、候診走廊"
    $ play_bgm("calm")
    scene bg clinic_day
    with Dissolve(0.45)
    show dog anxious at dog_bottom
    call tg_d7_clinic_calm from _call_tg_d7
    jump d7_choice_adopt


label d7_choice_adopt:
    $ smell_text = "診所單據、消毒水"
    $ play_bgm("tender")
    scene bg clinic_day
    show dog shy at dog_bottom

    narrator "「身體目前看起來還穩定。接下來疫苗與驅蟲要排程。」\n「你呢——確定要養下來嗎？」"
    menu:
        "「再觀察一週」":
            narrator "獸醫點頭，沒有責備。小晴抱著[dog_label]，掌心卻虛。"
            xq "我不是不要。我只是……怕我又弄不好。"
            $ set_flag("adopted", False)
            $ set_flag("deferred_adoption", True)
            jump d7_home_again
        "「我想正式養下來」":
            narrator "聲音比預想的穩。獸醫笑了一下，開始寫單。"
            xq "名字叫[dog_label]。我……會學。"
            $ set_flag("adopted", True)
            $ set_flag("deferred_adoption", False)
            jump d7_home_again


label d7_home_again:
    $ smell_text = "家、尿墊、褲管"
    $ play_bgm("tender")
    scene bg living_night
    with Dissolve(0.5)
    show dog shy at dog_bottom
    $ dog_sfx("soft")

    narrator "門開。毯子還在。紙箱不在客廳正中央了。\n[dog_label]踩過門檻，先嗅尿墊，再嗅小晴的褲管——確認這趟外出有把「家」帶回來。"
    jump d7_choice_name


label d7_choice_name:
    $ smell_text = "飼料、夜客廳"
    scene bg living_night
    show dog shy at dog_bottom

    if get_flag("adopted"):
        ## 診所已報名：不可再選「喂」
        narrator "你剛跟醫生說了名字。回家怎麼叫？"
        menu:
            "敷衍喊一下名字，就去忙別的":
                $ dog_sfx("murmur")
                xq "[dog_label]——吃飯。"
                narrator "有叫到。可是像點名，溫度薄一點。"
                $ set_flag("uses_proper_name", True)
                $ set_flag("name_said_casually", True)
                jump d7_ending
            "認真叫名字，並輕摸背":
                if trust >= 4:
                    show dog sleepy at dog_bottom
                    $ dog_sfx("yip")
                    xq "[dog_label]。"
                    narrator "耳朵轉過來。她等牠聞手，再摸背——短、穩。\n尾巴慢搖了一小段。不是表演，是還在學怎麼待在同一個房間。"
                    $ set_flag("uses_proper_name", True)
                else:
                    $ dog_sfx("soft")
                    xq "[dog_label]。"
                    narrator "輕聲叫了名字，沒有強摸。距離還在，但名字落地了半步。"
                    $ set_flag("uses_proper_name", True)
                jump d7_ending
    else:
        narrator "回家後，怎麼叫牠？"
        menu:
            "仍叫「喂」或「小狗」":
                $ dog_sfx("murmur")
                narrator "[dog_label]有反應，但耳朵只動一下。名字像還沒落地。"
                xq "喂——過來吃飯。"
                narrator "功能夠用。溫度薄一點。"
                $ set_flag("uses_proper_name", False)
                jump d7_ending
            "認真叫名字，並輕摸背":
                if trust >= 4:
                    show dog sleepy at dog_bottom
                    $ dog_sfx("yip")
                    xq "[dog_label]。"
                    narrator "耳朵轉過來。她等牠聞手，再摸背——短、穩。\n尾巴慢搖了一小段。不是表演，是還在學怎麼待在同一個房間。"
                    $ set_flag("uses_proper_name", True)
                else:
                    $ dog_sfx("soft")
                    xq "[dog_label]。"
                    narrator "輕聲叫了名字，沒有強摸。距離還在，但名字落地了半步。"
                    $ set_flag("uses_proper_name", True)
                jump d7_ending


label d7_ending:
    $ smell_text = "水碗、牙印玩具、家"
    scene bg living_night
    show dog sleepy at dog_bottom

    if trust >= 6:
        $ play_bgm("ending_warm")
        show dog shy at dog_bottom
        $ dog_sfx("soft")
        narrator "雨後的第七天。陽台紙箱安靜。客廳有水碗、尿墊、牙印玩具，\n還有一個會加班、會搞砸、會道歉的人。"
        narrator "[dog_label]把下巴擱在她拖鞋邊。不重。夠了。"
        if get_flag("adopted"):
            xq "我們一起過平常的日子。"
        else:
            xq "先留下來。我們慢慢學怎麼過平常的日子。"
        if get_flag("uses_proper_name"):
            xq "紙箱以外——你叫[dog_label]。"
            xq "我叫小晴。我們……回家了。"
        else:
            xq "紙箱以外——這裡是你家。我叫小晴。"
    elif trust >= 3:
        $ play_bgm("ending_quiet")
        $ dog_sfx("sigh")
        narrator "同毯兩端。中間空一掌寬。[dog_label]偶爾靠近，又退回去一點。"
        if get_flag("adopted"):
            xq "慢慢來。我留下。"
        elif get_flag("deferred_adoption"):
            xq "再觀察。但水碗是滿的。門沒關死。"
        else:
            xq "慢慢來。我在。"
        if get_flag("checklist_started"):
            narrator "備忘錄上的勾選還在。比猶豫多了一點形狀。"
    else:
        $ play_bgm("ending_quiet")
        show dog anxious at dog_bottom
        $ dog_sfx("murmur")
        narrator "牠還是會縮。小晴也還是會慌。\n但門沒關死。水碗是滿的。明天還有疫苗單上的電話。"
        xq "先別決定世界。先吃一口。"
        if get_flag("deferred_adoption") or not get_flag("adopted"):
            narrator "暫留、再學——不是懲罰。只是距離還在。"

    if get_flag("adopted"):
        $ add_landmark("landmark_adopted")
    $ add_landmark("landmark_week0_complete")
    $ save_name = "第7天結束｜" + dog_label + "｜信任 " + str(trust)
    narrator "—— 第 7 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]"
    return
