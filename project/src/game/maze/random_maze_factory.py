import random
from components import Components
import numpy as np
from maze import Maze

class RandomMazeFactory():


    ''' Create the text file representation of a random maze'''
    def __init__(self, width, height, intersection_step = 2, density=0.2, seed=random.random):
        ''' seed and density are float between 0 and 1'''
        self.width = width
        self.height = height
        self.seed = seed
        self.density = density
        self.intersection_step = intersection_step
        self.maze

    def set_intersection_step(self, intersection_step: int) -> None:
        self.intersection_step = intersection_step

    def set_density(self, density: float) -> None:
        self.density = density
    
    def new_seed(self) -> None:
        self.seed = random.random()

    def create(self, file: str) -> None:
        '''Create a random maze and write it in a text file'''
        random.seed(self.seed)
        self.maze = np.zeros((self.height, self.width // 2), dtype=Components)
        # Create the left side of the maze
        self.__create_left_side()
        # Write the maze in a file

    def create_left_side(self) -> None:
        '''Create the left side of the maze'''
    
    def __place_intersection(self) -> None:
        ''' Place intersections in the maze'''
        for i in range()

    def __create_left_side(self, maze: np.ndarray) -> None:
        '''Create the left side of the maze'''
        # Create the left side of the maze
        for i in range(0, self.height):
            if i % self.intersection_step == 0:
                maze[i,0] = Components.WALL
            else:
                if random.random() < self.density:
                    maze[i,0] = Components.WALL
                else:
                    maze[i,0] = Components.EMPTY