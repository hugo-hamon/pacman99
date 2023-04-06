from ...utils.policy_function import get_policy_agent_state
from ...game.direction import Direction
from ...game.game import Game
from typing import List
import numpy as np

DIRECTION = [Direction.NORTH, Direction.EAST, Direction.WEST, Direction.SOUTH]

class PolicyAgent:
    def __init__(self, vector: List[float]) -> None:
        self.vector = vector
        self.filters = self.init_filters()

    def init_filters(self) -> List[np.ndarray]:
        """Initialize the filters"""
        a, b, c, d, e, f = self.vector
        basic_filter = np.array(
            [[a, b, c, d, c, b, a],
             [b, c, d, e, d, c, b],
             [c, d, e, f, e, d, c],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0]]
        )
        return [
            basic_filter, np.rot90(basic_filter, 3),
            np.rot90(basic_filter, 1), np.rot90(basic_filter, 2)
        ]

    def get_policy_agent_move(self, game: Game) -> Direction:
        """Return the best move for the agent given the state of the maze"""
        state = get_policy_agent_state(game)
        values = [np.sum(state * self.filters[i]) for i in range(4)]
        return DIRECTION[np.argmax(values)]
    
    def get_filters_values(self, game : Game) -> np.ndarray:
        """Return the values of the filters applied to the state"""
        state = get_policy_agent_state(game)
        values = [np.sum(state * self.filters[i]) for i in range(4)]
        return values