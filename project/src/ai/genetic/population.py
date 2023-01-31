from .individual import Individual
from random import choice, randint, random
import numpy as np
from typing import List, Union
from ...config import Config
from ...game.maze.maze import Maze

from ...graphics.sounds import Sounds


def breed(mother: Individual, father: Individual) -> Individual:
    """Breed two individuals to create a new individual using hugo's breeding."""
    mother_moves = mother.get_genes()[:randint(0, len(mother.get_genes()))]
    father_moves = father.get_genes()[randint(0, len(father.get_genes())):]
    moves = mother_moves + father_moves
    child = Individual()
    child.set_genes(moves)
    return child


def breed2(mother: Individual, father: Individual, slice_idx) -> Individual:
    """Breed two individuals to create a new individual using simple breeding."""
    mother_moves = mother.get_genes()[:slice_idx]
    father_moves = father.get_genes()[slice_idx:]
    moves = mother_moves + father_moves
    child = Individual()
    child.set_genes(moves)
    return child


def breed3(mother: Individual, father: Individual, slice_idx1, slice_idx2) -> Individual:
    """Breed two individuals to create a new individual using double breeding."""
    if slice_idx1 > slice_idx2:
        slice_idx1, slice_idx2 = slice_idx2, slice_idx1
    moves = mother.get_genes()[:slice_idx1] + father.get_genes()[
        slice_idx1:slice_idx2] + mother.get_genes()[slice_idx2:]
    child = Individual()
    child.set_genes(moves)
    return child


MOVES = ["n", "s", "e", "w"]


class Population:

    def __init__(self, config: Config, sounds: Sounds, maze: Maze) -> None:
        self.config = config
        self.sounds = sounds
        self.population: List[Individual] = []
        self.graded_retain_count = int(
            self.config.genetic.population_size *
            self.config.genetic.graded_retain_percentage
        )
        self.generation = 0
        self.maze = maze

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
        for individual in self.population:
            res = ""
            for _ in range(20):
                res += choice(MOVES)
            individual.set_genes(res)

    def select_by_rank(self) -> None:
        """Select the population by rank."""
        self.population.sort(
            key=lambda individual: individual.get_fitness(), reverse=True)
        self.population = self.population[:self.graded_retain_count]

    def select_by_roulette(self) -> None:
        """Select the population by roulette."""
        segments = np.ones(len(self.population))
        for i in range(1, len(self.population)):
            segments[i] = (segments[i - 1] +
                           self.population[i].get_fitness() + 1)
        new_population = []
        for _ in range(self.graded_retain_count - 5):
            rand = randint(0, int(segments[-1]))
            for idx, segment in enumerate(segments):
                if rand <= segment:
                    new_population.append(self.population[idx])
                    break
        self.population = new_population

    def select_by_tournament(self) -> None:
        """Select the population by tournament."""
        new_population = []
        tournament_size = 5
        for _ in range(self.graded_retain_count):
            competitors = []
            for _ in range(tournament_size):
                competitors.append(choice(self.population))
            competitors.sort(
                key=lambda individual: individual.get_fitness(), reverse=True)
            new_population.append(competitors[0])
        self.population = new_population

    def select_population(self) -> None:
        """Select the population."""
        match self.config.genetic.selection_type:
            case "rank":
                self.select_by_rank()
            case "roulette":
                self.select_by_roulette()
            case "tournament":
                self.select_by_tournament()
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
                slice_idx1 = randint(0, len(mother.get_genes()))
                slice_idx2 = randint(0, len(mother.get_genes()))
                children.append(breed3(mother, father, slice_idx1, slice_idx2))
                children.append(breed3(mother, father, slice_idx1, slice_idx2))
        self.population.extend(children)

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for individual in self.population:
            # Extend the length of the genes by one.
            individual_genes = individual.get_genes()
            individual_genes += choice(MOVES)
            individual.set_genes(individual_genes)
            # Mutate the individual.
            if random() <= self.config.genetic.mutation_chance:
                individual.mutate()

    def evolve_population(self) -> None:
        """Evolve the population."""
        queue = []
        for individual in self.population:
            self.maze.reset()
            individual.play(self.config, self.sounds, maze=self.maze)
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
