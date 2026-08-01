init offset = -2

init python:
    gui.init(1280, 720)

define CJK_FONT = "SourceHanSansLite.ttf"
## SourceHanSansLite 缺字勿用：U+00B7 間隔點、U+25B8 小三角、U+2726 四角星（會變方框／X）
## 間隔請用 U+FF5C 全形直線 或 U+30FB；箭頭可用 U+25B6

## —— Theme：暖夜細節（深褐層次＋米金點綴＋半透明字幕）——
## 靈感：雨夜紙箱 → 家裡小燈；避免冷紫／純黑／刺眼白
define LHTL_BG = "#100E0C"
define LHTL_BG_WARM = "#18140F"
define LHTL_PANEL = "#1C1814"
define LHTL_PANEL_EDGE = "#3D3428"
define LHTL_PANEL_ALT = "#26201A"
define LHTL_PANEL_HOVER = "#3A3228"
define LHTL_PANEL_LOCKED = "#1A161288"
define LHTL_TEXT = "#F0E9DF"
define LHTL_TEXT_SOFT = "#D0C3B0"
define LHTL_TEXT_MUTED = "#A89880"
define LHTL_ACCENT = "#D4B57A"
define LHTL_ACCENT_DIM = "#9A7A3E"
define LHTL_ACCENT_GLOW = "#C9A96E55"
define LHTL_ROSE = "#C4A090"          # 溫柔點綴（靠膝／羈絆）
define LHTL_TEXTBOX = "#14110F96"     # 半透明字幕
define LHTL_TEXTBOX_EDGE = "#C9A96E66"
define LHTL_OVERLAY = "#0A0806CC"
define LHTL_QUICK_BG = "#0A0806AA"
define LHTL_SMELL_BG = "#0C0A0888"
define LHTL_CHOICE_BG = "#26201A99"       # 半透明選項
define LHTL_CHOICE_HOVER = "#3A3228CC"
define LHTL_CHOICE_EDGE = "#C9A96E55"

define gui.accent_color = LHTL_ACCENT
define gui.idle_color = LHTL_TEXT_SOFT
define gui.idle_small_color = LHTL_TEXT_MUTED
define gui.hover_color = LHTL_ACCENT
define gui.selected_color = LHTL_TEXT
define gui.insensitive_color = "#5555557f"
define gui.muted_color = LHTL_TEXT_MUTED
define gui.hover_muted_color = LHTL_TEXT_SOFT
define gui.text_color = LHTL_TEXT
define gui.interface_text_color = LHTL_TEXT

define gui.text_font = CJK_FONT
define gui.name_text_font = CJK_FONT
define gui.interface_text_font = CJK_FONT
define gui.text_size = 22
define gui.name_text_size = 24
define gui.interface_text_size = 20
define gui.label_text_size = 24
define gui.notify_text_size = 16
define gui.title_text_size = 34
define gui.smell_text_size = 14

define gui.main_menu_background = Solid(LHTL_BG)
define gui.game_menu_background = Solid(LHTL_BG)

define gui.textbox_yalign = 1.0
define gui.name_xpos = 40
define gui.name_ypos = 0
define gui.name_xalign = 0.0
define gui.name_yalign = 0.0
define gui.dialogue_xpos = 40
define gui.dialogue_ypos = 8
define gui.dialogue_width = 1160
define gui.dialogue_text_xalign = 0.0
## 字幕固定顯示約 3 行
define gui.dialogue_lines = 3
define gui.dialogue_line_spacing = 8
define gui.dialogue_text_height = (gui.text_size * gui.dialogue_lines) + (gui.dialogue_line_spacing * (gui.dialogue_lines - 1))
## 字幕框高度：上緣線＋名字列＋三行對白＋內距
define gui.textbox_height = gui.dialogue_text_height + 72

define gui.choice_button_width = 720
define gui.choice_button_height = None
define gui.choice_button_tile = False
define gui.choice_button_borders = Borders(20, 12, 20, 12)
define gui.choice_button_text_font = CJK_FONT
define gui.choice_button_text_size = gui.interface_text_size
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = LHTL_TEXT
define gui.choice_button_text_hover_color = LHTL_ACCENT
define gui.choice_button_text_insensitive_color = gui.insensitive_color

define gui.button_width = None
define gui.button_height = None
define gui.button_borders = Borders(16, 12, 16, 12)
define gui.button_tile = False
define gui.button_text_font = CJK_FONT
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color

define gui.quick_button_borders = Borders(8, 6, 8, 6)
define gui.quick_button_text_size = 15
define gui.quick_button_text_idle_color = LHTL_TEXT_MUTED
define gui.quick_button_text_selected_color = LHTL_ACCENT
define gui.quick_button_text_hover_color = LHTL_ACCENT

## 狗掌游標（cursor.cc file_id=255278，CC 免署名；0.5×＝32px）
## 來源：https://www.cursor.cc/?action=icon&file_id=255278
define config.mouse = {
    "default": [("gui/cursor_paw.png", 2, 1)],
    "button": [("gui/cursor_paw_hover.png", 2, 1)],
    "say": [("gui/cursor_paw.png", 2, 1)],
    "with": [("gui/cursor_paw.png", 2, 1)],
    "menu": [("gui/cursor_paw_hover.png", 2, 1)],
    "prompt": [("gui/cursor_paw.png", 2, 1)],
}

define config.font_replacement_map = {
    "DejaVuSans.ttf": (CJK_FONT, False, False),
    "DejaVuSans-Bold.ttf": (CJK_FONT, False, True),
    "DejaVuSans-Oblique.ttf": (CJK_FONT, False, False),
    "DejaVuSans-BoldOblique.ttf": (CJK_FONT, False, True),
}

init python:
    def lhtl_panel(bg=LHTL_PANEL, edge=LHTL_PANEL_EDGE):
        """雙層邊框面板：外金線感＋內深褐。"""
        return Frame(
            Composite(
                (64, 64),
                (0, 0), Solid(edge),
                (2, 2), Solid(bg),
            ),
            8, 8,
        )

    def lhtl_choice_idle():
        return Frame(
            Composite(
                (64, 48),
                (0, 0), Solid(LHTL_CHOICE_EDGE),
                (1, 1), Solid(LHTL_CHOICE_BG),
            ),
            6, 6,
        )

    def lhtl_choice_hover():
        return Frame(
            Composite(
                (64, 48),
                (0, 0), Solid(LHTL_ACCENT),
                (2, 2), Solid(LHTL_CHOICE_HOVER),
            ),
            6, 6,
        )

    def lhtl_textbox_bg():
        return Frame(
            Composite(
                (64, 64),
                (0, 0), Solid(LHTL_TEXTBOX_EDGE),
                (0, 3), Solid(LHTL_TEXTBOX),
            ),
            10, 10,
        )

    _cjk_styles = [
        style.default,
        style.say_dialogue,
        style.say_thought,
        style.say_label,
        style.choice_button,
        style.button,
        style.quick_button,
    ]
    for _s in _cjk_styles:
        _s.font = CJK_FONT
        _s.italic = False

    style.say_dialogue.color = LHTL_TEXT
    style.say_dialogue.outlines = [(1, "#00000055", 0, 1)]
    style.say_dialogue.line_spacing = gui.dialogue_line_spacing
    style.say_dialogue.size = gui.text_size
    style.say_label.color = LHTL_ACCENT
    style.say_label.size = gui.name_text_size
    style.choice_button.background = lhtl_choice_idle()
    style.choice_button.hover_background = lhtl_choice_hover()
    style.choice_button.top_padding = 4
    style.choice_button.bottom_padding = 4
    style.choice_button.top_margin = 4
    style.choice_button.bottom_margin = 4
    style.button.background = lhtl_panel(LHTL_PANEL_ALT, LHTL_PANEL_EDGE)
    style.button.hover_background = lhtl_panel(LHTL_PANEL_HOVER, LHTL_ACCENT)
    style.label_text.color = LHTL_TEXT
    style.label_text.outlines = [(1, "#00000044", 0, 1)]
    style.input.color = LHTL_TEXT
    style.input.caret = Solid(LHTL_ACCENT)
    style.bar.left_bar = Solid(LHTL_ACCENT)
    style.bar.right_bar = Solid(LHTL_PANEL_ALT)
    style.bar.thumb = Solid(LHTL_TEXT_SOFT)
    style.bar.ysize = 16
    style.vscrollbar.base_bar = Solid(LHTL_PANEL_ALT)
    style.vscrollbar.thumb = Solid(LHTL_TEXT_MUTED)
