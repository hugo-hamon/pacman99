from ..game.maze.components import Components
from ..game.maze.maze import Maze


def get_wall_name(x: int, y: int, maze: Maze) -> str:
    """Return the name of the wall"""
    if get_wall_name_corner(x, y, maze) != "":
        return get_wall_name_corner(x, y, maze)
    elif get_wall_name_cross(x, y, maze) != "":
        return get_wall_name_cross(x, y, maze)
    elif get_other_wall_name(x, y, maze) != "":
        return get_other_wall_name(x, y, maze)
    return "void"


def get_wall_name_corner(x: int, y: int, maze: Maze) -> str:
    if is_top_left_wall(x, y, maze):
        return "left_top_corner_wall"
    elif is_top_right_wall(x, y, maze):
        return "right_top_corner_wall"
    elif is_bottom_left_wall(x, y, maze):
        return "left_bottom_corner_wall"
    elif is_bottom_right_wall(x, y, maze):
        return "right_bottom_corner_wall"
    return ""


def get_wall_name_cross(x: int, y: int, maze: Maze) -> str:
    if is_bottom_left_corner_wall(x, y, maze):
        return "left_bottom_corner_wall"
    elif is_bottom_right_corner_wall(x, y, maze):
        return "right_bottom_corner_wall"
    elif is_top_left_corner_wall(x, y, maze):
        return "left_top_corner_wall"
    elif is_top_right_corner_wall(x, y, maze):
        return "right_top_corner_wall"
    return ""


def get_other_wall_name(x: int, y: int, maze: Maze) -> str:
    if is_left_wall(x, y, maze) and is_right_wall(x, y, maze):
        return "left_wall" if x == 0 else "right_wall"
    elif is_left_wall(x, y, maze):
        return "left_wall"
    elif is_right_wall(x, y, maze):
        return "right_wall"
    elif is_top_wall(x, y, maze) and is_bottom_wall(x, y, maze):
        return "top_wall" if y == 0 else "bottom_wall"
    elif is_top_wall(x, y, maze):
        return "top_wall"
    elif is_bottom_wall(x, y, maze):
        return "bottom_wall"
    return ""


# Standalone function for wall
def is_left_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a left wall"""
    return True if x == 0 else maze.get_cell(x - 1, y) != Components.WALL


def is_right_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a right wall"""
    return True if x == maze.get_width() - 1 else maze.get_cell(x + 1, y) != Components.WALL


def is_top_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a top wall"""
    return True if y == 0 else maze.get_cell(x, y - 1) != Components.WALL


def is_bottom_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a bottom wall"""
    return True if y == maze.get_height() - 1 else maze.get_cell(x, y + 1) != Components.WALL


def is_top_left_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a top left wall"""
    return is_top_wall(x, y, maze) and is_left_wall(x, y, maze)


def is_top_right_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a top right wall"""
    return is_top_wall(x, y, maze) and is_right_wall(x, y, maze)


def is_bottom_left_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a bottom left wall"""
    return is_bottom_wall(x, y, maze) and is_left_wall(x, y, maze)


def is_bottom_right_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a bottom right wall"""
    return is_bottom_wall(x, y, maze) and is_right_wall(x, y, maze)


def is_bottom_left_corner_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a bottom left corner wall"""
    if x + 1 >= maze.get_width() or y < 1:
        return False
    return maze.get_cell(x + 1, y - 1) != Components.WALL and maze.get_cell(x + 1, y) == Components.WALL and maze.get_cell(x, y - 1) == Components.WALL


def is_bottom_right_corner_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a bottom right corner wall"""
    if x < 1 or y < 1:
        return False
    return maze.get_cell(x - 1, y - 1) != Components.WALL and maze.get_cell(x - 1, y) == Components.WALL and maze.get_cell(x, y - 1) == Components.WALL


def is_top_left_corner_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a top left corner wall"""
    if x + 1 >= maze.get_width() or y + 1 >= maze.get_height():
        return False
    return maze.get_cell(x + 1, y + 1) != Components.WALL and maze.get_cell(x + 1, y) == Components.WALL and maze.get_cell(x, y + 1) == Components.WALL


def is_top_right_corner_wall(x: int, y: int, maze: Maze) -> bool:
    """Return True if the wall is a top right corner wall"""
    if x < 1 or y + 1 >= maze.get_height():
        return False
    return maze.get_cell(x - 1, y + 1) != Components.WALL and maze.get_cell(x - 1, y) == Components.WALL and maze.get_cell(x, y + 1) == Components.WALL
