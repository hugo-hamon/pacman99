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

    #CONSTANTS
    
    def __init__(self, maze: Maze, pac: Entities, speed: float = 0, direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (5, 5), scatter_pos: Tuple[int, int] = (8, 8)) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.pac = pac
        self.state = gs.EXITTING
        self.inside_ghostbox = True
        self.outside_ghostbox_position = (self.maze.get_width() // 2, self.maze.get_height() // 2 - 2)
        self.scatter_position = scatter_pos

    # REQUESTS
    def get_possible_direction(self):
        '''Compute and return the possible direction where the ghost can go.
        A ghost can't go back or go through a wall.'''
        possible_direction = []
        position = self.get_position()
        area = self.maze.get_neighbors(round(position[0]), round(position[1]))
        for d in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
            checkw = tuple(map(operator.add, d.to_vector(), (1, 1)))
            if area[checkw[1]][checkw[0]] not in [Components.WALL, Components.DOOR]:
                possible_direction.append(d)
            if area[checkw[1]][checkw[0]] == Components.DOOR and self.state in [gs.EXITTING, gs.EATEN]:
                possible_direction.append(d)
        return possible_direction

    def distance_euclidienne(self, ghost_pos, pac_pos):
        '''Compute the distance between the ghost and the pacman.'''
        return sqrt((ghost_pos[0] - pac_pos[0])**2 + (ghost_pos[1] - pac_pos[1])**2)

    def _get_next_direction(self) -> Direction:
        '''Return and set the next direction of the ghost.'''
        if self.inside_ghostbox and self.state != gs.EATEN:
            self.state = gs.EXITTING
        match self.state:
            case gs.CHASE:
                return self.get_chase_direction()
            case gs.SCATTER:
                return self.get_scatter_direction()
            case gs.FRIGHTENED:
                return self.get_frightened_direction()
            case gs.EATEN:
                return self.get_eaten_direction()
            case gs.EXITTING:
                return self.get_outside_ghostbox_direction()

    def get_scatter_direction(self) -> Direction:
        '''Return the direction of the ghost in scatter mode.'''
        position = self.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, self.scatter_position)
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction
    
    def get_frightened_direction(self) -> Direction:
        '''Return the direction of the ghost in frightened mode.'''
        if self.inside_ghostbox:
            return self.get_outside_ghostbox_direction()
        position = self.get_position()
        pac_pos = self.pac.get_position()
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction != Direction.NONE and direction == self.direction.opposite():
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
        '''Return the direction of the ghost in eaten mode.'''
        position = self.get_position()
        ghostbox_pos = (self.maze.get_width()//2, self.maze.get_height()//2)
        if position[0] == ghostbox_pos[0] and position[1] == ghostbox_pos[1]:
            return Direction.NONE
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, ghostbox_pos)
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction

    def get_outside_ghostbox_direction(self) -> Direction:
        '''Return the direction of the ghost to get outside the box'''
        position = self.get_position()
        if round(position[0]) == self.outside_ghostbox_position[0] and round(position[1]) == self.outside_ghostbox_position[1]:
            self.inside_ghostbox = False
            self.state = gs.CHASE
            return Direction.NORTH
        prefered_direction = Direction.NONE
        dist = np.inf
        for direction in self.get_possible_direction():
            if direction == self.direction.opposite():
                continue
            dir_ghost_pos = round(
                position[0] + direction.to_vector()[0]), round(position[1] + direction.to_vector()[1])
            dist_to_dir = self.distance_euclidienne(dir_ghost_pos, self.outside_ghostbox_position)
            if dist_to_dir < dist or prefered_direction == Direction.NONE:
                prefered_direction = direction
                dist = dist_to_dir
        self.direction = prefered_direction
        return prefered_direction

    @abstractmethod
    def get_chase_direction(self) -> Direction:
        '''Return the direction of the ghost in chase mode.'''
        pass

    # COMMANDS

    def set_state(self, ghoststate : gs) -> None :
        """Set the ghost state"""
        if ghoststate == gs.EATEN:
            self.inside_ghostbox = True
        self.state = ghoststate