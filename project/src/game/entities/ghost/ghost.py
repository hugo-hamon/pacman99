from .ghoststate import Ghoststate as gs
from ...direction import Direction
from ...direction import Direction
from ..entities import Entities
from ...maze.components import Components
from ...maze.maze import Maze
from typing import Tuple
from abc import ABC, abstractmethod
from math import sqrt
import numpy as np
import operator

class GeneralGhost(Entities) :
    '''Abstract class representing a ghost.
    Each subclass must implement the method _get_next_direction() which tells the ghost behavior.'''
    def __init__(self, maze: Maze, pac: Entities, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (5, 5)) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.pac = pac
        self.state = gs.CHASE
    
    # REQUESTS

    def get_possible_direction(self):
        '''Compute and return the possible direction where the ghost can go.
        A ghost can't go back or go through a wall.'''
        possible_direction = []
        position = self.get_position()
        area = self.maze.get_neighbors(int(position[0]), int(position[1]))
        for d in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            checkw = tuple(map(operator.add, d.to_vector(), (1, 1)))
            if area[checkw[1]][checkw[0]] != Components.WALL:
                possible_direction.append(d)
        return possible_direction

    def distance_euclidienne(self, ghost_pos, pac_pos):
        '''Compute the distance between the ghost and the pacman.'''
        return sqrt((ghost_pos[0] - pac_pos[0])**2 + (ghost_pos[1] - pac_pos[1])**2)
    
    @abstractmethod
    def _get_next_direction(self) -> Direction:
        '''Return and set the next direction of the ghost.'''
        pass

    # COMMANDS

    def set_state(self, ghoststate : gs) -> None :
        """Set the ghost state"""
        self.state = ghoststate
    