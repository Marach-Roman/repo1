import sys

import pygame

from pygame.locals import USEREVENT, QUIT

import pygame.mixer
# from moviepy.editor import VideoFileClip
# from PIL import Image  # Ensure you import Image from PIL
from alien_invasion import AlienInvasion
from settings import Settings
from music import Music
from buttons import ButtonHelp, ButtonPlay, ButtonSettings
from win_help import Help
from win_settings import WSettings

class MainMenu:
    """Головне меню з кнопками такі як: Play, Settings, Help"""

    def __init__(self):
        """Ініціалізувати головне меню гри"""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # створити екземпляр музики
        self.music = Music(self)

        # Завантаження та відтворення відео як фон
        self.bg_image = pygame.image.load('bg/bg_menu.jpg').convert()
        # Ініціалізація кнопок
        self.play_button = ButtonPlay(self, "Play")
        self.help_button = ButtonHelp(self, "Help")
        self.settings_button = ButtonSettings(self, "Settings")

        self.bg_image = pygame.transform.scale(self.bg_image,
            (self.settings.screen_width, self.settings.screen_height))

        self.settings_window_open = False
        self.settings_window = None        

    def run_menu(self):
        """Основний цикл меню"""
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """Реагувати на натискання клавіш та події миші"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_help_button(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == self.music.start_music_event:
                self.music.play_music()
                pygame.time.set_timer(self.music.start_music_event, 0)


    def _check_keydown_events(self, event):
        """Реагувати на натискання клавіш"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            self.esc()
            return self.run_menu()
        elif event.key == pygame.K_p:
            self._start_new_game()
        elif event.key == pygame.K_h:
            self._open_help()
        elif event.key == pygame.K_s:
            self.music.stop_music()
        elif event.key == pygame.K_t:
            self.music.play_music()
        elif event.key == pygame.K_r:
            self.settings_window_open = not self.settings_window_open
            if self.settings_window_open:
                self.settings_window.run_setting()
                self.settings_window = WSettings()



    def _check_play_button(self, mouse_pos):
        """
        Розпочати нову гру та перейти на 
        сторінку гри, коли натиснуто користувачем
        кнопку Play
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self._start_new_game()

    def _check_help_button(self, mouse_pos):
        """
        Розпочати ознайомлення з грою 
        та перейти на сторінку з допомогою
        """
        btn_clicked_help = self.help_button.rect.collidepoint(mouse_pos)
        if btn_clicked_help:
            self._open_help()


    def _start_new_game(self):
        """Преходити під час натискання кнопки Play на іншу сторінку з грою"""
        self.music.stop_music()
        ai = AlienInvasion()
        ai.run_game()


    def _open_help(self):
        """Відкрити Вікно Допомоги"""
        self.music.stop_music()
        self.sections = [
        ('Опис сюжету гри:', 'list_win_help.txt'),
        ('Вид прибульців:', 'list_win_help_2.txt'),
        ('Рейтинг очок:', 'list_win_help_3.txt'),
        ('Клавіші:', 'list_win_help_4.txt')
        ]
        wh = Help(self.sections)
        wh.run_help()


    def _update_screen(self):
        """Увімкнути зображення на екрані"""
        self.screen.blit(self.bg_image, (0, 0))

        if self.settings_window_open and self.settings_window:
            self.settings_window.run_settings()

        # Намалювати кнопки
        self.help_button.draw_button()
        self.play_button.draw_button()
        self.settings_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Створити екземпляр гри та запустити гри
    mu = MainMenu()
    mu.run_menu()
