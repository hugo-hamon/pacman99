from __future__ import annotations
from ...game.direction import Direction
from ...graphics.sounds import Sounds
from matplotlib import pyplot as plt
from numpy.random import random
from ...game.game import Game
from .network import Network
from ...config import Config
from PIL import Image
from math import log
import numpy as np


def fitness_function_1(mask: Mask) -> float:
    """Get the fitness of the mask."""
    score = mask.score
    dead = mask.dead
    winner = mask.winner
    distance = log(mask.distance + 1) * mask.distance / 20
    return score - distance - (dead * 100) + (winner * 200)


class Mask:

    # Constructor

    def __init__(self, config: Config, sounds: Sounds) -> None:
        self.networks = []
        self.config = config
        self.sound = sounds

        self.score = 0
        self.distance = 0
        self.dead = False
        self.winner = False

    def is_winner(self) -> bool:
        """Check if the mask can solve the maze."""
        return self.winner

    def randomize(self) -> None:
        """Randomize the mask. Used for initial population."""
        if len(self.networks) == 0:
            self.initialize_network()
        for network in self.networks:
            network.randomize()

    def initialize_network(self) -> None:
        """Create a new network in the mask."""
        network = Network(config=self.config, direction=Direction.NONE.random())
        network.add_neuron(network.create_random_neuron())
        self.add_network(network)

    def add_network(self, network: Network) -> None:
        """Add a network to the mask."""
        self.networks.append(network)

    def get_fitness(self) -> float:
        """Get the fitness of the mask."""
        return fitness_function_1(self)

    def mutate(self) -> None:
        """Mutate the mask by mutating each individual networks.
        For now, the mutation doesn't change the number of networks
        It could eventually be changed to add or remove networks"""
        for network in self.networks:
            network.mutate_network()

    def crossover(self, other: Mask) -> Mask:
        """Crossover the mask with another mask by selecting random networks from each mask."""
        child = Mask(config=self.config, sounds=self.sound)
        networks = self.networks + other.networks
        for network in networks:
            if random() < 0.5:
                child.add_network(network)
        if len(child.networks) == 0:
            child.initialize_network()
        return child

    def play(self, maze=None) -> None:
        """Play the mask."""
        game = Game(config=self.config, sounds=self.sound, maze=maze)
        self.distance, self.score, self.dead, self.won = game.run_with_mask(
            self
        )

    def get_move(self, state: np.ndarray) -> Direction:
        """Get the move from the mask."""
        for network in self.networks:
            if network.is_triggered(state):
                return network.get_direction()
        return Direction.NONE
    
    # REPRENSATION
    
    def plot(self):
        """Plot each network in the mask on one plot."""
        for network in self.networks:
            plt.title(network.get_direction())
            network_array = network.get_network_as_array()
            print(network_array)
            plt.imshow(network_array)
            plt.show()
        
        