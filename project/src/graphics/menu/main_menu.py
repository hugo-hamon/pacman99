from .box import Box
import pygame as pg


class MainMenu:

    def __init__(self, screen: pg.surface.Surface) -> None:
        pg.font.init()
        self.font = pg.font.Font("assets/font/pac-font.TTF", 20)
        self.screen = screen
        self.clock = pg.time.Clock()

        self.menu_sprite = Box("Menu", int(self.screen.get_width() / 12), self.screen,
                               int(self.screen.get_width() / 2),
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.1))

        self.game_button = Box("Jouer", int(self.screen.get_width() / 24), self.screen,
                               int(self.screen.get_width() / 3),
                               (self.screen.get_width() / 2,
                                self.screen.get_height() * 0.37))

        self.config_button = Box("Config", int(self.screen.get_width() / 24), self.screen,
                                 int(self.screen.get_width() / 3),
                                 (self.screen.get_width() / 2,
                                     self.screen.get_height() * 0.52))

        self.credit_button = Box("Credits", int(self.screen.get_width() / 24), self.screen,
                                 int(self.screen.get_width() / 3),
                                 (self.screen.get_width() / 2,
                                     self.screen.get_height() * 0.67))

    def run(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            mx, my = pg.mouse.get_pos()

            if self.game_button.is_collide(mx, my) and pg.mouse.get_pressed()[0]:
                running = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            self.display_button()
            self.clock.tick(60)
            pg.display.update()

    def display_button(self) -> None:
        self.menu_sprite.display()
        self.game_button.display()
        self.config_button.display()
        self.credit_button.display()
