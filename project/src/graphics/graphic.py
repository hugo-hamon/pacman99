from ..game.maze.components import Components
from .spritesheet import SpriteSheet
from .wall_func import get_wall_name
from typing import List, Union
from ..game.game import Game
from ..config import Config
from .sprites import Sprite
import pygame as pg



spritesheet_path = "assets/images/palettes.png"


class Graphic:

    def __init__(self, config: Config, game: Game) -> None:
        self.screen = pg.display.set_mode(
            (config.graphics.width, config.graphics.height))
        pg.display.set_caption(config.graphics.title)
        self.canvas = pg.Surface(
            (config.graphics.width, config.graphics.height))
        self.group = pg.sprite.Group()
        self.clock = pg.time.Clock()
        self.mixer = pg.mixer

        self.spritesheet = SpriteSheet(spritesheet_path)
        self.fps = config.graphics.fps
        self.game = game
        self.run = False

        self.maze_sprites = []

    # REQUESTS
    def draw(self) -> None:
        """Draw the sprites on the screen"""
        self.group.draw(self.screen)

    def update_sprites(self) -> None:
        """Update the sprites"""
        self.group.update()

    def play_sound(self, sound_path: str, loop_enable: bool) -> None:
        """Play a sound in loop or not"""
        self.mixer.music.load(sound_path)
        self.mixer.music.play(-1 if loop_enable else 0)

    def display_maze(self) -> None:
        """Display the maze"""
        maze = self.game.get_maze()
        for i in range(maze.get_height()):
            for j in range(maze.get_width()):
                self.canvas.blit(self.maze_sprites[i][j], (j * self.maze_sprites[i][j].get_width(), i * self.maze_sprites[i][j].get_height()))

    def rescale(self, element: pg.surface.Surface) -> pg.surface.Surface:
        """Rescale the element size"""
        w = self.screen.get_width() / self.game.get_maze().get_width()
        h = self.screen.get_height() / self.game.get_maze().get_height()
        return pg.transform.scale(element, (w, h))

    # COMMANDS
    def start(self) -> None:
        """Run the graphic"""
        # Init the graphic
        self.create_maze_sprites()

        self.run = True
        while self.run:
            self.clock.tick(self.fps)
            self.canvas.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            self.display_maze()
            self.draw()
            self.screen.blit(self.canvas, (0, 0))
            pg.display.update()

    def add_sprites_to_group(self, sprites: Union[List[Sprite], Sprite]) -> None:
        """Add a sprite or a list of sprites to the group"""
        self.group.add(sprites)

    def create_maze_sprites(self) -> None:
        """Create the sprites of the maze"""
        maze = self.game.get_maze()
        sprites = {
            Components.EMPTY: "void",
            Components.DOT: "dot",
            Components.SUPERDOT: "super_dot",
            Components.FRUIT: "fruit",
        }
        for i in range(maze.get_height()):
            new_sprites = []
            for j in range(maze.get_width()):
                cell = maze.get_cell(j, i)
                sprite_name = ""
                if cell == Components.WALL:
                    sprite_name = get_wall_name(j, i, maze)
                else:
                    sprite_name = sprites[cell]
                new_sprites.append(self.rescale(self.spritesheet.parse_sprite(sprite_name)))
            self.maze_sprites.append(new_sprites)
