from typing import Tuple
import pygame as pg

ARROW_PADDING = 0.15
ARROW_SHRINK = 0.9
POINT = Tuple[float, float]


class ArrowBox:

    def __init__(self, text: str, font_size: int, screen: pg.surface.Surface, width: int, position: Tuple[float, float]) -> None:
        self.font = pg.font.Font("assets/font/pac-font.TTF", font_size)
        self.position = position
        self.screen = screen
        self.width = width
        self.text = text

        self.box_sprite = self.load_and_resize(
            "assets/images/menu/empty_box.png", width)
        self.right_arrow_sprite = self.load_and_resize(
            "assets/images/menu/arrow.png", round(width / 6))
        self.left_arrow_sprite = pg.transform.flip(
            self.right_arrow_sprite, True, False)

    def load_and_resize(self, path: str, width: int) -> pg.surface.Surface:
        """Load and resize the sprite"""
        sprite = pg.image.load(path)
        return self.resize(width, sprite)

    def resize(self, width: int, sprite: pg.surface.Surface) -> pg.surface.Surface:
        """Resize the sprite"""
        factor = sprite.get_width() / sprite.get_height()
        return pg.transform.scale(sprite, (width, width / factor))

    def display(self) -> None:
        """Display the arrow box"""
        x = self.position[0] - self.box_sprite.get_width() / 2
        y = self.position[1]
        self.screen.blit(self.box_sprite, (x, y))
        text = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(text, (x + self.box_sprite.get_width() / 2 - text.get_width() / 2,
                                y + self.box_sprite.get_height() / 2 - text.get_height() / 2))
        padding = self.box_sprite.get_width() * ARROW_PADDING
        self.screen.blit(self.left_arrow_sprite, (x - self.left_arrow_sprite.get_width() / 2 -
                         padding, y + self.box_sprite.get_height() / 2 - self.left_arrow_sprite.get_height() / 2))
        self.screen.blit(self.right_arrow_sprite, (x + self.box_sprite.get_width() - self.right_arrow_sprite.get_width() /
                         2 + padding, y + self.box_sprite.get_height() / 2 - self.right_arrow_sprite.get_height() / 2))

    def get_left_arrow_vertex_coordinate(self) -> Tuple[POINT, POINT, POINT]:
        """Return the left arrow vertex coordinate"""
        padding = self.box_sprite.get_width() * ARROW_PADDING
        x1 = self.position[0] - self.box_sprite.get_width() / \
            2 - self.left_arrow_sprite.get_width() / 2 - padding
        y1 = self.position[1] + self.box_sprite.get_height() / 2 - \
            self.left_arrow_sprite.get_height() / 2 + self.left_arrow_sprite.get_height() / 2
        x2 = x1 + self.left_arrow_sprite.get_width()
        y2 = y1 - self.left_arrow_sprite.get_height() / 2
        x3 = x2
        y3 = y1 + self.left_arrow_sprite.get_height() / 2
        return (x1, y1), (x2, y2), (x3, y3)

    def get_right_arrow_vertex_coordinate(self) -> Tuple[POINT, POINT, POINT]:
        """Return the right arrow dimension"""
        padding = self.box_sprite.get_width() * ARROW_PADDING
        x1 = self.position[0] + self.box_sprite.get_width() / \
            2 + self.right_arrow_sprite.get_width() / 2 + padding
        y1 = self.position[1] + self.box_sprite.get_height() / 2 - self.right_arrow_sprite.get_height() / \
            2 + self.right_arrow_sprite.get_height() / 2
        x2 = x1 - self.right_arrow_sprite.get_width()
        y2 = y1 - self.right_arrow_sprite.get_height() / 2
        x3 = x2
        y3 = y1 + self.right_arrow_sprite.get_height() / 2
        return (x1, y1), (x2, y2), (x3, y3)

    def is_left_collide(self, x: float, y: float) -> bool:
        """Return True if the left arrow is collide with the mouse"""
        coord = self.get_left_arrow_vertex_coordinate()
        p1 = coord[0]
        p2 = coord[1]
        p3 = coord[2]
        return self.is_collide(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], x, y)

    def is_right_collide(self, x: float, y: float) -> bool:
        """Return True if the right arrow is collide with the mouse"""
        coord = self.get_right_arrow_vertex_coordinate()
        p1 = coord[0]
        p2 = coord[1]
        p3 = coord[2]
        return self.is_collide(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], x, y)

    def is_collide(self, x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x: float, y: float) -> bool:
        """Return True if the point is collide with the triangle"""
        c1 = (x3 - x) * (y1 - y) - (y3 - y) * (x1 - x) > 0
        c2 = (x1 - x) * (y2 - y) - (y1 - y) * (x2 - x) > 0
        c3 = (x2 - x) * (y3 - y) - (y2 - y) * (x3 - x) > 0
        return c1 == c2 == c3
