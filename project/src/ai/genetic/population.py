from ...graphics.sounds import Sounds
from .individual import Individual
from random import choice, randint
from typing import List, Union
from ...config import Config


def breed(mother: Individual, father: Individual) -> Individual:
    """Breed two individuals to create a new individual."""
    mother_moves = mother.get_genes()[:randint(0, len(mother.get_genes()))]
    father_moves = father.get_genes()[randint(0, len(father.get_genes())):]
    moves = mother_moves + father_moves
    child = Individual()
    child.set_genes(moves)
    return child


MOVES = ["n", "s", "e", "w"]


class Population:

    def __init__(self, config: Config, sounds: Sounds) -> None:
        self.config = config
        self.sounds = sounds
        self.population: List[Individual] = []
        self.graded_retain_count = int(
            self.config.genetic.population_size *
            self.config.genetic.graded_retain_percentage
        )
        self.generation = 0

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

    def get_generation(self) -> int:
        """Get the generation."""
        return self.generation

    # Commands
    def generate_population(self, population_size: int) -> None:
        """Generate a population of random individuals."""
        self.population = [Individual() for _ in range(population_size)]

    def select_by_rank(self) -> None:
        """Select the population by rank."""
        self.population.sort(
            key=lambda individual: individual.get_fitness(), reverse=True)
        self.population = self.population[:self.graded_retain_count]

    def select_by_roulette(self) -> None:
        """Select the population by roulette."""
        return NotImplemented()

    def select_population(self) -> None:
        """Select the population."""
        match self.config.genetic.selection_type:
            case "rank":
                self.select_by_rank()
            case "roulette":
                self.select_by_roulette()
            case _:
                raise ValueError(
                    "Invalid selection type for genetic algorithm."
                    "Please use 'rank' or 'roulette'."
                )

    def crossover_population(self) -> None:
        """Crossover the population."""
        parents = self.population
        desired_length = self.config.genetic.population_size - len(parents)
        children = []
        if len(parents) < 2:
            raise ValueError("graded_retain_percentage is too low.")
        while len(children) < desired_length:
            mother = choice(parents)
            father = choice(parents)
            if mother != father:
                children.append(breed(mother, father))
        self.population.extend(children)

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for individual in self.population:
            if randint(0, 100) <= self.config.genetic.mutation_chance * 100:
                individual_genes = individual.get_genes()
                individual.set_genes(
                    individual_genes + MOVES[randint(0, len(MOVES) - 1)]
                )
            if randint(0, 100) <= self.config.genetic.mutation_chance * 100 and len(individual.get_genes()) > 0:
                individual_genes = individual.get_genes()
                slice_idx = randint(0, len(individual_genes) - 1)
                individual_genes = individual_genes[:slice_idx] + \
                    MOVES[randint(0, len(MOVES) - 1)]
                individual.set_genes(
                    individual_genes[:randint(0, len(individual_genes) - 1)]
                )

    def evolve_population(self) -> None:
        """Evolve the population."""
        queue = []
        for individual in self.population:
            individual.play(self.config, self.sounds)
        self.select_population()
        print("The best individual has a fitness of: ",
              self.population[0].get_fitness())
        print("This move are", self.population[0].get_genes())
        self.crossover_population()
        self.mutate_population()
        if len(queue) == 10:
            queue.pop(0)
            if queue[-1] == queue[0]:
                queue = []
                for individual in self.population:
                    individual.set_genes(individual.get_genes()[:-10])

        queue.append(self.population[0].get_genes())

        self.generation += 1
