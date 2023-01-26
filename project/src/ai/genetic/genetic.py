from ...graphics.sounds import Sounds
from .individual import Individual
from .population import Population
from ...game.game import Game
from ...config import Config
from typing import List


def individual_fitness(self, individual: Individual) -> float:
    """Get the fitness of an individual."""
    return NotImplemented()


def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
    """Crossover two parents to create a child."""
    return NotImplemented()


class Genetic:

    def __init__(self, config: Config, sounds: Sounds) -> None:
        self.config = config
        self.sounds = sounds
        self.population = Population(config=config)

    def run(self) -> None:
        """Run the genetic algorithm."""
        self.population.generate_population(
            population_size=self.config.genetic.population_size
        )
        while not self.population.is_solution_found():
            self.population.evolve_population()
        winner = self.population.get_winner()
