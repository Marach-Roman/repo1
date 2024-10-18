import sys

import pygame

from settings import Settings

class WSettings:
    """Ініціалізувати Вікно Параметрів"""

    def __init__(self):
        """
        Ініціалізувати вікно Параметри з 
        мовою, рекордами, музикою та ін.
        """
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.Surface((500, 500))


    def run_settings(self):
        """Головний цикл Параметрів"""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Реагувати на натискання клавіш і події миші"""
        for event in pygame.event.get():  # Правильний спосіб отримання подій
            if event.type == pygame.QUIT:  # Виправлення умови
                sys.exit()


    def _update_screen(self):
        """Увімкнути зображення на екрані"""
        self.screen.fill(self.settings.bg_color_sett)

        pygame.display.flip()

if __name__ == '__main__':
    ws = WSettings()
    ws.run_settings()