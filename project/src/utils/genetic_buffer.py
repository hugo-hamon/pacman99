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

    def add(self, games: List[Game], movesList: List[str]) -> None:
        """Add games and moveLists to the buffer"""
        new_data = dict(zip(movesList, games))
        self.buffer.append(new_data)
        if len(self.buffer) > self.size:
            self.buffer.pop(0)

    def get(self, movesList: List[str]) -> List[Tuple[Game, str]]:
        """Return vector of games with the closest moves"""
        return [(self.get_single(moves)) for moves in movesList]

    def get_single(self, moves: str) -> Tuple[Game, str]:
        """Return a game with the closest move"""
        for data in self.buffer:
            if moves in data:
                return data[moves], ""
        
        for data in self.buffer:
            for key in data:
                if moves.startswith(key) and len(key) > 0:
                    game = deepcopy(data[key])
                    return game, moves[len(key):]
        return Game(self.config, deepcopy(self.maze), lambda _: NotImplemented), moves