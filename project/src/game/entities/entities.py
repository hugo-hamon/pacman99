from abc import ABC, abstractmethod
from ..direction import Direction
from ..maze.maze import Maze
from typing import Tuple


UNITSPERCELL = 1009


class Entities(ABC):

    def __init__(self, maze: Maze, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (0, 0)) -> None:
        super().__init__()
        self.x, self.y = int(
            coordinate[0] * UNITSPERCELL), int(coordinate[1] * UNITSPERCELL)
        self.speed = (int)(speed * UNITSPERCELL)
        self.direction = direction
        self.movedistance: int = 0
        self.maze = maze
        self.isInIntersection = True

    # REQUESTS
    def get_speed(self) -> float:
        """Return the speed of the entity"""
        return self.speed / UNITSPERCELL

    def get_position(self) -> Tuple[float, float]:
        """Return the position of the entity"""
        return self.x / UNITSPERCELL, self.y / UNITSPERCELL

    def get_direction(self) -> Direction:
        """Return the direction of the entity"""
        return self.direction

    # COMMANDS
    def set_position(self, position: Tuple[int, int]) -> None:
        """Set the position of the entity"""
        self.x, self.y = position[0] * UNITSPERCELL, position[1] * UNITSPERCELL

    def set_speed(self, speed: float) -> None:
        """Set the speed of the entity"""
        self.speed = speed * UNITSPERCELL

    def move(self, timestep: int) -> None:
        """Move the entity"""
        self.movedistance += int(self.speed / timestep)
        while self.movedistance > 0 and self.direction != Direction.NONE:
            if self.isInIntersection:
                self.direction = self._get_next_direction()
                self.isInIntersection = False
            else:
                self.__moveToNextStep()
        self.movedistance = 0

    def __moveToNextStep(self) -> None:
        """Move the entity to the next step"""
        xd, xy = self.direction.to_vector()
        # UNITSPERCELL - ((xd * self.x + xy * self.y) % UNITSPERCELL)
        # est la distance à la prochaine intersection
        distanceToMove = min(self.movedistance, UNITSPERCELL -
                             ((xd * self.x + xy * self.y) % UNITSPERCELL))
        if self.movedistance >= (UNITSPERCELL -
                                 ((xd * self.x + xy * self.y) % UNITSPERCELL)):
            self.isInIntersection = True
        self.movedistance -= distanceToMove
        self.x += distanceToMove * xd
        self.y += distanceToMove * xy

    @abstractmethod
    def _get_next_direction(self) -> Direction:
        """Return the next direction of the entity"""
        return NotImplemented
