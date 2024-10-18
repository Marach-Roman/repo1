import sys
import pygame
import pygame.font

from settings import Settings

class Help:
    """Ініціалізувати вікно Допомоги"""

    def __init__(self, sections):
        """Ініціалізувати вікно з допомогою користувачеві"""
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.arrow = pygame.image.load('images/arrow_all_rd.png')
        self.arrow_rect = self.arrow.get_rect()
        self.arrow_rect.topleft = (10, 10)


        self.text_color = (0, 0, 0)
        self.sections = sections

        self.font_title = pygame.font.SysFont(None, 48)
        self.font_subtitle = pygame.font.SysFont(None, 42)
        self.font_text = pygame.font.SysFont(None, 36)

        # Викликати метод prepare_text() для створення повідомлення і всього іншого
        self.prepare_text()

        self.screen_rect = self.screen.get_rect()

        self.scroll_up = False
        self.scroll_down = False

    def run_help(self):
        """Основний цикл Допомоги"""
        while True:
            self._check_events()
            self._update_scroll()
            self._update_screen()

    def _check_events(self):
        """Реагувати на натискання клавіш та події миші"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.settings.scroll_offset += 20 # Прокрутка вверх
                elif event.button == 5:
                    self.settings.scroll_offset -= 20 # Прокрутка вниз


    def _check_keydown_events(self, event):
        """Реагувати на натискання клавіш"""
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_UP:
            self.settings.scroll_up = True
        elif event.key == pygame.K_DOWN:
            self.settings.scroll_down = True

    def _check_keyup_events(self, event):
        """Реагувати, коли клавіша не натиснута"""
        if event.key == pygame.K_UP:
            self.scroll_up = False
        if event.key == pygame.K_DOWN:
            self.scroll_down = False


    def _update_scroll(self):
        """Оновити зсув прокрутки"""
        if self.scroll_up:
            self.settings.scroll_offset += self.settings.scroll_speed
        if self.scroll_down:
            self.settings.scroll_offset -= self.settings.scroll_speed


    def read_file(self, filename):
        """відкриті файли, де містяться cписки"""
        with open(filename, "r", encoding='utf-8') as f:
            self.text_lines = f.read().splitlines()


    def prepare_text(self):
        """Створити повідомлення"""
        self.msg_images = []
        self.msg_image_rects = []

        # Початковий віступ
        y_offset = 25
        welcome_title = 'Привіт, це допомога для гравця!'
        welcome_title_im = self.font_title.render(
                welcome_title, True, self.text_color)
        welcome_title_rect = welcome_title_im.get_rect()
        welcome_title_rect.midtop = (self.settings.screen_width // 2, y_offset)
        y_offset += welcome_title_rect.height + 40

        self.msg_images.append((welcome_title_im, welcome_title_rect))

        for section in self.sections:
            subtitle, filename = section

            # Рендер підзаголовка
            subtitle_im = self.font_subtitle.render(subtitle, True, self.text_color)
            subtitle_rect = subtitle_im.get_rect()
            subtitle_rect.midtop = (self.settings.screen_width // 2, y_offset)
            # y_offset += subtitle_rect.top + 20
            y_offset += subtitle_rect.height + 20

            self.msg_images.append((subtitle_im, subtitle_rect))

            # Зчитування тексту з файлу
            text_lines = self.read_file(filename)

            # Рендер тексту з файлу
            for line in self.text_lines:
                self.msg_im = self.font_text.render(line, True, self.text_color)
                self.msg_image_rect = self.msg_im.get_rect()
                self.msg_image_rect.topleft = (50, y_offset)
                y_offset += self.msg_image_rect.height + 10

                self.msg_images.append((self.msg_im, self.msg_image_rect))
    def _check_edges(self):
        """Повертає істинуу, якщо досягнуто кінця екрану""" 
        if self.screen.top and self.screen_rect.top > 0:
            if self.settings.scroll_offset > 0:  # Перевірка, щоб не прокручувати далі тексту
                self.settings.scroll_offset -= self.settings.scroll_speed
        if self.screen.bottom and self.screen_rect.bottom > self.screen.get_height():
            if self.settings.scroll_offset < 0:
                self.settings.scroll_offset += self.settings.scroll_speed
            return False
        return True



    def _update_screen(self):
        """Увімкнути зображення на екрані"""
        self.screen.fill(self.settings.bg_color)
        
        # Відобразити текст на екрані
        for img, rect in self.msg_images:
            adjusted_rect = rect.copy()
            adjusted_rect.y += self.settings.scroll_offset
            self.screen.blit(img, adjusted_rect)

        self.screen.blit(self.arrow, self.arrow_rect)
            
        pygame.display.flip()

if __name__ == '__main__':
    sections = [
        ('Опис сюжету гри:', 'list_win_help.txt'),
        ('Вид прибульців:', 'list_win_help_2.txt'),
        ('Рейтинг очок:', 'list_win_help_3.txt'),
        ('Клавіші:', 'list_win_help_4.txt')
        ]
    hl = Help(sections)
    hl.run_help()
