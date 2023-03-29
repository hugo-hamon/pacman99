from .maze.random_maze_factory import RandomMazeFactory
from typing import List, Tuple, Union
from .maze.maze import Maze
from ..config import Config
from .game import Game
import copy
import math


class GeneticManager():
    """Class allowing multiple games to be played at the same time with genetic algorithms"""

    def __init__(self, config: Config, game_nb: int, maze: Maze):
        self.config = config
        self.maze = maze
        self.games: List[Game] = []
        self.game_nb = game_nb
        self.moveLists = [""] * game_nb
        self.run_result = []
        # TODO paramètre nbGeneration dans les settings
        self.genBuffer = 5
        self.buffer = []

    def setMovements(self, moveLists: List[str]):
        assert (len(moveLists) == len(self.moveLists))
        self.moveLists = moveLists

    def setStartingMoves(self, moveList: str):
        self.moveLists = [moveList] * len(self.moveLists)

    def get_run_result(self):
        return self.run_result

    def runGames(self):
        # TODO Do buffer shenanigans
        """Résumé : Buffer 
                    Début parallélisation
                    On récupère les games buffered ou les games proches
                    On run les games de ce qui reste et on les récupères
                    Fin parallélisation
                    On met toute les games dans le buffer
                    """
        self.run_result = []
        for _ in range(self.game_nb):
            self.maze.reset()
            self.games.append(Game(config=self.config, maze=self.maze))
        # Run les games avec l'implémentation propre
        for k, game in enumerate(self.games):
            # TODO Remplacer par l'implémentation propre quand Game est refait
            dist, score, is_dead, is_win = game.run_with_movement(self.moveLists[k])
            self.run_result.append({"dist": dist, "score": score, "is_dead": is_dead, "is_win": is_win})
        
        self.buffer.append(copy.deepcopy(self.games))
        if len(self.buffer) > self.genBuffer:
            self.buffer.pop(0)