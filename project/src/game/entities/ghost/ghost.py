import abc
from ...direction import Direction
from .ghoststate import Ghoststate as gs

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
            __turnaround()
            
    def __turnaround() -> None :
        #self.direction = self.direction.opposite TODO
        pass
    
    def convert_to_xy(way : int) -> Tuple(int, int) :
        """Converti la direction en coordonées x, y)"""
        match way :
            case NORTH :
                return (0,1)
            case SOUTH :
                return (0,-1)
            case EAST :
                return (1, 0)
            case WEST :
                return (-1, 0)
            case other :
                raise ValueError("Direction non supportée")