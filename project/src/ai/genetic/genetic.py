from ...game.game import Game
from ...config import Config


class Genetic:

    def __init__(self, config: Config, game: Game) -> None:
        self.config = config
        self.game = game
    