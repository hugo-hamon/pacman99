from abc import ABC, abstractmethod
from ..direction import Direction
from typing import Tuple


class Entities(ABC):

    def __init__(self, speed=0, direction=Direction.WEST, coordinate=(0, 0)) -> None:
        super().__init__()
        self.coordinates = coordinate
        self.direction = direction
        self.speed = speed

    # REQUESTS
    def get_speed(self) -> int:
        return self.speed

    def get_position(self) -> Tuple[int, int]:
        return self.coordinates

    def get_direction(self) -> Direction:
        return self.direction

    # COMMANDS
    def set_speed(self, speed: int) -> None:
        self.speed = speed

    @abstractmethod
    def move(self, direction: Direction) -> None:
        pass
