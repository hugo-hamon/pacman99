from ...direction import Direction
from ..entities import Entities
from ...maze.maze import Maze
from .ghost import GeneralGhost
from .ghoststate import Ghoststate
from typing import Tuple
import numpy as np

class Inky(GeneralGhost):

    PACMAN_OFFSET = 2

    def __init__(self, maze: Maze, pac: Entities, blinky: Entities, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (5, 5), scatter_pos: Tuple[int, int] = (8, 8)) -> None:
        super().__init__(maze, pac, speed, direction, coordinate, scatter_pos)
        self.blinky = blinky

    def get_chase_direction(self) -> Direction:
        '''Return the direction of the ghost in chase mode.'''
        if self.inside_ghostbox:
            return self.get_outside_ghostbox_direction()
        position = self.get_position()
        blinky_pos = self.blinky.get_position()
        pac_pos = (lambda x, y: (x[0] + self.PACMAN_OFFSET * y[0], x[1] + self.PACMAN_OFFSET * y[1])) (self.pac.get_position(), self.pac.get_direction().to_vector())
        target_pos = [2*pac_pos[0] - blinky_pos[0],2*pac_pos[1] - blinky_pos[1]]
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if self.get_direction() != Direction.NONE and direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, target_pos)
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction
