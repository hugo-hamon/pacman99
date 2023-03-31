from ..utils.genetic_iterator import GeneticIterator
from ..graphics.graphic_game import GraphicGame
from ..graphics.sounds import Sounds
from .maze.maze import Maze
from ..config import Config
from typing import Union
from .game import Game

class GeneticGame():
    """Class allowing a game controlled by genetic algorithm"""

    def __init__(self, config: Config, maze: Maze, sounds: Union[Sounds, None] = None) -> None:
        """If sounds is set creates a graphic game otherwise creates a normal game"""
        self.config = config
        self.maze = maze
        self.geneticIterator = GeneticIterator()
        if sounds is None:
            self.games = Game(config, self.maze, self.geneticIterator.getNextMove)
        else:
            self.games = GraphicGame(config, sounds, self.maze, self.geneticIterator.getNextMove)

    def setMovements(self, moves: str) -> None:
        self.geneticIterator.set_moves(moves)

    def run(self):
        return self.games.run()