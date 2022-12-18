from __future__ import annotations
from typing import Tuple
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    NONE = 4

    def opposite(self) -> Direction:
        """Return the opposite direction"""
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.NONE: Direction.NONE
        }[self]

    def to_vector(self) -> Tuple[int, int]:
        """Return the direction as a vector"""
        return {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
            Direction.NONE: (0, 0)
        }[self]
