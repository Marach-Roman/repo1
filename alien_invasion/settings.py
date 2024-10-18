import pygame

class Settings:
    """Клас для збереження всіх налаштувань гри."""

    def __init__(self):
        """Ініціалізувати постійні налаштування гри."""
        # Screen settings
        self.screen_width_new = 1200
        self.screen_height_new = 750
        self.bg_color = (230, 230, 230)
        self.bg_color_sett = (20, 20, 20)

        # Основні налаштування звуків тп музики
        self.main_menu_music = 'sound/main_menu.mp3'

        # Налаштування корабля.
        # self.ship_speed = 1.5
        self.ship_limit = 3

        # Налаштування прокрутки екрану
        self.scroll_offset = 0
        self.scroll_speed = 3.5

        # Налаштування кулі.
        # self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60 ,60)
        self.bullets_allowed = 3

        # Налаштування прибульця.
        # self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction 1 означає напрямок руху праворуч; -1 -- ліворуч.
        # self.fleet_direction = 1

        # Як швидко гра має прискорюватись.
        self.speedup_scale = 1.1

        # Як швидко збільшується вартість прибульця.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Ініціалізація змінних налаштувань гри."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.6

        # fleet_direction 1 означає напрямок руху праворуч; -1 -- ліворуч.
        self.fleet_direction = 1

        # Отримання балів.
        self.alien_points = 50

    def increase_speed(self):
        """Збільшення налаштувань швидкості та вартості прибульців."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
