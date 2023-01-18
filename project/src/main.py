from .game import app
from .config import load_config

config_path = "config.toml"

def run() -> None:
    """Run the app"""
    config = load_config(config_path)
    application = app.App(config=config)
<<<<<<< HEAD
    application.create_random_maze()
    application.run()
=======
    application.run()
>>>>>>> 7e40f6d2688bf001997edbf77e2b3f48faaeb21c
