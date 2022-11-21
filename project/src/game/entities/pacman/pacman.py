import abc
from ...direction import Direction

class Pacman(abc.ABC):

    def __init__(self):
        super().__init__()
        self.boost_state = False
        self.actual_dir = None
        self.next_dir = None
    

    def check_collision(self):
        pass


    # Set-up la prochaine direction que pac-man devra prendre quand il le pourra
    def set_next_direction(self, dir : Direction):
        self.next_dir = dir

    # Change l'état de pac-man lorsqu'il ramasse un boost ou que celui-ci se termine
    def change_state(self):
        self.boost_state = not self.boost_state

