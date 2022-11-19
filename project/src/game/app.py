from ..graphics.graphic import Graphic
from ..config import Config
from .game import Game
from .maze.random_maze_factory import RandomMazeFactory

WIDTH = 30
HEIGHT = 30

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

    def create_random_maze(self) -> None:
        """Create a random maze"""
        RandomMazeFactory(width=WIDTH, height=HEIGHT, intersection_step=3).create()