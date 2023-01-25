from ...maze.components import Components
from ...direction import Direction
from ..entities import Entities
from ...maze.maze import Maze
from .ghost import GeneralGhost
from .ghoststate import Ghoststate
from typing import Tuple
import numpy as np

class Pinky(GeneralGhost):

    PACMAN_OFFSET = 47

    def __init__(self, maze: Maze, pac: Entities, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (5, 5), scatter_pos: Tuple[int, int] = (8, 8)) -> None:
        super().__init__(maze, pac, speed, direction, coordinate, scatter_pos)

    def get_chase_direction(self) -> Direction:
        '''Return the direction of the ghost in chase mode.'''
        if self.inside_ghostbox:
            return self.get_outside_ghostbox_direction()
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, (lambda x, y: (x[0] + self.PACMAN_OFFSET * y[0], x[1] + self.PACMAN_OFFSET * y[1])) (pac_pos, self.pac.get_direction().to_vector()))
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction