from ..game.sprites import Sprite
from typing import List, Union
import pygame as pg


class Graphic:

    def __init__(self, screen_width: int, screen_height: int, fps: int) -> None:
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.group = pg.sprite.Group()
        self.clock = pg.time.Clock()
        self.mixer = pg.mixer

        self.run = False
        self.fps = fps

    # REQUESTS
    def draw(self) -> None:
        """Draw the sprites on the screen"""
        self.group.draw(self.screen)

    def update_sprites(self, sprites: Union[List[Sprite], Sprite]) -> None:
        """Update a sprite or a list of sprites"""
        self.group.update(sprites)

    def play_sound(self, sound_path: str, loop_enable: bool) -> None:
        """Play a sound in loop or not"""
        self.mixer.music.load(sound_path)
        self.mixer.music.play(-1 if loop_enable else 0)

    # COMMANDS
    def start(self) -> None:
        """Run the graphic"""
        self.run = True
        while self.run:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            self.draw()
            pg.display.flip()

    def add_sprites_to_group(self, sprites: Union[List[Sprite], Sprite]) -> None:
        """Add a sprite or a list of sprites to the group"""
        self.group.add(sprites)
