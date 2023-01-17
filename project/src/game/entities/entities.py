from ..direction import Direction
from typing import Tuple, Union
from ..maze.maze import Maze


UNITSPERCELL = 1000


class Entities():

    def __init__(self, maze: Maze, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (0, 0)) -> None:
        self.x, self.y = int(
            coordinate[0] * UNITSPERCELL), int(coordinate[1] * UNITSPERCELL)
        self.direction = direction
        self.next_direction: Direction = Direction.NONE
        self.speed = (int)(speed * UNITSPERCELL)
        self.movedistance = 0
        self.distance = 0
        self.maze = maze

    # REQUESTS
    def get_speed(self) -> float:
        """Return the speed of the entity"""
        return self.speed / UNITSPERCELL

    def get_position(self) -> Tuple[float, float]:
        """Return the position of the entity"""
        return self.x / UNITSPERCELL, self.y / UNITSPERCELL

    def get_direction(self) -> Union[None, Direction]:
        """Return the direction of the entity"""
        return self.direction

    def get_distance(self) -> int:
        """Return the distance of the entity from the start"""
        return self.distance

    # COMMANDS
    def set_position(self, position: Tuple[int, int]) -> None:
        """Set the position of the entity"""
        self.x, self.y = position[0] * UNITSPERCELL, position[1] * UNITSPERCELL
        print(self.x, self.y)

    def set_speed(self, speed: int) -> None:
        """Set the speed of the entity"""
        self.speed = speed * UNITSPERCELL

    def move(self, timestep: int) -> None:
        """Move the entity"""
        self.movedistance += self.speed / timestep
        self.__moveToNextStep()
        while self.movedistance > 0 and self.direction is not None:
            self.direction = self.__get_next_direction()
            self.__moveToNextStep()
        self.distance += 1
        self.movedistance = 0

    def __moveToNextStep(self) -> None:
        """Move the entity to the next step"""
        xd, xy = self.direction.to_vector() if self.direction is not None else (0,0)
        distanceToMove = min(self.movedistance, UNITSPERCELL - ((xd * self.x + xy * self.y) % UNITSPERCELL))
        self.movedistance -= distanceToMove
        self.x += distanceToMove * xd
        self.y += distanceToMove * xy

    def __get_next_direction(self) -> Union[None, Direction]:
        """Get the next direction of the entity"""
        position = self.get_position()
        if self.maze.is_intersection(int(position[0]), int(position[1])):
            area = self.maze.get_neighbors(int(position[0]), int(position[1]))
            check = (1, 1) + self.next_direction.to_vector()
            if area[check[0]][check[1]] != 0:
                return self.next_direction
        
