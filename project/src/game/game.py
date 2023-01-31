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
import math

DOT_SCORE = 100
SUPER_DOT_SCORE = 500
GHOST_SCORE = 200


class Game:

    def __init__(self, config: Config) -> None:
        path = config.graphics.maze_path
        if config.user.enable_random_maze:
            RandomMazeFactory(config).create()
            path = config.maze.random_maze_path
        self.config = config
        self.maze = Maze(filename=path)
        self.pacman = self.init_pacman()
        self.ghosts = self.init_ghosts()
        self.super_mode_timer = 0
        self.score = 0
        self.switch_ghost_state_timer = self.config.game.chase_duration * 60
        self.ghost_state = Ghoststate.CHASE

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
                                             Direction.NORTH, (self.maze.get_width(
                                             ) / 2, self.maze.get_height() / 2),
                                             (self.maze.get_width(), 0))]
        ghosts.append(Pinky(self.maze, self.pacman, self.config.game.game_speed * 0.5,
                      Direction.NORTH, (self.maze.get_width() / 2 + 1, self.maze.get_height() / 2), (self.maze.get_width(), self.maze.get_height())))
        ghosts.append(Clyde(self.maze, self.pacman, self.config.game.game_speed * 0.6,
                      Direction.NORTH, (self.maze.get_width() / 2 - 1, self.maze.get_height() / 2), (0, self.maze.get_height())))
        ghosts.append(Inky(self.maze, self.pacman, self.config.game.game_speed * 0.6,
                      Direction.NORTH, (self.maze.get_width() / 2, self.maze.get_height() / 2 - 1), (0, 0)))
        return ghosts

    def update(self) -> None:
        """Update the game"""
        self.pacman.move(60)
        for ghost in self.ghosts:
            ghost.move(60)
            self.__manage_collision(ghost)
        self.__check_super_dot_timer()
        self.__switch_ghosts_state()
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
            ghost.state = Ghoststate.EXITTING
            ghost.inside_ghostbox = True
            ghost.set_speed(ghost.speed_at_init)
            ghost.set_position((self.maze.get_width() // 2,
                               self.maze.get_height() // 2))

    def eat_dot(self) -> None:
        pac_pos = (round(self.pacman.get_position()[0]), round(
            self.pacman.get_position()[1]))
        if pac_pos[0] >= 0 and pac_pos[0] < self.maze.get_width() and \
                pac_pos[1] >= 0 and pac_pos[1] < self.maze.get_height():
            match self.maze.get_cell(pac_pos[0], pac_pos[1]):
                case Components.DOT:
                    self.score += DOT_SCORE
                    self.maze.set_component(
                        Components.EMPTY, pac_pos[1], pac_pos[0])
                case Components.SUPERDOT:
                    self.get_pacman().change_state()
                    self.super_mode_timer = self.config.game.super_mode_duration * self.config.graphics.fps / self.config.game.game_speed
                    for ghost in self.ghosts:
                        if ghost.state != Ghoststate.EATEN:
                            ghost.set_state(Ghoststate.FRIGHTENED)
                    self.score += SUPER_DOT_SCORE
                    self.maze.set_component(
                        Components.EMPTY, pac_pos[1], pac_pos[0])

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
                self.score += GHOST_SCORE
            else:
                self.pacman.lose_life()
                self.respawn_pacman()
                self.respawn_ghosts()

    def __is_pacman_ghost_colliding(self, ghost: GeneralGhost) -> bool:
        """Check if the pacman collide with a ghost"""
        if ghost.state == Ghoststate.EATEN:
            return False
        pacman_position = self.pacman.get_position()
        ghost_position = ghost.get_position()
        return math.sqrt((pacman_position[0] - ghost_position[0])**2 
        + (pacman_position[1] - ghost_position[1])**2) < 0.75

    def __check_super_dot_timer(self) -> None:
        """Check if the super dot timer is over"""
        self.super_mode_timer -= 1
        if self.super_mode_timer == 0:
            for ghost in self.ghosts:
                if ghost.state == Ghoststate.EATEN:
                    ghost.set_speed(ghost.get_speed() / 4)
                    ghost.direction = Direction.NORTH
                ghost.set_state(self.ghost_state)
            self.get_pacman().change_state()

    def __switch_ghosts_state(self) -> None:
        """Switch the ghosts state"""
        self.switch_ghost_state_timer -= 1
        if self.switch_ghost_state_timer == 0:
            if self.ghost_state == Ghoststate.CHASE:
                self.switch_ghost_state_timer = self.config.game.scatter_duration * \
                    self.config.graphics.fps
                self.ghost_state = Ghoststate.SCATTER
                if self.ghosts[0].state == Ghoststate.CHASE:
                    for ghost in self.ghosts:
                        ghost.set_state(Ghoststate.SCATTER)
            else:
                self.switch_ghost_state_timer = self.config.game.chase_duration * \
                    self.config.graphics.fps
                self.ghost_state = Ghoststate.CHASE
                if self.ghosts[0].state == Ghoststate.SCATTER:
                    for ghost in self.ghosts:
                        ghost.set_state(Ghoststate.CHASE)

    def read_movement(self) -> str:
        """Read the movement of the pacman"""
        with open(self.config.genetic.move_path, "r") as file:
            return file.read()

    def run_with_movement(self, movements: str) -> Tuple[int, int, bool, bool]:
        """
        Play a game with a movement file and return information about the game.
        return: Tuple[distance, score, is_dead, is_won]
        """
        self.pacman.set_movement(movements)
        if movements != "":
            self.run()

        return self.pacman.get_distance(), self.score, self.pacman.get_lives() != self.config.game.pacman_lives, self.is_game_won()

    def run(self) -> None:
        """Play a game"""
        while self.pacman.direction != Direction.NONE:
            self.update()
            if self.pacman.get_lives() != self.config.game.pacman_lives:
                break
