## 立繪尺（唯一數字來源）
## 對照：Ch1_Trust_Version3/agents/image_scale.md
## 改大小：只改本檔 SCALE_S02／SCALE，不要在 script.rpy 寫死 zoom。
## 同場遠近只改 xalign；狗一律 zoom 1.0 + xzoom／yzoom（勿混用 zoom）。
## 例外：有透視的場（S08 巷口 S08_ALLEY；S09 起 PERSP＋PV_PT）＝腳底 y 決定 zoom，見檔尾。
## 誰說了算：場景 zoom＝本檔；pose 尺＝script.rpy CHAR_POSE_SCALE／DOG_POSE_SCALE（別名列 #xxx）；
##   腳底裁切＝本檔 SPRITE_FOOT。image 定義不要寫數字字面值（lint 會列出蓋掉表的字面值）。

init -1 python:
    # dog=None → 該場無獨立狗層（抱走合成圖跟人同尺，不另疊）
    SCALE_S02 = {
        "office":      {"char": 0.28,  "dog": None,  "fit": "椅背／桌面到腰；S02 開場站右側走道"},
        "convenience": {"char": 0.29,  "dog": None,  "fit": "櫃面／高腳椅到腰"},
        "street":      {"char": 0.23,  "dog": None,  "fit": "左側木門框（頭頂低於門楣）"},
        "backdoor":    {"char": 0.31,  "dog": 0.12,  "fit": "卸貨門；幼犬可見高≈人×0.28，四姿同高"},
        "clinic":      {"char": 0.27,  "dog": None,  "fit": "窗內木櫃檯（抱走；勿站玻璃門）"},
        "entrance":    {"char": 0.33,  "dog": None,  "fit": "大門／鞋櫃到腰（抱走）"},
        "living":      {"char": 0.32,  "dog": None,  "fit": "落地窗門框（抱走）"},
        "gate":        {"char": 0.28,  "dog": None,  "fit": "鐵門／木門框"},
    }

    # 幼犬 zoom = 後門狗／後門人；可見高 ≈ 人 ×0.28～0.37（勿用舊 1.048，會跟人差不多高）
    _PUPPY = 0.12 / 0.31

    def _puppy(char_z):
        return round(char_z * _PUPPY, 3)

    # S04–S10（及 S01／S03 共用的日常場）：人＝image_bg.md 對景；狗＝同平面幼犬比
    # kitchen／stairwell 狗為深度例外（門檻／門墊中遠景），不套幼犬比
    SCALE = {
        "living":        {"char": 0.36,  "dog": _puppy(0.36),  "fit": "落地窗全景（S04–S10 站）"},
        "living_center": {"char": 0.384, "dog": _puppy(0.36),  "fit": "客廳置中"},
        "living_chair":  {"char": 0.304, "dog": _puppy(0.36),  "fit": "矮凳坐姿；狗同客廳平面"},
        # 人沿床躺（頭在右枕）；小於客廳站姿 0.36；狗在地板，沿用客廳平面 0.139
        "bedroom":       {"char": 0.18,  "dog": _puppy(0.36),  "fit": "S07 沿床躺／看向門邊的狗；狗同客廳地板"},
        # 指尖特寫：頭距對齊 guard_door 後再近一檔（約地板尺 ×2.16）；勿用 visH 把全身縮小
        "bedroom_nose":  {"char": None,  "dog": 0.30,          "fit": "S07 鼻尖碰指尖；頭距母尺再靠近"},
        "living_wire":   {"char": None,  "dog": 0.30,          "fit": "S05 會後嗅線特寫；頭距再靠近"},
        "entrance_nudge":{"char": None,  "dog": 0.28,          "fit": "S06 額碰頭特寫；頭距再靠近"},
        "kitchen":       {"char": 0.52,  "dog": 0.19,          "fit": "POV；門檻深度例外"},
        "entrance":      {"char": 0.33,  "dog": _puppy(0.33),  "fit": "大門／鞋櫃（日常）"},
        # S08 巷口已改透視（見下方 S08_ALLEY），此鍵目前無 transform 使用，保留供 S10 等日後參考
        "alley":         {"char": 0.32,  "dog": _puppy(0.32),  "fit": "巷口散步（S08 改用 S08_ALLEY 透視）"},
        "cafe":          {"char": 0.36,  "dog": _puppy(0.36),  "fit": "咖啡廳門口"},
        "stairwell":     {"char": None,  "dog": 0.187,         "fit": "門墊中遠景（深度例外）"},
        "corridor":      {"char": 0.36,  "dog": _puppy(0.36),  "fit": "S06 門排／護衛"},
        "nudge":         {"char": None,  "dog": _puppy(0.36),  "fit": "頂額近景裁切；同客廳狗尺"},
    }

    def s02_char(place):
        return SCALE_S02[place]["char"]

    def s02_dog(place, flip=False):
        z = SCALE_S02[place]["dog"]
        if z is None:
            raise ValueError("SCALE_S02[%r] has no dog zoom (carry composite)" % place)
        return -z if flip else z

    def sc_char(place, flip=False):
        z = SCALE[place]["char"]
        if z is None:
            raise ValueError("SCALE[%r] has no char zoom" % place)
        return -z if flip else z

    def sc_dog(place, flip=False):
        z = SCALE[place]["dog"]
        if z is None:
            raise ValueError("SCALE[%r] has no dog zoom" % place)
        return -z if flip else z

    # ------------------------------------------------------------
    # S08 巷口透視（bg alley_day；2026-09-28）｜例外：本場「遠近＝ypos＋zoom 一起變」
    # 其他場仍遵守「同場遠近只改 xalign」。對照 image_scale.md §S08 巷口透視。
    # 量測（720p）：左側近木門 高198px、底 y=496；遠木門 高104px、底 y=463
    #   → 兩門等高反推地平線 y≈430；門 2.05 m → 鏡頭高≈0.68 m。
    # 人 1.62 m：可見高 = 1.62/0.68 ×(腳y−430) = 2.382×(腳y−430) px；
    #   walk 內容高 1437/1536 → 可見高 = 1197.5 × char zoom → char zoom = 0.001989×(腳y−430)。
    # 狗（2–3 月齡短腿幼犬，坐姿頭頂約 32 cm）：同深度 leash_wait 可見高 ≈ 人 ×0.195
    #   → dog zoom = char zoom × 0.3346（舊 alley 0.124/0.32 = 0.3875，狗偏大約 16%）。
    # 機車：停放車高 1.15 m（內容 754px）；騎士＋車 1.4 m（內容 1001px）。
    # 腳底 y 上限 578（字幕框上緣 572 附近；可略壓 6px）。
    S08_ALLEY = {
        "horizon": 430,
        "char_k": 0.001989,
        "dog_ratio": 0.3346,
        "size_y": 560,
        "prop_k": {"parked": 0.002243, "pass": 0.002057},
    }

    # 站位點：(畫布中心 x px, 腳底 y px)。予安從左下角、空車右側往路口走。
    # 面朝右。身後＝更左；前方＝更右。移動不改 zoom（人／狗／呼嘯車同一把 size_y）。
    # 空車在左下角。有人的車從右中車道出現，順著路面往前（zoom 不變）。
    # 樹幹根部約 (975, 572) 在右側花台上；路面：左人行道緣 y≈605−0.139x，右花台緣 x≈815–850（y 580–640）。
    # 巷道本身往右上縮向遠端（遠端在樹幹左側 x≈870–950、y≈470–505 露出路面）＝「轉角那頭」。
    # 左側牆邊由左而右：盆栽排（x 0–450）→木門＋台階（x 465–560）→盆栽（555–600）→電線桿（603–632，底 y≈517）
    #   →深色木屋牆面（x 640–780，無門）→盆栽（780–830）→小門（830–850）。
    S08_ALLEY_PT = {
        # 予安（面右；從左下角、空車右側走出來）
        "yuan_start":        (440, 572),
        "yuan_halfstep":     (500, 566),
        "yuan_step":         (550, 560),
        "yuan_pass":         (590, 554),
        "yuan_center":       (640, 548),
        "yuan_yanked":       (540, 562),   # 從路中趕快往後拉一步（面仍朝右）
        "yuan_drag1":        (760, 546),
        "yuan_drag2":        (830, 542),
        "yuan_home1":        (520, 562),
        "yuan_home2":        (450, 570),
        # 狗：身後＝更左；前方＝更右
        "dog_behind_start":  (360, 576),   # 她左後方，在空車右緣外側
        "dog_shuffle":       (400, 572),
        "dog_follow":        (470, 566),
        "dog_beside":        (580, 558),
        "dog_sniff_scooter": (340, 580),   # 高信任：面朝左下角空車
        "dog_behind_pass":   (520, 558),
        "dog_explore":       (720, 544),
        "dog_heel":          (670, 554),   # 被往後拉近，仍在她前面；抗拒圖繩朝左朝她
        "dog_wait_mid":      (840, 542),
        "dog_wait_shade":    (900, 538),
        "dog_drag1":         (680, 550),
        "dog_drag2":         (750, 546),
        "dog_home1":         (420, 566),
        "dog_home2":         (360, 572),
        # 機車
        "scooter_parked":    (70, 640),    # 左下角近景；與呼嘯車不同圖層，不要被換掉
        # 呼嘯：右中再偏右，順著車道往鏡頭前開，zoom 固定
        "scooter_pass_from": (1010, 500),
        "scooter_pass_mid":  (840, 610),
        "scooter_pass_to":   (600, 760),
    }

    def s08_pt(name):
        return S08_ALLEY_PT[name]

    def s08_char_z(name=None):
        # 移動不改大小：全場同一把，不跟腳底 y 變
        y = S08_ALLEY["size_y"]
        return round(S08_ALLEY["char_k"] * (y - S08_ALLEY["horizon"]), 4)

    def s08_dog_z(name=None):
        return round(s08_char_z() * S08_ALLEY["dog_ratio"], 4)

    # 立繪原圖面朝左；face="r" → 水平翻面
    def s08_char_xz(name, face="r"):
        z = s08_char_z(name)
        return -z if face == "r" else z

    def s08_dog_xz(name, face="r"):
        z = s08_dog_z(name)
        return -z if face == "r" else z

    def s08_prop_z(kind, y):
        return round(S08_ALLEY["prop_k"][kind] * (y - S08_ALLEY["horizon"]), 4)

    # ------------------------------------------------------------
    # 通用透視（2026-10-03；S09 起）｜流程見 agents/image_scale.md §0「透視與尺寸流程」
    # 原理同 S08_ALLEY：同一張背景裡，人可見高 = PERSON_H_M / cam_h × (腳底y − horizon) px。
    #   char zoom = PERSON_H_M / (cam_h × WALK_PX) × (腳底y − horizon)
    #   dog zoom  = char zoom × DOG_PERSON_RATIO（同 S08；cafe_tense 站姿 ≈ 人 ×0.205、leash_wait 坐 ≈ ×0.195）
    # horizon：背景消失線（窗框、地板縫、門楣、桌緣）延長的交點 y（720p）。
    # cam_h（鏡頭高 m）：用已知高度的物件反推 cam_h = 物高m × (物底y − horizon) / 物高px，至少兩件互相驗算。
    # 站位 PV_PT 的 y 一律是「腳底 y」；立繪必須 foot="auto" 裁掉腳下透明列（SPRITE_FOOT），否則會浮起。
    # 舊 SCALE["office"／"living"／"entrance"／"cafe"] 固定值仍給其他場用；S09 不再讀它們。
    PERSON_H_M = 1.62
    WALK_PX = 1197.5           # 母尺站姿 walk 內容高 1437/1536 × CHAR_REF_H 1280（char zoom 1.0 的可見高 px）
    DOG_PERSON_RATIO = 0.3346  # = S08_ALLEY["dog_ratio"]；舊 _PUPPY 0.387 讓狗大約 16%
    PERSP = {
        "office":   {"horizon": 230, "cam_h": 1.97,  "fit": "窗牆消失線；辦公椅 1.05 m（頂 414／底 625）、桌面 533 驗算"},
        "living":   {"horizon": 250, "cam_h": 1.16,  "fit": "落地窗底 458、高 392；沙發座 0.45 m（腳 586／座 445）"},
        "entrance": {"horizon": 250, "cam_h": 1.235, "fit": "大門高 411、底 497（2.05 m）；鞋櫃 0.85 m 驗算"},
        "cafe":     {"horizon": 330, "cam_h": 1.05,  "fit": "長凳座 0.42 m（腳 568／座 470）；門底 523（台階 0.15 m）"},
        # 2026-10-03 全場透視（S02–S08 室內、S10、結局）
        "kitchen":  {"horizon": 285, "cam_h": 1.35,  "fit": "左右流理台前緣交於 y≈280；流理台 0.9 m（x300：檯面 400／踢腳 625）；門口寬約 1.7 m 驗算"},
        # S10 巷口夜／街夜＝同一條巷子（S08 巷口構圖）：數字由 S08_ALLEY 換算，不另調
        #   cam_h = PERSON_H_M /(WALK_PX × char_k 0.001989) = 0.6802 → pv_char_z 與 s08 char_k 一致
        "alley":    {"horizon": 430, "cam_h": 0.6802, "fit": "= S08_ALLEY（horizon 430、char_k 0.001989）；S10 只有人"},
        "backdoor": {"horizon": 330, "cam_h": 0.95,  "fit": "右側巷道消失於路燈 y≈330；卸貨門 2.0 m（頂 165／底 445）＋垃圾箱 1.0 m（頂 335／底 445）互驗"},
        # S03／S06 梯廳（day／night 同構圖）：左門 2.05 m（頂 37／底 531）與電梯門 2.1 m（頂 50／底 519）等高反推
        "stairwell":{"horizon": 292, "cam_h": 1.00,  "fit": "左門 494px／電梯 469px 等高 → 地平線 292；門 2.05 m → 0.99、電梯 2.1 m → 1.02"},
        # S07 臥室夜：左牆踢腳線×地毯左緣交於 y≈342；門 2.05 m（底 531）、床頭櫃 0.6 m（底 637）、床墊 0.55 m 互驗
        "bedroom":  {"horizon": 342, "cam_h": 0.80,  "fit": "門 0.78／床頭櫃 0.83／床墊前緣 0.83 → 0.80"},
        # S03 大門夜：門廊左側牆上下緣交於 y≈365；木門 2.0 m（頂 225／底 506）；鐵門頂 175／底 515 ≈ 2.27 m 驗算
        "gate":     {"horizon": 365, "cam_h": 1.00,  "fit": "木門 281px＝2.0 m → 1.00"},
    }

    def pv_char_z(place, y):
        p = PERSP[place]
        return round(PERSON_H_M / (p["cam_h"] * WALK_PX) * (y - p["horizon"]), 4)

    def pv_dog_z(place, y):
        return round(pv_char_z(place, y) * DOG_PERSON_RATIO, 4)

    # 站位點：名稱 → (PERSP 場名, 畫布中心 x px, 腳底 y px)。只寫位置，zoom 一律由腳底 y 算。
    # 同一拍要「走過去不變大小」→ 起訖點用同一個 y（或差幾 px）。
    PV_PT = {
        # S09 辦公室（同事站走道、不站桌上；兩人都在走道地板）
        "s09_office_cw":      ("office", 800, 600),
        "s09_office_yuan":    ("office", 960, 590),
        # S09 夜客廳：予安坐右前木凳（圖含凳）；狗趴地毯
        "s09_lnight_chair":   ("living", 890, 612),
        "s09_lnight_door":    ("living", 600, 560),
        "s09_lnight_near":    ("living", 690, 560),
        # S09 週六客廳：先站＋遠狗；告別跪姿（左、翻面朝右）對狗（右）
        "s09_lday_stand":     ("living", 890, 582),
        "s09_lday_dog":       ("living", 690, 560),
        "s09_lday_kneel":     ("living", 540, 585),
        "s09_lday_dog_near":  ("living", 760, 600),
        # S09 玄關：予安蹲地墊；狗在她左前方（較近＝y 較大）
        "s09_ent_yuan":       ("entrance", 915, 553),
        "s09_ent_far":        ("entrance", 745, 575),
        "s09_ent_mid":        ("entrance", 800, 575),
        "s09_ent_near":       ("entrance", 850, 572),
        "s09_ent_back":       ("entrance", 680, 580),
        # S09 咖啡廳：同事在門前地墊（不站在前景盆栽上）；予安右側騎樓；狗同一條地面線 y 596
        "s09_cafe_cw":        ("cafe", 470, 600),
        "s09_cafe_cw_reach":  ("cafe", 540, 600),
        "s09_cafe_yuan":      ("cafe", 980, 590),
        "s09_cafe_by_yuan":   ("cafe", 880, 596),
        # 聞手：鼻尖貼同事右掌（掌心約 x546）。翻面後鼻尖在腳點左約 54px，所以腳點比掌心再右一點。
        "s09_cafe_hand":      ("cafe", 575, 596),
        "s09_cafe_hand_low":  ("cafe", 620, 596),
        "s09_cafe_hand_give": ("cafe", 575, 596),
        "s09_cafe_guard":     ("cafe", 900, 596),
        "s09_cafe_mid":       ("cafe", 735, 596),
        "s09_cafe_home":      ("cafe", 900, 596),
        # ---- 2026-10-03 全場透視 ----
        # 共用客廳狗位（dog_near／mid／far；S03–S05、S10、結局）：腳底 ≤ 578（字幕框上緣 572）
        "lv_far":             ("living", 760, 520),
        "lv_mid":             ("living", 640, 548),
        "lv_near":            ("living", 540, 574),
        # 共用玄關狗位（dog_entrance_mid／far；S03、S06、S10、結局）
        "ent_far":            ("entrance", 700, 548),
        "ent_mid":            ("entrance", 790, 572),
        # 廚房門口外（dog_kitchen_threshold；S04、S10）：門檻線 y≈615 在字幕框下，狗站門口外客廳地板
        "kit_door":           ("kitchen", 590, 560),
        # S10 巷口夜／街夜（只有人；同 S08 巷口 size_y 560）
        "s10_alley_yuan":     ("alley", 640, 560),
        "s10_street_yuan":    ("alley", 640, 560),
        # S10 玄關夜：予安站門墊右；狗在她左前（ent_mid／ent_far 共用）
        "s10_ent_yuan":       ("entrance", 905, 562),
        # S10 廚房夜：予安站右側流理台轉角前的地磚（流理台下方沒有地板可站；腳在字幕框下）
        "kit_sink":           ("kitchen", 880, 690),
        # S10 客廳夜：站右側木凳前；坐沙發右端（腳踩地毯前緣）
        "s10_lv_yuan":        ("living", 905, 568),
        "s10_lv_sofa":        ("living", 330, 566),
        # 結局 coda（endings.rpy）
        "cd_thin_ice":        ("living", 800, 528),
        "cd_check_near":      ("living", 600, 556),
        # S02 後門（夜）：狗趴紙箱左緣；予安在右側濕路面；腳底 ≤ 578
        "s02_bd_dog":         ("backdoor", 440, 562),
        "s02_bd_mid":         ("backdoor", 600, 568),
        "s02_bd_near":        ("backdoor", 760, 566),
        "s02_bd_yuan":        ("backdoor", 1040, 562),
        "s02_bd_squat":       ("backdoor", 985, 558),
        "s02_bd_carry":       ("backdoor", 640, 562),
        # S03 大門（只有人）／梯廳門墊狗窩／週六客廳
        "s03_gate_yuan":      ("gate", 665, 556),
        "s03_stair_mat":      ("stairwell", 300, 545),
        "s03_lv_to_yuan":     ("living", 620, 552),
        # S04 客廳：予安坐右前木凳（同 S09 夜客廳位）；狗在她左前地毯；尾隨往左下廚房門（越走越近＝越大）
        "s04_chair":          ("living", 890, 612),
        "s04_dog_near":       ("living", 745, 576),
        "s04_dog_mid":        ("living", 640, 562),
        "s04_dog_to_yuan":    ("living", 710, 545),
        "s04_follow_start":   ("living", 590, 560),
        "s04_follow_mid":     ("living", 450, 585),
        "s04_follow_left":    ("living", 320, 612),
        "s04_follow_door":    ("living", 200, 640),
        # S05 客廳：予安坐左前矮凳（圖含凳，翻面朝右）；狗用共用 lv_near／mid／far
        "s05_chair_left":     ("living", 415, 626),
        # S06 梯廳：鄰居左門前、予安走道偏右；狗在兩人間；behind＝她右小腿後（較遠一點）
        "s06_neighbor":       ("stairwell", 380, 560),
        "s06_yuan":           ("stairwell", 735, 565),
        "s06_dog_far":        ("stairwell", 550, 572),
        "s06_dog_mid":        ("stairwell", 640, 574),
        "s06_dog_behind":     ("stairwell", 800, 562),
        "s06_ent_yuan":       ("entrance", 880, 560),
        # S07 臥室：狗只走床左側地板（床左緣 x≈527@y576；舊 near 0.46 站在床沿上）
        "s07_bd_far":         ("bedroom", 300, 538),
        "s07_bd_mid":         ("bedroom", 400, 556),
        "s07_bd_shift":       ("bedroom", 440, 566),
        "s07_bd_near":        ("bedroom", 475, 578),
        # S07 夜客廳（關到客廳）：沙發前地板
        "s07_lv_far":         ("living", 525, 548),
        "s07_lv_sofa":        ("living", 400, 568),
        # S08 玄關：予安蹲門墊（同 S09 玄關位）；狗在鞋櫃與她之間，同一條地面線
        "s08_ent_yuan":       ("entrance", 905, 553),
        "s08_ent_far":        ("entrance", 690, 575),
        "s08_ent_to_yuan":    ("entrance", 740, 575),
        "s08_ent_mid":        ("entrance", 790, 575),
        "s08_ent_near":       ("entrance", 840, 572),
        # S08 辦公室夜（拍照回憶）：同 S09 辦公室位
        "s08_office_yuan":    ("office", 960, 590),
    }

    def pv_x(name):
        return PV_PT[name][1]

    def pv_y(name):
        return PV_PT[name][2]

    # 立繪原圖朝向不一（人多面左）；flip=True → xzoom 取負
    def pv_cz(name, flip=False):
        z = pv_char_z(PV_PT[name][0], PV_PT[name][2])
        return -z if flip else z

    def pv_dz(name, flip=False):
        z = pv_dog_z(PV_PT[name][0], PV_PT[name][2])
        return -z if flip else z

    # ------------------------------------------------------------
    # 腳底列（PNG 內 alpha>16 最下面一列 +1）。char_sprite／dog_sprite(foot="auto") 查這裡。
    # 量法：python tools/measure_sprite_foot.py <路徑…>（動畫用 --anim，取各幀最大）。換圖必重量。
    # S08 巷口那批仍寫在 image 定義的 foot= 字面值（若與本表衝突，lint 會列出）。
    SPRITE_FOOT = {
        "char/char-coworker.png": 1457,             # 1024x1536 內容高 1402 底留白 79
        "char/char-coworker-cafe.png": 1376,        # 內容高 1234 底留白 160
        "char/char-yuan-headphones.png": 1473,      # 內容高 1418 底留白 63
        "char/char-yuan-home-sit.png": 1451,        # 內容高 1391 底留白 85（含凳腳）
        "char/char-yuan-home-stand.png": 1482,      # 內容高 1434 底留白 54
        "char/char-yuan-farewell.png": 1438,        # 內容高 1341 底留白 98
        "char/char-yuan-cafe.png": 1495,            # 內容高 1460 底留白 41
        "char/char-yuan-leash-pass.png": 1519,      # 內容高 1488 底留白 17
        "char/char-yuan-leash.png": 1063,           # 864x1152 內容高 1004 底留白 89（= S08 leash_street foot）
        "char/char-yuan-squat-side.png": 1409,      # 內容高 1269 底留白 127
        "dog/dog-parallel.png": 841,                # 1536x1024 內容高 564 底留白 183
        "dog/dog-leash-wait.png": 1513,             # 內容高 1037 底留白 23
        "dog/dog-paper-bag-sniff.png": 1241,        # 內容高 821 底留白 295（含紙袋）
        "dog/dog-cafe-tense.png": 1512,             # 內容高 716 底留白 24
        "dog/dog-cafe-refuse.png": 1511,            # 內容高 653 底留白 25
        "dog/dog-farewell.png": 1346,               # 靜態備援；內容高 1078 底留白 190
        "dog/farewell/dog-farewell-01.png": 1362,   # 5 幀取最大；底留白 174
        "dog/farewell/dog-farewell-02.png": 1362,
        "dog/farewell/dog-farewell-03.png": 1362,
        "dog/farewell/dog-farewell-04.png": 1362,
        "dog/farewell/dog-farewell-05.png": 1362,
        "dog/cafe-sniff/dog-cafe-sniff-01.png": 1530,  # 5 幀取最大；底留白 6（比 cafe_tense 低 18 列）
        "dog/cafe-sniff/dog-cafe-sniff-02.png": 1530,
        "dog/cafe-sniff/dog-cafe-sniff-03.png": 1530,
        "dog/cafe-sniff/dog-cafe-sniff-04.png": 1530,
        "dog/cafe-sniff/dog-cafe-sniff-05.png": 1530,
        # ---- 2026-10-03 全場透視補量（tools/measure_sprite_foot.py）----
        "char/char-yuan-commute.png": 1493,  # 內容高 1452 底留白 43
        "char/char-yuan-paper-bag.png": 1497,  # 內容高 1460 底留白 39
        "char/char-yuan-sofa.png": 1466,  # 內容高 1391 底留白 70（坐姿）
        "dog/dog-halfstep.png": 1513,  # 內容高 1499 底留白 23
        "dog/dog-kitchen-door.png": 1226,  # 內容高 999 底留白 310
        "dog/dog-back-sleep.png": 874,  # 靜態備援
        "dog/dog-check-sleep.png": 822,  # 靜態備援
        "dog/dog-door-edge.png": 840,  # 靜態備援
        "char/char-yuan-carry-pup.png": 1460,  # 內容高 1385 底留白 76
        "dog/dog-s04-anxious.png": 929,  # 1536x1024 內容高 811 底留白 95
        "dog/dog-sniff-bento.png": 1512,  # 內容高 1343 底留白 24
        "dog/dog-ear-flat.png": 1513,  # 內容高 1332 底留白 23
        "char/char-yuan-headphones-sit.png": 1468,  # 1024x1536 內容高 1408 底留白 68
        "char/char-yuan-headphones-off-sit.png": 1439,  # 1024x1536 內容高 1390 底留白 97
        "char/char-yuan-door-hold.png": 1128,  # 864x1152 內容高 1099 底留白 24
        "char/char-yuan-block.png": 1118,  # 864x1152 內容高 1087 底留白 34
        "char/char-neighbor-idle.png": 1116,  # 864x1152 內容高 1093 底留白 36
        "char/char-neighbor.png": 1495,  # 1024x1536 內容高 1473 底留白 41
        "char/char-neighbor-lower.png": 1107,  # 864x1152 內容高 1068 底留白 45
        "char/char-neighbor-withdraw.png": 1123,  # 864x1152 內容高 1099 底留白 29
        "dog/dog-coat-sniff.png": 1183,  # 1024x1536 內容高 765 底留白 353
        "dog/dog-stair-watch.png": 1203,  # 1024x1536 內容高 936 底留白 333
        "dog/dog-street-tense.png": 1067,  # 1024x1536 內容高 652 底留白 469
        "dog/dog-ear-perk.png": 878,  # 1536x1024 內容高 722 底留白 146
        "dog/dog-chin-hover.png": 819,  # 1536x1024 內容高 532 底留白 205
        "dog/dog-head-turn.png": 930,  # 1536x1024 內容高 813 底留白 94
        "dog/dog-chin-floor.png": 989,  # 1536x1024 內容高 716 底留白 35
        "dog/dog-head-up.png": 966,  # 1536x1024 內容高 904 底留白 58
        "dog/dog-chair-paw.png": 1476,  # 1024x1536 內容高 1345 底留白 60
        "dog/dog-chair-stuck.png": 1398,  # 1024x1536 內容高 1137 底留白 138
        "dog/dog-s06-retreat.png": 663,  # 859x680 內容高 640 底留白 17
        "dog/dog-s06-watch-hand.png": 926,  # 835x940 內容高 904 底留白 14
        "dog/dog-s06-flinch.png": 603,  # 861x620 內容高 578 底留白 17
        "dog/dog-behind-legs.png": 553,  # 862x569 內容高 528 底留白 16
        "dog/dog-s06-freeze.png": 887,  # 840x904 內容高 864 底留白 17
        "dog/dog-s08-sniff-harness.png": 957,  # 864x958 內容高 726 底留白 1
        "dog/dog-harness-bite.png": 1510,  # 1024x1536 內容高 924 底留白 26
        "dog/dog-s08-threshold.png": 958,  # 864x958 內容高 744 底留白 0
        "dog/dog-shoe-sleep.png": 859,  # 1536x1024 內容高 677 底留白 165
    }
    # 動畫幀：各 5 幀取最大腳底列（幀已 normalize 回原框）
    for _d, _f in {
        "back-sleep": 883,
        "check-sleep": 832,
        "door-edge": 851,
        "door-sleep": 833,
        "sniff-wire": 1072,
        "guard-door": 861,
        "wag": 762,
    }.items():
        SPRITE_FOOT.update({"dog/%s/dog-%s-%02d.png" % (_d, _d, _i): _f for _i in range(1, 6)})
