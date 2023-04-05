from .maze.random_maze_factory import RandomMazeFactory
from ..utils.genetic_iterator import GeneticIterator
from ..graphics.graphic_game import GraphicGame
from ..ai.genetic.genetic import Genetic
from ..graphics.sounds import Sounds
from .geneticGame import GeneticGame
from ..ai.dqn.function2 import train
from .policy_game import PolicyGame
from .dqn_game import DQNGame
from .maze.maze import Maze
from ..config import Config
from .game import Game

MOVE_PATH = "moves.txt"


class App:

    def __init__(self, config: Config) -> None:
        self.config = config

    # TODO
    def run(self) -> None:
        """Run the app"""
        sounds = Sounds()
        path = self.config.graphics.maze_path
        if self.config.user.enable_random_maze:
            RandomMazeFactory(self.config).create()
            path = self.config.maze.random_maze_path
        maze = Maze(path)

        if self.config.genetic.genetic_enable:
            self.run_genetic_game(maze, sounds)
        
        # TODO: Changer ca par une classe qui gere les mouvements du joueur
        genetic_iterator = GeneticIterator()
        genetic_iterator.set_moves("")
        
        if self.config.dqn.dqn_enable:
            self.run_dqn_game(maze, sounds)

        if self.config.policy.policy_enable:
            self.run_policy(maze, sounds)
        
        if self.config.user.enable_graphics:
            game = GraphicGame(
                config=self.config, sounds=sounds, maze=maze, control_func=genetic_iterator.getNextMove
            )
        else:
            game = Game(
                config=self.config, maze=maze, control_func=genetic_iterator.getNextMove
            )
            
        if self.config.user.enable_graphics:
            game.run()

    def run_genetic_game(self, maze: Maze, sounds: Sounds) -> None:
        moves = self.read_movement()
        if self.config.user.enable_graphics:
            genetic = GeneticGame(self.config, maze, sounds)
            genetic.setMovements(moves)
        else:
            genetic = Genetic(self.config, maze)
        genetic.run()
    
    def read_movement(self) -> str:
        with open(self.config.genetic.move_path, "r") as f:
            return f.read()

    # DQN
    def run_dqn_game(self, maze: Maze, sounds: Sounds) -> None:
        if self.config.user.enable_graphics:
            dqn = DQNGame(self.config, maze, sounds)
            dqn.run()
        else:
            train(self.config, maze)

    # Policy
    def run_policy(self, maze: Maze, sounds: Sounds) -> None:
        policy = PolicyGame(self.config, maze, sounds)
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