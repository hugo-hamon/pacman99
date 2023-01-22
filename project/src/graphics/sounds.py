import pygame as pg


class Sounds:

    def __init__(self) -> None:
        self.mixer = pg.mixer
        self.mixer.init()

    def play_sound(self, sound_path: str, loop_enable: bool) -> None:
        """Play a sound in loop or not"""
        self.mixer.music.load(sound_path)
        self.mixer.music.play(-1 if loop_enable else 0)

    def play_sound_once(self, sound_path: str) -> None:
        """Play a sound once"""
        self.mixer.Sound(sound_path).play()

    def stop_sound(self) -> None:
        """Stop the sound"""
        self.mixer.music.stop()

    def fadeout_sound(self, time: int) -> None:
        """Fadeout the sound in time ms"""
        self.mixer.music.fadeout(time)