from ...game.direction import Direction
from ...graphics.sounds import Sounds
from ...game.maze.maze import Maze
from random import choice, random
from typing import List, Union
from ...config import Config
from .network import Network
from .mask import Mask
import time


class Population:

    def __init__(self, config: Config, sounds: Sounds, maze: Maze) -> None:
        self.config = config
        self.sounds = sounds
        self.maze = maze

        self.population: List[Mask] = []
        self.graded_retain_count = int(
            self.config.neural_mask.population_size *
            self.config.neural_mask.graded_retain_percentage
        )

    # REQUEST
    def get_population(self) -> List[Mask]:
        """Get the population."""
        return self.population

    def is_solution_found(self) -> bool:
        """Check if the solution has been found."""
        return next((True for mask in self.get_population()
                     if mask.is_winner()), False)

    def get_winner(self) -> Union[Mask, None]:
        """Get the winner of the population."""
        return next((mask for mask in self.get_population()
                     if mask.is_winner()), None)

    # COMMANDS
    def generate_population(self, population_size: int) -> None:
        """Generate a population of random individuals."""
        self.population = [Mask(self.config, self.sounds)
                           for _ in range(population_size)]
        for mask in self.population:
            mask.randomize()

    def select_population(self) -> None:
        """Select the population by tournament."""
        new_population = []
        tournament_size = 5
        for _ in range(self.graded_retain_count):
            competitors = [choice(self.population)
                           for _ in range(tournament_size)]
            competitors.sort(
                key=lambda mask: mask.get_fitness(), reverse=True)
            new_population.append(competitors[0])
        self.population = new_population

    def crossover_population(self) -> None:
        """Crossover the population."""
        parents = self.population
        desired_length = self.config.neural_mask.population_size - len(parents)
        children = []
        if len(parents) < 2:
            raise ValueError("graded_retain_percentage is too low.")
        while len(children) < desired_length:
            mother = choice(parents)
            father = choice(parents)
            if mother != father:
                child = mother.crossover(father)
                children.append(child)
        self.population.extend(children)

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for mask in self.population:
            if random() <= self.config.neural_mask.mutation_chance:
                mask.mutate()

    def evolve_population(self) -> None:
        """Evolve the population."""
        
        for mask in self.population:
            self.maze.reset()
            mask.play(maze=self.maze)
        self.select_population()
        print(f"Best fitness: {self.population[0].get_fitness()}")
        self.crossover_population()
        self.mutate_population()
