from .maze.random_maze_factory import RandomMazeFactory
from .entities.ghost import Blinky, Pinky, Clyde, Inky
from .entities.ghost.ghoststate import Ghoststate
from .entities.ghost.ghost import GeneralGhost
from .maze.components import Components
from ..graphics.sounds import Sounds
from .entities.pacman import Pacman
from .direction import Direction
from typing import List, Tuple
from .maze.maze import Maze
from ..config import Config


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
        self.super_mode_timer = 0
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
        self.pacman.reset()
        self.respawn_pacman()
        for ghost in self.ghosts:
            ghost.reset()
        self.maze.reset()
        self.score = 0
        self.super_mode_timer = 0

    def init_pacman(self) -> Pacman:
        """Initialize the pacman and return it"""
        movements = self.read_movement() if self.config.genetic.genetic_enable else ""
        pacman = Pacman(
            self.maze, self.config.game.game_speed, Direction.WEST, (0, 0),
            self.config.game.pacman_lives, movements
        )
        pacman.set_position(self.maze.get_pacman_start())
        return pacman

    def init_ghosts(self) -> List[GeneralGhost]:
        """Initialize the ghosts and return them"""
        ghosts: List[GeneralGhost] = [Blinky(self.maze, self.pacman, self.config.game.game_speed * 0.7,
                                             Direction.NORTH, (self.maze.get_width() / 2, self.maze.get_height() / 2))]
        ghosts.append(Pinky(self.maze, self.pacman, self.config.game.game_speed * 0.9,
                      Direction.NORTH, (self.maze.get_width() / 2 + 1, self.maze.get_height() / 2)))
        ghosts.append(Clyde(self.maze, self.pacman, self.config.game.game_speed * 0.8,
                      Direction.NORTH, (self.maze.get_width() / 2 - 1, self.maze.get_height() / 2)))
        ghosts.append(Inky(self.maze, self.pacman, self.config.game.game_speed * 0.9,
                      Direction.NORTH, (self.maze.get_width() / 2, self.maze.get_height() / 2 - 1)))
        return ghosts

    def update(self) -> None:
        """Update the game"""
        self.pacman.move(60)
        for ghost in self.ghosts:
            ghost.move(60)
            self.__manage_collision(ghost)
        self.__check_super_dot_timer()
        self.eat_dot()
        self.pacman_tp()
        self.ghosts_tp()
        if self.pacman.get_lives() == 0:
            print("You lost")
        if self.is_game_won():
            print("You won")

    def respawn_pacman(self):
        self.pacman.set_position(self.maze.get_pacman_start())
        self.pacman.direction = Direction.WEST

    def respawn_ghosts(self):
        for ghost in self.ghosts:
            ghost.direction = Direction.NORTH
            ghost.set_position((self.maze.get_width() // 2,
                               self.maze.get_height() // 2))

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
                self.get_pacman().change_state()
                self.super_mode_timer = self.config.game.super_mode_duration * 60
                for ghost in self.ghosts:
                    if ghost.state == Ghoststate.CHASE or ghost.state == Ghoststate.SCATTER:
                        ghost.set_state(Ghoststate.FRIGHTENED)
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

    def __manage_collision(self, ghost: GeneralGhost) -> None:
        """Manage the collision between pacman and ghost"""
        if self.__is_pacman_ghost_colliding(ghost):
            if ghost.state in [Ghoststate.FRIGHTENED, Ghoststate.EATEN]:
                ghost.set_state(Ghoststate.EATEN)
                ghost.set_speed(ghost.get_speed() * 4)
                self.score += 200
            else:
                if self.config.user.enable_graphics and self.config.user.sound_enable:
                    self.sounds.play_sound_once("assets/music/death_1.wav")
                self.pacman.lose_life()
                self.respawn_pacman()
                self.respawn_ghosts()

    def __is_pacman_ghost_colliding(self, ghost: GeneralGhost) -> bool:
        """Check if the pacman collide with a ghost"""
        if ghost.state == Ghoststate.EATEN:
            return False
        pacman_position = (round(self.pacman.get_position()[0]), round(
            self.pacman.get_position()[1]))
        ghost_position = (round(ghost.get_position()[0]), round(
            ghost.get_position()[1]))
        return pacman_position == ghost_position

    def __check_super_dot_timer(self) -> None:
        """Check if the super dot timer is over"""
        self.super_mode_timer -= 1
        if self.super_mode_timer == 0:
            for ghost in self.ghosts:
                if ghost.state == Ghoststate.EATEN:
                    ghost.set_speed(ghost.get_speed() / 4)
                    ghost.direction = Direction.NORTH
                ghost.set_state(Ghoststate.CHASE)
            self.get_pacman().change_state()

    def read_movement(self) -> str:
        """Read the movement of the pacman"""
        with open(self.config.genetic.move_path, "r") as file:
            return file.read()

    def run_with_movement(self, movements: str) -> Tuple[int, int, bool, bool]:
        """
        Play a game with a movement file and return information about the game.
        return: Tuple[distance, score, is_dead, is_won]
        """
        self.reset()
        self.pacman.set_movement(movements)
        self.run(movements)
        return self.pacman.get_distance(), self.score, self.pacman.get_lives() != self.config.game.pacman_lives, self.is_game_won()

    def run(self, movements: str) -> None:
        """Play a game"""
        while self.pacman.direction != Direction.NONE:
            self.update()
            if self.pacman.get_lives() != self.config.game.pacman_lives:
                break
        