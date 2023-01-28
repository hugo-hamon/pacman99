from ...graphics.sounds import Sounds
from typing import Dict, Union
from random import randint
from ...game.game import Game
from ...config import Config
class Individual:

    def __init__(self, distance=0, score=0, dead=False, won=False) -> None:
        self.distance = distance
        self.genes = ["n", "s", "e", "w"][randint(0, 3)]
        self.score = score
        self.dead = dead
        self.won = won

    # Request
    def get_data(self) -> Dict[str, Union[int, bool]]:
        """Get the data of the individual."""
        return {
            "distance": self.distance,
            "score": self.score,
            "dead": self.dead,
            "won": self.won
        }

    def get_genes(self) -> str:
        """Get the genes of the individual."""
        return self.genes

    def get_gene(self, index: int) -> str:
        """Get a gene of the individual."""
        if index >= len(self.genes):
            raise IndexError("Index out of range")
        return self.genes[index]

    def is_winner(self) -> bool:
        """Check if the individual is a winner."""
        return self.won

    def get_fitness(self, explore: bool = True) -> float:
        """Get the fitness of the individual."""
        if explore :
            return self.score + self.distance - (self.dead * 1000) + (self.won * 2000)
        else :
            return self.score - self.distance - (self.dead * 1000) + (self.won * 2000) 
        
    # Commands
    def set_genes(self, genes: str) -> None:
        """Set the genes of the individual."""
        self.genes = genes

    def play(self, config: Config, sounds: Sounds) -> None:
        """Play the game with the individual."""
        game = Game(config=config, sounds=sounds)
        self.distance, self.score, self.dead, self.won = game.run_with_movement(
            movements=self.genes
        )
        # print("Dots reamining: ", game.get_maze().get_total_remain_dots())
