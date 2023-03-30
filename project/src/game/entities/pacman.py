from ..maze.components import Components
from typing import Tuple, Callable
from ..direction import Direction
from .entities import Entities
from ..maze.maze import Maze
import operator


class Pacman(Entities):
    # TODO replace move_list par Game
    def __init__(self,
                 maze: Maze,
                 control_func: Callable,
                 speed: float = 0,
                 direction: Direction = Direction.WEST,
                 coordinate: Tuple[float, float] = (0, 0),
                 lives: int = 3,
                 ) -> None:
        super().__init__(maze, speed, direction, coordinate)
        self.next_direction: Direction = Direction.NONE
        self.boost_state = False
        self.lives = lives
        self.alive = True
        self.distance = 0
        self.control_func = control_func

    # Requests
    def is_dead(self) -> bool:
        """retourne vraie si le pacman est mort (plus de vie)"""
        return self.alive

    def get_lives(self) -> int:
        """retourne le nombre de vie restante"""
        return self.lives

    def get_distance(self) -> int:
        return self.distance

    def is_wall(self, dir: Direction) -> bool:
        """retourne vrai si il y a un mur dans la direction dir"""
        position = self.get_position()
        area = self.maze.get_neighbors(round(position[0]), round(position[1]))
        checkw = tuple(map(operator.add, dir.to_vector(), (1, 1)))
        return area[checkw[1]][checkw[0]] in [Components.WALL, Components.DOOR]

    def is_boosted(self):
        """retourne vrai si pacman est boosté"""
        return self.boost_state

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

    def respawn(self) -> None:
        "Pacman revient à la vie"
        self.alive = True

    def lose_life(self) -> None:
        """Perd une vie"""
        self.alive = False
        self.lives -= 1

    def set_movement(self, move_list: str) -> None:
        """Enregistre la liste de mouvement"""
        self.move_list = move_list
        self.move_list_index = 0

    # TODO Déplacer dans geneticManager
    def get_next_valid_move(self) -> Direction:
        """retourne la prochaine direction valide"""
        while self.move_list_index < len(self.move_list):
            self.direction = Direction.from_string(
                self.move_list[self.move_list_index])
            if self.is_wall(self.direction):
                self.direction = Direction.NONE
            self.move_list_index += 1
            if self.direction != Direction.NONE:
                self.distance += 1
                return self.direction
        return Direction.NONE

    def _get_next_direction(self):
        return self.control_func()

    # TODO Déplacer dans playerGame
    """
    def _get_next_direction(self) -> Direction:
        Get the next direction of the entity
        position = self.get_position()
        area = self.maze.get_neighbors(round(position[0]), round(position[1]))
        check = tuple(
            map(operator.add, self.next_direction.to_vector(), (1, 1)))
        if self.move_list:
            return self.get_next_valid_move()
        if area[check[1]][check[0]] not in [Components.DOOR, Components.WALL] and self.next_direction != Direction.NONE:
            self.direction = self.next_direction
        elif self.is_wall(self.direction):
            self.direction = Direction.NONE
            self.next_direction = Direction.NONE
        if self.direction != Direction.NONE:
            self.distance += 1
        return self.direction
    """