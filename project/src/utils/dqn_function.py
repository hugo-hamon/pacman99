from ..game.game import Game
from ..game.direction import Direction
from ..ai.policy.policy_agent import get_filters_values
from math import dist
import numpy as np

def get_reward(game: Game, previous_score: float, wrong_direction) -> float:
        """Return the reward of the game
        A good reward is between -1 and 1"""
        # Initialisation de certaines variables
        pac_x, pac_y = game.pacman.get_position()
        distance = 0
        min_distance = np.inf
        for ghost in game.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            pacman_dist_to_ghost = dist((pac_x, pac_y), (ghost_x, ghost_y))
            distance += pacman_dist_to_ghost
            if pacman_dist_to_ghost < min_distance:
                min_distance = pacman_dist_to_ghost
        # On veut induire un comportement à pacman via la récompense :
        # Si Pacman meurt
        if game.pacman.get_lives() == 0 or game.pacman.get_direction() == Direction.NONE:
            return -1.0
        if wrong_direction:
            return -0.1
        # Si fantome trop proche
        if min_distance < 3:
            if game.super_mode_timer > 0:
                return 0.2
            return -0.4
        # Si score augmente
        return 0.7 if game.score - previous_score > 0 else 0.15

def get_conv_state(game: Game, size: int = 7):
        """Return the image of the game with a size centered on the pacman"""
        length = size * 2 + 1
        env = np.zeros((length, length, 5), dtype=np.uint8)
        pac_x, pac_y = game.pacman.get_position()
        pac_x = round(pac_x)
        pac_y = round(pac_y)
        # Set the path 
        env[game.maze.get_wall_size_matrix(
            pac_x, pac_y, size) == 0] = [1, 0, 0, 0, 0]
        # Set the dots 
        env[game.maze.get_dot_size_matrix(
            pac_x, pac_y, size) == 1] = [0, 1, 0, 0, 0]
        # Set the super dots 
        env[game.maze.get_superdot_size_matrix(
            pac_x, pac_y, size) == 1] = [0, 1, 1, 0, 0]
        # Set the pacman 
        env[size, size] = [0, 0, 0, 1, 0]
        # Set if pacman is super
        if game.super_mode_timer > 0:
            env[size, size] = [0, 0, 1, 1, 0]
        # Set the ghosts 
        for ghost in game.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            ghost_x = round(ghost_x)
            ghost_y = round(ghost_y)
            if abs(ghost_x - pac_x) <= size and abs(ghost_y - pac_y) <= size:
                env[size + ghost_y - pac_y, size +
                    ghost_x - pac_x] = [0, 0, 0, 0, 1]
                # Set the ghost direction
                '''env[size + ghost_y - pac_y, size +
                    ghost_x - pac_x][ghost.direction.value] = 1'''
        return np.array(env)

def step(game: Game, action):
        """Update the game with an action and return the next state, the reward and if the game is over"""
        previous_score = game.score
        wrong_direction = game.pacman.is_wall(action)
        game.step(game.config.graphics.fps // 4)
        next_state = get_state(game)
        reward = get_reward(game, previous_score, wrong_direction)
        done = game.pacman.get_lives() == 0 or game.is_game_won() or game.pacman.get_direction() == Direction.NONE
        return next_state, reward, done

def get_state(game : Game) -> np.ndarray:
        """Return various information about the game
        Position of Pacman,
        direction of pacman,
        position, direction and distance of the four ghosts,
        nb of remaining dots,
        superdot mode timer,
        Total parameters : 2 + 4 * 4 + 2 + 4 = 18
        """
        state = []
        pac_x, pac_y = game.pacman.get_position()
        state.append(game.pacman.get_direction().value)
        state.append(pac_x)
        state.append(pac_y)
        for ghost in game.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            state.append(ghost_x)
            state.append(ghost_y)
            state.append(ghost.get_direction().value)
            state.append(dist((pac_x, pac_y), (ghost_x, ghost_y)))
        state.append(game.maze.remain_dots)
        state.append(game.super_mode_timer)
        neighbors = game.maze.get_neighbors(round(pac_x), round(pac_y))
        for dir in [Direction.NORTH.to_vector(), Direction.SOUTH.to_vector(), Direction.EAST.to_vector(), Direction.WEST.to_vector()]:
            state.append(neighbors[dir[0]][dir[1]].value)
        policy = get_filters_values(game)
        for filter in policy:
            state.append(filter)
        return np.array(state)