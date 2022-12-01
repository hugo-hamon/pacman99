import abc
from ...direction import Direction

class Pacman(abc.ABC):

    def __init__(self):
        super().__init__()
        self.boost_state = False
        self.next_dir = None
    
    # Requêtes

    def _get_next_direction(self) -> Direction:
        # J'aurais ici besoin d'accéder aux données du maze
        # pour savoir si pac-man est à une intersection et peut tourner, ou non TODO
        pass


    # Commandes

    def set_next_direction(self, dir : Direction) -> None:
        """Enregistre la prochaine direction que pac-man doit prendre dès que possible"""
        self.next_dir = dir

    def accept_next_direction(self) -> None:
        """Effectue le changement de direction"""
        self.direction = self.next_dir
        self.next_dir = None

    def change_state(self) -> None:
        """Switch l'état de pac-man pour les super pac-gum"""
        self.boost_state = not self.boost_state
