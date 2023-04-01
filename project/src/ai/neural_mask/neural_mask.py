from ...graphics.sounds import Sounds
from ...game.maze.maze import Maze
from .population import Population
from ...config import Config
from .mask import Mask
import time


class NeuralMask:

    def __init__(self, config: Config, sounds: Sounds, maze: Maze) -> None:
        self.config = config
        self.sounds = sounds
        self.maze = maze

        self.population = Population(config=config, sounds=sounds, maze=maze)

    def run(self) -> None:
        """Run the neural mask algorithm."""
        self.population.generate_population(
            population_size=self.config.neural_mask.population_size
        )
        start_time = time.time()
        generation_number = 0
        while not self.population.is_solution_found():
            self.population.evolve_population()
            print(
                f"Generation: {generation_number}, Time: {time.time() - start_time:.2f}")
            generation_number += 1
        winner = self.population.get_winner()
        if winner is not None:
            print(
                f"Solution found at generation {generation_number} in \
                {time.time() - start_time: .2f} seconds"
            )
            self.write_solution(solution=winner)

    def write_solution(self, solution: Mask) -> None:
        """Write the solution to a file."""
        with open(self.config.neural_mask.mask_path, "w") as file:
            file.write(str(solution))
