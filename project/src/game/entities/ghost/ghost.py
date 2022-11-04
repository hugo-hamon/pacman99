import abc
import .ghoststate as gs

class generalGhost(abc.ABC) :
    
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
        if ghoststate = gs.SCATTER :
            __turnaround()
            
    def __turnaround() -> None :
        #self.direction = self.direction.opposite TODO
        pass
