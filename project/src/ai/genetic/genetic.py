from .geneticManager import GeneticManager
from ...game.maze.maze import Maze
from ...config import Config


class Genetic:

    def __init__(self, config: Config, maze: Maze) -> None:
        self.config = config
        self.genetic_manager = GeneticManager(config, self.config.genetic.population_size, maze)

    def run(self) -> None:
        """Run the genetic algorithm."""
        self.genetic_manager.set_random_starting_moves()
        while not self.genetic_manager.is_winner():
            self.genetic_manager.evolve_population()
            print("Generation: ", self.genetic_manager.get_generation())
        winner = self.genetic_manager.get_winner()
        if winner is not None:
            print("Solution found: ", winner)
            self.write_solution(solution=winner)
        else:
            print("No solution found.")

    def write_solution(self, solution: str) -> None:
        """Write the solution to a file."""
        with open(self.config.genetic.move_path, "w") as file:
            file.write(solution)
