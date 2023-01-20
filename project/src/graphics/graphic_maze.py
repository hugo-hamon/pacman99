from ..game.maze.components import Components
from .spritesheet import SpriteSheet
from .wall_func import get_wall_name
from .standalone import rescale
from ..game.game import Game
from typing import List
import pygame as pg


class GraphicMaze:

    def __init__(self, screen: pg.surface.Surface, game: Game, spritesheet: SpriteSheet) -> None:
        self.screen = screen
        self.game = game
        self.spritesheet = spritesheet
        self.maze_sprites = self.create_maze_sprites()

    def create_maze_sprites(self) -> List[List[pg.surface.Surface]]:
        """Create the sprites of the maze"""
        maze = self.game.get_maze()
        sprites = {
            Components.EMPTY: "void",
            Components.DOT: "dot",
            Components.SUPERDOT: "super_dot",
            Components.FRUIT: "fruit",
        }
        maze_sprites = []
        for i in range(maze.get_height()):
            new_sprites = []
            for j in range(maze.get_width()):
                cell = maze.get_cell(j, i)
                sprite_name = ""
                if cell == Components.WALL:
                    sprite_name = get_wall_name(j, i, maze)
                else:
                    sprite_name = sprites[cell]
                new_sprites.append(rescale(
                    self.spritesheet.parse_sprite(sprite_name), self.screen, self.game)
                )
            maze_sprites.append(new_sprites)
        return maze_sprites

    def display_maze(self, canvas: pg.surface.Surface) -> None:
        """Display the maze"""
        maze = self.game.get_maze()
        for i in range(maze.get_height()):
            for j in range(maze.get_width()):
                # Check if the state of a dot has changed to empty
                if maze.get_cell(j, i) == Components.EMPTY:
                    self.maze_sprites[i][j] = self.spritesheet.parse_sprite(
                        "void")
                canvas.blit(self.maze_sprites[i][j], (
                    j * self.maze_sprites[i][j].get_width(), i * self.maze_sprites[i][j].get_height()))
