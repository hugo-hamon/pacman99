from .direction import Direction
from .maze.maze import Maze
from ..config import Config
from .entities.pacman import Pacman

MAZE_FILE_PATH = "assets/data/random.txt"



class Game:

    def __init__(self, config: Config) -> None:
        self.maze = Maze(filename=config.graphics.maze_path)
        self.pacman = Pacman(
            self.maze, config.game.game_speed, Direction.NORTH, (0, 0), config.game.pacman_lives
        )
        self.pacman.set_position(self.maze.get_packman_start())
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
        print("Pacman position: ", self.pacman.get_position())
        self.pacman.move(60)

    def go(self, direction: Direction) -> None:
        """Go in a direction"""
        pass
