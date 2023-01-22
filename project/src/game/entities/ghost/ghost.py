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
        self.state = gs.EATEN
    
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
    
    def get_scatter_direction(self) -> Direction:
        '''Return the direction of the ghost in scatter mode.'''
        # TODO
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, pac_pos)
            if dist_to_dir > dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction
    
    def get_frightened_direction(self) -> Direction:
        '''Return the direction of the ghost in frightened mode.'''
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, pac_pos)
            if dist_to_dir > dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction

    def get_eaten_direction(self) -> Direction:
        '''Return the direction of the ghost in frightened mode.'''
        position = self.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, (self.maze.get_width()//2, self.maze.get_height()//2))
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction

    # COMMANDS

    def set_state(self, ghoststate : gs) -> None :
        """Set the ghost state"""
        self.state = ghoststate
    