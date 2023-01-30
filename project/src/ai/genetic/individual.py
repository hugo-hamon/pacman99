from ...graphics.sounds import Sounds
from typing import Dict, Union
from ...game.game import Game
from ...config import Config
from ...game.maze.maze import Maze

from random import choice, randint

class Individual:

    def __init__(self, distance=0, score=0, dead=False, won=False, game=None) -> None:
        self.distance = distance
        self.genes = ""
        self.score = score
        self.dead = dead
        self.won = won
        self.game = game

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

    def get_fitness(self) -> float:
        """Get the fitness of the individual."""
        return (self.score) / (self.dead * 10000 + 1) + (self.won * 100000) 

    # Commands
    def set_genes(self, genes: str) -> None:
        """Set the genes of the individual."""
        self.genes = genes

    def mutate(self) -> None:
        '''Mutate the individual.'''
        mutation = randint(1, 2)
        match mutation:
            case 1:
                self.__mutate_by_invert()
            case 2:
                self.__mutate_by_invert_order()

    def __mutate_by_shift(self) -> None:
        """Mutate the individual by shifting a gene."""
        if len(self.genes) == 0:
            return
        index = randint(0, len(self.genes) - 1)
        gene = self.genes[index]
        self.genes = self.genes[:index] + self.genes[index + 1:] + gene

    def __mutate_by_invert(self) -> None:
        '''Mutate the individual by inverting two genes.'''
        if len(self.genes) == 0:
            return
        index1 = randint(0, len(self.genes) - 1)
        index2 = randint(0, len(self.genes) - 1)
        gene1 = self.genes[index1]
        gene2 = self.genes[index2]
        self.genes = self.genes[:index1] + gene2 + self.genes[index1 + 1:index2] + gene1 + self.genes[index2 + 1:]

    def __mutate_by_invert_order(self) -> None:
        '''Mutate the individual by inverting the order of the genes.'''
        if len(self.genes) == 0:
            return
        index1 = randint(0, len(self.genes) - 1)
        index2 = randint(0, len(self.genes) - 1)
        if index1 > index2:
            index1, index2 = index2, index1
        self.genes = self.genes[:index1] + self.genes[index1:index2][::-1] + self.genes[index2:]

    def play(self, config: Config, sounds: Sounds, maze: Maze) -> None:
        """Play the game with the individual."""
        game = Game(config=config, sounds=sounds, maze=maze)
        self.distance, self.score, self.dead, self.won, self.nb_remain_dots = game.run_with_movement(
            movements=self.genes
        )
        # print("Dots reamining: ", game.get_maze().get_total_remain_dots())
