from ...maze.components import Components
from ...direction import Direction
from ..entities import Entities
from ...maze.maze import Maze
from typing import Tuple
import operator

class chaser(Entities):
    
    def __init__(self, maze: Maze, pac: Entities, speed: float = 0, direction: Direction = Direction.WEST, 
                 coordinate: Tuple[float, float] = (5, 5)) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.pac = pac
        
    def __get_possible_direction(self):
        possible_direction = []
        position = self.get_position()
        area = self.maze.get_neighbors(int(position[0]), int(position[1]))
        for n in range(len(Direction)):
            checkw = tuple(map(operator.add, Direction[n].to_vector(), (1, 1)))
            if area[checkw[1]][checkw[0]] != Components.WALL:
                possible_direction.append(Direction[n])
        return possible_direction
    
    def distance_euclidienne(ghost_pos, pac_pos):
        return (ghost_pos[0] - pac_pos[0])**2 + (ghost_pos[1] - pac_pos[1])**2
    
    def _get_next_direction(self) -> Direction:
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = 0
        directions = self.__get_possible_direction()
        if len(directions) == 2:
            return directions[0] if directions[0] == self.direction.opposite() else directions[1] 
        for direction in self.__get_possible_direction():
            ghost_pos = tuple(map(operator.add, direction.to_vector(), (1, 1)))
            dir_dist = self.distance_euclidienne(ghost_pos, pac_pos)
            if dir_dist < dist or prefered_direction == Direction.NONE:
                    prefered_direction = direction
                    dist = dir_dist
        return prefered_direction