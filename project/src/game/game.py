from __future__ import annotations
from ..ai.neural_network.convDQNAgent import ConvDQNAgent, get_move
from ..ai.policy_agent.policy_agent import get_policy_agent_move
from .maze.random_maze_factory import RandomMazeFactory
from .entities.ghost import Blinky, Pinky, Clyde, Inky
from ..ai.policy.agent import Agent, get_policy_move
from typing import List, Tuple, Union, TYPE_CHECKING
from .entities.ghost.ghoststate import Ghoststate
from .entities.ghost.ghost import GeneralGhost
from ..ai.tree_agent.tree_agent import a_star
from .maze.components import Components
from ..graphics.sounds import Sounds
from .entities.pacman import Pacman
from .direction import Direction
from .maze.maze import Maze
from ..config import Config
from PIL import Image
import numpy as np
from math import dist
import random

if TYPE_CHECKING:
    from ..ai.neural_mask.mask import Mask


DOT_SCORE = 1
SUPER_DOT_SCORE = 2
GHOST_SCORE = 2

AREA_SIZE = 7


class Game:

    def __init__(self, config: Config, sounds: Sounds, maze: Union[Maze, None] = None) -> None:
        path = config.graphics.maze_path
        self.config = config
        self.sounds = sounds
        self.maze = Maze(filename=path) if maze is None else maze
        self.pacman = self.init_pacman()
        self.ghosts = self.init_ghosts()
        self.super_mode_timer = 0
        self.score = 0
        self.previous_score = 0
        self.switch_ghost_state_timer = self.config.game.chase_duration * 60
        self.ghost_state = Ghoststate.CHASE

        self.agent = ConvDQNAgent(config=config)
        if config.neural.play_enable:
            self.agent.load(config.neural.output_dir +
                            config.neural.weights_path)

        self.policy_agent = Agent(
            config.policy.alpha, config.policy.gamma, config.policy.n_actions)
        if config.policy.play_enable:
            self.policy_agent.policy(tf.convert_to_tensor(
                np.random.random((1, 225)), dtype=tf.float32))
            self.policy_agent.policy.load_weights(
                config.policy.output_dir + config.policy.weights_path
            )

        # algorithme a*
        self.current_dot = (-1, -1)

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
                    if self.config.user.enable_graphics and self.config.user.sound_enable:
                        self.sounds.play_sound_once("assets/music/munch_1.wav")
                    self.score += DOT_SCORE
                    self.maze.set_component(
                        Components.EMPTY, pac_pos[1], pac_pos[0])
                case Components.SUPERDOT:
                    if self.config.user.enable_graphics and self.config.user.sound_enable:
                        self.sounds.play_sound_once("assets/music/munch_2.wav")
                        self.sounds.play_sound_once(
                            "assets/music/power_pellet.wav")
                    self.get_pacman().change_state()
                    self.super_mode_timer = self.config.game.super_mode_duration * self.config.graphics.fps
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

    def get_game(self) -> Game:
        """Return the game"""
        return self

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
                if self.config.user.enable_graphics and self.config.user.sound_enable:
                    self.sounds.play_sound_once("assets/music/death_1.wav")
                self.pacman.lose_life()
                self.respawn_pacman()
                self.respawn_ghosts()

    def __is_pacman_ghost_colliding(self, ghost: GeneralGhost) -> bool:
        """Check if the pacman collide with a ghost"""
        if ghost.state == Ghoststate.EATEN:
            return False
        pacman_position = self.pacman.get_position(
        )[0], self.pacman.get_position()[1]
        ghost_position = ghost.get_position()[0], ghost.get_position()[1]
        return dist(pacman_position, ghost_position) < 1

    def __check_super_dot_timer(self) -> None:
        """Check if the super dot timer is over"""
        self.super_mode_timer = max(0, self.super_mode_timer - 1)
        if self.super_mode_timer == 0:
            for ghost in self.ghosts:
                if ghost.state == Ghoststate.EATEN:
                    ghost.set_speed(ghost.get_speed() / 4)
                    ghost.direction = Direction.NORTH
                ghost.set_state(self.ghost_state)
            self.get_pacman().change_state()

    def __switch_ghosts_state(self) -> None:
        """Switch the ghosts state"""
        if len(self.ghosts) == 0:
            return
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

    # GENETIC RELATED METHODS

    def read_movement(self) -> str:
        """Read the movement of the pacman"""
        with open(self.config.genetic.move_path, "r") as file:
            return file.read()

    def run_with_movement(self, movements: str) -> Tuple[int, int, bool, bool, int]:
        """
        Play a game with a movement file and return information about the game.
        return: Tuple[distance, score, is_dead, is_won]
        """
        self.pacman.set_movement(movements)
        if movements != "":
            self.run()

        return self.pacman.get_distance(), self.score, self.pacman.get_lives() != self.config.game.pacman_lives, self.is_game_won(), self.get_maze().get_total_remain_dots()

    def run(self) -> None:
        """Play a game"""
        while self.pacman.direction != Direction.NONE:
            self.update()
            if self.pacman.get_lives() != self.config.game.pacman_lives:
                break

    # NEURAL NETWORK RELATED METHODS

    def get_conv_state(self, full_size: bool = False, size: int = 7):
        """Return the state of the game for the convolutional neural network"""
        if full_size:
            return np.array(self.get_image())
        else:
            return np.array(self.get_crop_image2(size))

    def get_image(self):
        """Return the image of the game"""
        env = np.zeros(
            (self.maze.get_height(), self.maze.get_width(), 3), dtype=np.uint8)
        # Set the path to white
        env[self.maze.get_wall_matrix() == 0] = (255, 255, 255)
        # Set the dots to yellow
        env[self.maze.get_dot_matrix() == 1] = (255, 255, 0)
        # Set the super dots to blue
        env[self.maze.get_superdot_matrix() == 1] = (0, 0, 255)
        # Set the pacman to red
        pac_x, pac_y = self.pacman.get_position()
        env[round(pac_y), round(pac_x)] = (255, 0, 0)
        # Set the ghosts to green
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            env[round(ghost_y), round(ghost_x)] = (0, 255, 0)

        return Image.fromarray(env, 'RGB')

    def get_crop_image2(self, size: int):
        """Return the image of the game with a size centered on the pacman"""
        length = size * 2 + 1
        env = np.zeros((length, length, 5), dtype=np.uint8)
        pac_x, pac_y = self.pacman.get_position()
        pac_x = round(pac_x)
        pac_y = round(pac_y)
        # Set the path 
        env[self.maze.get_wall_size_matrix(
            pac_x, pac_y, size) == 0] = [1, 0, 0, 0, 0]
        # Set the dots 
        env[self.maze.get_dot_size_matrix(
            pac_x, pac_y, size) == 1] = [0, 1, 0, 0, 0]
        # Set the super dots 
        env[self.maze.get_superdot_size_matrix(
            pac_x, pac_y, size) == 1] = [0, 1, 1, 0, 0]
        # Set the pacman 
        env[size, size] = [0, 0, 0, 1, 0]
        # Set if pacman is super
        if self.super_mode_timer > 0:
            env[size, size] = [0, 0, 1, 1, 0]
        # Set the ghosts 
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            ghost_x = round(ghost_x)
            ghost_y = round(ghost_y)
            if abs(ghost_x - pac_x) <= size and abs(ghost_y - pac_y) <= size:
                env[size + ghost_y - pac_y, size +
                    ghost_x - pac_x] = [0, 0, 0, 0, 1]
                # Set the ghost direction
                env[size + ghost_y - pac_y, size +
                    ghost_x - pac_x][ghost.direction.value] = 1
        return np.array(env)
    
    def get_state(self) -> np.ndarray:
        """Return various information about the game
        Position of Pacman,
        direction of pacman,
        position, direction and distance of the four ghosts,
        nb of remaining dots,
        superdot mode timer,
        Total parameters : 2 + 4 * 4 + 2 = 18
        """
        state = []
        pac_x, pac_y = self.pacman.get_position()
        state.append(self.pacman.get_direction().value)
        state.append(pac_x)
        state.append(pac_y)
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            state.append(ghost_x)
            state.append(ghost_y)
            state.append(ghost.get_direction().value)
            state.append(dist((pac_x, pac_y), (ghost_x, ghost_y)))
        state.append(self.maze.remain_dots)
        state.append(self.super_mode_timer)
        return np.array(state, dtype=np.float32)


    def get_reward(self) -> int:
        """Return the reward of the game
        A good reward is between -1 and 1"""
        # Initialisation de certaines variables
        pac_x, pac_y = self.pacman.get_position()
        distance = 0
        min_distance = np.inf
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            pacman_dist_to_ghost = dist((pac_x, pac_y), (ghost_x, ghost_y))
            distance += pacman_dist_to_ghost
            if pacman_dist_to_ghost < min_distance:
                min_distance = pacman_dist_to_ghost
        # On veut induire un comportement à pacman via la récompense :
        # Si Pacman meurt
        if self.pacman.get_lives() != self.config.game.pacman_lives:
            return -1
        # Si fantome trop proche
        if min_distance < 3:
            return -0.4
        # Si score augmente
        if self.score - self.previous_score > 0:
            return 1
        # On veut que pacman s'éloigne des fantômes
        return distance / 500

    def step(self, action: Direction):
        """Update the game with an action and return the next state, the reward and if the game is over"""
        self.previous_score = self.score
        self.pacman.set_next_direction(action)
        for _ in range(self.config.graphics.fps // 4):
            self.update()
        next_state = self.get_conv_state()
        reward = self.get_reward()
        done = self.pacman.get_lives() != self.config.game.pacman_lives or self.is_game_won()
        return next_state, reward, done

    def play_neural_move(self) -> None:
        """Play a move with the neural network"""
        move = get_move(self.get_game(), self.agent)
        self.pacman.set_next_direction(move)

    def play_policy_move(self) -> None:
        """Play a move with the policy gradient"""
        move = get_policy_move(self.get_game(), self.policy_agent)
        self.pacman.set_next_direction(move)

    def get_policy_state(self) -> np.ndarray:
        """Return the state of the game for the policy gradient"""
        image = self.get_crop_image(7).convert('L')
        normalized_image = np.array(image) / 255
        return normalized_image.flatten()

    def get_policy_reward(self) -> int:
        """Return the reward of the game for the policy gradient"""
        return self.score - self.previous_score

    def policy_step(self, action: int):
        """Update the game with an action and return the next state, the reward and if the game is over"""
        self.previous_score = self.score
        self.pacman.set_next_direction(Direction(action))
        for _ in range(20):
            self.update()
        if self.score == self.previous_score:
            self.score += 0.1
        next_state = self.get_policy_state()
        reward = self.get_policy_reward()
        done = self.pacman.get_lives() != self.config.game.pacman_lives or self.is_game_won()
        if done:
            reward = 10 if self.is_game_won() else -5
        return next_state, reward, done

    # MASK RELATED METHODS

    def run_with_mask(self, mask: Mask) -> Tuple[int, int, bool, bool]:
        """Play a game with a mask"""
        while not self.is_game_over():
            state = self.get_mask_state()
            action = mask.get_move(state)
            self.pacman.set_next_direction(action)
            for _ in range(20):
                self.update()

        return self.pacman.get_distance(), self.score, self.pacman.get_lives() != self.config.game.pacman_lives, self.is_game_won()

    def get_mask_state(self) -> np.ndarray:
        """Return the state of the game with a mask"""
        length = self.config.neural_mask.mask_size
        env = np.zeros((length, length), dtype=np.uint8)
        pac_x, pac_y = self.pacman.get_position()
        pac_x = round(pac_x)
        pac_y = round(pac_y)
        # Set the path
        env[self.maze.get_wall_size_matrix(
            pac_x, pac_y, length // 2) == 0] = 1
        # Set the dots
        env[self.maze.get_dot_size_matrix(
            pac_x, pac_y, length // 2) == 1] = 2
        # Set the super dots
        env[self.maze.get_superdot_size_matrix(
            pac_x, pac_y, length // 2) == 1] = 3
        # Set the ghosts
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            ghost_x = round(ghost_x)
            ghost_y = round(ghost_y)
            if abs(ghost_x - pac_x) <= length // 2 and abs(ghost_y - pac_y) <= length // 2:
                env[length // 2 + ghost_y - pac_y, length // 2 +
                    ghost_x - pac_x] = 4

        return env

    def get_policy_agent_state(self, radius: int = 3) -> np.ndarray:
        """return a matrix representing the game for policy_agent"""
        ghostvalue = 5
        x, y = np.array(
            np.floor(np.array(self.pacman.get_position()) + 0.5), dtype=int)
        # Changer default_value entre Components.WALL et Components.EMPTY
        # pour changer le comportement
        state = self.maze.get_area(
            x, y, radius, default_value=Components.EMPTY) - 1
        for i in self.ghosts:
            if i.state not in [Ghoststate.FRIGHTENED, Ghoststate.EATEN]:
                gx, gy = np.array(
                    np.floor(np.array(i.get_position()) + 0.5), dtype=int)
                if np.abs(gx - x) <= radius and np.abs(gy - y) <= radius:
                    state[gy - y + radius, gx - x + radius] = -ghostvalue
        return state

    def play_policy_agent_move(self) -> None:
        """Play a move with the policy agent"""
        move = get_policy_agent_move(self.get_policy_agent_state())
        self.pacman.set_next_direction(move)

    # A* methods
    def get_neighbours(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Return the neighbours of a position"""
        neighbours = self.maze.get_area(
            pos[0], pos[1], 1, default_value=Components.EMPTY)
        for ghost in self.ghosts:
            if ghost.state not in [Ghoststate.FRIGHTENED, Ghoststate.EATEN]:
                ghost_x, ghost_y = ghost.get_position()
                ghost_x = round(ghost_x)
                ghost_y = round(ghost_y)
                if abs(ghost_x - pos[0]) <= 1 and abs(ghost_y - pos[1]) <= 1:
                    neighbours[ghost_y - pos[1] + 1, ghost_x - pos[0] + 1] = 0
        four_neighbours = []
        if neighbours[0, 1] != 0:
            four_neighbours.append((pos[0], pos[1] - 1))
        if neighbours[2, 1] != 0:
            four_neighbours.append((pos[0], pos[1] + 1))
        if neighbours[1, 0] != 0:
            four_neighbours.append((pos[0] - 1, pos[1]))
        if neighbours[1, 2] != 0:
            four_neighbours.append((pos[0] + 1, pos[1]))
        return four_neighbours

    def get_move_by_pos(self, pos: Tuple[int, int]) -> Direction:
        """Return the direction to go to a position"""
        if pos[0] < self.pacman.get_position()[0]:
            return Direction.WEST
        elif pos[0] > self.pacman.get_position()[0]:
            return Direction.EAST
        elif pos[1] < self.pacman.get_position()[1]:
            return Direction.NORTH
        else:
            return Direction.SOUTH
        

    def get_nearest_point(self, pac_x: int, pac_y: int) -> Tuple[int, int]:
        """Return the nearest dot if there is no ghost around in a radius of 3 else return a random dot"""
        dots = self.maze.get_dot_position()
        if len(dots) == 0:
            return (-1, -1)
        dots.sort(key=lambda x: np.sqrt((x[0] - pac_x) ** 2 + (x[1] - pac_y) ** 2))
        for dot in dots:
            distances = [np.sqrt((dot[0] - ghost.get_position()[0]) ** 2 + (dot[1] - ghost.get_position()[1]) ** 2) for ghost in self.ghosts]
            if min(distances) > 3:
                return dot
        return random.choice(dots)

    def choose_point(self, pac_x: int, pac_y: int) -> None:
        self.current_dot = self.get_nearest_point(pac_x, pac_y)

    def play_a_star_move(self) -> None:
        pac_x, pac_y = self.pacman.get_position()
        pac_x, pac_y = round(pac_x), round(pac_y)
        self.choose_point(pac_x, pac_y)
        new_pos = a_star((pac_x, pac_y), self.current_dot, self)
        if len(new_pos) <= 1:
            return
        move = self.get_move_by_pos(new_pos[1])
        self.pacman.set_next_direction(move)
