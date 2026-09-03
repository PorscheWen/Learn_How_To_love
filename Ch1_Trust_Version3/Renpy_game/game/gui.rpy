init offset = -2

init python:
    gui.init(1280, 720)

define CJK_FONT = "SourceHanSansLite.ttf"

define LHTL_BG = "#17120F"
define LHTL_PANEL = "#F3E9D9AA"
define LHTL_PANEL_GLASS = "#F3E9D955"
## 選單外框透、按鈕略實（半透明仍透出油畫，字可讀）
define LHTL_MENU_SHELL = "#17120F22"
define LHTL_MENU_ITEM = "#F3E9D9C4"
define LHTL_MENU_ITEM_HOVER = "#E8C9A0F0"
define LHTL_MENU_ITEM_PRIMARY = "#D9B48AE8"
define LHTL_MENU_ITEM_PRIMARY_HOVER = "#C99A6CF5"
define LHTL_MENU_ITEM_MUTED = "#F3E9D988"
define LHTL_MENU_ITEM_MUTED_HOVER = "#E2C8A7CC"
define LHTL_PANEL_DARK = "#2E241FCC"
define LHTL_TEXT = "#4A3728"
define LHTL_TEXT_LIGHT = "#F7EFE4"
define LHTL_TEXT_SOFT = "#D9C8B3"
define LHTL_ACCENT = "#B77A45"
define LHTL_ACCENT_DARK = "#7A4E2E"
define LHTL_CHOICE = "#F3E9D9EE"
define LHTL_CHOICE_HOVER = "#E2C8A7F5"

define gui.text_font = CJK_FONT
define gui.name_text_font = CJK_FONT
define gui.interface_text_font = CJK_FONT
define gui.text_size = 25
define gui.name_text_size = 22
define gui.interface_text_size = 20
define gui.label_text_size = 30
define gui.title_text_size = 46

define gui.text_color = LHTL_TEXT
define gui.interface_text_color = LHTL_TEXT
define gui.accent_color = LHTL_ACCENT
define gui.idle_color = LHTL_TEXT
define gui.hover_color = LHTL_ACCENT_DARK
define gui.selected_color = LHTL_ACCENT_DARK
define gui.insensitive_color = "#8C817777"

define gui.textbox_height = 148
define gui.dialogue_xpos = 54
define gui.dialogue_ypos = 18
define gui.dialogue_width = 1172
define gui.name_xpos = 54
define gui.name_ypos = 18

define gui.choice_button_width = 760
define gui.choice_button_borders = Borders(28, 16, 28, 16)
define gui.choice_button_text_font = CJK_FONT
define gui.choice_button_text_size = 22
define gui.choice_button_text_xalign = 0.5
define gui.choice_button_text_idle_color = LHTL_TEXT
define gui.choice_button_text_hover_color = LHTL_ACCENT_DARK

define gui.main_menu_background = Solid(LHTL_BG)
## 實際圖層由 script.rpy init 1 覆寫為 theme/title-main.png、theme/menu-bg.png
define gui.game_menu_background = Solid(LHTL_BG)

style default:
    font CJK_FONT
    color LHTL_TEXT

style say_window:
    background None
    xfill True
    yalign 1.0
    yminimum gui.textbox_height
    ymaximum gui.textbox_height
    padding (38, 16, 38, 18)

style say_label:
    color LHTL_ACCENT_DARK
    size gui.name_text_size
    outlines [(2, "#F7EFE4D9", 0, 0)]

style say_dialogue:
    color "#000000"
    size gui.text_size
    line_spacing 16
    outlines [(2, "#F7EFE4D9", 0, 0)]

style choice_button:
    background Solid(LHTL_CHOICE)
    hover_background Solid(LHTL_CHOICE_HOVER)
    padding (28, 16)
    xsize gui.choice_button_width

style choice_button_text:
    font CJK_FONT
    size gui.choice_button_text_size
    color LHTL_TEXT
    hover_color LHTL_ACCENT_DARK
    xalign 0.5

style quick_button:
    background Solid("#2E241FAA")
    hover_background Solid("#7A4E2EDD")
    padding (10, 6)

style quick_button_text:
    font CJK_FONT
    size 15
    color LHTL_TEXT_LIGHT

## 主選單／一般選項（可點區加大、hover 清楚）
style menu_button:
    background Solid(LHTL_MENU_ITEM)
    hover_background Solid(LHTL_MENU_ITEM_HOVER)
    selected_background Solid(LHTL_MENU_ITEM_HOVER)
    padding (20, 10)
    xminimum 240
    yminimum 44
    xalign 0.5

style menu_button_text:
    font CJK_FONT
    size 19
    color LHTL_TEXT
    hover_color LHTL_ACCENT_DARK
    selected_color LHTL_ACCENT_DARK
    xalign 0.5
    text_align 0.5
    outlines [(1, "#F7EFE455", 0, 0)]

## 「開始」主行動：略深、更醒目
style menu_primary_button is menu_button:
    background Solid(LHTL_MENU_ITEM_PRIMARY)
    hover_background Solid(LHTL_MENU_ITEM_PRIMARY_HOVER)
    padding (20, 12)
    yminimum 50

style menu_primary_button_text is menu_button_text:
    size 21
    color LHTL_ACCENT_DARK
    hover_color "#5C3A22"

## 返回／次要
style menu_back_button is menu_button:
    background Solid(LHTL_MENU_ITEM_MUTED)
    hover_background Solid(LHTL_MENU_ITEM_MUTED_HOVER)
    xminimum 160
    yminimum 40
    padding (16, 8)

style menu_back_button_text is menu_button_text:
    size 17
    color "#5C4A3A"

## 長列表（結局／隱藏內容）：左對齊方便掃讀
style menu_list_button is menu_button:
    padding (16, 9)
    xminimum 180
    yminimum 40
    xalign 0.0

style menu_list_button_text is menu_button_text:
    size 17
    xalign 0.0
    text_align 0.0

## 嵌在 menu-bg 上的選項／卡片
style embed_menu_button is menu_button:
    background Solid(LHTL_MENU_ITEM)
    hover_background Solid(LHTL_MENU_ITEM_HOVER)

style embed_menu_button_text is menu_button_text
