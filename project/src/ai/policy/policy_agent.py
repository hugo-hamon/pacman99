from ...utils.policy_function import get_policy_agent_state
from ...game.direction import Direction
from ...game.game import Game
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


def get_policy_agent_move(game: Game) -> Direction:
    """Return the best move for the agent given the state of the maze"""
    direction = [Direction.NORTH, Direction.EAST,
                 Direction.WEST, Direction.SOUTH]
    filters = [FILTER_NORTH, FILTER_EAST, FILTER_WEST, FILTER_SOUTH]
    state = get_policy_agent_state(game)
    values = [np.sum(state * filters[i]) for i in range(4)]
    return direction[np.argmax(values)]
