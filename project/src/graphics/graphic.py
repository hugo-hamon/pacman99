from ..game.maze.components import Components
from ..game.direction import Direction
from .spritesheet import SpriteSheet
from .wall_func import get_wall_name
from ..game.game import Game
from ..config import Config
from typing import List
import pygame as pg


spritesheet_path = "assets/images/palettes.png"


class Graphic:

    def __init__(self, config: Config, game: Game) -> None:
        self.screen = pg.display.set_mode(
            (config.graphics.width, config.graphics.height))
        pg.display.set_caption(config.graphics.title)
        self.canvas = pg.Surface(
            (config.graphics.width, config.graphics.height))

        self.clock = pg.time.Clock()
        self.mixer = pg.mixer

        self.spritesheet = SpriteSheet(spritesheet_path)
        self.fps = config.graphics.fps
        self.game = game
        self.run = False

        self.maze_sprites = self.create_maze_sprites()
        self.pacman_sprite = self.create_pacman_sprite()

    # REQUESTS
    def play_sound(self, sound_path: str, loop_enable: bool) -> None:
        """Play a sound in loop or not"""
        self.mixer.music.load(sound_path)
        self.mixer.music.play(-1 if loop_enable else 0)

    def display_maze(self) -> None:
        """Display the maze"""
        maze = self.game.get_maze()
        for i in range(maze.get_height()):
            for j in range(maze.get_width()):
                self.canvas.blit(self.maze_sprites[i][j], (
                    j * self.maze_sprites[i][j].get_width(), i * self.maze_sprites[i][j].get_height()))

    def display_pacman(self) -> None:
        """Display pacman"""
        pacman_position = self.game.get_pacman().get_position()
        pacman_position = (
            pacman_position[0] * self.pacman_sprite.get_width(),
            pacman_position[1] * self.pacman_sprite.get_height()
        )
        self.canvas.blit(self.pacman_sprite, pacman_position)

    def rescale(self, element: pg.surface.Surface) -> pg.surface.Surface:
        """Rescale the element size"""
        w = self.screen.get_width() / self.game.get_maze().get_width()
        h = self.screen.get_height() / self.game.get_maze().get_height()
        return pg.transform.scale(element, (w, h))

    # COMMANDS
    def start(self) -> None:
        """Run the graphic"""
        # Init the graphic
        self.run = True
        k = 0
        while self.run:
            self.clock.tick(self.fps)
            self.canvas.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.game.get_pacman().set_next_direction(Direction.WEST)
                    if event.key == pg.K_d:
                        self.game.get_pacman().set_next_direction(Direction.EAST)
                    if event.key == pg.K_z:
                        self.game.get_pacman().set_next_direction(Direction.NORTH)
                    if event.key == pg.K_s:
                        self.game.get_pacman().set_next_direction(Direction.SOUTH)
                    self.game.get_pacman().accept_next_direction()
            self.game.update()
            self.display_maze()
            self.display_pacman()
            self.screen.blit(self.canvas, (0, 0))
            pg.display.update()

    def create_pacman_sprite(self) -> pg.surface.Surface:
        """Create a pacman sprite"""
        return self.rescale(
            self.spritesheet.parse_sprite("pacman_0")
        )

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
                new_sprites.append(self.rescale(
                    self.spritesheet.parse_sprite(sprite_name)))
            maze_sprites.append(new_sprites)
        return maze_sprites
