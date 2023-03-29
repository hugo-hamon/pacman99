from .maze.random_maze_factory import RandomMazeFactory
from ..graphics.graphic import GraphicGame
from ..ai.genetic.genetic import Genetic
from ..graphics.sounds import Sounds
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
        if self.config.user.enable_graphics:
            game = GraphicGame(config=self.config, sounds=sounds, maze=maze)
        else:
            game = Game(config=self.config, maze=maze)
        if self.config.genetic.genetic_enable:
            genetic = Genetic(config=self.config, sounds=sounds)
            # genetic.run()
        if self.config.user.enable_graphics:
            game.start()

    # TODO

    def reset(self) -> None:
        """Reset the app"""
        pass
