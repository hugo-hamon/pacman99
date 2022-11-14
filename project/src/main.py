from .game import app
from .config import load_config

config_path = "config.toml"

def run() -> None:
    """Run the app"""
    config = load_config(config_path)
    application = app.App(config=config)
    application.run()
