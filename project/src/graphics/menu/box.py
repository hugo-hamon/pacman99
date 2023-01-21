from typing import Tuple
import pygame as pg


class Box:

    def __init__(self, text: str, font_size: int, screen: pg.surface.Surface, width: int, position: Tuple[float, float]) -> None:
        self.font = pg.font.Font("assets/font/pac-font.TTF", font_size)
        self.sprite = pg.image.load("assets/images/menu/empty_box.png")
        self.sprite = self.resize(width, self.sprite)
        self.position = position
        self.screen = screen
        self.text = text

    def resize(self, width: int, sprite: pg.surface.Surface) -> pg.surface.Surface:
        """Resize the sprite"""
        factor = sprite.get_width() / sprite.get_height()
        return pg.transform.scale(sprite, (width, width / factor))

    def display(self) -> None:
        """Display the box"""
        x = self.position[0] - self.sprite.get_width() / 2
        y = self.position[1]
        self.screen.blit(self.sprite, (x, y))
        text = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(text, (x + self.sprite.get_width() / 2 - text.get_width() / 2,
                                y + self.sprite.get_height() / 2 - text.get_height() / 2))

    def get_dimension(self) -> Tuple[float, float, float, float]:
        """Return the box"""
        x = self.position[0] - self.sprite.get_width() / 2
        y = self.position[1]
        return (x, y, self.sprite.get_width(), self.sprite.get_height())

    def is_collide(self, x: float, y: float) -> bool:
        """Return True if the box is collide with the mouse"""
        x_box, y_box, width, height = self.get_dimension()
        return x_box < x < x_box + width and y_box < y < y_box + height
