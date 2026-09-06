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
        "kitchen":       {"char": 0.52,  "dog": 0.19,          "fit": "POV；門檻深度例外"},
        "entrance":      {"char": 0.33,  "dog": _puppy(0.33),  "fit": "大門／鞋櫃（日常）"},
        "alley":         {"char": 0.32,  "dog": _puppy(0.32),  "fit": "巷口散步"},
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
