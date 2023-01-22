from ..graphics.graphic import Graphic
from ..graphics.sounds import Sounds
from ..config import Config
from .game import Game

MOVE_PATH = "moves.txt"

class App:

    def __init__(self, config: Config) -> None:
        self.config = config

    # TODO
    def run(self) -> None:
        """Run the app"""
        sounds = Sounds()
        game = Game(config=self.config, sounds=sounds)
        if self.config.user.enable_graphics:
            graphic = Graphic(config=self.config, game=game, sounds=sounds)
            graphic.start()

    def read_moves(self) -> None:
        """Read the moves from the file"""
        pass

    # TODO
    def reset(self) -> None:
        """Reset the app"""
        pass
