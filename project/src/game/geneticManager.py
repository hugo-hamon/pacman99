from ..utils.genetic_iterator import GeneticIterator
from ..utils.genetic_buffer import GeneticBuffer
from .maze.maze import Maze
from ..config import Config
from typing import List
from .game import Game
import multiprocessing
import time


class GeneticManager():
    """Class allowing multiple games to be played at the same time with genetic algorithms"""

    def __init__(self, config: Config, game_nb: int, maze: Maze):
        self.config = config
        self.maze = maze
        self.games: List[Game] = []
        self.game_nb = game_nb
        self.geneticIterators = [GeneticIterator() for _ in range(game_nb)]
        self.run_result = []
        # TODO paramètre nbGeneration dans les settings
        self.genBuffer = 5
        self.buffer = GeneticBuffer(self.genBuffer, self.config, self.maze)

    def setStartingMoves(self, moves: str):
        for geneticIterator in self.geneticIterators:
            geneticIterator.set_moves(moves)

    def get_run_result(self):
        return self.run_result
    
    def reset(self):
        """Reset before a new run"""
        self.games = []
        self.run_result = []

    def runGames(self):
        # TODO Do buffer shenanigans
        """Résumé : Buffer 
                    Début parallélisation
                    On récupère les games buffered ou les games proches
                    On run les games de ce qui reste et on les récupères
                    Fin parallélisation
                    On met toute les games dans le buffer
                    """
        self.reset()
        # TODO mettre en paramètre le nombre de processus
        n = 8
        with multiprocessing.Pool(processes=n) as pool:
            self.games = pool.map(self.run_single_game, self.geneticIterators, int(self.game_nb / n / 2) + 1)

        for game in self.games:
            dist, score = game.pacman.get_distance(), game.score
            is_dead, is_win =  game.pacman.get_lives() != self.config.game.pacman_lives, game.is_game_won()
            self.run_result.append({"dist": dist, "score": score, "is_dead": is_dead, "is_win": is_win})
        self.buffer.add(self.games, self.geneticIterators)

    def run_single_game(self, genetic_iterator: GeneticIterator) -> Game:
        # TODO Remplacer par l'implémentation propre quand Game est refait
        game, new_genetic_iterator = self.buffer.get_single(genetic_iterator)
        if genetic_iterator == new_genetic_iterator:
            return game
        game.run()
        return game