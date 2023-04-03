from ...game.maze.components import Components
from ...game.direction import Direction
from ...game.game import Game
import numpy as np


def get_next_move(game: Game) -> Direction:
    weights = compute_weights(game)
    # compute the next move


def compute_weights(game: Game) -> np.ndarray:
    weights_maze = game.maze.get_maze()
    weights = np.zeros(weights_maze.shape)

    pacman_pos = game.pacman.get_position()
    pac_x = round(pacman_pos[0])
    pac_y = round(pacman_pos[1])

    ghost_coords = []
    for ghost in game.ghosts:
        ghost_pos = ghost.get_position()
        ghost_coords.append((round(ghost_pos[0]), round(ghost_pos[1])))

    for i in range(weights_maze.shape[0]):
        for j in range(weights_maze.shape[1]):
            cell_weight = 0

            dist_to_pacman = np.sqrt((i - pac_x)**2 + (j - pac_y)**2)

            for ghost_coord in ghost_coords:
                dist_to_ghost = np.sqrt(
                    (i - ghost_coord[0])**2 + (j - ghost_coord[1])**2)

                # If the ghost is close, add a negative weight using a Gaussian function
                if dist_to_ghost <= 5:
                    cell_weight -= gaussian(i, j,
                                            ghost_coord[0], ghost_coord[1], 1)

            if weights_maze[i, j] == Components.DOT:
                cell_weight += 1

            if weights_maze[i, j] == Components.SUPERDOT:
                cell_weight += 2

            if dist_to_pacman <= 3:
                cell_weight += gaussian(i, j, pac_x, pac_y, 1)

            weights[i, j] = cell_weight

    return weights


def gaussian(x: float, y: float, mu0: float, mu1: float, sigma: float = 1) -> float:
    left = 1 / (2 * np.pi * sigma ** 2)
    right = np.exp(-((x - mu0) ** 2 + (y - mu1) ** 2) / (2 * sigma ** 2))
    return left * right
