import random
from .components import Components
import numpy as np
from ..direction import Direction

RANDOM_MAZE_FILE_PATH = "assets/data/random.txt"

class RandomMazeFactory():
    
    ''' Create the text file representation of a random maze'''
    def __init__(self, width, height, intersection_step = 3, density=0.1, seed=random.random()):
        ''' seed and density are float between 0 and 1 '''
        ''' width and height are multiples of intersection_step '''
        self.width = width // intersection_step * intersection_step
        self.height = height // intersection_step * intersection_step
        self.seed = seed
        self.density = density
        self.intersection_step = intersection_step
        self.maze = np.zeros((self.height, self.width // 2), dtype=Components)
        self.graph = {}

    def set_intersection_step(self, intersection_step: int) -> None:
        self.intersection_step = intersection_step

    def set_density(self, density: float) -> None:
        self.density = density
    
    def new_seed(self) -> None:
        self.seed = random.random()

    def create(self) -> None:
        '''Create a random maze and write it in a text file'''
        random.seed(self.seed)
        
        self.__create_graph()
        # Write the maze in a file
        with open(RANDOM_MAZE_FILE_PATH, 'w') as f:
            for i in range(self.height):
                for j in range(self.width // 2):
                    f.write(str(self.maze[i,j]))
                for j in range(self.width // 2 - 1, -1, -1):
                    f.write(str(self.maze[i,j]))
                f.write('\n')
                
    def __create_graph(self) -> None:
        ''' Create a graph representation of the paths in the maze where each node is an intersection and each edge is a path'''
        self.graph = {}
        # Create the nodes of the graph
        # Each node is an intersection and has 1 - density probability to exist
        for i in range(1,(self.height // self.intersection_step) * (self.width // self.intersection_step) + 1):
                self.graph[i] = []
        # Create the edges of the graph
        # Each edge is a path between two intersections
        # the degree of each node is between 2 and 4 which means that each intersection is connected to at least 2 paths
        for k, v in self.graph.items():
            # Compute the candidates for each neighbor of k
            candidates = [(k + 1, Direction.EAST), (k - 1, Direction.WEST), (k + self.width // self.intersection_step, Direction.SOUTH), (k - self.width // self.intersection_step, Direction.NORTH)]
            for i in range(2):
                if candidates[i][0] in self.graph.keys() and (candidates[i][0] - 1) // (self.height // self.intersection_step) == (k - 1) // (self.height // self.intersection_step):
                    self.graph[k].append(candidates[i])
            for i in range(2,4):
                if candidates[i][0] in self.graph.keys():
                    self.graph[k].append(candidates[i])
            # Choose randomly two to four neighbors for k
            for i in range(4):
                if len(self.graph[k]) > 2:
                    self.graph[k].pop(random.randint(0, len(self.graph[k]) - 1))
        keys = list(self.graph.keys())
        '''
        # Remove the nodes that have one neighbors
        for k in keys:
            if len(self.graph[k]) < 1:
                self.graph.pop(k)
        '''
        self.__graph_to_maze()
        
            
    def __graph_to_maze(self) -> None:
        ''' Convert the graph representation of the maze into a text file representation'''
        self.maze = np.zeros((self.height, self.width), dtype=Components)
        for k, v in self.graph.items():
            # Place the intersection
            x = ((self.intersection_step * (k - 1)) % self.width) + 1
            y = (k - 1) // (self.height // self.intersection_step) * self.intersection_step + 1
            self.maze[y, x] = Components.DOT
            for i, dir in v:
                # Compute the position of the next intersection
                xi = ((self.intersection_step * (i - 1)) % self.width) + 1
                yi = (i - 1) // (self.height // self.intersection_step) * self.intersection_step + 1
                xv = x
                yv = y
                while True:
                    # Place the path until the next intersection
                    xv += dir.to_vector()[0]
                    yv += dir.to_vector()[1]
                    if xi == xv and yi == yv:
                        break
                    self.maze[yv, xv] = Components.DOT
        
    def __create_left_side(self) -> None:
        '''Create the left side of the maze'''
        self.__place_intersection()

    def __roy_warshall(self) -> np.array:
        '''Compute if there is a path between each pair of intersections'''
        # np.eye renvoie la matrice identité
        n = (self.width // self.intersection_step) * (self.height // self.intersection_step)
        A = np.array([[False for _ in range(n)] for _ in range(n)])
        for k, v in self.graph.items():
            for u in v:
                A[k - 1][u[0]-1] = True
        print(self.graph)
        print(list(A))
        res = A | np.eye(n, dtype=bool)
        for k in range(0, n):
            for i in range(0, n):
                for j in range(0, n):
                    res[i, j] = res[i, j] | (res[i, k] & res[k, j])
        return res
    
    def __place_intersection(self) -> None:
        ''' Place intersections in the maze'''
        for i in range(1, self.height - 1, self.intersection_step):
            for j in range(1, self.width // 2 - 1, self.intersection_step):
                if random.random() > self.density:
                    self.maze[i,j] = Components.EMPTY
        print(self.maze)
    
    def __place_path(self) -> None:
        ''' Place paths in the maze'''
        


if __name__ == "__main__":
    maze = RandomMazeFactory(50, 50)
    maze.create(RANDOM_MAZE_FILE_PATH)
