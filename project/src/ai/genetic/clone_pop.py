from .individual import Individual
from random import choice, randint
from typing import List, Union
from ...config import Config
from ...graphics.sounds import Sounds

MOVES = ["n", "s", "e", "w"]

def clone(father: Individual) -> Individual:
    """Create a new individual from another one."""
    moves = father.get_genes()[:]
    child = Individual()
    child.set_genes(moves)
    return child

class Clone_pop:

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
        while len(children) < desired_length:
            father = choice(parents)
            children.append(clone(father))
        self.population.extend(children)

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for individual in self.population:
            if randint(0, 100) <= self.config.genetic.mutation_chance * 100:
                individual_genes = individual.get_genes()
                randx = randint(0, 100)  
                if randx <= self.config.genetic.addition_chance * 100:
                    individual_genes = individual_genes + MOVES[randint(0, len(MOVES) - 1)]
                    
                elif randx <= (self.config.genetic.replacement_chance +
                             self.config.genetic.mutation_chance) * 100:
                    # Selects one of the last 10 moves to replace with a random move
                    replacement_idx = randint((max(0,len(individual_genes) - 10)),
                                              len(individual_genes) - 1)
                    # Replaces it
                    individual_genes[replacement_idx] = MOVES[randint(0, len(MOVES) - 1)]
                    individual.set_genes(individual_genes)
                    
                # Last option should always be True
                elif randx <= (self.config.genetic.deletion_chance +
                             self.config.genetic.replacement_chance +
                             self.config.genetic.mutation_chance) * 100:
                    slice_idx = randint(0, len(individual_genes) - 1)
                    individual_genes = individual_genes[:slice_idx] +\
                        individual_genes[slice_idx + 1:]
                individual.set_genes(individual_genes)
                
    def evolve_population(self) -> None:
        """Evolve the population."""
        for individual in self.population:
            individual.play(self.config, self.sounds)
        self.select_population()
        print("The best individual has a fitness of: ",
              self.population[0].get_fitness())
        print("This move are", self.population[0].get_genes())
        self.crossover_population()
        self.mutate_population()
        self.generation += 1
