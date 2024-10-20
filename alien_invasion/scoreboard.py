import time

import pygame.font

from pygame.sprite import Group

from ship import Ship

class ScoreBoard:
    """КЛас, що виводить рахунок."""

    def __init__(self, ai_game):
        """Ініціалізація атрибутів, пов'язана із рахунком."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Налаштування шрифту для відображення рахунку.
        self.text_color = (255, 255,255)
        self.black = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_images()


    def prep_images(self):
        """
        Підготувати зображення з початковим рахунком, 
        рекордом, рівнем та кораблями
        """
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_high_score(self):
        """Згенерувати рекорд у зображення."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
           self.black, self.text_color)

        # Відцентрувати рекорд по горизонталі
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_score(self):
        """Перетворити рахунок на зображення>."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, 
                self.black, self.text_color)

        # Показати рахунок у верхньому правому куті екрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def check_high_score(self):
        """Перевірити, чи встановлено рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            self.stats.save_high_score()

    def prep_level(self):
        """Перетворити рівенб у зображення"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, 
                self.black, self.text_color)

        # Розташувати рівень під рахунком
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10    

    def check_ult(self):
        """Поява ульти в корабля як бонус"""
        if self.stats.level == 5:
            time_q = 5
            for i in range(time_q, 0, -1):
                self.ult = self.settings.bullet_width + 147
                if i == 0:
                    self.settings.bullet_width = 3




    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Показати рахунок, рівень та кораблі на екрані."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)