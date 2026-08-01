## 圖像定義（相對 game/assets）
## 背景命名：bg-{place}-{light} — 見 agents/image_bg.md
## 背景：cover 滿版（裁切邊緣、不留黑邊）
## 插圖：同時間只顯示 dog 或 char 其一（見 day1 hide／show）

image bg street_night = Transform("bg/bg-street-night.png", fit="cover", xysize=(1280, 720))
image bg street_day = Transform("bg/bg-street-day.png", fit="cover", xysize=(1280, 720))
image bg treestreet_day = Transform("bg/bg-treestreet-day.png", fit="cover", xysize=(1280, 720))
image bg living_day = Transform("bg/bg-living-day.png", fit="cover", xysize=(1280, 720))
image bg living_night = Transform("bg/bg-living-night.png", fit="cover", xysize=(1280, 720))
image bg entrance_night = Transform("bg/bg-entrance-night.png", fit="cover", xysize=(1280, 720))
image bg petshop_day = Transform("bg/bg-petshop-day.png", fit="cover", xysize=(1280, 720))
image bg clinic_day = Transform("bg/bg-clinic-day.png", fit="cover", xysize=(1280, 720))

image dog box = "dog/dog-box.png"
image dog anxious = "dog/dog-anxious.png"
image dog wet = "dog/dog-wet.png"
image dog hungry = "dog/dog-hungry.png"
image dog shy = "dog/dog-shy.png"
image dog scare = "dog/dog-scare.png"
image dog sleepy = "dog/dog-sleepy.png"

image char hand_reach = "char/char-hand-reach.png"
image char carry_box = "char/char-carry-box.png"
image char sit_floor = "char/char-sit-floor.png"
image char shop_aunt = "char/char-shop-aunt.png"
image char shop_cashier = "char/char-shop-cashier.png"

## 單插圖置中偏下（一次只 show 一個 tag）
transform dog_bottom:
    xalign 0.5
    yanchor 1.0
    ypos 0.92
    zoom 0.38

transform char_center:
    xalign 0.5
    yanchor 1.0
    ypos 0.94
    zoom 0.42

define narrator = Character(None, what_font="SourceHanSansLite.ttf", what_color="#F0E9DF", what_size=22, what_outlines=[(1, "#00000055", 0, 1)])
define xq = Character("小晴", what_font="SourceHanSansLite.ttf", who_font="SourceHanSansLite.ttf", what_color="#F0E9DF", who_color="#D4B57A", what_size=22, who_size=20, what_outlines=[(1, "#00000055", 0, 1)])
## Day1 未取名：dog_label =「小狗狗」；寵物店取名後改為玩家輸入名
define pudding = Character("[dog_label]", what_font="SourceHanSansLite.ttf", who_font="SourceHanSansLite.ttf", what_color="#E8DCC8", who_color="#C4A090", what_size=20, who_size=18, what_outlines=[(1, "#00000044", 0, 1)])
## 寵物店 NPC（立繪：char shop_aunt／shop_cashier）
define shop_aunt = Character("寵物店阿姨", what_font="SourceHanSansLite.ttf", who_font="SourceHanSansLite.ttf", what_color="#F0E9DF", who_color="#C9A86A", what_size=22, who_size=20, what_outlines=[(1, "#00000055", 0, 1)])
define shop_cashier = Character("結帳妹妹", what_font="SourceHanSansLite.ttf", who_font="SourceHanSansLite.ttf", what_color="#F0E9DF", who_color="#A8B88A", what_size=22, who_size=20, what_outlines=[(1, "#00000055", 0, 1)])
