from .maze.random_maze_factory import RandomMazeFactory
from ..utils.eventBroadcast import EventBroadcast
from typing import List, Tuple, Union
from .maze.maze import Maze
from ..config import Config
import math
from .game import Game
from ..graphics.sounds import Sounds

class GeneticGame():
    """Class allowing a game controlled by genetic algorithm"""
    def __init__(self, config: Config, sounds: Sounds=None) -> None:
        """If sounds is set creates a graphic game otherwise creates a normal game"""
        self.config = config
        path = self.config.graphics.maze_path
        if self.config.user.enable_random_maze:
            RandomMazeFactory(self.config).create()
            path = self.config.maze.random_maze_path
        self.maze = Maze(path)
        self.games = Game(config, self.maze, getNextMove) if 
        self.movesList = [[]] * maze_Nb
        #Initialiser Buffer?
    
    def setMovements(self, movesList: List):
        assert(len(movesList) == len(self.movesList))
        self.moveList = movesList

    def runGame(self):
        #TODO Do buffer shenanigans
        """Résumé : Buffer 
                    Début parallélisation
                    On récupère les games buffered ou les games proches
                    On run les games de ce qui reste et on les récupères
                    Fin parallélisation
                    On met toute les games dans le buffer
                    """
        return self.games

    def getNextMove(self, _):

