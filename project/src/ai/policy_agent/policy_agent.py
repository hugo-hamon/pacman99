from ...game.direction import Direction
from ...game.maze import maze
import numpy as np

BASIC_FILTER = np.array(
    [[1, 2, 3, 4, 3, 2, 1],
     [2, 3, 4, 5, 4, 3, 2],
     [3, 4, 5, 20, 5, 4, 3],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0]]
)

FILTER_NORTH = BASIC_FILTER

FILTER_EAST = np.rot90(BASIC_FILTER, 3)

FILTER_WEST = np.rot90(BASIC_FILTER, 1)

FILTER_SOUTH = np.rot90(BASIC_FILTER, 2)


def get_policy_agent_move(state: np.ndarray) -> Direction:
    """Return the best move for the agent given the state of the maze"""
    direction = [Direction.NORTH, Direction.EAST,
                 Direction.WEST, Direction.SOUTH]
    filters = [FILTER_NORTH, FILTER_EAST, FILTER_WEST, FILTER_SOUTH]
    values = [np.sum(state * filters[i]) for i in range(4)]
    return direction[np.argmax(values)]
