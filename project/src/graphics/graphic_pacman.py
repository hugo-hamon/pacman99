from ..game.direction import Direction
from .spritesheet import SpriteSheet
from .standalone import rescale
from ..game.game import Game
from typing import List
import pygame as pg

ANIMATION_SPEED = 0.1


class GraphicPacman():

    def __init__(self, screen: pg.surface.Surface, game: Game, spritesheet: SpriteSheet) -> None:
        self.screen = screen
        self.game = game
        self.spritesheet = spritesheet
        self.sprites = self.create_sprites()
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def display_pacman(self, canvas: pg.surface.Surface) -> None:
        """Display pacman"""
        current_direction = self.game.get_pacman().get_direction()
        self.image = pg.transform.rotate(
            self.image, current_direction.to_angle())
        pacman_position = self.game.get_pacman().get_position()
        pacman_position = (
            pacman_position[0] * self.image.get_width(),
            pacman_position[1] * self.image.get_height()
        )
        canvas.blit(self.image, pacman_position)

    def update(self) -> None:
        """Update the pacman sprite"""
        self.current_sprite = (self.current_sprite +
                               ANIMATION_SPEED) % len(self.sprites)
        self.image = self.sprites[int(self.current_sprite)]

    def create_sprites(self) -> List[pg.surface.Surface]:
        """Create the sprites"""
        sprites = [rescale(
            self.spritesheet.parse_sprite("pacman_0"), self.screen, self.game
        )
        ]
        sprites.append(rescale(
            self.spritesheet.parse_sprite("pacman_1"), self.screen, self.game
        ))

        return sprites
