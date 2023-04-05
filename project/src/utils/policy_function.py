from ..game.entities.ghost.ghoststate import Ghoststate
from ..game.maze.components import Components
from ..game.game import Game
import numpy as np


def get_policy_agent_state(game: Game, radius: int = 3) -> np.ndarray:
    """return a matrix representing the game for policy_agent"""
    ghostvalue = -5
    x, y = np.array(
        np.floor(np.array(game.pacman.get_position()) + 0.5), dtype=int
    )
    # Changer default_value entre Components.WALL et Components.EMPTY
    # pour changer le comportement
    state = game.maze.get_area(
        x, y, radius, default_value=Components.EMPTY)
    state[state == Components.DOOR.value] = Components.WALL.value
    state -= 1
    for ghost in game.ghosts:
        if ghost.state not in [Ghoststate.FRIGHTENED, Ghoststate.EATEN]:
            gx, gy = np.array(
                np.floor(np.array(ghost.get_position()) + 0.5), dtype=int
            )
            if np.abs(gx - x) <= radius and np.abs(gy - y) <= radius:
                state[gy - y + radius, gx - x + radius] = ghostvalue
    return state