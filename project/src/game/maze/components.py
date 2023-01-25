from enum import Enum

class Components(Enum):
    '''Enum of all the components in the maze except entities(Pacman, Ghosts)'''
    WALL = 0
    EMPTY = 1
    DOT = 2
    SUPERDOT = 3
    FRUIT = 4
    DOOR = 5
    
    def __str__(self):
        return str(self.value)