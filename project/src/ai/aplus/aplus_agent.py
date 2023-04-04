from ...game.entities.ghost.ghoststate import Ghoststate
from ...game.maze.components import Components
from ...game.direction import Direction
from typing import Tuple, List
from ...game.game import Game
import numpy as np
import heapq

GAUSSIAN_EFFECT_GHOST = 0.01
GAUSSIAN_EFFECT_PACMAN = 0.1


def pretty_print_array(array: np.ndarray) -> None:
    np.set_printoptions(precision=3, suppress=True)
    # print column index
    print("    ", end=" ")
    for i in range(array.shape[1]):
        print(f"{i:4}", end=" ")
    print()
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if j == 0:
                print(f"{i:4}", end=" ")
            print(f"{array[i, j]:4.0f}", end=" ")
        print()


def get_next_move(game: Game) -> Direction:
    weights = compute_weights(game)
    pacman_pos = game.pacman.get_position()
    pac_x = round(pacman_pos[0])
    pac_y = round(pacman_pos[1])
    weights[pac_y, pac_x] = 0

    pretty_print_array(weights)
    # get pos with max weight
    max_x, max_y = np.unravel_index(np.argmax(weights), weights.shape)
    print(f"pacman: {pac_x}, {pac_y}")
    print(f"max: {max_x}, {max_y}")
    coords = a_plus((pac_x, pac_y), (int(max_y), int(max_x)), game)
    print(coords)
    if len(coords) <= 1:
        return game.pacman.direction

    return get_move_by_pos(coords[1], (pac_x, pac_y))


def compute_weights(game: Game) -> np.ndarray:
    weights_maze = game.maze.get_maze()
    weights = np.zeros(weights_maze.shape)

    pacman_pos = game.pacman.get_position()
    pac_x = round(pacman_pos[0])
    pac_y = round(pacman_pos[1])
        
    for i in range(weights_maze.shape[0]):
        for j in range(weights_maze.shape[1]):
            cell_weight = 0

            dist_to_pacman = np.sqrt((i - pac_y)**2 + (j - pac_x)**2)

            for ghost in game.ghosts:
                ghost_pos = ghost.get_position()
                ghost_coord = (round(ghost_pos[0]), round(ghost_pos[1]))
                dist_to_ghost = np.sqrt(
                    (i - ghost_coord[1])**2 + (j - ghost_coord[0])**2)

                # If the ghost is close, add a negative weight using a Gaussian function
                if dist_to_ghost <= 5:
                    weight = gaussian(i, j, ghost_coord[1], ghost_coord[0], 1) / GAUSSIAN_EFFECT_GHOST
                    cell_weight -= weight

            if weights_maze[i, j] == Components.DOT:
                cell_weight += 1

            if weights_maze[i, j] == Components.SUPERDOT:
                cell_weight += 2

            if weights_maze[i, j] in [Components.WALL, Components.DOOR]:
                cell_weight = -100

            if dist_to_pacman <= 3 and weights_maze[i, j] not in [Components.WALL, Components.DOOR, Components.EMPTY]:
                cell_weight += gaussian(i, j, pac_y, pac_x, 1) / GAUSSIAN_EFFECT_PACMAN
                print("Gaussian pacman", gaussian(i, j, pac_y, pac_x, 1) / GAUSSIAN_EFFECT_PACMAN)


            weights[i, j] = cell_weight

    return weights


def gaussian(x: float, y: float, mu0: float, mu1: float, sigma: float = 1) -> float:
    left = 1 / (2 * np.pi * sigma ** 2)
    right = np.exp(-((x - mu0) ** 2 + (y - mu1) ** 2) / (2 * sigma ** 2))
    return left * right


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


def heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """Manhattan distance heuristic"""
    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])


def a_plus(start: Tuple[int, int], end: Tuple[int, int], game: Game) -> List[Tuple[int, int]]:
    """A* algorithm"""
    start_node = Node(start, 0, heuristic(start, end))
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

        for neighbor_pos in get_neighbours(node.pos, game):
            if neighbor_pos in explored:
                continue
            g_cost = node.g_cost + 1
            h_cost = heuristic(neighbor_pos, end)
            neighbor_node = Node(neighbor_pos, g_cost, h_cost, node)
            heapq.heappush(frontier, neighbor_node)
        if len(frontier) > 100:
            return []

    # No path found
    return []


def get_move_by_pos(pos: Tuple[int, int], pac_pos: Tuple[int, int]) -> Direction:
    """Return the direction to go to a position"""
    if pos[0] < pac_pos[0]:
        return Direction.WEST
    elif pos[0] > pac_pos[0]:
        return Direction.EAST
    elif pos[1] < pac_pos[1]:
        return Direction.NORTH
    else:
        return Direction.SOUTH


def get_neighbours(pos: Tuple[int, int], game: Game) -> List[Tuple[int, int]]:
    """Return the neighbours of a position"""
    neighbours = game.maze.get_area(
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
