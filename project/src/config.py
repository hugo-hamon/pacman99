from dataclasses import dataclass
from dacite.core import from_dict
import toml


@dataclass
class UserConfig:
    enable_graphics: bool
    enable_random_maze: bool


@dataclass
class GraphicConfig:
    width: int
    height: int
    title: str
    fps: int
    maze_path: str


@dataclass
class GameConfig:
    game_speed: float
    pacman_lives: int


@dataclass
class Config:
    user: UserConfig
    graphics: GraphicConfig
    game: GameConfig


def load_config(config_path: str) -> Config:
    """Load the config"""
    return from_dict(data_class=Config, data=toml.load(config_path))
