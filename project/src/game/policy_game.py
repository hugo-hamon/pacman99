from ..ai.policy.policy_agent import PolicyAgent
from ..graphics.graphic_game import GraphicGame
from ..graphics.sounds import Sounds
from .maze.maze import Maze
from ..config import Config
from typing import Union
from .game import Game

VECTOR = [0.02476395688483124, 0.10595997921149858, 0.12932670599894536, 0.05063700075536426, 0.23964333344823674, 0.8945732052166709]

class PolicyGame:
    """Class allowing a game controlled by DQN"""

    def __init__(self, config: Config, maze: Maze, sounds: Union[Sounds, None] = None) -> None:
        """If sounds is set creates a graphic game otherwise creates a normal game"""
        self.config = config
        self.maze = maze
        policy_agent = PolicyAgent(VECTOR)
        if sounds is None:
            self.game = Game(config, self.maze, policy_agent.get_policy_agent_move)
        else:
            self.game = GraphicGame(
                config, sounds, self.maze, policy_agent.get_policy_agent_move
            )

    def run(self):
        return self.game.run()
