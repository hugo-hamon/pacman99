from ..game.maze.components import Components
from .graphic_pacman import GraphicPacman
from .graphic_ghost import GraphicGhost
from ..game.direction import Direction
from .graphic_maze import GraphicMaze
from .spritesheet import SpriteSheet
from ..game.game import Game
from ..config import Config
from .menu import MainMenu
import pygame as pg


spritesheet_path = "assets/images/palettes.png"


class Graphic:

    def __init__(self, config: Config, game: Game) -> None:
        self.config = config
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

        # Create the sprites
        self.maze_sprites = GraphicMaze(
            self.screen, self.game, self.spritesheet
        )
        self.pacman_sprite = GraphicPacman(
            self.screen, self.game, self.spritesheet
        )
        self.ghost = GraphicGhost(
            self.screen, self.game, self.spritesheet
        )
        self.create_sprites()

        self.main_menu = MainMenu(self.screen, self.game, self)

    # REQUESTS
    def play_sound(self, sound_path: str, loop_enable: bool) -> None:
        """Play a sound in loop or not"""
        self.mixer.music.load(sound_path)
        self.mixer.music.play(-1 if loop_enable else 0)

    # COMMANDS
    def start(self) -> None:
        """Run the graphic"""
        if self.config.user.enable_menu:
            self.main_menu.run()
        self.run = True
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN:
                    self.__process_key_event(event)

            # Update the game
            self.game.update()

            # Display the sprites
            self.display_sprites()
            self.screen.blit(self.canvas, (0, 0))

            # Update the display
            self.canvas.fill((0, 0, 0))
            pg.display.update()
            self.clock.tick(self.fps)

    # TODO Rename this here and in `start`
    def __process_key_event(self, event: pg.event.Event) -> None:
        if event.key == pg.K_q:
            self.game.get_pacman().set_next_direction(Direction.WEST)
        if event.key == pg.K_d:
            self.game.get_pacman().set_next_direction(Direction.EAST)
        if event.key == pg.K_z:
            self.game.get_pacman().set_next_direction(Direction.NORTH)
        if event.key == pg.K_s:
            self.game.get_pacman().set_next_direction(Direction.SOUTH)
        if event.key == pg.K_SPACE:
            self.game.get_maze().set_component(Components.SUPERDOT, 1, 1)
        if event.key == pg.K_ESCAPE and self.config.user.enable_menu:
            self.main_menu.run()

    def create_sprites(self) -> None:
        """Create the sprites"""
        self.pacman_sprite.create_sprites()
        self.maze_sprites.create_maze_sprites()
        self.ghost.create_ghost_sprite()

    def display_sprites(self) -> None:
        """Display the sprites"""
        self.pacman_sprite.display_pacman(self.canvas)
        self.maze_sprites.display_maze(self.canvas)
        self.ghost.display_ghost(self.canvas)

    def set_fps(self, fps: int) -> None:
        """Set the fps"""
        self.fps = fps

    def get_fps(self) -> int:
        """Get the fps"""
        return self.fps
