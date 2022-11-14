from ..graphics.graphic import Graphic
from ..config import Config
from .game import Game


class App:

    def __init__(self, config: Config) -> None:
        self.config = config

    # TODO
    def run(self) -> None:
        """Run the app"""
        game = Game(config=self.config)
        if self.config.user.enable_graphics:
            graphic = Graphic(config=self.config, game=game)
            graphic.start()

    # TODO
    def reset(self) -> None:
        """Reset the app"""
        pass
