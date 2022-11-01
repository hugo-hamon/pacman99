from src.main import run
import toml

config = toml.load("config.toml")
user_config = config["user"]

if __name__ == '__main__':
    run(graphics_enable=user_config["enable_graphics"])
