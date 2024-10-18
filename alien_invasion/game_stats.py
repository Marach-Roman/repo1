import json

filename = 'high_score_file/high_score.json'

class GameStats:
    """Відстежування статистики гри."""

    def __init__(self, ai_game):
        """ІНіціалізувати статистики."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Розпочати гру в неактивному стані.
        self.game_active = False

        # Завантажити рекорд з файлу або встановити 0, та зберегти його
        try:
            with open(filename) as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0
            

    def save_high_score(self):
        """Якщо рекорд не збережеений - зберегри його"""
        with open(filename, "w") as f:
            json.dump(self.high_score, f)

    def reset_stats(self):
        """Ініціалізувати статистики, що може змінюватися впродовж гри."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        