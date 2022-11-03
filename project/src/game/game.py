from .direction import Direction
# from maze.maze import Maze

class Game:

    def __init__(self) -> None:
        # self.maze = Maze(filepath)
        # self.pacman = Pacman(self.maze.get_start_pos())
        pass

    # REQUESTS
    def is_game_over(self) -> bool:
        """Return True if the game is over"""
        # return self.maze.get_dots() == 0 or self.pacman.is_dead()
        return False

    def is_game_won(self) -> bool:
        """Return True if the game is won"""
        # return self.maze.get_dots() == 0
        return False

    def get_score(self) -> int:
        """Return the score"""
        # return self.pacman.get_score()
        return 0

    def get_distance(self) -> int:
        """Return the distance"""
        # return self.pacman.get_distance()
        return 0

    # COMMANDS
    def reset(self) -> None:
        """Reset the game"""
        # self.maze.reset()
        # self.pacman.reset()
        pass
    
    def update(self) -> None:
        """Update the game"""
        pass

    def go(self, direction: Direction) -> None:
        """Go in a direction"""
        pass
