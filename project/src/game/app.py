from .maze.random_maze_factory import RandomMazeFactory
from ..graphics.graphic import Graphic
from ..config import Config
from .game import Game
from .maze.random_maze_factory import RandomMazeFactory


class App:

    def __init__(self, config: Config) -> None:
        self.config = config

    # TODO
    def run(self) -> None:
        """Run the app"""
        game = Game(config=self.config)
        if self.config.user.enable_graphics:
            graphic = Graphic(config=self.config, game=game)
            graphic.start()

    # TODO
    def reset(self) -> None:
        """Reset the app"""
        pass

    # pour des tests
    def get_random_maze(self, width, height) -> None:
        """Create a random maze"""
        RandomMazeFactory(width, height, intersection_step=3, density=0.05, seed= 5).create()