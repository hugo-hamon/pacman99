from .ghoststate import Ghoststate as gs
from ...direction import Direction
from typing import Tuple
import abc


class GeneralGhost(abc.ABC) :
    
    def __init__(self, pacman_ref) :
        super().__init__()
        self.pac_ref = pacman_ref
        self.state = gs.CHASE
        
    @abc.abstractmethod
    def _choose_direction(self, intersection) :
        """Retourne la direction préférée"""
        pass
    
    def set_state(self, ghoststate : gs) -> None :
        """Set l'état du fantome"""
        self.state = ghoststate
        if ghoststate == gs.SCATTER :
            self.__turnaround()
            
    def __turnaround(self) -> None :
        #self.direction = self.direction.opposite TODO
        pass
    
    def convert_to_xy(self, way : Direction) -> Tuple[int, int] :
        """Convertie la direction en coordonées (x, y)"""
        return Direction.to_vector(way)