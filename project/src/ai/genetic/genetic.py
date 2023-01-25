from ...game.game import Game
from ...config import Config
from time import time

class Genetic:

    def __init__(self, config: Config, game: Game) -> None:
        self.config = config
        self.game = game
        dist, score, death, won = self.game.run_with_movement("eeeennnn")
        dist, score, death, won = self.game.run_with_movement("eeeennnn")
        """
        a = time()
        for _ in range(100):
            dist, score, death, won = self.game.run_with_movement("eeeennnn")
        print(time() - a)
        """