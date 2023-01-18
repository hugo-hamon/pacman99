from ..maze.components import Components
from ..direction import Direction
from .entities import Entities
from ..maze.maze import Maze
from typing import Tuple
import operator


class Pacman(Entities):

    def __init__(self, maze: Maze, speed: float = 0, direction: Direction = Direction.WEST, coordinate: Tuple[float, float] = (0, 0), lives: int = 3) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.next_direction: Direction = Direction.NONE
        self.boost_state = False
        self.lives = lives
        self.distance = 0

    # Requests
    def is_dead(self) -> bool:
        """retourne vraie si le pacman est mort (plus de vie)"""
        return self.lives == 0

    def get_lives(self) -> int:
        """retourne le nombre de vie restante"""
        return self.lives
    
    def get_distance(self) -> int:
        return self.distance

    def is_wall(self, dir: Direction) -> bool:
        """retourne vrai si il y a un mur dans la direction dir"""
        position = self.get_position()
        area = self.maze.get_neighbors(int(position[0]), int(position[1]))
        checkw = tuple(map(operator.add, dir.to_vector(), (1, 1)))
        return area[checkw[1]][checkw[0]] == Components.WALL

    # Commandes
    def set_next_direction(self, dir: Direction) -> None:
        """Enregistre la prochaine direction que pac-man doit prendre dès que possible"""
        if self.direction.opposite() == dir:
            self.direction = dir
            self.next_direction = Direction.NONE
        elif self.direction == Direction.NONE and not self.is_wall(dir):
            self.direction = dir
            self.next_direction = Direction.NONE
        else:
            self.next_direction = dir

    def change_state(self) -> None:
        """Switch l'état de pac-man pour les super pac-gum"""
        self.boost_state = not self.boost_state

    def lose_life(self) -> None:
        """Perd une vie"""
        self.lives -= 1

    def _get_next_direction(self) -> Direction:
        """Entrée : direction self.buffer
            Si on peut aller dans la direction buffer, go buffer
            Sinon on peut continuer tout droit, tout droit
            Sinon null"""
        """Get the next direction of the entity"""
        position = self.get_position()
        area = self.maze.get_neighbors(int(position[0]), int(position[1]))
        check = tuple(map(operator.add, self.next_direction.to_vector(), (1, 1)))
        print(self.is_wall(self.direction), self.direction, area)
        if area[check[1]][check[0]] != Components.WALL and self.next_direction != Direction.NONE:
            self.direction = self.next_direction
        elif self.is_wall(self.direction):
            self.direction = Direction.NONE
            self.next_direction = Direction.NONE
        if self.direction != Direction.NONE:
            self.distance += 1
        print(self.get_position())
        print("Direction suivante:", self.next_direction)
        return self.direction
