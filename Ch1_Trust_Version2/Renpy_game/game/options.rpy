## Learn How to Love｜Version2 Ren'Py

define config.name = _("Learn How to Love")
define config.version = "0.4.0-day7"
define gui.show_name = True
define config.window_title = "Learn How to Love"

init python:
    import os
    _asset_root = os.path.join(config.gamedir, "assets")
    if os.path.isdir(_asset_root):
        config.searchpath.append(_asset_root)

define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = None
define config.enter_transition = Dissolve(0.4)
define config.exit_transition = Dissolve(0.3)
define config.after_load_transition = Dissolve(0.2)

define config.save_directory = "LearnHowToLove-V2"
define config.has_autosave = True
define config.autosave_on_quit = True
define config.autosave_frequency = 20
define config.autosave_slots = 6

define config.quit_action = Quit(confirm=True)
define config.window_icon = "gui/window_icon.png"

default preferences.text_cps = 32
default preferences.afm_time = 18
default quick_menu = True
define config.history_length = 250

init python:
    def _lhtl_boot_text_speed():
        try:
            init_text_speed()
        except Exception:
            preferences.text_cps = 32
            preferences.afm_time = 18

    config.start_callbacks.append(_lhtl_boot_text_speed)
    config.after_load_callbacks.append(_lhtl_boot_text_speed)
