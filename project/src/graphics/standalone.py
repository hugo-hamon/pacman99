from ..game.game import Game
import pygame as pg


def rescale(element: pg.surface.Surface, screen: pg.surface.Surface, game: Game) -> pg.surface.Surface:
    """Rescale the element size"""
    w = screen.get_width() / game.get_maze().get_width()
    h = screen.get_height() / game.get_maze().get_height()
    return pg.transform.scale(element, (min(w, h), min(w, h)))
