from random import choice, randint, random
from .policy_agent import PolicyAgent
from typing import List, Union, Dict
from ...game.maze.maze import Maze
from ...game.game import Game
from ...config import Config
from copy import deepcopy
import multiprocessing
import numpy as np

VALUES_COUNT = 6

class PolicyTrain:

    def __init__(self, config: Config, maze: Maze):
        self.config = config
        self.maze = maze
        # TODO paramètre game_nb dans les settings
        self.game_nb = config.policy.population_size
        self.vector_list = [[]] * self.game_nb
        self.run_result = {}
        self.generation = 0
        self.max_fitness = 0

        # TODO paramètre graded_retain_percentage dans les settings
        self.graded_retain_count = int(
            self.config.policy.population_size *
            self.config.policy.graded_retain_percentage
        )

    def set_starting_values(self, values: List[float]) -> None:
        self.vector_list = [values] * self.game_nb

    def set_random_starting_values(self):
        self.vector_list = [[random() for _ in range(VALUES_COUNT)]
                            for _ in range(self.game_nb)]

    def get_run_result(self) -> Dict[float, List[List[float]]]:
        return self.run_result

    def get_generation(self) -> int:
        return self.generation

    def run(self) -> Union[List[float], None]:
        """
        self.run_result = {}
        for k in range(self.game_nb):
            policy_agent = PolicyAgent(self.vector_list[k])
            game = Game(self.config, deepcopy(self.maze),
                        policy_agent.get_policy_agent_move)
            game.run()
            # dist, score = game.pacman.get_distance(), game.score
            ratio = game.maze.get_remain_dots() / game.maze.get_total_dots()
            is_win = game.is_game_won()
            if is_win:
                return self.vector_list[k]
            result = self.get_fitness(ratio, is_win)
            if result in self.run_result:
                self.run_result[result].append(self.vector_list[k])
            else:
                self.run_result[result] = [self.vector_list[k]]
        return None
        """
        # Multiprocessing
        n = 8
        temp_result = []
        with multiprocessing.Pool(processes=n) as pool:
            temp_result = pool.map(self.run_game, self.vector_list, int(self.game_nb / n / 2) + 1)
        for k in range(self.game_nb):
            if temp_result[k] >= 1:
                return self.vector_list[k]
            if temp_result[k] in self.run_result:
                self.run_result[temp_result[k]].append(self.vector_list[k])
            else:
                self.run_result[temp_result[k]] = [self.vector_list[k]]
        return None
        

    def run_game(self, vector: List[float]) -> float:
        policy_agent = PolicyAgent(vector)
        game = Game(self.config, deepcopy(self.maze),
                    policy_agent.get_policy_agent_move)
        game.run()
        ratio = game.maze.get_remain_dots() / game.maze.get_total_dots()
        return 1 if (is_win := game.is_game_won()) else self.get_fitness(ratio, is_win)

    def get_fitness(self, ratio: float, is_win: bool) -> float:
        """Return the fitness of one game"""
        # use yield to return a generator
        return 1 - ratio + is_win

    # Evolution de la population
    def select_population(self) -> None:
        """Select a random individual from the population."""
        new_population = []
        tournament_size = 5
        sort = sorted(self.run_result.items(), reverse=True)
        for _ in range(self.graded_retain_count):
            competitors = []
            for _ in range(tournament_size):
                random_fitness = choice(sort)
                competitors.append(
                    (random_fitness[0], choice(random_fitness[1])))
            competitors.sort(reverse=True)
            new_population.append(competitors[0][1])

        self.vector_list = new_population

    def crossover_population(self) -> None:
        parents = self.vector_list
        children = []
        desired_length = self.config.policy.population_size - self.graded_retain_count
        while len(children) < desired_length:
            mother = choice(parents)
            father = choice(parents)
            if mother != father:
                pattern = np.array([choice([0.0, 1.0]) for _ in range(VALUES_COUNT)])
                new_child = np.array((mother * pattern) + father * (1 - pattern))
                children.append(new_child.tolist())
        self.vector_list.extend(children)


    def mutate_population(self) -> None:
        """Mutate the population according to the mutation chance."""
        for k in range(len(self.vector_list)):
            if random() <= self.config.policy.mutation_chance:
                self.vector_list[k][randint(0, VALUES_COUNT-1)] = random()

    def evolve_population(self) -> Union[List[float], None]:
        """Evolve the population."""
        print(f"Generation {self.generation}")
        if run_result := self.run():
            return run_result
        # print(self.vector_list)
        max_score = max(self.run_result.keys())
        print(f"Le meilleur score est : {max_score}")
        if max_score > self.max_fitness:
            self.max_fitness = max_score
            print("Le nouveau vecteur gagnant est : ", self.run_result[max_score][0])
        self.select_population()
        self.crossover_population()
        self.mutate_population()
        self.generation += 1
        return None


class PolicyTrainManager:

    def __init__(self, config: Config, maze: Maze) -> None:
        self.config = config
        self.policy_train = PolicyTrain(config, maze)

    def run(self) -> None:
        """Run the policy train."""
        self.policy_train.set_random_starting_values()
        train_result = None
        while train_result is None:
            train_result = self.policy_train.evolve_population()
        print("Le vecteur gagnant est : ", train_result)
