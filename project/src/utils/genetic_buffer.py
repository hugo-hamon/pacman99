from ..utils.genetic_iterator import GeneticIterator
from ..game.maze.maze import Maze
from typing import List, Tuple
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

    def get(self, genetic_iterators: List[GeneticIterator]) -> List[Tuple[Game, GeneticIterator]]:
        """Return vector of games with the closest moves"""
        return [(self.get_single(genetic_iterator)) for genetic_iterator in genetic_iterators]

    def get_single(self, genetic_iterator: GeneticIterator) -> Tuple[Game, GeneticIterator]:
        """Return a game with the closest move"""
        for data in self.buffer:
            if genetic_iterator in data:
                return data[genetic_iterator], genetic_iterator
        for data in self.buffer:
            for key in data:
                if key.startswith(genetic_iterator):
                    key.moves = genetic_iterator.moves
                    return deepcopy(data[key]), key
        genetic_iterator = GeneticIterator()
        genetic_iterator.set_moves(genetic_iterator.moves)
        return Game(self.config, deepcopy(self.maze), genetic_iterator.getNextMove), genetic_iterator