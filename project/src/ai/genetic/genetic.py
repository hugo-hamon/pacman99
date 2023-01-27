from ...graphics.sounds import Sounds
from .population import Population
from ...config import Config
from typing import List


class Genetic:

    def __init__(self, config: Config, sounds: Sounds) -> None:
        self.config = config
        self.sounds = sounds
        self.population = Population(config=config, sounds=sounds)

    def run(self) -> None:
        """Run the genetic algorithm."""
        self.population.generate_population(
            population_size=self.config.genetic.population_size
        )
        while not self.population.is_solution_found():
            self.population.evolve_population()
            print("Generation: ", self.population.get_generation())
        winner = self.population.get_winner()
        if winner is not None:
            print("Solution found: ", winner.get_genes())
            self.write_solution(solution=winner.get_genes())

    def write_solution(self, solution: str) -> None:
        """Write the solution to a file."""
        with open(self.config.genetic.move_path, "w") as file:
            file.write(solution)
