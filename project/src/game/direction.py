from __future__ import annotations
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def opposite(self) -> Direction:
        """Return the opposite direction"""
        return Direction((self.value + 2) % 4)
