from enum import Enum


class Ghoststate(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2
    EATEN = 3
    EXITTING = 4