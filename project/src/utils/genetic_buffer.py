from ..utils.genetic_iterator import GeneticIterator
from typing import List, Tuple, Union
from ..game.maze.maze import Maze
from ..game.game import Game
from ..config import Config
from copy import deepcopy


class GeneticBuffer:
    """Provides a way to retrieve games faster than regenerating them"""

    def __init__(self, size: int, config: Config, maze: Maze) -> None:
        self.config = config
        self.size = size
        self.maze = maze
        self.buffer = []

    def add(self, games: List[Game], genetic_iterators: List[GeneticIterator]) -> None:
        """Add games and moveLists to the buffer"""
        new_data = dict(zip(genetic_iterators, games))
        self.buffer.append(new_data)
        if len(self.buffer) > self.size:
            self.buffer.pop(0)

    def get(self, genetic_iterators: List[GeneticIterator]) -> List[Tuple[Game, Union[GeneticIterator, None]]]:
        """Return vector of games with the closest moves"""
        return [(self.get_single(genetic_iterator)) for genetic_iterator in genetic_iterators]

    def get_single(self, genetic_iterator: GeneticIterator) -> Tuple[Game, Union[GeneticIterator, None]]:
        """Return a game with the closest move"""
        for data in self.buffer:
            if genetic_iterator in data:
                return data[genetic_iterator], genetic_iterator
        
        for data in self.buffer:
            for key in data:
                if genetic_iterator.startswith(key) and len(genetic_iterator.moves) > len(key.moves) and len(key.moves) > 0:
                    game = deepcopy(data[key])
                    iterator = deepcopy(key)
                    iterator.moves = genetic_iterator.moves
                    game.control_func = iterator.getNextMove
                    return game, None
        new_iterator = GeneticIterator()
        new_iterator.set_moves(genetic_iterator.moves)
        return Game(self.config, deepcopy(self.maze), new_iterator.getNextMove), None