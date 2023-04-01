from typing import Tuple, List
import heapq
import time


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


def a_star(start: Tuple[int, int], end: Tuple[int, int], game) -> List[Tuple[int, int]]:
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

        for neighbor_pos in game.get_neighbours(node.pos):
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
