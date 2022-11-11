from components import Components 
import numpy as np
class Maze():
    def __init__(self, file):
        '''Create a maze from a text file
        The text file must be a matrix of 0, 1, 2, 3, 4
        0: Wall
        1: Empty
        2: Dot
        3: Superdot
        4: Fruit
        '''
        f = open(file, "r")
        lines = f.readlines()
        self.width = len(lines[0]) - 1
        self.height = len(lines)
        print("width: ", self.width, "height: ", self.height)
        self.maze = np.zeros((self.height, self.width), dtype=Components)
        for j in range(0, self.width):
            for i in range(0, self.height):
                match lines[i][j]:
                    case '0':
                        self.maze[i,j] = Components.WALL
                    case '1':
                        self.maze[i,j] = Components.EMPTY
                    case '2':
                        self.maze[i,j] = Components.DOT
                    case '3':
                        self.maze[i,j] = Components.SUPERDOT
                    case '4':
                        self.maze[i,j] = Components.FRUIT
        f.close()
        self.total_dots = np.count_nonzero(self.maze == Components.DOT) + np.count_nonzero(self.maze == Components.SUPERDOT)

    def display(self) -> None:
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.get_cell(x,y) == Components.WALL:
                    print("0", end='')
                elif self.get_cell(x,y) == Components.EMPTY:
                    print("1", end='')
                elif self.get_cell(x,y) == Components.DOT:
                    print("2", end='')
                elif self.get_cell(x,y) == Components.SUPERDOT:
                    print("3", end='')
                elif self.get_cell(x,y) == Components.FRUIT:
                    print("4", end='')
            print()

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_maze(self) -> np.array:
        '''Return a copy of a np.array representing the maze'''
        return self.maze.copy()

    def get_cell(self, x: int, y: int) -> Components:
        '''Return the cell at the position (x,y)'''
        return self.maze[y,x]

    def get_neighbors (self, x: int, y: int) -> np.array:
        '''Return a 3x3 np.array of the neighbors of the cell (x,y)
        For cells on the border, the neighbors outside the maze are considered as walls'''
        neighbors = np.zeros((3,3), dtype=Components)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x+i >= 0 and x+i < self.height and y+j >= 0 and y+j < self.width:
                    neighbors[i+1,j+1] = self.maze[x+i,y+j]
        return neighbors

    def is_intersection(self, x: int, y: int) -> bool:
        return self.get_cell(x, y) != Components.WALL and np.count_nonzero(self.get_neighbors(x, y) == Components.WALL) <= 2

    def get_total_dots(self) -> int:
        return self.total_dots

    def get_total_remain_dots(self) -> int:
        return np.count_nonzero(self.maze == Components.DOT) + np.count_nonzero(self.maze == Components.SUPERDOT)

    def set_component(self, c: Components,x: int, y: int) -> None:
        self.maze[x,y] = c