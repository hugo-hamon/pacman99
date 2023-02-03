from .game import app
from .config import load_config

default_config_path = "config.toml"

def run(config_path=default_config_path) -> None:
    """Run the app"""
    config = load_config(config_path)
    application = app.App(config=config)
    application.run()