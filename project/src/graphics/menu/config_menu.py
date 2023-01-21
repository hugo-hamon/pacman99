from __future__ import annotations
from typing import TYPE_CHECKING
from .arrow_box import ArrowBox
from ...game.game import Game
from .box import Box
import pygame as pg
if TYPE_CHECKING:
    from ..graphic import Graphic


class ConfigMenu:

    def __init__(self, screen: pg.surface.Surface, game: Game, graphic: Graphic) -> None:
        pg.font.init()
        self.font = pg.font.Font("assets/font/pac-font.TTF", 20)
        self.screen = screen
        self.clock = pg.time.Clock()
        self.game = game
        self.graphic = graphic

        self.menu_sprite = Box("Config", int(self.screen.get_width() / 12), self.screen,
                               int(self.screen.get_width() / 2),
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.1))

        self.volume_button = ArrowBox("Volume", int(self.screen.get_width() / 24), self.screen,
                                      int(self.screen.get_width() / 3),
                                      (self.screen.get_width() / 2,
                                       self.screen.get_height() * 0.37))

        self.game_speed_button = ArrowBox("Vitesse", int(self.screen.get_width() / 24), self.screen,
                                          int(self.screen.get_width() / 3),
                                          (self.screen.get_width() / 2,
                                           self.screen.get_height() * 0.52))

        self.frame_rate_button = ArrowBox("Fps", int(self.screen.get_width() / 24), self.screen,
                                          int(self.screen.get_width() / 3),
                                          (self.screen.get_width() / 2,
                                           self.screen.get_height() * 0.67))

        self.back_button = Box("Retour", int(self.screen.get_width() / 24), self.screen,
                               int(self.screen.get_width() / 3),
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.82))

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONUP and self.process_mouse_event():
                    running = False
            self.screen.fill((0, 0, 0))
            self.display_button()
            self.clock.tick(60)
            pg.display.update()

    def process_mouse_event(self) -> bool:
        """Process the mouse event and return True if the user click on the back button"""
        mx, my = pg.mouse.get_pos()
        if self.back_button.is_collide(mx, my):
            return True
        if self.volume_button.is_right_collide(mx, my):
            # TODO: Changer le volume quand les sons seront implémentés
            pass
        if self.volume_button.is_left_collide(mx, my):
            # TODO: Changer le volume quand les sons seront implémentés
            pass
        if self.game_speed_button.is_right_collide(mx, my):
            self.game.get_pacman().set_speed(self.game.get_pacman().get_speed() + 1)
        if self.game_speed_button.is_left_collide(mx, my) and self.game.get_pacman().get_speed() > 1:
            self.game.get_pacman().set_speed(self.game.get_pacman().get_speed() - 1)
        if self.frame_rate_button.is_right_collide(mx, my):
            self.graphic.set_fps(self.graphic.get_fps() + 1)
        if self.frame_rate_button.is_left_collide(mx, my) and self.graphic.get_fps() > 1:
            self.graphic.set_fps(self.graphic.get_fps() - 1)
        return False

    def display_button(self) -> None:
        """Display the button on the screen mx and my are the mouse position use for the hover effect"""
        self.menu_sprite.display()
        self.volume_button.display()
        self.game_speed_button.display()
        self.frame_rate_button.display()
        self.back_button.display()
