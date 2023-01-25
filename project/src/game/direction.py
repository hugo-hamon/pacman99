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

    def to_angle(self) -> int:
        """Return the direction as an angle"""
        return {
            Direction.NORTH: 90,
            Direction.EAST: 0,
            Direction.SOUTH: 270,
            Direction.WEST: 180,
            Direction.NONE: 0
        }[self]

    @staticmethod
    def from_string(string: str) -> Direction:
        """Return the direction from a string"""
        return {
            "n": Direction.NORTH,
            "e": Direction.EAST,
            "s": Direction.SOUTH,
            "w": Direction.WEST
        }[string]
