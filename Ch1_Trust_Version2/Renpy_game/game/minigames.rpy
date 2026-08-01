## Day1 小遊戲：知識 5 題＋信任靜距餵食

label kg_d1_puppy_first_aid:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "幼犬急救卡"
    show screen knowledge_hud
    narrator "螢幕亮著，拇指滑得飛快。\n標題一行比一行兇，她卻只抓得住關鍵句。"

    ## Q1｜絕對不能馬上洗澡
    narrator "剛撿到、全身濕透的幼犬，現在可以洗澡嗎？"
    menu:
        "可以，髒就要立刻用沐浴乳洗乾淨":
            narrator "不行。只能用溫水毛巾吸乾，再低溫保暖。\n這時洗澡，免疫力低又受驚，可能引發嚴重疾病。"
        "不行；溫水毛巾吸乾，再低溫保暖":
            $ knowledge_correct_today += 1
            narrator "不行。只能用溫水毛巾吸乾，再低溫保暖。\n這時洗澡，免疫力低又受驚，可能引發嚴重疾病。"
        "先泡熱水澡暖身體再擦":
            narrator "不行。只能用溫水毛巾吸乾，再低溫保暖。\n這時洗澡，免疫力低又受驚，可能引發嚴重疾病。"

    ## Q2｜安全避難所
    narrator "剛帶回家，怎麼給[dog_label]一個「安全避難所」？"
    menu:
        "紙箱或籠子鋪舊衣服，放安靜角落；不強迫[dog_label]出來":
            $ knowledge_correct_today += 1
            narrator "讓[dog_label]有地方躲。不要硬抱出來，安全感比熱情重要。"
        "一直抱在懷裡，才能讓[dog_label]安心":
            narrator "讓[dog_label]有地方躲。不要硬抱出來，安全感比熱情重要。"
        "趕緊拿到客廳正中央，讓全家輪流看":
            narrator "讓[dog_label]有地方躲。不要硬抱出來，安全感比熱情重要。"

    ## Q3｜保暖至上
    narrator "淋過雨的幼犬，保暖要注意什麼？"
    menu:
        "開窗通風，讓毛自然吹乾":
            narrator "體溫調節差。室內要無風，並給保暖的毛毯。"
        "確保室內無風，並給保暖的毛毯":
            $ knowledge_correct_today += 1
            narrator "體溫調節差。室內要無風，並給保暖的毛毯。"
        "蓋厚被悶緊，完全不要透氣":
            narrator "體溫調節差。室內要無風，並給保暖的毛毯。"

    ## Q4｜乾淨飲水
    narrator "飲水怎麼準備比較安心？"
    menu:
        "自來水直接裝滿大碗就好":
            narrator "用乾淨淺碗裝生開水，不要用自來水；隨時補充。"
        "乾淨淺碗裝生開水，隨時補充":
            $ knowledge_correct_today += 1
            narrator "用乾淨淺碗裝生開水，不要用自來水；隨時補充。"
        "冰牛奶當正餐最補水":
            narrator "用乾淨淺碗裝生開水，不要用自來水；隨時補充。"

    ## Q5｜三不原則（空間給信任；誤食細節另見 Day2 隱藏知識）
    narrator "剛換環境，實行「三不原則」是指？"
    menu:
        "多吵鬧陪玩、硬抱安撫、一直盯著看":
            narrator "三不：不吵鬧、不強抱、不一直盯。先讓牠有地方躲，比你熱心更重要。"
        "不吵鬧、不強抱、不一直盯著看":
            $ knowledge_correct_today += 1
            narrator "三不：不吵鬧、不強抱、不一直盯。先讓牠有地方躲，比你熱心更重要。"
        "零食和小物隨便放地上沒關係，多陪就好":
            narrator "三不：不吵鬧、不強抱、不一直盯。先讓牠有地方躲，比你熱心更重要。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d1_puppy_first_aid")
        $ knowledge_score += 1
        $ set_flag("knows_towel_first", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "所以是……先擦乾、保暖、給水。\n洗澡以後再說。也別太吵、別硬抱、別一直盯。"
    else:
        xq "好亂。算了，先別亂沖，應該沒差吧……"
    return


label tg_d1_space_feed:
    $ _tg_retries = 1
    jump tg_d1_space_feed_try

label tg_d1_space_feed_try:
    narrator "把食盤拖到紙箱前，然後後退——\n倒數幾秒，不要伸手、不要戳牠。"
    menu:
        "放好食盤，自己退後等待":
            call screen tg_space_feed_wait(seconds=4.0)
            if _return == "success":
                jump tg_d1_space_feed_success
            else:
                jump tg_d1_space_feed_fail
        "忍不住伸手想安撫":
            jump tg_d1_space_feed_fail

label tg_d1_space_feed_success:
    show dog shy at dog_bottom
    $ dog_sfx("soft")
    narrator "盤子停在開口前。小晴整個人往後坐，背靠沙發腳。\n\n[dog_label]鼻子伸出來，縮回去，再伸出來。\n嗚嗚變軟。前爪踩過毛巾邊，一小步、一小步，終於低頭開吃。\n\n尾巴尖端極輕顫了一下，又很快停住。"
    xq "……慢點啦。"
    $ add_trust(2)
    $ show_trust_toast(2)
    $ clear_minigame("tg_d1_space_feed")
    $ set_flag("fed", True)
    $ set_flag("gave_space", True)
    return

label tg_d1_space_feed_fail:
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "手指一伸，[dog_label]猛退，嗚嗚變尖，盤子被撞歪。"
    xq "對不起——我又手賤……"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        narrator "再試一次。這次，把手放好。"
        show dog hungry at dog_bottom
        jump tg_d1_space_feed_try
    narrator "[dog_label]稍後才肯靠近那點食物。今晚先這樣。"
    return


## —— Day2：知識｜定點迷思 5 題 ——
label kg_d2_potty_myths:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "定點迷思卡"
    show screen knowledge_hud
    narrator "標題一個比一個兇。她只想找一句不會讓兩人都更慘的話。"

    narrator "幼犬在家亂尿，用力罵一頓會更快學會定點嗎？"
    menu:
        "會，要當下糾正":
            narrator "不會。罵聲常讓[dog_label]把「人靠近」跟「可怕」連在一起，定點更難。"
        "不會；驚嚇常讓[dog_label]更躲著尿":
            $ knowledge_correct_today += 1
            narrator "不會。罵聲常讓[dog_label]把「人靠近」跟「可怕」連在一起，定點更難。"

    narrator "兩個月大的幼犬可以憋很久嗎？"
    menu:
        "可以像大人一樣半天":
            narrator "不行。膀胱很小，通常需要很常帶去墊子／戶外機會。"
        "不行；通常需要很常帶去墊子／戶外機會":
            $ knowledge_correct_today += 1
            narrator "不行。膀胱很小，通常需要很常帶去墊子／戶外機會。"

    narrator "發現地上已乾的便便，把[dog_label]抓過來罵有用嗎？"
    menu:
        "有用，[dog_label]會連起來":
            narrator "沒用。[dog_label]連不起「現在」和「剛才」；事後罰只會嚇到當下的[dog_label]。"
        "沒用；[dog_label]連不起「現在」和「剛才」":
            $ knowledge_correct_today += 1
            narrator "沒用。[dog_label]連不起「現在」和「剛才」；事後罰只會嚇到當下的[dog_label]。"

    narrator "清潔尿味時，用很香的漂白水猛噴最好？"
    menu:
        "對，蓋過味道":
            narrator "不建議。刺激又刺鼻；溫和清潔＋除尿味產品比較安心。"
        "不建議；溫和清潔比較安心":
            $ knowledge_correct_today += 1
            narrator "不建議。刺激又刺鼻；溫和清潔＋除尿味產品比較安心。"

    narrator "尿墊要放哪裡較合理（新手期）？"
    menu:
        "每天換房間訓練「隨機應變」":
            narrator "先固定位置，讓氣味與習慣穩定。亂換＝每天重新學。"
        "固定位置，讓氣味與習慣穩定":
            $ knowledge_correct_today += 1
            narrator "先固定位置，讓氣味與習慣穩定。亂換＝每天重新學。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d2_potty_myths")
        $ knowledge_score += 1
        $ set_flag("knows_potty_routine", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "哦。所以是我要常帶你去那個點。\n不是你要一次學會。"
    else:
        xq "好亂。總之先清掉，別再兇一次。"
    return


## —— Day2：隱藏知識｜狗不能吃的（5 選 4；請假在家觸發）——
label kg_d2_toxic_foods:
    $ toxic_food_picks = []
    $ knowledge_hud_title = "隱藏知識｜不能吃"
    narrator "茶几上還有便當殘渣。她突然頓住——\n這些……能給[dog_label]吃嗎？"
    xq "搜一下好了。狗不能吃什麼……"
    call screen kg_toxic_food_pick

    if toxic_food_answer_correct():
        $ knowledge_correct_today = 4
        $ clear_minigame("kg_d2_toxic_foods")
        $ knowledge_score += 1
        $ set_flag("knows_toxic_foods", True)
        $ add_trust(1)
        $ show_trust_toast(1)
        narrator "巧克力、葡萄、洋蔥大蒜、木糖醇口香糖——都不能給。\n煮熟的紅蘿蔔可以，但她還是決定先別亂餵。"
        xq "好。茶几上的通通收回去。\n你不是垃圾桶。"
    else:
        $ knowledge_correct_today = 0
        narrator "答案是：巧克力、葡萄／葡萄乾、生洋蔥／大蒜、含木糖醇的口香糖——都不能給。\n煮熟的紅蘿蔔其實可以；其他四樣，碰不得。"
        xq "……差點搞錯。還好有查。"
        $ set_flag("knows_toxic_foods", True)
    return


## —— Day2：信任｜溫柔聲 ——
label tg_d2_soft_voice:
    $ _tg_retries = 1
    $ _soft_anxiety = 0.75
    jump tg_d2_soft_voice_try

label tg_d2_soft_voice_try:
    show screen tg_soft_voice_bar(_soft_anxiety)
    show dog anxious at dog_bottom
    narrator "蹲到[dog_label]視線高度。選一個不會把[dog_label]嚇回去的聲音。"
    menu:
        "低聲、慢慢蹲下：「嘿，我在這。」":
            $ _soft_anxiety = 0.25
            show screen tg_soft_voice_bar(_soft_anxiety)
            jump tg_d2_soft_voice_success
        "普通音量、半蹲：「沒事啦。」":
            $ _soft_anxiety = 0.4
            show screen tg_soft_voice_bar(_soft_anxiety)
            jump tg_d2_soft_voice_success
        "提高音量、站著靠近：「你乖一點！」":
            jump tg_d2_soft_voice_fail

label tg_d2_soft_voice_success:
    hide screen tg_soft_voice_bar
    show dog shy at dog_bottom
    $ dog_sfx("soft")
    narrator "她蹲下來。膝蓋喀一聲，自己先皺眉。"
    xq "嘿。我在這。沒要打你。"
    $ dog_sfx("sigh")
    narrator "[dog_label]耳朵慢慢從貼平變成半豎。\n尾巴尖動了一下，又停住。嗚嗚像被調小音量。"
    $ add_trust(2)
    $ show_trust_toast(2)
    $ clear_minigame("tg_d2_soft_voice")
    $ set_flag("soft_voice_ok", True)
    return

label tg_d2_soft_voice_fail:
    hide screen tg_soft_voice_bar
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "聲音一尖，或人影一壓過來，\n[dog_label]退到箱角，焦慮條回彈。"
    xq "……對不起。我再蹲一次。"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        $ _soft_anxiety = 0.85
        show dog anxious at dog_bottom
        jump tg_d2_soft_voice_try
    narrator "[dog_label]仍警戒。先往下走，別再逼近。"
    return


## —— Day3：知識｜飼料貨架 5 題（寵物店販售商品）——
label kg_d3_food_shelf:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "飼料貨架卡"
    show screen knowledge_hud
    narrator "成犬、幼犬、室內、美毛——每一袋都像在保證奇蹟。\n她只想買對的那一種。"

    narrator "兩個月幼犬，飼料貨架上優先選？"
    menu:
        "成犬飼料大包（比較省）":
            narrator "月齡不同，熱量與營養比例不同。先選幼犬配方。"
        "幼犬配方飼料":
            $ knowledge_correct_today += 1
            narrator "月齡不同，熱量與營養比例不同。先選幼犬配方。"
        "「通用全齡」最大包就好":
            narrator "月齡不同，熱量與營養比例不同。先選幼犬配方。"

    narrator "一次買超大袋成犬糧「以後也用得到」？"
    menu:
        "很聰明，單位比較便宜":
            narrator "不建議；月齡需求不同，易過期／吃錯。先少樣試胃口。"
        "不建議；月齡需求不同，易過期／吃錯":
            $ knowledge_correct_today += 1
            narrator "不建議；月齡需求不同，易過期／吃錯。先少樣試胃口。"

    narrator "玩具架上很多款。兩個月幼犬的玩具怎麼挑？"
    menu:
        "選太大、太硬、容易咬碎掉屑的":
            narrator "選尺寸適中、耐咬不易碎的咬咬玩具；太小易誤食，太硬傷牙床。"
        "選尺寸適中、耐咬、不容易碎成小塊的":
            $ knowledge_correct_today += 1
            narrator "選尺寸適中、耐咬不易碎的咬咬玩具；太小易誤食，太硬傷牙床。"
        "買人用的毛線球、橡皮筋就好":
            narrator "選尺寸適中、耐咬不易碎的咬咬玩具；太小易誤食，太硬傷牙床。"

    narrator "尿墊區：新手比較穩的買法是？"
    menu:
        "挑最香的芳香款，把味道蓋過去就好":
            narrator "先看吸水力與尺寸；香味蓋不住尿味，還可能刺激鼻子。"
        "吸水力夠、尺寸夠大，先別被香味牽著走":
            $ knowledge_correct_today += 1
            narrator "先看吸水力與尺寸；香味蓋不住尿味，還可能刺激鼻子。"
        "最小片最省錢，怎麼漏都沒差":
            narrator "先看吸水力與尺寸；香味蓋不住尿味，還可能刺激鼻子。"

    narrator "牽繩架上很多款。兩個月大，今天買牽繩的意思是？"
    menu:
        "買了就能立刻練到脫力的長距離散步":
            narrator "牽繩可以先買著；先短、慢、觀察，疫苗與月齡都要考慮。"
        "可以先買；先短、慢、觀察，疫苗與月齡要考慮":
            $ knowledge_correct_today += 1
            narrator "牽繩可以先買著；先短、慢、觀察，疫苗與月齡都要考慮。"
        "幼犬不用牽繩，買了也沒用":
            narrator "牽繩可以先買著；先短、慢、觀察，疫苗與月齡都要考慮。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d3_food_shelf")
        $ knowledge_score += 1
        $ set_flag("knows_puppy_kibble", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "好。幼犬糧、少樣試、咬咬玩具、尿墊看吸水、牽繩先短走。"
    else:
        narrator "店員好心提醒：「幼犬看配方月齡，玩具看尺寸，尿墊別只看香味。」小晴連點了好幾下頭。"
        xq "……好。我再看一次標籤。"
    return


## —— Day3：信任｜新舊碗並排 ——
label tg_d3_two_bowls:
    $ _tg_retries = 1
    jump tg_d3_two_bowls_try

label tg_d3_two_bowls_try:
    show dog hungry at dog_bottom
    narrator "新碗與舊盤並排放下。觀察[dog_label]走向——\n不可拖頭進碗、不可拍碗催促。"
    menu:
        "並排放好，後退等待":
            $ dog_sfx("soft")
            jump tg_d3_two_bowls_success
        "忍不住把[dog_label]的頭推向新碗":
            jump tg_d3_two_bowls_fail
        "拍碗催促「快吃啦」":
            jump tg_d3_two_bowls_fail

label tg_d3_two_bowls_success:
    show dog shy at dog_bottom
    $ dog_sfx("yip")
    narrator "[dog_label]先聞舊盤，再繞到新碗邊。鼻子貼邊緣，後退半步，再靠近。\n終於低頭啃了兩口幼犬糧——咀嚼聲小小的，像在試這屋子還能不能信。\n\n尾巴尖極輕顫一下。"
    $ add_trust(1)
    $ show_trust_toast(1)
    $ clear_minigame("tg_d3_two_bowls")
    $ set_flag("fed", True)
    $ set_flag("chose_bowl_freely", True)
    $ set_flag("bowls_side_by_side", True)
    return

label tg_d3_two_bowls_fail:
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "手一壓，[dog_label]猛退，嗚嗚變尖，新碗被撞歪，糧撒一地。"
    xq "抱歉！我急什麼……"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        narrator "再試一次。這次，把手放好，讓[dog_label]自己選。"
        show dog hungry at dog_bottom
        jump tg_d3_two_bowls_try
    narrator "[dog_label]稍後才肯靠近。先別催。"
    return


## —— Day4：知識｜分離焦慮 5 題 ——
label kg_d4_separation:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "分離焦慮卡"
    show screen knowledge_hud
    narrator "凌晨兩點，螢幕亮度調到最低。文章互相打架。\n有人說不理，有人說要陪。她只想找一個明天還能醒來的做法。"

    narrator "幼犬關門後大哭，最好的長期做法是？"
    menu:
        "完全不理到牠哭累":
            narrator "長期靠哭累或整晚悶抱，都難永續。漸進＋可預期比較穩。"
        "漸進練習＋可見／可預期的離開回來":
            $ knowledge_correct_today += 1
            narrator "長期靠哭累或整晚悶抱，都難永續。漸進＋可預期比較穩。"
        "每次一哭就緊抱整晚當唯一方法":
            narrator "長期靠哭累或整晚悶抱，都難永續。漸進＋可預期比較穩。"

    narrator "「開電視當陪伴」可以完全取代人在場嗎？"
    menu:
        "可以，電視＝家人":
            narrator "聲音有時有用，但不是萬能鑰匙。有些狗需要看得見你。"
        "不能完全取代；有些狗需要看得見你":
            $ knowledge_correct_today += 1
            narrator "聲音有時有用，但不是萬能鑰匙。有些狗需要看得見你。"

    narrator "分離焦慮時，突然消失（不說一聲就出門）通常？"
    menu:
        "比較不會依賴":
            narrator "短短一句「我去一下」比人間蒸發溫和。突然消失可能更焦慮。"
        "可能更焦慮；簡短固定儀式較好":
            $ knowledge_correct_today += 1
            narrator "短短一句「我去一下」比人間蒸發溫和。突然消失可能更焦慮。"

    narrator "半夜安撫，一直把牠悶在懷裡不放？"
    menu:
        "最好，永遠抱著":
            narrator "緊抱當唯一解，人會垮，狗也可能更黏分離。同室可見、語氣穩較可持續。"
        "同室可見、語氣穩，比強制緊抱更可持續":
            $ knowledge_correct_today += 1
            narrator "緊抱當唯一解，人會垮，狗也可能更黏分離。同室可見、語氣穩較可持續。"

    narrator "回來時大驚小怪「媽媽好想你」大叫？"
    menu:
        "一定要很誇張才有愛":
            narrator "進出越平靜，離開越不像世界末日。"
        "平靜進出，較不易把離開／回來變成高潮焦慮":
            $ knowledge_correct_today += 1
            narrator "進出越平靜，離開越不像世界末日。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d4_separation")
        $ knowledge_score += 1
        $ set_flag("knows_separation", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "可見……可預期。聽起來比較不像地獄。"
    else:
        xq "可見……可預期……半信半疑，但先記著。"
    return


## —— Day4：信任｜可見陪睡 ——
label tg_d4_visible_sleep:
    $ _tg_retries = 1
    jump tg_d4_visible_sleep_try

label tg_d4_visible_sleep_try:
    show dog anxious at dog_bottom
    narrator "把枕頭／毯子放到客廳「可見圈」。維持在圈內，直到[dog_label]入睡。\n走出可見圈或突然撲抱 → 失敗。"
    menu:
        "枕頭丟地板，坐在紙箱看得見處等待":
            $ dog_sfx("soft")
            jump tg_d4_visible_sleep_success
        "忍不住一把抱起安撫":
            jump tg_d4_visible_sleep_fail
        "起身回房「一下就好」":
            jump tg_d4_visible_sleep_fail

label tg_d4_visible_sleep_success:
    show dog sleepy at dog_bottom
    $ dog_sfx("sigh")
    narrator "枕頭丟在地板上。小晴蜷著，能看見紙箱口。\n[dog_label]嗚嗚越來越稀，鼻子埋進毛巾，呼吸終於拉長。\n\n尾巴尖動了一下，停住。睡著了。"
    xq "……終於。"
    $ add_trust(2)
    $ show_trust_toast(2)
    $ clear_minigame("tg_d4_visible_sleep")
    $ set_flag("visible_sleep_ok", True)
    return

label tg_d4_visible_sleep_fail:
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "她一離開可見範圍，或一把抱起，[dog_label]又尖起來，四腳亂蹬。"
    xq "好啦好啦我回去坐……"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        narrator "再試一次。這次，坐住。"
        show dog anxious at dog_bottom
        jump tg_d4_visible_sleep_try
    narrator "[dog_label]稍後才安靜。先別逼。"
    return


## —— Day5：知識｜身體語言 5 題 ——
label kg_d5_body_language:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "身體語言卡"
    show screen knowledge_hud
    narrator "圖上的狗耳朵、尾巴、眼神——她把螢幕轉給自己看，像在猜一題不能錯的考題。"

    narrator "耳朵緊貼、身體縮成一團，多半是？"
    menu:
        "想玩到翻":
            narrator "縮團不是撒嬌保證。先給空間。"
        "不安／想躲":
            $ knowledge_correct_today += 1
            narrator "縮團不是撒嬌保證。先給空間。"

    narrator "尾巴緊貼身體、不太敢動？"
    menu:
        "開心到不行":
            narrator "要看整隻狗，不只看尾巴。常是警戒或害怕。"
        "警戒或害怕（視整體）":
            $ knowledge_correct_today += 1
            narrator "要看整隻狗，不只看尾巴。常是警戒或害怕。"

    narrator "軟眼、眨眼、慢慢靠近？"
    menu:
        "想玩、在撒嬌":
            narrator "慢，才是邀請。較放鬆時可嘗試慢接觸——但別一次解讀成「一定要玩」。"
        "較放鬆、可嘗試慢接觸":
            $ knowledge_correct_today += 1
            narrator "慢，才是邀請。較放鬆時可嘗試慢接觸。"

    narrator "接觸前先做？"
    menu:
        "從上方突然摸頭":
            narrator "手是氣味，也是訊息。先讓牠聞手，等牠靠過來。"
        "讓牠先聞手，等牠靠過來":
            $ knowledge_correct_today += 1
            narrator "手是氣味，也是訊息。先讓牠聞手，等牠靠過來。"

    narrator "牠轉頭避開、舔唇、想走？"
    menu:
        "再追著摸表示親密":
            narrator "回避信號＝暫停鍵。不是「再努力一點」。停手給空間。"
        "停手給空間":
            $ knowledge_correct_today += 1
            narrator "回避信號＝暫停鍵。不是「再努力一點」。停手給空間。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d5_body_language")
        $ knowledge_score += 1
        $ set_flag("knows_body_language", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "先聞手。好。我記得。可以伸手——慢。"
    else:
        xq "先聞手。好。我記得。"
    return


## —— Day5：信任｜聞手再摸背 ——
label tg_d5_sniff_then_pet:
    $ _tg_retries = 1
    jump tg_d5_sniff_then_pet_try

label tg_d5_sniff_then_pet_try:
    show dog shy at dog_bottom
    narrator "伸出手（掌心向下／側）→ 等待聞完 → 再輕摸背。\n在「聞」完成前就摸 → 失敗。"
    menu:
        "伸手等待，等[dog_label]聞完再摸背":
            $ dog_sfx("soft")
            jump tg_d5_sniff_then_pet_success
        "等不及，直接摸頂毛":
            jump tg_d5_sniff_then_pet_fail

label tg_d5_sniff_then_pet_success:
    show dog shy at dog_bottom
    $ dog_sfx("yip")
    narrator "鼻頭涼涼地碰指節。一下、兩下。[dog_label]自己把肩靠進掌心範圍。\n她只摸背——短、輕、停。\n\n尾巴尖又顫了一下。嗚嗚幾乎聽不見。"
    xq "這樣可以嗎。"
    narrator "不是問句。是怕問句太重。"
    $ add_trust(2)
    $ show_trust_toast(2)
    $ clear_minigame("tg_d5_sniff_then_pet")
    $ set_flag("sniff_then_pet_ok", True)
    return

label tg_d5_sniff_then_pet_fail:
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "手指才碰到頂毛，[dog_label]閃頭，短促嗚嗚，退半步。"
    xq "太快了。我知道。"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        narrator "再試一次。這次，等聞完。"
        show dog shy at dog_bottom
        jump tg_d5_sniff_then_pet_try
    narrator "先停手。距離還在，機會也還在。"
    return


## —— Day6：知識｜為什麼咬 5 題 ——
label kg_d6_why_chew:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "為什麼咬卡"
    show screen knowledge_hud
    narrator "標題有的寫「領導力」，有的寫「出牙」。她只想確認：這不是恨。"

    narrator "幼犬咬東西，主要原因常包括？"
    menu:
        "出牙不適、探索、無聊、焦慮等":
            $ knowledge_correct_today += 1
            narrator "咬＝需求與探索，不是辦公室復仇劇。"
        "單純「故意報復主人上班」":
            narrator "咬＝需求與探索，不是辦公室復仇劇。"

    narrator "「咬壞東西＝恨你」這句？"
    menu:
        "正確":
            narrator "多半是迷思；情緒歸因為報復常不準。把報復安在狗身上，人會更用力懲罰。"
        "多半是迷思；情緒歸因為報復常不準":
            $ knowledge_correct_today += 1
            narrator "多半是迷思；情緒歸因為報復常不準。把報復安在狗身上，人會更用力懲罰。"

    narrator "發現咬充電線，第一步？"
    menu:
        "先大罵三分鐘":
            narrator "活著比道理優先。先確保安全（拔電／拿走危險物）。"
        "先確保安全（拔電／拿走危險物）":
            $ knowledge_correct_today += 1
            narrator "活著比道理優先。先確保安全（拔電／拿走危險物）。"

    narrator "比較好的做法是？"
    menu:
        "只有懲罰、不給替代":
            narrator "空嘴巴會找下一個目標。收好危險物＋提供合適咬咬玩具。"
        "收好危險物＋提供合適咬咬玩具":
            $ knowledge_correct_today += 1
            narrator "空嘴巴會找下一個目標。收好危險物＋提供合適咬咬玩具。"

    narrator "用食物／玩具「交換」拿走危險物，比硬搶？"
    menu:
        "通常較不破壞信任":
            $ knowledge_correct_today += 1
            narrator "交換＝還有商量。硬搶＝戰爭。"
        "硬搶才顯示領導力":
            narrator "交換＝還有商量。硬搶＝戰爭。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d6_why_chew")
        $ knowledge_score += 1
        $ set_flag("knows_why_chew", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "先安全。再給可以咬的。"
    else:
        xq "先安全。再給可以咬的。大概。"
    return


## —— Day6：信任｜玩具交換 ——
label tg_d6_trade_toy:
    $ _tg_retries = 1
    jump tg_d6_trade_toy_try

label tg_d6_trade_toy_try:
    show dog shy at dog_bottom
    narrator "出示咬咬玩具 → 等[dog_label]鬆口／興趣轉移 → 再收走危險殘片。\n不可硬搶。"
    menu:
        "晃玩具交換，等牠咬玩具再抽走碎膠皮":
            $ dog_sfx("soft")
            jump tg_d6_trade_toy_success
        "直接從嘴邊搶走危險物":
            jump tg_d6_trade_toy_fail

label tg_d6_trade_toy_success:
    show dog shy at dog_bottom
    $ dog_sfx("yip")
    narrator "橡膠玩具在眼前晃。[dog_label]鼻子湊過去，咬住玩具的瞬間，她把碎膠皮抽走。\n\n沒有拉鋸。只有一次乾淨的交換。\n尾巴尖動了一下——很短，像鬆氣。"
    xq "咬這個。這個可以。"
    $ add_trust(2)
    $ show_trust_toast(2)
    $ clear_minigame("tg_d6_trade_toy")
    $ set_flag("traded_toy_ok", True)
    return

label tg_d6_trade_toy_fail:
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "手一扯，[dog_label]咬得更緊，嗚嗚變怒，關係像橡皮筋拉到極限。"
    xq "好、好，我不搶——我換。"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        narrator "再試一次。用交換，不要搶。"
        show dog shy at dog_bottom
        jump tg_d6_trade_toy_try
    narrator "稍後再換。先別硬來。"
    return


## —— Day7：知識｜照顧清單 5 題 ——
label kg_d7_care_checklist:
    $ knowledge_correct_today = 0
    $ knowledge_hud_title = "照顧清單卡"
    show screen knowledge_hud
    narrator "這不是考試。但她希望自己答得出來——至少別再靠猜。"

    narrator "正式養下來，疫苗／驅蟲時程應該？"
    menu:
        "有空再講":
            narrator "月齡與針劑有表。依獸醫建議排程，不要靠猜。"
        "依獸醫建議排程，不要靠猜":
            $ knowledge_correct_today += 1
            narrator "月齡與針劑有表。依獸醫建議排程，不要靠猜。"

    narrator "幼犬每日照顧，最基本包含？"
    menu:
        "適齡餵食、清水、清潔排泄、安全環境":
            $ knowledge_correct_today += 1
            narrator "愛要變成：餵、清、收、陪。不然只是嘴上講。"
        "只靠「有愛就夠」不需花費時間":
            narrator "愛要變成：餵、清、收、陪。不然只是嘴上講。"

    narrator "幼犬突然不吃不喝、精神很差，比較該怎麼做？"
    menu:
        "再觀察三天，可能只是挑食":
            narrator "盡快聯絡獸醫或急診；幼犬惡化很快，別硬撐。"
        "盡快聯絡獸醫／急診，別硬撐":
            $ knowledge_correct_today += 1
            narrator "盡快聯絡獸醫或急診；幼犬惡化很快，別硬撐。"
        "先餵人吃的雞湯跟牛奶再說":
            narrator "盡快聯絡獸醫或急診；幼犬惡化很快，別硬撐。"

    narrator "「收養」比較像？"
    menu:
        "只要拍一張貼文就結束":
            narrator "貼文是一秒。日常是很多個早上。收養＝決定一起過日常與責任。"
        "決定一起過日常與責任":
            $ knowledge_correct_today += 1
            narrator "貼文是一秒。日常是很多個早上。收養＝決定一起過日常與責任。"

    narrator "不確定時最好？"
    menu:
        "看網路上最極端的說法照做":
            narrator "新手允許慢。不許瞎。問可靠來源／獸醫，再慢慢調整。"
        "問可靠來源／獸醫，再慢慢調整":
            $ knowledge_correct_today += 1
            narrator "新手允許慢。不許瞎。問可靠來源／獸醫，再慢慢調整。"

    hide screen knowledge_hud

    if knowledge_correct_today >= 4:
        $ clear_minigame("kg_d7_care_checklist")
        $ knowledge_score += 1
        $ set_flag("knows_care_checklist", True)
        if knowledge_correct_today >= 5:
            $ add_trust(1)
            $ show_trust_toast(1)
        xq "餵、水、清、安全。其他的——我問醫生。"
    else:
        narrator "仍可進診所；獸醫會補課。"
        xq "餵、水、清、安全……我再問醫生。"
    return


## —— Day7：信任｜候診安撫 ——
label tg_d7_clinic_calm:
    $ _tg_retries = 1
    jump tg_d7_clinic_calm_try

label tg_d7_clinic_calm_try:
    show dog anxious at dog_bottom
    narrator "走廊很吵。消毒水味很重。你現在怎麼陪？"
    menu:
        "低聲、掌心停在能聞的距離，不強迫摸頭":
            $ dog_sfx("soft")
            jump tg_d7_clinic_calm_success
        "提高音量安撫「沒事啦！」並硬摸頭":
            jump tg_d7_clinic_calm_fail
        "一把抱緊不讓動":
            jump tg_d7_clinic_calm_fail

label tg_d7_clinic_calm_success:
    show dog shy at dog_bottom
    $ dog_sfx("sigh")
    narrator "診所消毒水味很重。別的狗叫了一聲，[dog_label]全身一顫。\n小晴沒撲上去抱死，只把掌心停在牠能聞的距離，聲音壓平。\n\n焦慮慢慢降。尾巴尖動了一下。"
    $ add_trust(2)
    $ show_trust_toast(2)
    $ clear_minigame("tg_d7_clinic_calm")
    $ set_flag("clinic_calm_ok", True)
    return

label tg_d7_clinic_calm_fail:
    show dog scare at dog_bottom
    $ dog_sfx("whimper")
    narrator "摸頭太急，或聲調一尖，焦慮爆開。[dog_label]掙扎，嗚嗚回盪在走廊。"
    xq "對不起——我重新來。"
    $ add_trust(-1)
    $ show_trust_toast(-1)
    if _tg_retries > 0:
        $ _tg_retries -= 1
        narrator "再試一次。低聲、可見、不強迫。"
        show dog anxious at dog_bottom
        jump tg_d7_clinic_calm_try
    narrator "候診仍緊張。先撐過這一關。"
    return
