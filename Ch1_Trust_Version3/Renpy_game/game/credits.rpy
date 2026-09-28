## 主選單「製作群／授權」｜對齊 assets/audio/CREDITS.md

init python:
    CREDITS_SECTIONS = [
        (
            "音樂（BGM）",
            (
                "Peaceful Intro (Looping) — Eric Matyas（soundimage.org）｜CC BY\n"
                "Peace at last — bart｜CC BY\n"
                "Thoughtful Piano Theme — Trinnox｜CC BY\n"
                "Emotional Piano — Centurion_of_war｜CC0\n"
                "The Budding of Consciousness — Yoiyami｜CC0\n"
                "First Light Particles — Yoiyami｜CC0\n"
                "Yoiyami Core Theme — Yoiyami｜CC0\n"
                "（以上取自 OpenGameArt.org）"
            ),
        ),
        (
            "音效（SFX）",
            (
                "Chihuahua Puppy Whine — AustinXYZ（Freesound）｜CC0\n"
                "Puppy (8) — johnnypanic（Freesound）｜CC0\n"
                "Baby Animals sounds pack — OpenGameArt｜CC0\n"
                "Dog Grunt — qubodup／Frieda（OpenGameArt）｜CC0"
            ),
        ),
        (
            "字型",
            (
                "Source Han Sans（本遊戲使用 Lite 子集）\n"
                "Copyright © 2014–2021 Adobe、Google 等｜SIL Open Font License 1.1\n"
                "授權全文見 game/OFL.txt"
            ),
        ),
        (
            "引擎",
            (
                "Ren'Py Visual Novel Engine\n"
                "Copyright © 2004–2024 Tom Rothamel 等｜MIT License\n"
                "https://www.renpy.org/"
            ),
        ),
    ]


screen credits():
    tag menu

    add "lhtl_menu_bg"
    add Solid("#17120F33")

    frame:
        background Solid(LHTL_PANEL_GLASS)
        padding (28, 20)
        xalign 0.5
        yalign 0.5
        xsize 820
        ysize 620

        side "t c b":
            xfill True
            yfill True
            spacing 10

            vbox:
                spacing 2
                xfill True
                text "製作群／授權":
                    font CJK_FONT
                    size 24
                    color LHTL_TEXT_LIGHT
                    outlines [(2, "#17120F99", 0, 0)]
                text "音樂、音效與字型須保留署名":
                    font CJK_FONT
                    size 13
                    color LHTL_TEXT_SOFT

            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xfill True
                yfill True

                vbox:
                    spacing 16
                    xfill True
                    for section_title, section_body in CREDITS_SECTIONS:
                        text section_title:
                            font CJK_FONT
                            size 16
                            color LHTL_ACCENT_DARK
                        text section_body:
                            font CJK_FONT
                            size 15
                            color LHTL_TEXT
                            line_spacing 4

            textbutton "返回" style "menu_back_button" action Return():
                xalign 0.5
