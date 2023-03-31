from __future__ import annotations
from ..game.direction import Direction
from ..game.game import Game


class GeneticIterator:

    def __init__(self) -> None:
        self.moves = ""
        self.index = 0

    def set_moves(self, moves: str) -> None:
        self.moves = moves
        self.index = 0

    def getNextMove(self, game: Game) -> Direction:
        while self.index < len(self.moves):
            self.direction = Direction.from_string(
                self.moves[self.index])
            self.index += 1
            if not game.pacman.is_wall(self.direction):
                return self.direction
        return Direction.NONE
    
    def __eq__(self, other: GeneticIterator) -> bool:
        return self.moves == other.moves
    
    def startswith(self, other: GeneticIterator) -> bool:
        return self.moves.startswith(other.moves)

    def __hash__(self) -> int:
        return self.moves.__hash__()