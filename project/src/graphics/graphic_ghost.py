from .spritesheet import SpriteSheet
from .standalone import rescale
from ..game.game import Game
from typing import List
import pygame as pg


class GraphicGhost():

    def __init__(self, screen: pg.surface.Surface, game: Game, spritesheet: SpriteSheet) -> None:
        self.screen = screen
        self.game = game
        self.spritesheet = spritesheet
        self.ghost = self.create_ghost_sprite()

    def rescale_sprite(self, path: str) -> pg.surface.Surface:
        """Rescale a sprite"""
        return rescale(
            self.spritesheet.parse_sprite(
                path), self.screen, self.game
        )

    def create_ghost_sprite(self) -> List[pg.surface.Surface]:
        """Create a ghost sprite"""
        ghost_sprites = [self.rescale_sprite("red_ghost_0")]
        ghost_sprites.append(self.rescale_sprite("pink_ghost_0"))
        ghost_sprites.append(self.rescale_sprite("orange_ghost_0"))
        ghost_sprites.append(self.rescale_sprite("blue_ghost_0"))
        return ghost_sprites

    def display_ghost(self, canvas: pg.surface.Surface) -> None:
        """Display ghost"""
        # Order: Blinky, Pinky, Clyde, Inky
        for k, ghost in enumerate(self.game.get_ghosts()):
            ghost_position = ghost.get_position()
            ghost_position = (
                ghost_position[0] * self.ghost[k].get_width(),
                ghost_position[1] * self.ghost[k].get_height()
            )
            canvas.blit(self.ghost[k], ghost_position)
