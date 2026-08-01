## Week0 Day3｜第一次出門買東西
## 來源：week0/day3_first_shop_run.md ｜ agents/plot.md ｜ agents/audio.md

label d3_empty_can:
    $ story_day = 3
    $ smell_text = "空罐頭、舊淺盤、幼犬體溫"
    $ play_bgm("warm")
    scene bg living_day
    with Dissolve(0.5)
    show dog hungry at dog_bottom
    with Dissolve(0.3)
    $ dog_sfx("murmur")

    narrator "勺子刮過罐底，金屬聲乾乾的。\n[dog_label]盯著空盤，鼻子伸出來又縮回去。"
    xq "……沒了。"
    xq "[dog_label]，我們得出門一趟。"
    $ dog_sfx("soft")
    narrator "牠聽到名字，耳朵豎一下，又立刻貼平——\n門、鞋子、鑰匙，都還是危險組合。"
    narrator "小晴把紙箱挪到角落，水碗裝滿，窗簾拉到半開。"
    xq "我很快。你……先別拆家。"
    jump d3_to_shop


label d3_to_shop:
    ## 日間巷口路程：客廳 → 寵物店（對齊 Day7 treestreet 有路程、Day3 不該直接切店內）
    $ smell_text = "陽光、機車排氣、乾柏油"
    $ play_bgm("warm")
    scene bg street_day
    with Dissolve(0.45)
    hide dog
    hide char

    narrator "門一關，走廊的回音比想像中安靜。\n外面是白天——乾的路、亮的招牌影子、偶爾一台機車擦過。"
    narrator "她把提袋挽緊一點。手機地圖沒開；巷口那間寵物店，她路過很多次，從沒進去過。"
    xq "就買飼料。別亂買。"
    narrator "說完自己也不信。腳還是往那扇玻璃門走。"
    jump d3_petshop_enter


label d3_petshop_enter:
    $ smell_text = "飼料袋、塑膠包裝、消毒水"
    $ play_bgm("shop_bustle")
    scene bg petshop_day
    with Dissolve(0.45)
    hide dog

    narrator "門一開，飼料袋氣味、塑膠包裝、消毒水混在一起。\n貨架高到天花板，標籤字小到像考試。"
    show char shop_aunt at char_center
    with Dissolve(0.3)
    narrator "寵物店阿姨笑著迎上來，聲音太亮。小晴下意識把肩帶往上撈。"
    shop_aunt "第一次養嗎？幼犬區在那邊——需要我介紹嗎？"
    xq "呃、對。牠大概……兩個月？我也不確定。"
    narrator "她掏出手機，螢幕還停在昨天的搜尋紀錄。"
    hide char
    jump d3_kg_food_shelf_scene


label d3_kg_food_shelf_scene:
    $ smell_text = "飼料袋、標籤墨水"
    scene bg petshop_day
    show char shop_aunt at char_center
    with Dissolve(0.2)
    narrator "成犬、幼犬、室內、美毛——每一袋都像在保證奇蹟。\n她只想買對的那一種。阿姨偶爾在旁邊插話，聲音還是太亮。"
    hide char
    call kg_d3_food_shelf from _call_kg_d3
    jump d3_choice_kibble


label d3_choice_kibble:
    $ smell_text = "飼料袋、購物籃塑膠"
    scene bg petshop_day
    show char shop_aunt at char_center

    narrator "貨架好高。你拿哪一袋？"
    menu:
        "拿比較便宜的成犬大包":
            narrator "袋面狗很帥，公斤數很驚人。小晴看了看價錢，心裡鬆一口氣。"
            shop_aunt "這款是成犬喔——幼犬要看那邊小一點的。"
            xq "啊。對喔。"
            narrator "她把大包放回，改拿旁邊幼犬小包。\n差點省錯錢——手心還有點涼。"
            $ set_flag("almost_bought_adult_kibble", True)
            $ set_flag("bought_puppy_kibble", True)
            $ set_flag("bought_adult_kibble", False)
            jump d3_choice_toys
        "問店員月齡，買幼犬糧少樣":
            narrator "阿姨蹲下來指標籤。小晴把「約兩個月」說得結結巴巴，還是說完了。\n\n籃子裡多了一小袋幼犬糧、一包尿墊補充包。"
            xq "先這樣。吃得下去再說。"
            $ set_flag("bought_puppy_kibble", True)
            $ set_flag("bought_adult_kibble", False)
            jump d3_choice_toys


label d3_choice_toys:
    $ smell_text = "玩具橡膠、零食袋"
    scene bg petshop_day
    show char shop_aunt at char_center

    narrator "阿姨又遞來一排玩具與噴霧。荷包要怎麼辦？（信任不變）"
    menu:
        "幾乎全買":
            narrator "玩具、零食、清潔噴霧——籃子沉下去。\n阿姨笑得更亮，像過年。"
            xq "……當是提前過年。"
            $ set_flag("shop_splurge", True)
            jump d3_checkout
        "只買咬咬玩具＋尿墊":
            narrator "阿姨有點失望，但仍幫她找了一支軟的橡膠玩具。"
            xq "其他的……我先活過這個禮拜再說。"
            $ set_flag("shop_minimal", True)
            jump d3_checkout


label d3_checkout:
    ## 結帳：結帳妹妹登場（兩條購物分歧匯合）
    $ smell_text = "收據紙、塑膠袋、消毒水"
    scene bg petshop_day
    hide char
    show char shop_cashier at char_center
    with Dissolve(0.3)

    if get_flag("shop_splurge"):
        narrator "結帳數字跳上去。小晴臉也跟著熱。\n提袋勒進手指，像加班後的肩帶。"
        shop_cashier "第一次養會這樣啦——需要袋子嗎？"
        xq "……要。謝謝。"
    else:
        narrator "櫃檯的妹妹掃過那支咬咬玩具與尿墊，動作很快。"
        shop_cashier "這樣就好喔？幼犬糧要再加一點嗎？"
        xq "先這樣。吃得下去再說。"
        shop_cashier "好——那加油。"

    narrator "塑膠袋換手。外面巷口的陽光從門縫擠進來一點——\n她記得狗還在家，門還沒開。"
    hide char
    jump d3_return_home


label d3_return_home:
    $ smell_text = "新飼料、塑膠、外出的味道"
    $ play_bgm("warm")
    scene bg living_day
    with Dissolve(0.45)
    show dog anxious at dog_bottom
    $ dog_sfx("murmur_b")

    narrator "門一開，[dog_label]從紙箱口探頭。鼻子抽得很快——\n新塑膠、新飼料、外出的味道。"
    $ dog_sfx("whimper")
    narrator "嗚嗚短促，尾巴緊貼。不是歡迎儀式，\n是盤點陌生人有沒有把外面帶進來。"
    xq "我回來了。買了……一堆我自己也看不懂的東西。"
    narrator "她洗手、拆袋、把舊淺盤洗乾淨。新碗還貼著標價貼紙。"
    jump d3_tg_two_bowls_scene


label d3_tg_two_bowls_scene:
    $ smell_text = "幼犬糧、清水、舊淺盤"
    $ play_bgm("tender")
    scene bg living_day
    show dog hungry at dog_bottom
    call tg_d3_two_bowls from _call_tg_d3
    jump d3_choice_bowl


label d3_choice_bowl:
    $ smell_text = "幼犬糧、新碗塑膠味"
    scene bg living_day

    ## 信任小遊戲成功：已演過並排，勿重考同一拍
    if get_flag("chose_bowl_freely"):
        show dog shy at dog_bottom
        $ dog_sfx("soft")
        narrator "舊盤還在，新碗也在。[dog_label]吃兩口抬頭看人，\n漸漸連那一下也省了。"
        xq "慢點。沒人跟你搶。"
        $ dog_sfx("yip")
        $ set_flag("bowls_side_by_side", True)
        $ set_flag("fed", True)
        jump d3_day_end

    show dog hungry at dog_bottom
    narrator "新碗牠不太碰。你要怎麼辦？"
    menu:
        "收走舊盤，只留新碗":
            show dog scare at dog_bottom
            $ dog_sfx("whimper_b")
            narrator "熟悉的氣味沒了。[dog_label]在新碗前站著，聞了又聞，就是不吃。\n嗚嗚一聲，退回紙箱。"
            xq "可是這個比較正式啊……"
            narrator "她後來還是把舊盤洗出來並排——今晚進食延後了一截。"
            $ add_trust(-1)
            $ show_trust_toast(-1)
            $ set_flag("removed_old_bowl", True)
            jump d3_day_end
        "把舊盤拿回來並排，再等一次":
            show dog shy at dog_bottom
            $ dog_sfx("soft")
            narrator "兩碗並排。[dog_label]先聞舊盤，再繞到新碗邊，\n終於低頭啃了兩口。"
            xq "慢點。沒人跟你搶。"
            $ dog_sfx("yip")
            $ add_trust(1)
            $ show_trust_toast(1)
            $ set_flag("bowls_side_by_side", True)
            $ set_flag("fed", True)
            jump d3_day_end


label d3_day_end:
    $ smell_text = "尿墊、咬咬玩具、清水"
    $ play_bgm("warm_quiet")
    scene bg living_night
    with Dissolve(0.5)
    show dog sleepy at dog_bottom
    $ dog_sfx("sigh")

    narrator "尿墊補了新的一角。咬咬玩具躺在沙發腳邊，還沒被碰。\n[dog_label]肚子微鼓，紙箱邊多了一個真正的水碗——乾淨的。"
    xq "今天花好多錢。"
    xq "可是你有東西吃了。這算……投資？"
    narrator "她自己笑了一下，笑完又覺得有點丟臉。"

    $ add_landmark("landmark_first_shop")
    $ save_name = "第3天結束｜" + dog_label + "｜信任 " + str(trust)
    narrator "—— 第 3 天結束 ——\n[dog_label]　信任：[trust]　知識分：[knowledge_score]\n\n今晚若關上門，也許會聽見另一種哭聲。"
    jump d4_bedtime
