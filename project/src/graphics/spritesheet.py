import pygame as pg
import json


class SpriteSheet:

    def __init__(self, file_name: str) -> None:
        self.sprite_sheet = pg.image.load(file_name).convert()
        self.file_name = file_name
        self.meta_data = self.file_name.replace(".png", ".json")
        with open(self.meta_data) as file:
            self.data = json.load(file)

    def get_sprite(self, x: int, y: int, width: int, height: int) -> pg.Surface:
        """Return a sprite from the sprite sheet"""
        sprite = pg.Surface((width, height))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey((0, 0, 0))
        return sprite

    def parse_sprite(self, sprite_name: str) -> pg.Surface:
        """Parse a sprite from the sprite sheet"""
        sprite = self.data["frames"][sprite_name]["frame"]
        return self.get_sprite(sprite["x"], sprite["y"], sprite["w"], sprite["h"])
