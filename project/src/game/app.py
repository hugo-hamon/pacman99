from ..game.maze.random_maze_factory import RandomMazeFactory
from ..ai.neural_network import function2
from ..ai.neural_mask.neural_mask import NeuralMask
from ..ai.neural_network import function
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
        game = Game(config=self.config, sounds=sounds, maze=maze)
        
        self.launch_policy(sounds)
        self.launch_neural(sounds)
        self.launch_genetic(sounds, maze)
        self.launch_neural_mask(sounds, maze)
        self.run_graphics(sounds, game)

    def launch_policy(self, sounds: Sounds) -> None:
        """Launch policy"""
        if self.config.policy.train_enable:
            policy_train.train(self.config, sounds)

    def launch_neural(self, sounds: Sounds) -> None:
        """Launch neural"""
        if self.config.neural.train_enable:
            function.train(self.config, sounds)

    def launch_genetic(self, sounds: Sounds, maze: Maze) -> None:
        """Launch genetic"""
        if self.config.genetic.genetic_enable:
            genetic = Genetic(config=self.config, sounds=sounds, maze=maze)
            # genetic.run()

    def launch_neural_mask(self, sounds: Sounds, maze: Maze) -> None:
        """Launch neural mask"""
        if self.config.neural_mask.neural_mask_enable:
            neural_mask = NeuralMask(
                config=self.config, sounds=sounds, maze=maze
            )
            neural_mask.run()

    def run_graphics(self, sounds: Sounds, game: Game) -> None:
        """Run graphics"""
        if self.config.user.enable_graphics:
            graphic = Graphic(config=self.config, game=game, sounds=sounds)
            graphic.start()
            

    def reset(self) -> None:
        """Reset the app"""
        pass
