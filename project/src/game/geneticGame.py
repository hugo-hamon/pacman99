from .maze.random_maze_factory import RandomMazeFactory
from ..utils.eventBroadcast import EventBroadcast
from typing import List, Tuple, Union
from .maze.maze import Maze
from ..config import Config
from .direction import Direction
import math
from .game import Game
from ..graphics.sounds import Sounds

class GeneticGame():
    """Class allowing a game controlled by genetic algorithm"""
    def __init__(self, config: Config, sounds: Sounds=None) -> None:
        """If sounds is set creates a graphic game otherwise creates a normal game"""
        self.config = config
        self.maze = maze
        if sounds == None:
            self.games = Game(config, self.maze, getNextMove)
        else:
            self.games = graphicGame(config, sounds, self.maze, getNextMove)
        self.moveList = []
        self.index = 0
    
    def setMovements(self, moveList: List):
        self.moveList = moveList

    def runGame(self):
        return self.games

    def getNextMove(self, game):
         while self.index < len(self.moveList):
            self.direction = Direction.from_string(self.move_list[self.move_list_index])
            self.index += 1
            if not self.is_wall(self.direction):
                return self.direction
        return Direction.NONE

