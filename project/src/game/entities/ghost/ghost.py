import abc
import ghoststate as gs

class generalGhost(abc.ABC) :
    
    def __init__(self, pacman_ref) :
        super().__init__()
        pac_ref = pacman_ref
        state = gs.CHASE
        
    @abc.abstractmethod
    def _choose_direction(self, intersection) :
        """Retourne la direction préférée"""
        pass
    
    def set_state(self, ghoststate : gs) -> None :
        """Set l'état du fantome"""
        state = ghoststate