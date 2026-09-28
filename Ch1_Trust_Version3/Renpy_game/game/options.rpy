## Learn How to Love｜Version3 Ren'Py

define config.name = _("Learn How to Love")
define config.version = "1.0.0-ch1"
define config.window_title = "Learn How to Love｜Ch1 Trust"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False
## 主選單用 S01 空白夜感；檔案不存在時 Ren'Py 會略過
define config.main_menu_music = "audio/calm.ogg"
define config.check_conflicting_properties = True

## ESC／右鍵開遊戲選單時，直接進「設定」頁
define _game_menu_screen = "preferences"

define config.enter_transition = Dissolve(0.45)
define config.exit_transition = Dissolve(0.35)
define config.after_load_transition = Dissolve(0.25)

## 關窗／Alt+F4／離開一律不再跳確認（autosave_on_quit 仍會自動存檔）
define config.quit_action = Quit(confirm=False)

define config.save_directory = "LearnHowToLove-Version3"
define config.has_autosave = True
define config.autosave_on_quit = True
define config.autosave_frequency = 20
define config.history_length = 250

## 視窗圖示（由 game/window-icon.png 產生，來源：theme/title-main.png）
define config.window_icon = "window-icon.png"

init python:
    import os

    ## 發行建置：排除開發工具與規劃文件（資產已置於 game/ 內）
    build.name = "LearnHowToLove-Ch1Trust"
    build.directory_name = "LearnHowToLove-Ch1Trust-{}".format(config.version)

    _build_exclude = (
        "tools/**",
        "**/dialogue_editor/**",
        "**/output/seedance/**",
        "**/*.ps1",
        "**/*.bat",
        "**/*.md",
        "**/.git/**",
        "**/.github/**",
        "**/__pycache__/**",
        "**/*.pyc",
        "../agents/**",
        "../tools/**",
        "../../agent/**",
        "../../MEMORY.md",
        "../../guide_line.md",
        "../../.cursorrules",
    )
    for _pattern in _build_exclude:
        build.classify(_pattern, None)

    ## 字型授權須隨正式版發行
    build.classify("game/SourceHanSansLite.ttf", "all")
    build.classify("game/OFL.txt", "all")

    ## 開發用：Shift+U／F8 全解鎖（僅 config.developer）
    if config.developer:
        if "_dev_unlock_hotkey" not in config.always_shown_screens:
            config.always_shown_screens.append("_dev_unlock_hotkey")

default preferences.text_cps = 30
default preferences.afm_time = 18
default quick_menu = True
