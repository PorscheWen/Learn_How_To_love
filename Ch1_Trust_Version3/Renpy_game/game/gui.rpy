init offset = -2

init python:
    gui.init(1280, 720)

define CJK_FONT = "SourceHanSansLite.ttf"

define LHTL_BG = "#17120F"
define LHTL_PANEL = "#F3E9D9EE"
define LHTL_PANEL_GLASS = "#F3E9D977"
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

define gui.textbox_height = 108
define gui.dialogue_xpos = 54
define gui.dialogue_ypos = 24
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
define gui.game_menu_background = Solid(LHTL_BG)

style default:
    font CJK_FONT
    color LHTL_TEXT

style say_window:
    background None
    xfill True
    yalign 1.0
    yminimum gui.textbox_height
    padding (38, 12, 38, 14)

style say_label:
    color LHTL_ACCENT_DARK
    size gui.name_text_size
    outlines [(2, "#F7EFE4D9", 0, 0)]

style say_dialogue:
    color "#000000"
    size gui.text_size
    line_spacing 8
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

style menu_button:
    background Solid("#F3E9D9E8")
    hover_background Solid("#E2C8A7F5")
    padding (24, 12)
    xminimum 260

style menu_button_text:
    font CJK_FONT
    size 21
    color LHTL_TEXT
    hover_color LHTL_ACCENT_DARK
    xalign 0.5
