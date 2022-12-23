from .direction import Direction
from .maze.maze import Maze
from ..config import Config
from .entities.pacman import Pacman


class Game:

    def __init__(self, config: Config) -> None:
        self.maze = Maze(file=config.graphics.maze_path)
        self.pacman = Pacman(
            self.maze, config.game.game_speed, Direction.WEST, (1, 1), config.game.pacman_lives
        )
        self.score = 0

    # REQUESTS

    def is_game_over(self) -> bool:
        """Return True if the game is over"""
        return self.is_game_won() or self.pacman.is_dead()

    def is_game_won(self) -> bool:
        """Return True if the game is won"""
        return self.maze.get_total_remain_dots() == 0

    def get_score(self) -> int:
        """Return the score"""
        return self.score

    def get_maze(self) -> Maze:
        """Return the maze"""
        return self.maze
    
    def get_pacman(self) -> Pacman:
        """Return the pacman"""
        return self.pacman

    # COMMANDS
    def reset(self) -> None:
        """Reset the game"""
        # self.maze.reset()
        # self.pacman.reset()

    def update(self) -> None:
        """Update the game"""
        pass

    def go(self, direction: Direction) -> None:
        """Go in a direction"""
        pass
