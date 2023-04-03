from ..ai.aplus.aplus_agent import get_next_move
from ..graphics.graphic_game import GraphicGame
from ..graphics.sounds import Sounds
from .maze.maze import Maze
from ..config import Config
from typing import Union
from .game import Game


class APlusGame:
    """Class allowing a game controlled by APlus"""

    def __init__(self, config: Config, maze: Maze, sounds: Union[Sounds, None] = None) -> None:
        """If sounds is set creates a graphic game otherwise creates a normal game"""
        self.config = config
        self.maze = maze
        if sounds is None:
            self.game = Game(config, self.maze, get_next_move)
        else:
            self.game = GraphicGame(
                config, sounds, self.maze, get_next_move
            )

    def run(self):
        return self.game.run()