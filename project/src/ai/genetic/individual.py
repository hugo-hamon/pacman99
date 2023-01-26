from typing import List, Dict, Union


class Individual:

    def __init__(self, distance: int, score: int, dead: bool, won: bool) -> None:
        self.distance = distance
        self.solution = ""
        self.score = score
        self.dead = dead
        self.won = won

    # Request
    def get_data(self) -> Dict[str, Union[int, bool]]:
        """Get the data of the individual."""
        return {
            "distance": self.distance,
            "score": self.score,
            "dead": self.dead,
            "won": self.won
        }

    def get_solution(self) -> str:
        """Get the solution of the individual."""
        return self.solution
    
    def is_winner(self) -> bool:
        """Check if the individual is a winner."""
        return self.won

    # Commands
    def set_solution(self, solution: str) -> None:
        """Set the solution of the individual."""
        self.solution = solution
