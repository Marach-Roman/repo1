import pygame
import pygame.mixer
from pygame.locals import USEREVENT

from settings import Settings

class Music:
    """Додати до всіх моментів музику та звуки"""

    def __init__(self, file_music):
        """Ініціалізувати музику та звуки"""
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.main_menu_music = file_music

        # СТворення події для запуску музики.
        self.start_music_event = USEREVENT + 1
        pygame.time.set_timer(self.start_music_event, 1000)

        self.load_music()

    def load_music(self):
        """Завантаження усіх звуків для гри"""

        # Завантажити музику головного меню
        pygame.mixer.music.load(self.settings.main_menu_music)

        # Завантажити музику гри

        # завантажити звук корабля

        # Завантажити звук програшу користувача

        # Завантажити звук відліку до гри

        # Завантажити звук для кнопок



    def play_music(self):
        """Грати музику"""
        pygame.mixer.music.play(-1)

    def stop_music(self):
        """Зупинити музику"""
        pygame.mixer.music.stop()

