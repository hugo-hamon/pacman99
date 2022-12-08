from abc import ABC, abstractmethod
from ..direction import Direction
from ..maze import Maze
from typing import Tuple

UNITSPERCELL = 1000
class Entities(ABC):
    
    def __init__(self, maze : Maze, speed : float = 0, direction : Direction = Direction.WEST,
                 coordinate : Tuple(float, float) = (0,0)) -> None:
        super().__init__()
        self.x, self.y = (int) (coordinate[0] * UNITSPERCELL), 
        (int) (coordinate[1] * UNITSPERCELL)
        self.direction = direction
        self.next_direction : Direction = None
        self.speed = (int) (speed * UNITSPERCELL)
        self.movedistance = 0
        self.maze = maze

    # REQUESTS
    def get_speed(self) -> int:
        return self.speed / UNITSPERCELL

    def get_position(self) -> Tuple[int, int]:
        return self.x / UNITSPERCELL, self.y / UNITSPERCELL

    def get_direction(self) -> Direction:
        return self.direction

    # COMMANDS
    def set_speed(self, speed: int) -> None:
        self.speed = speed * UNITSPERCELL

    def move(self, timestep : int) -> None:
        self.movedistance += (int) (self.speed / timestep) * UNITSPERCELL
        self.__moveToNextStep()
        while self.movedistance > 0 and self.direction is not None:
            self.direction = self.__get_next_direction()
            self.__moveToNextStep()
        self.movedistance = 0
            
    def __moveToNextStep(self) -> None:
        xd, xy = self.direction.to_vector() if self.direction is not None else 0,0
        distanceToMove = min(self.movedistance, (xd * self.x + xy * self.y) % UNITSPERCELL)
        self.movedistance -= distanceToMove
        self.x += distanceToMove * xd
        self.y += distanceToMove * xy
        
    def __get_next_direction(self) -> None:
        position = self.get_position()
        if self.maze.is_intersection(position[0],position[1]):
            area = self.maze.get_neighbors(position[0],position[1])
            check = [1,1] + self.next_direction.to_vector()
            if area[check[0]][check[1]] != 0:
                return self.next_direction
