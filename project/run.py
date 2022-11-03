from src import main
import toml

config = toml.load("config.toml")
user_config = config["user"]

if __name__ == '__main__':
    main.run(
        graphics_enable=user_config["enable_graphics"]
    )
