from .spritesheet import SpriteSheet
from .standalone import rescale
from ..game.game import Game
from ..game.entities.ghost.ghoststate import Ghoststate
from ..game.direction import Direction
from typing import List
import pygame as pg

class GraphicGhost():

    GHOST_SPRITE_PATH = {"Blinky": "red", "Pinky": "pink", "Clyde": "orange", "Inky": "blue"}

    def __init__(self, screen: pg.surface.Surface, game: Game, spritesheet: SpriteSheet) -> None:
        self.screen = screen
        self.game = game
        self.spritesheet = spritesheet
        self.ghost = self.create_ghost_sprite()
        self.animation_speed = 0.1

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
        self.animation_speed = (self.animation_speed + 0.1) % 2
        for k, ghost in enumerate(self.game.get_ghosts()):
            ghost_position = ghost.get_position()
            ghost_position = (
                ghost_position[0] * self.ghost[k].get_width(),
                ghost_position[1] * self.ghost[k].get_height()
            )
            if ghost.state == Ghoststate.FRIGHTENED or ghost.state == Ghoststate.EATEN:
                self.ghost[k] = self.rescale_sprite("dead_" + self.GHOST_SPRITE_PATH[ghost.__class__.__name__] + "_ghost_" + str(int(self.animation_speed)))
            else :
                direction_to_animation = {Direction.NORTH: 3, Direction.EAST: 0, Direction.SOUTH: 1, Direction.WEST: 2}
                self.ghost[k] = self.rescale_sprite(self.GHOST_SPRITE_PATH[ghost.__class__.__name__] + "_ghost_" + str(int(self.animation_speed + 2 * direction_to_animation[ghost.direction])))

            canvas.blit(self.ghost[k], ghost_position)
