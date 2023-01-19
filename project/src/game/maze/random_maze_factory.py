from .components import Components
from ..direction import Direction
from ...config import load_config
from ...config import Config
import numpy as np
import random
import copy


class RandomMazeFactory():
    ''' Create the text file representation of a random maze'''

    RANDOM_SEED = random.random()
    # Minimum size of the maze
    MIN_MAZE_HEIGHT = 15
    MIN_MAZE_WIDTH = 15
    # The ghost box is a predefined structure at the center of the maze
    GHOST_BOX = [[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 0, 0, 0, 1, 0, 0, 0, 2],
                 [2, 0, 1, 1, 1, 1, 1, 0, 2], [2, 0, 1, 1, 1, 1, 1, 0, 2],
                 [2, 0, 1, 1, 1, 1, 1, 0, 2], [2, 0, 0, 0, 0, 0, 0, 0, 2],
                 [2, 1, 1, 1, 1, 1, 1, 1, 2]]

   # CONSTRUCTOR
    def __init__(self, config: Config) -> None:
        self.intersection_step = config.maze.intersection_step
        self.is_symetric = config.maze.is_symetric
        self.density = config.maze.density
        self.height = config.maze.height
        self.width = config.maze.width
        self.seed = config.maze.seed
        self.config = config
        # Check conditions
        if self.width < self.MIN_MAZE_WIDTH:
            raise ValueError(
                f"The maze width must be at least {self.MIN_MAZE_WIDTH}")
        if self.height < self.MIN_MAZE_HEIGHT:
            raise ValueError(
                f"The maze height must be at least {self.MIN_MAZE_HEIGHT}")
        if self.width % self.intersection_step != 0:
            raise ValueError(
                f"The maze width must be a multiple of {self.intersection_step}")
        if self.height % self.intersection_step != 0:
            raise ValueError(
                f"The maze height must be a multiple of {self.intersection_step}")
        self.width = self.width // self.intersection_step * self.intersection_step
        self.height = self.height // self.intersection_step * self.intersection_step
        if self.density < 0 or self.density > 1:
            raise ValueError("The density must be between 0 and 1")
        if self.seed < 0:
            self.seed = self.RANDOM_SEED

    # COMMANDS

    def set_intersection_step(self, intersection_step: int) -> None:
        self.intersection_step = intersection_step

    def set_density(self, density: float) -> None:
        self.density = density

    def new_seed(self) -> None:
        self.seed = random.random()

    def create(self) -> None:
        '''Create a random maze and write it in a text file'''

        random.seed(self.seed)
        connex_comp_nb = 0
        g = self.__create_graph()
        while connex_comp_nb != 1:
            g = self.__create_graph()
            parent = self.__union_find(g)
            connex_comp_nb = np.count_nonzero(parent < 0)
        maze = self.__graph_to_maze(g)
        maze = self.__add_ghost_box(maze)
        self.__write_maze_in_file(maze)
        self.__write_pacman_position_in_file()

    # TOOLS

    def __create_graph(self) -> dict:
        """Create a graph representation of the paths in the maze where each node is an intersection and each edge is a path"""
        # Number of nodes
        n = (self.height // self.intersection_step) * \
            (self.width // self.intersection_step)
        g = {i: [] for i in range(1, n + 1)}
        # Create the edges of the graph
        # Each edge is a path between two intersections
        # the degree of each node is between 2 and 4 which means that each intersection is connected to at least 2 paths
        for node in g:
            # Compute the candidates for each neighbor of k
            candidates = [(node + 1, Direction.EAST), (node - 1, Direction.WEST), (node + self.width //
                                                                                   self.intersection_step, Direction.SOUTH), (node - self.width // self.intersection_step, Direction.NORTH)]
            # Add every candiate to the graph
            # Now every intersection is connected to every potential neighbor
            for i in range(2):
                if (
                    candidates[i][0] in g and (((candidates[i][0] - 1) * self.intersection_step) // self.width
                                               ) + 1 == (((node - 1) * self.intersection_step) // self.width) + 1
                ):
                    g[node].append(candidates[i])
                if candidates[i + 2][0] in g:
                    g[node].append(candidates[i + 2])

        # Remove randomly 0 to 2 edges of each node depending on the density and avoid to remove edges that lead to create dead ends
        for node in g:
            for _ in range(4):
                if len(g[node]) <= 2:
                    break
                if random.random() > self.density:
                    vertex_to_remove = random.choice(g[node])
                    if len(g[vertex_to_remove[0]]) >= 3:
                        g[node].remove(vertex_to_remove)
                        g[vertex_to_remove[0]].remove(
                            (node, vertex_to_remove[1].opposite()))
        return g

    def __add_ghost_box(self, maze) -> None:
        ''' Add the ghost box at the center of the maze
        It will also make sure the maze is connex if the symetric option is set to True'''
        # Compute the position of the ghost box
        x = self.width // 2 - len(self.GHOST_BOX[0]) // 2
        y = self.height // 2 - len(self.GHOST_BOX) // 2
        if self.is_symetric:
            # Add paths from the ghost box to the first and the last row
            for j in range(1, len(maze) - 2):
                maze[j, x + self.intersection_step - 1] = Components.DOT
                maze[j, x + len(self.GHOST_BOX[0]) -
                     self.intersection_step] = Components.DOT
        # Add the ghost box
        for i in range(len(self.GHOST_BOX)):
            for j in range(len(self.GHOST_BOX[0])):
                maze[y + i, x + j] = self.GHOST_BOX[i][j]
        # Make sure paths near the ghost box have a width of 1
        # Corners

        # Sides
        for i in range(1, len(self.GHOST_BOX) - 1):
            # Left side
            if (
                maze[y + i, x - 1] == Components.DOT
                and maze[y + i, x - 2] != Components.DOT
            ):
                maze[y + i, x - 1] = Components.WALL
            # Right side
            if (
                maze[y + i, x + len(self.GHOST_BOX[0])] == Components.DOT
                and maze[y + i, x + len(self.GHOST_BOX[0]) + 1] != Components.DOT
            ):
                maze[y + i, x + len(self.GHOST_BOX[0])] = Components.WALL
        for j in range(1, len(self.GHOST_BOX[0]) - 1):
            # Top side
            if (
                maze[y - 1, x + j] == Components.DOT
                and maze[y - 2, x + j] != Components.DOT
            ):
                maze[y - 1, x + j] = Components.WALL
            # Bottom side
            if (
                maze[y + len(self.GHOST_BOX), x + j] == Components.DOT
                and maze[y + len(self.GHOST_BOX) + 1, x + j] != Components.DOT
            ):
                maze[y + len(self.GHOST_BOX), x + j] = Components.WALL
        return maze

    def __graph_to_maze(self, g) -> np.ndarray:
        ''' Convert the graph representation of the maze into a text file representation'''
        maze = np.zeros((self.height + 1, self.width + 1), dtype=Components)
        for k, v in g.items():
            # Place the intersection
            x = ((self.intersection_step * (k - 1)) % self.width) + 1
            y = (((k - 1) * self.intersection_step) //
                 self.width) * self.intersection_step + 1
            maze[y, x] = Components.DOT
            for i, direction in v:
                # Compute the position of the next intersection
                xi = ((self.intersection_step * (i - 1)) % self.width) + 1
                yi = (((i - 1) * self.intersection_step) //
                      self.width) * self.intersection_step + 1
                xv = x
                yv = y
                while (xi, yi) != (xv, yv):
                    maze[yv, xv] = Components.DOT
                    xv += direction.to_vector()[0]
                    yv += direction.to_vector()[1]
        return maze

    def __write_maze_in_file(self, maze) -> None:
        # Write the maze in a file
        with open(self.config.maze.random_maze_path, 'w') as f:
            for i in range(self.height):
                if self.is_symetric:
                    for j in range(self.width // 2):
                        f.write(str(maze[i, j]))
                    for j in range(self.width // 2 - 1, -1, -1):
                        f.write(str(maze[i, j]))
                else:
                    for j in range(self.width):
                        f.write(str(maze[i, j]))
                f.write('\n')

    def __write_pacman_position_in_file(self) -> None:
        '''Write the default postion of pacman in the file at the end of the maze
        It can be deduced from the position of the ghost box'''
        x = self.width // 2
        y = self.height // 2 + len(self.GHOST_BOX) // 2
        with open(self.config.maze.random_maze_path, 'a') as f:
            f.write(f'{str(x)} {str(y)}')
        f.close()

    # CONNEXITY RELATED TOOLS
    def __union_find(self, g: dict):
        '''Compute the connex components of the graph using union-find algorithm
        Complexity : O(n + m*c) where c is a almost constant (A function that grows slower than log(n))'''
        parent = np.array([-1] * len(g))
        for k, v in g.items():
            for elt in v:
                r1 = self.__path_compression(parent, k - 1)
                r2 = self.__path_compression(parent, elt[0] - 1)
                parent = self.__union(parent, r1, r2)
        return parent

    def __path_compression(self, parent, i):
        '''Path compression for the union-find algorithm'''
        x = i
        while parent[x] >= 0:
            x = parent[x]
        root = x
        x = i
        while parent[x] > 0:
            y = parent[x]
            parent[x] = root
            x = y
        return root

    def __union(self, parent, r1, r2):
        '''Union of two sets for the union-find algorithm'''
        if r1 != r2:
            if parent[r1] > parent[r2]:
                parent[r2] += parent[r1]
                parent[r1] = r2
            else:
                parent[r1] += parent[r2]
                parent[r2] = r1
        return parent
