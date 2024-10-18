import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import ScoreBoard
from buttons import ButtonPlay
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Загальний клас, що керує ресурсами та поведінкою гри."""

    def __init__(self):
        """Ініціалізувати гру, створити ресурси гри"""
        pygame.init()
        self.settings = Settings()

        # Завантажити зображення з файлу
        self.original_image = pygame.image.load('bg/bg_game_5.jpg')
        
        
        # Отримати розміри екрану - example down
        # screen_info = pygame.display.Info()
        # self.screen_width = screen_info.current_w
        # self.screen_height = screen_info.current_h

        # Змінити розмір зображення на розміри екрану
        # self.resized_image = pygame.transform.scale(self.original_image, (self.screen_width, self.screen_height))

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")


        # Створити Екземпляр збереження ігрової статистики та табло на екрані.
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # СТворимо кнопку Play.
        self.play_button = ButtonPlay(self, "Play")

    def run_game(self):
        """Розпочати головний цикл гри."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()


    def _check_events(self):
        """Реагувати на натискання клавіш та події миші."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Розпочати нову гру, коли коп=ристувач натисне кнопку Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # АНалювати статистику гри.
            self.settings.initialize_dynamic_settings()
            self._start_game()

    def _check_keydown_events(self, event):
        """Реагувати на натискання клавіш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if not self.stats.game_active:
                self._start_game()

    def _check_keyup_events(self, event):
        """Реагувати, коли клавіша не натиснута"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game(self):
        """Розпочати нову гру, коли користувач натисне кнопку (p) Play."""
        # Анулювати ігрову статистику.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_images()

        # Приховати курсор миші.
        pygame.mouse.set_visible(False)

        # Позбавитися надлишку прибульців та куль.
        self.aliens.empty()
        self.bullets.empty()

        # Створити новий флот та відцентрувати корабель.
        self._create_fleet()
        self.ship.center_ship()

        # 
        # self.run_game()


    def _fire_bullet(self):
        """Створити нову кулю та додати її до групи куль"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Оновити позицію куль та позбавитися старих куль."""
        # Оновити позиції куль
        self.bullets.update()

        # Позбавитися куль, що зникли.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Реакція на зіткнення куль з прибульцями."""
        # ВИдалити всі кулі та прибульців, що зіткнулися.
        colisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if colisions:
            for aliens in colisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
        self.sb.prep_score()
        self.sb.check_high_score()

        if not self.aliens:
            # Знищити наявні кулі та створити новий флот.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            # Підвищити рівень
            self.start_new_level()

    def start_new_level(self):
        """Підвищити новий рівень"""
        self.stats.level += 1
        self.sb.prep_level()

    def _create_fleet(self):
        """Створити флот прибульців."""
        # Створити прибульців та визначити кількість прибульців у ряду.
        # Відстань між прибульцями дорівнює ширині одного прибульця.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Визначити, яка кількість рядів прибульцію поміщається на екрані.
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)

        # Створити повний флот прибульців.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)


        # # Створити перший ряд прибульців.
        # for alien_number in range(number_aliens_x):
        #     # Створити прибульця та поставити його до ряду.
        #     self._create_alien(alien_number)

    def _create_alien(self, alien_number, row_number):
        """Створити прибульця та поставити його до ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):

        """
        Реагує відповідно до того, чи досяг котрийсь
        із прибульців краю екрана.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Спуск всього флоту та зміна його напрямку."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self):
        """
        Перевірити, чи флот знаходиться на краю,
        тоді оновити позиції всіх прибульців флоту.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # укати зіткнення куль із прибульцями.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Шукати чи котрийсь із прибульців досяг нижнього краю екрана.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Реагувати на зіткнення прибульця з кораблем."""
        if self.stats.ship_left > 0:
            # Зменшити ship_left та оновити табло
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Позбавитися надлишку прибульців та куль.
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель.
            self._create_fleet()
            self.ship.center_ship()

            # ПАуза.
            sleep(1.0)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Перевірити, чи не досяг якийсь прибулець нижнього краю екрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Зреагувати так, ніби корабель підбито.
                self._ship_hit()
                break

    def _update_screen(self):
        """Увімкнути зображення на екрані та перемкнутися на новий екран."""
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.original_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Намалювати інформацію про рахунок.
        self.sb.show_score()

        # НАмалювати кнопку Play, якщо гра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Створити екземпляр гри та запустити гру.
    ai = AlienInvasion()
    ai.run_game()

