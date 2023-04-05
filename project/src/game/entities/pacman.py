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
        is_wall_in_dir = self.is_wall(dir)
        if not is_wall_in_dir:
            self.direction = dir
            self.next_direction = dir
        elif is_wall_in_dir:
            if self.is_wall(self.direction):
                self.direction = Direction.NONE
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

    def _get_next_direction(self):
        next_dir = self.control_func()
        return self.valid_move(next_dir)
    
    def valid_move(self, dir: Direction) -> Direction:
        pac_position = self.get_position()
        pac_x = round(pac_position[0])
        pac_y = round(pac_position[1])
        area = self.maze.get_neighbors(pac_x, pac_y)
        check = tuple(
            map(operator.add, dir.to_vector(), (1, 1)))
        if area[check[1]][check[0]] not in [Components.DOOR, Components.WALL] and dir != Direction.NONE:
            return dir
        elif self.is_wall(dir):
            return Direction.NONE
        return dir
