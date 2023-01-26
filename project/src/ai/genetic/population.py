from .individual import Individual
from typing import List, Union
from ...config import Config


class Population:

    def __init__(self, config: Config) -> None:
        self.config = config
        self.population: List[Individual] = []
        self.graded_retain_count = int(
            self.config.genetic.population_size *
            self.config.genetic.graded_retain_percentage
        )

    # Request
    def get_population(self) -> List[Individual]:
        """Get the population."""
        return self.population

    def is_solution_found(self) -> bool:
        """Check if a solution is found."""
        return next((True for individual in self.get_population()
                     if individual.is_winner()), False)

    def get_winner(self) -> Union[Individual, None]:
        """Get the winner."""
        return next((individual for individual in self.get_population()
                     if individual.is_winner()), None)

    # Commands

    def generate_population(self, population_size: int) -> None:
        """Generate a population of random individuals."""
        return NotImplemented()

    def select_population(self) -> None:
        """Select the population according to the graded retain count."""
        self.population = self.population[:self.graded_retain_count]

    def grade_population(self) -> None:
        """Grade the population according to the fitness function."""
        return NotImplemented()

    def crossover_population(self) -> None:
        """Crossover the population."""
        return NotImplemented()

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        return NotImplemented()

    def evolve_population(self) -> None:
        """Evolve the population."""
        self.grade_population()
        self.select_population()
        self.crossover_population()
        self.mutate_population()
