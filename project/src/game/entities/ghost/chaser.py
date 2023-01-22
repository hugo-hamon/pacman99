from ...maze.components import Components
from ...direction import Direction
from ..entities import Entities
from .ghost import GeneralGhost
from ...maze.maze import Maze
from typing import Tuple
import numpy as np

class Chaser(GeneralGhost):

    def __init__(self, maze: Maze, pac: Entities, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (5, 5)) -> None:
        super().__init__(maze, pac, speed, direction, coordinate)

    def _get_next_direction(self) -> Direction:
        '''Return and set the next direction of the ghost.'''
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        directions = self.get_possible_direction()
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, pac_pos)
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction
