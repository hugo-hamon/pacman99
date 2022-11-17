from ..game.maze.components import Components
from ..game.maze.maze import Maze
import numpy as np

N = 1
E = 2
S = 4
W = 8

directions = {
    "wall_0": [0, 0, 0, 0],
    "wall_1": [N, 0, 0, 0],
    "wall_2": [0, E, 0, 0],
    "wall_3": [N, E, 0, 0],
    "wall_4": [0, 0, S, 0],
    "wall_5": [N, 0, S, 0],
    "wall_6": [0, E, S, 0],
    "wall_7": [N, E, S, 0],
    "wall_8": [0, 0, 0, W],
    "wall_9": [N, 0, 0, W],
    "wall_10": [0, E, 0, W],
    "wall_11": [N, E, 0, W],
    "wall_12": [0, 0, S, W],
    "wall_13": [N, 0, S, W],
    "wall_14": [0, E, S, W],
    "wall_15": [N, E, S, W],
}

def get_wall_name(x: int, y: int, maze: Maze) -> str:
    cell = maze.get_cell(x, y)
    neighbors = maze.get_neighbors(x, y)
    neighbors = np.array([neighbors[0, 1], neighbors[1, 2], neighbors[2, 1], neighbors[1, 0]])
    direction = get_direction_from_neighbors(neighbors)
    print(direction)
    print([k for k, v in directions.items() if np.array_equal(v, direction)][0])
    return [k for k, v in directions.items() if np.array_equal(v, direction)][0]
    

def get_direction_from_neighbors(neighbors: np.ndarray) -> np.ndarray:
    direction = np.zeros(4, dtype=int)
    for i in range(4):
        if neighbors[i] != Components.WALL:
            direction[i] = 2**i 
    return direction