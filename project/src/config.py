from dataclasses import dataclass
from dacite.core import from_dict
import toml


@dataclass
class UserConfig:
    enable_graphics: bool
    enable_random_maze: bool
    menu_enable: bool
    sound_enable: bool


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
class MazeGenerationConfig:
    width: int
    height: int
    density: float
    seed: int
    intersection_step: int
    is_symetric: bool
    random_maze_path: str

@dataclass
class Config:
    user: UserConfig
    graphics: GraphicConfig
    game: GameConfig
    maze: MazeGenerationConfig


def load_config(config_path: str) -> Config:
    """Load the config"""
    return from_dict(data_class=Config, data=toml.load(config_path))
