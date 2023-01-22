from .maze.random_maze_factory import RandomMazeFactory
from .entities.ghost import Blinky, Pinky, Clyde, Inky
from .entities.ghost.ghost import GeneralGhost
from .maze.components import Components
from ..graphics.sounds import Sounds
from .entities.pacman import Pacman
from .direction import Direction
from .maze.maze import Maze
from ..config import Config
from typing import List


class Game:

    def __init__(self, config: Config, sounds: Sounds) -> None:
        path = config.graphics.maze_path
        if config.user.enable_random_maze:
            RandomMazeFactory(config).create()
            path = config.maze.random_maze_path
        self.config = config
        self.sounds = sounds
        self.maze = Maze(filename=path)
        self.pacman = self.init_pacman()
        self.ghosts = self.init_ghosts()

        self.score = 0

    # REQUESTS
    def is_game_over(self) -> bool:
        """Return True if the game is over"""
        return self.is_game_won() or self.pacman.is_dead()

    def is_game_won(self) -> bool:
        """Return True if the game is won"""
        return self.maze.get_total_remain_dots() == 0

    def get_score(self) -> int:
        """Return the score"""
        return self.score

    def get_maze(self) -> Maze:
        """Return the maze"""
        return self.maze

    def get_pacman(self) -> Pacman:
        """Return the pacman"""
        return self.pacman

    def get_ghosts(self) -> List[GeneralGhost]:
        """Return the ghosts"""
        return self.ghosts

    # COMMANDS
    def reset(self) -> None:
        """Reset the game"""
        # self.maze.reset()
        # self.pacman.reset()

    def init_pacman(self) -> Pacman:
        """Initialize the pacman and return it"""
        pacman = Pacman(
            self.maze, self.config.game.game_speed, Direction.NONE, (0, 0),
            self.config.game.pacman_lives
        )
        pacman.set_position(self.maze.get_pacman_start())
        return pacman

    def init_ghosts(self) -> List[GeneralGhost]:
        """Initialize the ghosts and return them"""
        ghosts: List[GeneralGhost] = [Blinky(self.maze, self.pacman, self.config.game.game_speed,
                                             Direction.NORTH, (self.maze.get_width() / 2, self.maze.get_height() / 2))]
        ghosts.append(Pinky(self.maze, self.pacman, self.config.game.game_speed,
                      Direction.NORTH, (self.maze.get_width() / 2 + 1, self.maze.get_height() / 2)))
        ghosts.append(Clyde(self.maze, self.pacman, self.config.game.game_speed,
                      Direction.NORTH, (self.maze.get_width() / 2 - 1, self.maze.get_height() / 2)))
        ghosts.append(Inky(self.maze, self.pacman, self.config.game.game_speed,
                      Direction.NORTH, (self.maze.get_width() / 2, self.maze.get_height() / 2 - 1)))
        return ghosts

    def update(self) -> None:
        """Update the game"""
        self.pacman.move(60)
        if self.is_pacman_dying():
            self.respawn_pacman()
        for ghost in self.ghosts:
            ghost.move(60)
            if self.is_pacman_dying():
                self.respawn_pacman()
        self.eat_dot()
        self.pacman_tp()
        self.ghosts_tp()
        if self.pacman.get_lives() == 0:
            print("You lost")
        if self.is_game_won():
            print("You won")

    def respawn_pacman(self):
        if self.config.user.enable_graphics and self.config.user.sound_enable:
            print("play sound")
            self.sounds.play_sound_once("assets/music/death_1.wav")
        self.pacman.lose_life()
        self.pacman.direction = Direction.NONE
        self.pacman.set_position(self.maze.get_pacman_start())

    def eat_dot(self) -> None:
        """Eat a dot"""
        pacman_position = (round(self.pacman.get_position()[0]), round(
            self.pacman.get_position()[1]))
        if pacman_position[0] >= 0 and pacman_position[0] < self.maze.get_width() and \
                pacman_position[1] >= 0 and pacman_position[1] < self.maze.get_height():
            if self.maze.get_cell(pacman_position[0], pacman_position[1]) == Components.DOT:
                if self.config.user.enable_graphics and self.config.user.sound_enable:
                    self.sounds.play_sound_once("assets/music/munch_1.wav")
                self.score += 1
                self.maze.set_component(
                    Components.EMPTY, pacman_position[1], pacman_position[0])
            if self.maze.get_cell(pacman_position[0], pacman_position[1]) == Components.SUPERDOT:
                if self.config.user.enable_graphics and self.config.user.sound_enable:
                    self.sounds.play_sound_once("assets/music/munch_2.wav")
                    self.sounds.play_sound_once(
                        "assets/music/power_pellet.wav")
                self.score += 1
                self.maze.set_component(
                    Components.EMPTY, pacman_position[1], pacman_position[0])

    def pacman_tp(self) -> None:
        """Teleport the pacman"""
        pacman_position = (round(self.pacman.get_position()[0]), round(
            self.pacman.get_position()[1]))
        if pacman_position[0] < 0:
            self.pacman.set_position(
                (self.maze.get_width() - 1, pacman_position[1]))
        if pacman_position[0] > self.maze.get_width() - 1:
            self.pacman.set_position((0, pacman_position[1]))

    def ghosts_tp(self) -> None:
        """Teleport the ghost"""
        for ghost in self.ghosts:
            ghost_position = (round(ghost.get_position()[0]), round(
                ghost.get_position()[1]))
            if ghost_position[0] < 0:
                ghost.set_position(
                    (self.maze.get_width() - 1, ghost_position[1]))
            if ghost_position[0] > self.maze.get_width() - 1:
                ghost.set_position((0, ghost_position[1]))

    def is_pacman_dying(self) -> bool:
        """Check if the pacman collide with a ghost"""
        pacman_position = (round(self.pacman.get_position()[0]), round(
            self.pacman.get_position()[1]))
        for ghost in self.ghosts:
            ghost_position = (round(ghost.get_position()[0]), round(
                ghost.get_position()[1]))
            if pacman_position == ghost_position:
                return True
        return False
