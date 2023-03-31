from .maze.random_maze_factory import RandomMazeFactory
from ..utils.genetic_iterator import GeneticIterator
from ..graphics.graphic_game import GraphicGame
from ..ai.genetic.genetic import Genetic
from ..graphics.sounds import Sounds
from .geneticGame import GeneticGame
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
        genetic_iterator = GeneticIterator()
        genetic_iterator.set_moves("eeeennnn")
        # genetic_game = GeneticGame(config=self.config, sounds=sounds, maze=maze)
        # genetic_game.setMovements("eeeennnn")
        # genetic_game.runGame()
        if self.config.user.enable_graphics:
            game = GraphicGame(config=self.config, sounds=sounds, maze=maze, control_func=genetic_iterator.getNextMove)
        else:
            game = Game(config=self.config, maze=maze, control_func=genetic_iterator.getNextMove)
        
        if self.config.genetic.genetic_enable:
            self.run_genetic_game(maze, sounds)
        if self.config.user.enable_graphics:
            game.run()

        

    def run_genetic_game(self, maze: Maze, sounds: Sounds) -> None:
        moves = self.read_movement()
        if self.config.user.enable_graphics:
            genetic = GeneticGame(self.config, maze, sounds)
            genetic.setMovements(moves)
        else:
            genetic = Genetic(self.config, sounds)
        genetic.run()


    def read_movement(self) -> str:
        with open(self.config.genetic.move_path, "r") as f:
            return f.read()

    def reset(self) -> None:
        """Reset the app"""
        pass
