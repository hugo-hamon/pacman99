from ..game.direction import Direction
from typing import Tuple
import pygame as pg



class Sprite(pg.sprite.Sprite):

    def __init__(self, width: int, height: int, pos_x: int, pos_y: int, direction: Direction) -> None:
        super().__init__()
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.direction = direction

    # REQUESTS
    def get_position(self) -> Tuple[int, int]:
        """Return the position of the sprite"""
        assert self.rect is not None
        return self.rect.center

    def get_direction(self) -> Direction:
        """Return the direction of the sprite"""
        return self.direction

    # COMMANDS
    def set_position(self, pos_x: int, pos_y: int) -> None:
        """Set the position of the sprite"""
        assert self.rect is not None
        self.rect.center = (pos_x, pos_y)

    def set_direction(self, direction: Direction) -> None:
        """Set the direction of the sprite"""
        self.direction = direction

    def update(self) -> None:
        """Update the sprite"""
        pass
