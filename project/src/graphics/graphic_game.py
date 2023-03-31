from ..game.maze.components import Components
from .graphic_pacman import GraphicPacman
from .graphic_ghost import GraphicGhost
from ..game.direction import Direction
from .graphic_maze import GraphicMaze
from .spritesheet import SpriteSheet
from ..game.maze.maze import Maze
from ..game.game import Game
from ..config import Config
from typing import Callable
from .menu import MainMenu
from .sounds import Sounds
import pygame as pg

spritesheet_path = "assets/images/palettes.png"
TILE_SIZE = 8

# TODO rename file to graphicGame.py
class GraphicGame(Game):

    def __init__(self, config: Config, sounds: Sounds, maze: Maze, control_func: Callable) -> None:
        super().__init__(config, maze, control_func)
        self.addListener(self.dot_eaten_event, "dotPickup", self)
        self.addListener(self.superdot_eaten_event, "superDotPickup", self)
        self.config = config
        factor = max(config.graphics.width, config.graphics.height) / \
            (self.get_maze().get_width() * TILE_SIZE)
        screen_width = self.get_maze().get_width() * TILE_SIZE * int(factor)
        screen_height = self.get_maze().get_height() * TILE_SIZE * int(factor)
        self.screen = pg.display.set_mode(
            (screen_width, screen_height))
        pg.display.set_caption(config.graphics.title)
        self.canvas = pg.Surface(
            (screen_width, screen_height))

        self.clock = pg.time.Clock()
        self.sound = sounds

        self.spritesheet = SpriteSheet(spritesheet_path)
        self.fps = config.graphics.fps
        self.game = self
        self.running = False

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

    # COMMANDS
    # TODO rename to run ?
    def run(self) -> None:
        """Run the graphic"""
        if self.config.user.menu_enable:
            self.launch_main_menu(self.config.user.sound_enable)

        # play the background sound
        if self.config.user.sound_enable:
            self.sound.play_sound("assets/music/siren_1.wav", True)

        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    self.__process_key_down(event)

            # Update the game
            self.update()

            # Display the sprites
            self.display_sprites()
            self.screen.blit(self.canvas, (0, 0))

            # Update the display
            self.canvas.fill((0, 0, 0))
            pg.display.update()
            self.clock.tick(self.fps)

    def __process_key_down(self, event: pg.event.Event) -> None:
        if not self.config.genetic.genetic_enable:
            if event.key in [pg.K_q, pg.K_LEFT]:
                self.get_pacman().set_next_direction(Direction.WEST)
            if event.key in [pg.K_d, pg.K_RIGHT]:
                self.get_pacman().set_next_direction(Direction.EAST)
            if event.key in [pg.K_z, pg.K_UP]:
                self.get_pacman().set_next_direction(Direction.NORTH)
            if event.key in [pg.K_s, pg.K_DOWN]:
                self.get_pacman().set_next_direction(Direction.SOUTH)
        if event.key == pg.K_ESCAPE and self.config.user.menu_enable:
            self.launch_main_menu(False)
            if self.config.user.sound_enable:
                self.sound.play_sound("assets/music/siren_1.wav", True)

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

    def launch_main_menu(self, play_sound: bool) -> None:
        """Launch the main menu"""
        self.sound.stop_sound()
        if play_sound:
            self.sound.play_sound("assets/music/title_screen.mp3", True)
        self.main_menu.run()
        if play_sound:
            self.sound.fadeout_sound(1000)
    
    def dot_eaten_event(self, coords):
        if self.config.user.sound_enable:
            self.sound.play_sound_once("assets/music/munch_1.wav")
    
    def superdot_eaten_event(self, coords):
        if self.config.user.sound_enable:
                        self.sound.play_sound_once("assets/music/munch_2.wav")
                        self.sound.play_sound_once(
                            "assets/music/power_pellet.wav")
    
    def lives_lost_event(self, args):
        if self.config.user.sound_enable:
                    self.sound.play_sound_once("assets/music/death_1.wav")