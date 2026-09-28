## 立繪尺（唯一數字來源）
## 對照：Ch1_Trust_Version3/agents/image_scale.md
## 改大小：只改本檔 SCALE_S02／SCALE，不要在 script.rpy 寫死 zoom。
## 同場遠近只改 xalign；狗一律 zoom 1.0 + xzoom／yzoom（勿混用 zoom）。

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
