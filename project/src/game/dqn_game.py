from ..graphics.graphic_game import GraphicGame
from ..ai.dqn.dqn_agent import ConvDQNAgent
from ..graphics.sounds import Sounds
from .maze.maze import Maze
from ..config import Config
from typing import Union
from .game import Game

class DQNGame:
    """Class allowing a game controlled by DQN"""

    def __init__(self, config: Config, maze: Maze, sounds: Union[Sounds, None] = None) -> None:
        """If sounds is set creates a graphic game otherwise creates a normal game"""
        self.config = config
        self.maze = maze
        self.agent = ConvDQNAgent(config)
        self.agent.load(self.config.dqn.output_dir + self.config.dqn.weights_path)
        if sounds is None:
            self.game = Game(config, self.maze, self.agent.get_move)
        else:
            self.game = GraphicGame(config, sounds, self.maze, self.agent.get_move)

    def run(self):
        return self.game.run()
