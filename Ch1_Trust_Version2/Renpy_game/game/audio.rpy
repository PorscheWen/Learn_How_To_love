## BGM／幼犬 SFX（對齊 agents/audio.md）
## 資產：game/assets/audio/（junction → Ch1_Trust_Version2/assets/audio）

define audio.bgm_melancholy = "audio/melancholy.ogg"
define audio.bgm_warm = "audio/warm.ogg"
define audio.bgm_calm = "audio/calm.ogg"
define audio.bgm_tender = "audio/tender.ogg"

define audio.sfx_whimper = "audio/sfx/puppy-whimper-a.wav"
define audio.sfx_whimper_b = "audio/sfx/puppy-whimper-b.wav"
define audio.sfx_murmur = "audio/sfx/puppy-murmur-a.wav"
define audio.sfx_murmur_b = "audio/sfx/puppy-murmur-b.wav"
define audio.sfx_soft = "audio/sfx/puppy-soft-a.wav"
define audio.sfx_soft_b = "audio/sfx/puppy-soft-b.wav"
define audio.sfx_sigh = "audio/sfx/puppy-sigh-a.wav"
define audio.sfx_yip = "audio/sfx/puppy-yip-a.ogg"
define audio.sfx_excited = "audio/sfx/puppy-excited-a.wav"
define audio.sfx_bark = "audio/sfx/puppy-bark-a.wav"
define audio.sfx_growl = "audio/sfx/dog-growl.ogg"

default _bgm_profile = ""

init python:
    BGM_TRACKS = {
        "melancholy": "audio/melancholy.ogg",
        "warm": "audio/warm.ogg",
        "calm": "audio/calm.ogg",
        "tender": "audio/tender.ogg",
        "rain_soft": "audio/melancholy.ogg",
        "warm_quiet": "audio/warm.ogg",
        "awkward_day": "audio/calm.ogg",
        "shop_bustle": "audio/warm.ogg",
        "night_thin": "audio/calm.ogg",
        "soft_growth": "audio/tender.ogg",
        "tension_soft": "audio/calm.ogg",
        "clinic_soft": "audio/calm.ogg",
        "ending_warm": "audio/warm.ogg",
        "ending_quiet": "audio/tender.ogg",
        "hopeful": "audio/warm.ogg",
        "tense": "audio/calm.ogg",
    }

    DOG_SFX = {
        "whimper": "audio/sfx/puppy-whimper-a.wav",
        "whimper_b": "audio/sfx/puppy-whimper-b.wav",
        "murmur": "audio/sfx/puppy-murmur-a.wav",
        "murmur_b": "audio/sfx/puppy-murmur-b.wav",
        "soft": "audio/sfx/puppy-soft-a.wav",
        "soft_b": "audio/sfx/puppy-soft-b.wav",
        "sigh": "audio/sfx/puppy-sigh-a.wav",
        "yip": "audio/sfx/puppy-yip-a.ogg",
        "excited": "audio/sfx/puppy-excited-a.wav",
        "bark": "audio/sfx/puppy-bark-a.wav",
        "growl": "audio/sfx/dog-growl.ogg",
    }

    def play_bgm(profile, fade=2.0, force=False):
        """換 BGM；同 profile 不重播（除非 force）。"""
        key = str(profile or "").strip()
        track = BGM_TRACKS.get(key)
        if not track:
            return
        if (not force) and store._bgm_profile == key:
            return
        store._bgm_profile = key
        renpy.music.play(track, channel="music", loop=True, fadein=fade, fadeout=1.5)

    def dog_sfx(cue, volume=0.85):
        """幼犬 one-shot；稀疏觸發。"""
        path = DOG_SFX.get(str(cue or "").strip())
        if not path:
            return
        try:
            renpy.sound.play(path, channel="sound", relative_volume=volume)
        except TypeError:
            renpy.sound.play(path, channel="sound")

    def stop_bgm(fade=1.5):
        store._bgm_profile = ""
        renpy.music.stop(channel="music", fadeout=fade)
