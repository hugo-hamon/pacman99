from ...utils.genetic_iterator import GeneticIterator
from ...utils.genetic_buffer import GeneticBuffer
from random import choice, randint, random
from ...game.maze.maze import Maze
from typing import List, Union
from ...game.game import Game
from ...config import Config
import multiprocessing


def breed(mother: GeneticIterator, father: GeneticIterator) -> GeneticIterator:
    """Breed two genetic iterators and return a child."""
    father_length = randint(0, min(len(father.moves), 5))
    mother_length = len(mother.moves) - father_length
    moves = mother.moves[:mother_length] + \
        father.moves[:father_length]
    child = GeneticIterator()
    child.set_moves(moves)
    return child


def breed3(mother: GeneticIterator, father: GeneticIterator, slice_idx1, slice_idx2) -> GeneticIterator:
    """Breed two individuals to create a new individual using double breeding."""
    if slice_idx1 > slice_idx2:
        slice_idx1, slice_idx2 = slice_idx2, slice_idx1
    moves = mother.moves[:slice_idx1] + father.moves[
        slice_idx1:slice_idx2] + mother.moves[slice_idx2:]
    child = GeneticIterator()
    child.set_moves(moves)
    return child


def clone(father: GeneticIterator) -> GeneticIterator:
    """Clone an individual."""
    moves = father.moves
    child = GeneticIterator()
    child.set_moves(moves)
    return child


MOVES = ["n", "s", "e", "w"]


class GeneticManager():
    """Class allowing multiple games to be played at the same time with genetic algorithms"""

    def __init__(self, config: Config, game_nb: int, maze: Maze):
        self.config = config
        self.maze = maze
        self.games: List[Game] = []
        self.game_nb = game_nb
        self.geneticIterators = [GeneticIterator() for _ in range(game_nb)]
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
        for geneticIterator in self.geneticIterators:
            geneticIterator.set_moves(moves)

    def set_random_starting_moves(self):
        for geneticIterator in self.geneticIterators:
            geneticIterator.set_moves(
                "".join([choice(MOVES) for _ in range(5)]))

    def get_run_result(self):
        return self.run_result

    def get_generation(self) -> int:
        return self.generation

    def reset(self):
        """Reset before a new run"""
        self.games = []
        self.run_result = []

    def run(self) -> None:
        # TODO Do buffer shenanigans
        """Résumé : Buffer 
                    Début parallélisation
                    On récupère les games buffered ou les games proches
                    On run les games de ce qui reste et on les récupères
                    Fin parallélisation
                    On met toute les games dans le buffer
                    """
        self.reset()
        # TODO mettre en paramètre le nombre de processus
        n = 8
        with multiprocessing.Pool(processes=n) as pool:
            self.games = pool.map(
                self.run_single_game, self.geneticIterators, int(self.game_nb / n / 2) + 1)

        for game in self.games:
            dist, score = game.pacman.get_distance(), game.score
            is_dead, is_win = game.pacman.get_lives(
            ) != self.config.game.pacman_lives, game.is_game_won()
            self.run_result.append(
                {"dist": dist, "score": score, "is_dead": is_dead, "is_win": is_win})
        self.buffer.add(self.games, self.geneticIterators)

    def run_single_game_with_buffer(self, genetic_iterator: GeneticIterator) -> Game:
        game, new_genetic_iterator = self.buffer.get_single(genetic_iterator)
        if new_genetic_iterator is not None and genetic_iterator == new_genetic_iterator:
            return game
        game.run()

        return game

    def run_single_game(self, genetic_iterator: GeneticIterator) -> Game:
        # TODO Remplacer par l'implémentation propre quand Game est refait
        game = Game(self.config, self.maze, genetic_iterator.getNextMove)
        game.run()
        return game

    def is_winner(self) -> bool:
        """Return if there is a winner in the games"""
        return next((True for game in self.games if game.is_game_won()), False)

    def get_winner(self) -> Union[GeneticIterator, None]:
        """Return the winner if there is one"""
        return next((self.geneticIterators[k] for k, game in enumerate(self.games)
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
        sort = sorted(zip(fitness, self.geneticIterators),
                      key=lambda x: x[0], reverse=True)
        for _ in range(self.graded_retain_count):
            competitors = [choice(sort) for _ in range(tournament_size)]
            competitors.sort(key=lambda x: x[0], reverse=True)
            new_population.append(competitors[0][1])

        self.geneticIterators = new_population

    def crossover_population(self) -> None:
        parents = self.geneticIterators
        desired_length = self.config.genetic.population_size - len(parents)
        children = []
        if len(parents) < 2:
            raise ValueError("graded_retain_percentage is too low.")
        while len(children) < desired_length:
            mother = choice(parents)
            father = choice(parents)
            if mother != father:
                slice_idx1 = randint(0, len(mother.moves))
                slice_idx2 = randint(0, len(mother.moves))
                children.extend((
                    breed3(mother, father, slice_idx1, slice_idx2),
                    breed3(mother, father, slice_idx1, slice_idx2),
                ))
        self.geneticIterators.extend(children)

    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for iterator in self.geneticIterators:
            iterator_genes = iterator.moves
            iterator_genes += choice(MOVES)
            iterator.set_moves(iterator_genes)
            # Mutate the individual.
            if random() <= self.config.genetic.mutation_chance:
                self.mutate_individual(iterator)

    def mutate_individual(self, individual: GeneticIterator) -> None:
        """Mutate the individual according to the mutation chance."""
        # Mutate the individual.
        if len(individual.moves) == 0:
            return
        mutation = randint(1, 2)
        index1 = randint(0, len(individual.moves) - 1)
        index2 = randint(0, len(individual.moves) - 1)
        if mutation == 1:
            gene1 = individual.moves[index1]
            gene2 = individual.moves[index2]
            individual.moves = individual.moves[:index1] + gene2 + individual.moves[index1 + 1:index2] + \
                gene1 + individual.moves[index2 + 1:]
        else:
            if index1 > index2:
                index1, index2 = index2, index1
            individual.moves = individual.moves[:index1] + individual.moves[index1:index2][::-1] + \
                individual.moves[index2:]

    def evolve_population(self) -> None:
        """Evolve the population."""
        self.run()
        self.select_population()
        print("The best individual has a fitness of: ", self.get_fitness()[0])
        print("This move are", self.geneticIterators[0].moves)
        self.crossover_population()
        self.mutate_population()
        self.generation += 1
