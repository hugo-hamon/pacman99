from ..ai.genetic.genetic import Genetic
from ..graphics.graphic import Graphic
from ..graphics.sounds import Sounds
from ..config import Config
from .game import Game
from ..game.maze.maze import Maze
from ..game.maze.random_maze_factory import RandomMazeFactory
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
        game = Game(config=self.config, sounds=sounds, maze=maze)
        if self.config.genetic.genetic_enable:
            genetic = Genetic(config=self.config, sounds=sounds, maze=maze)
            genetic.run()
        if self.config.user.enable_graphics:
            graphic = Graphic(config=self.config, game=game, sounds=sounds)
            graphic.start()
    # TODO

    def reset(self) -> None:
        """Reset the app"""
        pass
