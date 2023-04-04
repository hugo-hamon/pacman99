from ...utils.genetic_iterator import GeneticIterator
from ...utils.genetic_buffer import GeneticBuffer
from random import choice, randint, random
from ...game.maze.maze import Maze
from typing import List, Union
from ...game.game import Game
from ...config import Config
import multiprocessing
import time


def breed(mother: str, father: str) -> str:
    """Breed two genetic iterators and return a child."""
    father_length = randint(0, min(len(father), 5))
    mother_length = len(mother) - father_length
    return mother[:mother_length] + father[:father_length]


def breed3(mother: str, father: str, slice_idx1, slice_idx2) -> str:
    """Breed two individuals to create a new individual using double breeding."""
    if slice_idx1 > slice_idx2:
        slice_idx1, slice_idx2 = slice_idx2, slice_idx1
    return mother[:slice_idx1] + father[slice_idx1:slice_idx2] + mother[slice_idx2:]


def clone(father: str) -> str:
    """Clone an individual."""
    return father[:]


MOVES = ["n", "s", "e", "w"]


class GeneticManager():
    """Class allowing multiple games to be played at the same time with genetic algorithms"""

    def __init__(self, config: Config, game_nb: int, maze: Maze):
        self.config = config
        self.maze = maze
        self.games: List[Game] = []
        self.game_nb = game_nb
        self.movesList = [""] * game_nb
        self.run_result = []
        self.generation = 0
        self.graded_retain_count = int(
            self.config.genetic.population_size *
            self.config.genetic.graded_retain_percentage
        )
        # TODO paramètre genBuffer dans les settings
        self.genBuffer = 5
        self.buffer = GeneticBuffer(self.genBuffer, self.config, self.maze)

    def setStartingMoves(self, moves: str):
        self.movesList = [moves] * self.game_nb

    def set_random_starting_moves(self):
        self.movesList = ["".join([choice(MOVES) for _ in range(5)])
                          for _ in range(self.game_nb)]

    def get_run_result(self):
        return self.run_result

    def get_generation(self) -> int:
        return self.generation

    def reset(self):
        """Reset before a new run"""
        self.games = []
        self.run_result = []

    def run(self) -> None:
        self.reset()
        # TODO mettre en paramètre le nombre de processus
        n = 8
        with multiprocessing.Pool(processes=n) as pool:
            self.games = pool.map(
                self.run_single_game, self.movesList, int(self.game_nb / n / 2) + 1)

        for game in self.games:
            dist, score = game.pacman.get_distance(), game.score
            is_dead, is_win = game.pacman.get_lives(
            ) != self.config.game.pacman_lives, game.is_game_won()
            self.run_result.append(
                {"dist": dist, "score": score, "is_dead": is_dead, "is_win": is_win})
        self.buffer.add(self.games, self.movesList)

    def run_single_game(self, moves: str) -> Game:
        game, movesLeft = self.buffer.get_single(moves)
        if movesLeft != "":
            iterator = GeneticIterator(movesLeft)
            game.set_control_func(iterator.getNextMove)
            game.run()
        return game

    def is_winner(self) -> bool:
        """Return if there is a winner in the games"""
        return next((True for game in self.games if game.is_game_won()), False)

    def get_winner(self) -> Union[str, None]:
        """Return the winner if there is one"""
        return next((self.movesList[k] for k, game in enumerate(self.games)
                     if game.is_game_won()), None)

    def get_fitness(self) -> List[float]:
        """Return the fitness of each game"""
        # use yield to return a generator
        return [
            result["score"] - result["dist"] -
            (result["is_dead"] * 10000) + (result["is_win"] * 200000)
            for result in self.run_result
        ]

    # Evolution de la population

    def select_population(self) -> None:
        """Select a random individual from the population."""
        new_population = []
        tournament_size = 5
        fitness = self.get_fitness()
        sort = sorted(zip(fitness, self.movesList),
                      key=lambda x: x[0], reverse=True)
        for _ in range(self.graded_retain_count):
            competitors = [choice(sort) for _ in range(tournament_size)]
            competitors.sort(key=lambda x: x[0], reverse=True)
            new_population.append(competitors[0][1])

        self.movesList = new_population

    def crossover_population(self) -> None:
        parents = self.movesList
        desired_length = self.config.genetic.population_size - len(parents)
        children = []
        if len(parents) < 2:
            raise ValueError("graded_retain_percentage is too low.")
        while len(children) < desired_length:
            mother = choice(parents)
            father = choice(parents)
            if mother != father:
                slice_idx1 = randint(0, len(mother))
                slice_idx2 = randint(0, len(mother))
                children.extend((
                    breed3(mother, father, slice_idx1, slice_idx2),
                    breed3(mother, father, slice_idx1, slice_idx2),
                ))
            """
            father = choice(parents)
            children.append(clone(father))
            """
        self.movesList.extend(children)

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for k, moves in enumerate(self.movesList):
            new_moves = choice(MOVES)
            # Mutate the individual.
            if random() <= self.config.genetic.mutation_chance:
                moves = self.mutate_individual(moves)
            self.movesList[k] = moves

    def mutate_individual(self, individual: str) -> str:
        """Mutate the individual according to the mutation chance."""
        # Mutate the individual.
        if not individual:
            return individual
        mutation = randint(1, 2)
        index1 = randint(0, len(individual) - 1)
        index2 = randint(0, len(individual) - 1)
        if mutation == 1:
            gene1 = individual[index1]
            gene2 = individual[index2]
            return (
                individual[:index1] + gene2 + individual[index1 + 1: index2]
                + gene1 + individual[index2 + 1:]
            )
        else:
            if index1 > index2:
                index1, index2 = index2, index1
            return (
                individual[:index1] +
                individual[index1:index2][::-1] + individual[index2:]
            )

    def evolve_population(self) -> None:
        """Evolve the population."""
        self.run()
        self.select_population()
        print("The best individual has a fitness of: ", self.get_fitness()[0])
        print("This move are", self.movesList[0])
        self.crossover_population()
        self.mutate_population()
        self.generation += 1