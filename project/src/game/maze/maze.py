from .components import Components
from typing import Tuple
import numpy as np
import itertools


class Maze():

    def __init__(self, filename: str):
        self.filename = filename
        self.width = 0
        self.height = 0
        self.maze = np.zeros((0, 0), dtype=Components)
        self.pacman_start = (0, 0)
        self.total_dots = 0
        self.load_file()

    def load_file(self) -> None:
        """
        Load the maze from a file
        0: Wall
        1: Empty
        2: Dot
        3: Superdot
        4: Fruit
        """
        with open(self.filename, "r") as f:
            lines = f.readlines()
            self.width = len(lines[0]) - 1
            self.height = len(lines) - 1
            self.maze = np.zeros((self.height, self.width), dtype=Components)
            for j in range(self.width):
                for i in range(self.height):
                    self.maze[i, j] = self.get_component_type(lines[i][j])
            self.pacman_start = tuple(map(int, lines[-1].split(" ")))
            self.total_dots = np.count_nonzero(
                self.maze == Components.DOT) + np.count_nonzero(self.maze == Components.SUPERDOT)

    def get_component_type(self, symbol: str) -> Components:
        """
        Return the component type from a symbol
        """
        match symbol:
            case '0':
                return Components.WALL
            case '1':
                return Components.EMPTY
            case '2':
                return Components.DOT
            case '3':
                return Components.SUPERDOT
            case '4':
                return Components.FRUIT
            case _:
                raise ValueError("Invalid symbol")

    def display(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x, y) == Components.WALL:
                    print("0", end='')
                elif self.get_cell(x, y) == Components.EMPTY:
                    print("1", end='')
                elif self.get_cell(x, y) == Components.DOT:
                    print("2", end='')
                elif self.get_cell(x, y) == Components.SUPERDOT:
                    print("3", end='')
                elif self.get_cell(x, y) == Components.FRUIT:
                    print("4", end='')
            print()

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_maze(self) -> np.ndarray:
        '''Return a copy of a np.array representing the maze'''
        return self.maze.copy()

    def get_cell(self, x: int, y: int) -> Components:
        '''Return the cell at the position (x,y)'''
        return self.maze[y, x]

    def get_neighbors(self, x: int, y: int) -> np.ndarray:
        '''Return a 3x3 np.array of the neighbors of the cell (x,y)
        For cells on the border, the neighbors outside the maze are considered as EMPTY
        '''
        neighbors = np.zeros((3, 3), dtype=Components)
        for j, i in itertools.product(range(-1, 2), range(-1, 2)):
            neighbors[i + 1, j + 1] = (
                Components.EMPTY
                if x + j < 0
                or x + j >= self.width
                or y + i < 0
                or y + i >= self.height
                else self.maze[y + i, x + j]
            )
        return neighbors

    def get_pacman_start(self) -> Tuple[int, int]:
        """Return the position of the pacman start"""
        return self.pacman_start

    def get_total_dots(self) -> int:
        return self.total_dots

    def get_total_remain_dots(self) -> int:
        return np.count_nonzero(self.maze == Components.DOT) + np.count_nonzero(self.maze == Components.SUPERDOT)

    def set_component(self, c: Components, x: int, y: int) -> None:
        self.maze[x, y] = c
