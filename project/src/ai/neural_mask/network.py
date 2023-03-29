from ...game.direction import Direction
import matplotlib.pyplot as plt
from ...config import Config
import numpy.random as rd
from typing import List
import numpy as np


class Network:
    """A network of neurons. 
    Neurons are represented by a tuple (x, y, GameElement)
    They are triggered if the game element at (x, y) is the same as the one in the tuple
    The network is triggered if all neurons are triggered"""

    # Constructor

    def __init__(self, config: Config, direction: Direction) -> None:
        """List of neurons : (x, y, GameElement, is_inverse))"""
        self.neurons = []
        self.config = config
        self.direction = direction

    # Requests
    def is_triggered(self, state) -> bool:
        """Returns True if the network is triggered"""
        for neuron in self.neurons:
            if neuron[3]:
                if state[neuron[0]][neuron[1]] == neuron[2]:
                    return False
            elif state[neuron[0]][neuron[1]] != neuron[2]:
                return False
        return True

    def create_random_neuron(self) -> List:
        """Returns a random neuron"""
        return [
            rd.randint(0, self.config.neural_mask.mask_size), rd.randint(
                0, self.config.neural_mask.mask_size), rd.randint(0, 5),
            rd.random() < 0.5
        ]
    
    def get_direction(self) -> Direction:
        """Get the direction of the network"""
        return self.direction
    # Commands

    def add_neuron(self, neuron: List):
        """Add an neuron to the network : (x, y, GameElement, is_inverse)"""
        self.neurons.append(neuron)

    def randomize(self):
        """Randomize the network"""
        for _ in range(rd.randint(1,self.config.neural_mask.max_neurons_per_network // 2)):
            self.add_neuron(self.create_random_neuron())

    def mutate_network(self):
        """Mutate the network"""
        for neuron in self.neurons:
            if rd.random() < self.config.neural_mask.mutation_chance:
                step_x = rd.randint(-1, 2)
                step_y = rd.randint(-1, 2)
                if neuron[0] + step_x >= 0 and neuron[0] + step_x < self.config.neural_mask.mask_size:
                    neuron[0] += step_x
                if neuron[1] + step_y >= 0 and neuron[1] + step_y < self.config.neural_mask.mask_size:
                    neuron[1] += step_y
            if rd.random() < self.config.neural_mask.mutation_chance:
                neuron[2] = rd.randint(0, 5)
            if rd.random() < self.config.neural_mask.mutation_chance / 10:
                self.add_neuron(self.create_random_neuron())

    def get_network_as_array(self) -> np.ndarray:
        """Get the mask as a numpy array"""
        mask = np.full((self.config.neural_mask.mask_size, self.config.neural_mask.mask_size), -1)
        for neuron in self.neurons:
            mask[neuron[0]][neuron[1]] = neuron[2]
        return mask
        
    
        