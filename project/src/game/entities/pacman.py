from ..direction import Direction
from .entities import Entities
from ..maze.maze import Maze
from typing import Tuple


class Pacman(Entities):

    def __init__(self, maze: Maze, speed: float = 0, direction: Direction = Direction.WEST, coordinate: Tuple[float, float] = (0, 0), lives: int = 3) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.boost_state = False
        self.lives = lives

    # Requests
    def is_dead(self) -> bool:
        """retourne vraie si le pacman est mort (plus de vie)"""
        return self.lives == 0

    def get_lives(self) -> int:
        """retourne le nombre de vie restante"""
        return self.lives

    # Commandes

    def set_next_direction(self, dir: Direction) -> None:
        """Enregistre la prochaine direction que pac-man doit prendre dès que possible"""
        self.next_dir = dir

    def accept_next_direction(self) -> None:
        """Effectue le changement de direction"""
        self.direction = self.next_dir
        self.next_dir = None

    def change_state(self) -> None:
        """Switch l'état de pac-man pour les super pac-gum"""
        self.boost_state = not self.boost_state

    def lose_life(self) -> None:
        """Perd une vie"""
        self.lives -= 1
