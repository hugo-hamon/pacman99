from .direction import Direction

class Game:

    def __init__(self) -> None:
        self.game_over = False
        self.has_won = False
        self.distance = 0
        self.score = 0

    # REQUESTS
    def is_game_over(self) -> bool:
        """Return True if the game is over"""
        return self.game_over

    def is_game_won(self) -> bool:
        """Return True if the game is won"""
        return self.has_won

    def get_score(self) -> int:
        """Return the score"""
        return self.score

    def get_distance(self) -> int:
        """Return the distance"""
        return self.distance

    # COMMANDS
    def reset(self) -> None:
        """Reset the game"""
        self.game_over = False
        self.has_won = False
        self.distance = 0
        self.score = 0
    
    def update(self) -> None:
        """Update the game"""
        pass

    def go(self, direction: Direction) -> None:
        """Go in a direction"""
        pass
