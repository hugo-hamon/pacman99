from ...maze.components import Components
from ...direction import Direction
from ..entities import Entities
from ...maze.maze import Maze
from typing import Tuple
from math import sqrt
import numpy as np
import operator


class Chaser(Entities):

    def __init__(self, maze: Maze, pac: Entities, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (5, 5)) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.pac = pac

    def __get_possible_direction(self):
        possible_direction = []
        position = self.get_position()
        area = self.maze.get_neighbors(int(position[0]), int(position[1]))
        for d in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            checkw = tuple(map(operator.add, d.to_vector(), (1, 1)))
            if area[checkw[1]][checkw[0]] != Components.WALL:
                possible_direction.append(d)
        return possible_direction

    def distance_euclidienne(self, ghost_pos, pac_pos):
        return sqrt((ghost_pos[0] - pac_pos[0])**2 + (ghost_pos[1] - pac_pos[1])**2)

    def _get_next_direction(self) -> Direction:
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        directions = self.__get_possible_direction()
        for direction in self.__get_possible_direction():
            if direction == self.direction.opposite():
                continue
            ghost_pos = self.get_position()
            dir_ghost_pos = round(
                ghost_pos[0] + direction.to_vector()[0]), round(ghost_pos[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, pac_pos)
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction
