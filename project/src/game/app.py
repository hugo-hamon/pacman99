from ..game.maze.random_maze_factory import RandomMazeFactory
from ..ai.neural_network import function2
from ..ai.genetic.genetic import Genetic
from ..graphics.graphic import Graphic
from ..graphics.sounds import Sounds
from ..ai.policy import policy_train
from ..game.maze.maze import Maze
from ..config import Config
from .game import Game


MOVE_PATH = "moves.txt"


class App:

    def __init__(self, config: Config) -> None:
        self.config = config

    def run(self) -> None:
        """Run the app"""
        sounds = Sounds()
        path = self.config.graphics.maze_path
        if self.config.user.enable_random_maze:
            RandomMazeFactory(self.config).create()
            path = self.config.maze.random_maze_path
        maze = Maze(path)
        
        if self.config.policy.train_enable:
            policy_train.train(self.config, sounds)
        if self.config.neural.train_enable:
            function2.train(self.config, sounds, maze=maze)
        if self.config.genetic.genetic_enable:
            genetic = Genetic(config=self.config, sounds=sounds, maze=maze)
            # genetic.run()
        game = Game(config=self.config, sounds=sounds, maze=maze)
        if self.config.user.enable_graphics:
            graphic = Graphic(config=self.config, game=game, sounds=sounds)
            graphic.start()
            

    def reset(self) -> None:
        """Reset the app"""
        pass
