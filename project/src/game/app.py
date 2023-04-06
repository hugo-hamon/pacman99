from .maze.random_maze_factory import RandomMazeFactory
#from ..utils.genetic_iterator import GeneticIterator
#from ..graphics.sounds import Sounds
from .maze.maze import Maze
from ..config import Config
#from typing import Union
    
MOVE_PATH = "moves.txt"


class App:

    def __init__(self, config: Config) -> None:
        self.config = config
        if config.user.enable_graphics:
            from ..graphics.graphic_game import GraphicGame
    # TODO
    def run(self) -> None:
        """Run the app"""
        if self.config.user.enable_graphics:
            from ..graphics.sounds import Sounds
            sounds = Sounds()
        else :
            sounds = None
        path = self.config.graphics.maze_path
        if self.config.user.enable_random_maze:
            RandomMazeFactory(self.config).create()
            path = self.config.maze.random_maze_path
        maze = Maze(path)

        if self.config.genetic.genetic_enable:
            self.run_genetic_game(maze, sounds)
        
        # TODO: Ajouter une classe qui gere les mouvements du joueur

        if self.config.aplus.aplus_enable:
            self.run_aplus_game(maze, sounds)

        if self.config.dqn.dqn_enable:
            self.run_dqn_game(maze, sounds)

        if self.config.policy.policy_enable:
            self.run_policy(maze, sounds)


    def run_genetic_game(self, maze: Maze, sounds) -> None:
        moves = self.read_movement()
        if self.config.user.enable_graphics:
            from .geneticGame import GeneticGame
            genetic = GeneticGame(self.config, maze, sounds)
            genetic.setMovements(moves)
        else:
            from ..ai.genetic.genetic import Genetic
            genetic = Genetic(self.config, maze)
        genetic.run()
    
    def read_movement(self) -> str:
        with open(self.config.genetic.move_path, "r") as f:
            return f.read()

    # DQN

    def run_dqn_game(self, maze: Maze, sounds) -> None:
        if self.config.user.enable_graphics:
            from .dqn_game import DQNGame
            dqn = DQNGame(self.config, maze, sounds)
            dqn.run()
        else:
            from ..ai.dqn.function import train
            train(self.config, maze)

    # Policy
    def run_policy(self, maze: Maze, sounds) -> None:
        if self.config.user.enable_graphics:
            from .policy_game import PolicyGame
            policy = PolicyGame(self.config, maze, sounds)
        else:
            from ..ai.policy.policy_train import PolicyTrainManager
            policy = PolicyTrainManager(self.config, maze)
        policy.run()

    # Random maze
    def generate_mazes(self, n: int) -> None:
        """Generate n random mazes with same configuration but different seeds
        To configurate random mazes, see config.toml and random_maze_factory.py"""
        generator = RandomMazeFactory(self.config)
        for i in range(n):
            self.config.maze.random_maze_path = f'assets/data/mazes/maze{i}.txt'
            generator.new_seed()
            generator.create()
       

    # A+
    def run_aplus_game(self, maze: Maze, sounds) -> None:
        from .aplus_game import APlusGame
        aplus = APlusGame(self.config, maze, sounds)
        aplus.run()