from ...game.entities.ghost.ghoststate import Ghoststate
from ...game.maze.components import Components
from ...game.direction import Direction
from ...game.maze.maze import Maze
from typing import Tuple, List
from ...game.game import Game
from ...config import Config
import numpy as np
import random
import heapq


class Node:
    """Class representing a node in the A* algorithm"""

    def __init__(self, pos: Tuple[int, int], g_cost: int, h_cost: int, parent=None) -> None:
        self.pos = pos
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.parent = parent

    def __lt__(self, other) -> bool:
        """Comparison method to use heapq"""
        return self.g_cost + self.h_cost < other.g_cost + other.h_cost


class AplusAgent:

    def __init__(self, config: Config, maze: Maze) -> None:
        self.config = config
        self.maze = maze

        self.current_dot = (-1, -1)

    def get_next_move(self, game: Game) -> Direction:
        """Return the next move of the pacman"""
        pacman_pos = game.pacman.get_position()
        pac_x, pac_y = round(pacman_pos[0]), round(pacman_pos[1])
        # take the tunnel if possible
        if pac_x == 0:
            return Direction.WEST
        if pac_x == self.maze.get_width() - 1:
            return Direction.EAST
        self.choose_point(pac_x, pac_y, game)
        new_pos = self.a_star((pac_x, pac_y), self.current_dot, game)
        if len(new_pos) == 0:
            return game.pacman.get_direction()
        return self.get_move_by_pos(new_pos[1], (pac_x, pac_y))

    def choose_point(self, pac_x: int, pac_y: int, game: Game) -> None:
        """Choose the nearest point to the pacman"""
        self.current_dot = self.get_nearest_point(pac_x, pac_y, game)

    def get_nearest_point(self, pac_x: int, pac_y: int, game: Game) -> Tuple[int, int]:
        """Return the nearest dot if there is no ghost around in a radius of 3 else return a random dot"""
        dots = self.maze.get_dot_position()
        if len(dots) == 0:
            return (-1, -1)
        dots.sort(key=lambda x: np.sqrt(
            (x[0] - pac_x) ** 2 + (x[1] - pac_y) ** 2))
        for dot in dots:
            distances = [np.sqrt((dot[0] - ghost.get_position()[0]) ** 2 +
                                 (dot[1] - ghost.get_position()[1]) ** 2) for ghost in game.ghosts]
            if min(distances) > 3:
                return dot
        return random.choice(dots)

    def a_star(self, start: Tuple[int, int], end: Tuple[int, int], game) -> List[Tuple[int, int]]:
        """A* algorithm"""
        start_node = Node(start, 0, self.heuristic(start, end))
        frontier = [start_node]
        explored = set()
        while frontier:
            node = heapq.heappop(frontier)
            if node.pos == end:
                # Reconstruct path
                path = [node.pos]
                while node.parent:
                    node = node.parent
                    path.append(node.pos)
                return path[::-1]
            explored.add(node.pos)

            for neighbor_pos in self.get_neighbours(node.pos, game):
                if neighbor_pos in explored:
                    continue
                g_cost = node.g_cost + 1
                h_cost = self.heuristic(neighbor_pos, end)
                neighbor_node = Node(neighbor_pos, g_cost, h_cost, node)
                heapq.heappush(frontier, neighbor_node)
            if len(frontier) > 100:
                return []

        # No path found
        return []

    def get_move_by_pos(self, pos: Tuple[int, int], pac_pos: Tuple[int, int]) -> Direction:
        """Return the direction to go to a position"""
        if pos[0] < pac_pos[0]:
            return Direction.WEST
        elif pos[0] > pac_pos[0]:
            return Direction.EAST
        elif pos[1] < pac_pos[1]:
            return Direction.NORTH
        else:
            return Direction.SOUTH

    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Manhattan distance heuristic"""
        return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
    
    def get_neighbours(self, pos: Tuple[int, int], game: Game) -> List[Tuple[int, int]]:
        """Return the neighbours of a position"""
        neighbours = self.maze.get_area(
            pos[0], pos[1], 1, default_value=Components.EMPTY)
        for ghost in game.ghosts:
            if ghost.state not in [Ghoststate.FRIGHTENED, Ghoststate.EATEN]:
                ghost_x, ghost_y = ghost.get_position()
                ghost_x = round(ghost_x)
                ghost_y = round(ghost_y)
                if abs(ghost_x - pos[0]) <= 1 and abs(ghost_y - pos[1]) <= 1:
                    neighbours[ghost_y - pos[1] + 1, ghost_x - pos[0] + 1] = 0
        four_neighbours = []
        if neighbours[0, 1] != 0:
            four_neighbours.append((pos[0], pos[1] - 1))
        if neighbours[2, 1] != 0:
            four_neighbours.append((pos[0], pos[1] + 1))
        if neighbours[1, 0] != 0:
            four_neighbours.append((pos[0] - 1, pos[1]))
        if neighbours[1, 2] != 0:
            four_neighbours.append((pos[0] + 1, pos[1]))
        return four_neighbours
