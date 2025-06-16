from utils.logger import Logger
from .dark_theme import DarkTheme
from .light_theme import LightTheme
from .green_theme import GreenTheme
from .blue_theme import BlueTheme
from .red_theme import RedTheme
from .yellow_theme import YellowTheme
from .modern_dark_theme import ModernDarkTheme
import os
import json

class ThemeManager:
    _current_theme = DarkTheme
    _settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'settings.json')

    @classmethod
    def apply_theme(cls, theme):
        logger = Logger()
        logger.info(f"Зміна теми на: {theme.__name__ if hasattr(theme, '__name__') else str(theme)}")
        cls._current_theme = theme
        theme.apply()
        cls._save_theme_name(theme)

    @classmethod
    def _save_theme_name(cls, theme):
        theme_name = cls._theme_to_name(theme)
        try:
            with open(cls._settings_path, 'w', encoding='utf-8') as f:
                json.dump({'theme': theme_name}, f)
        except Exception as e:
            Logger().error(f"Не вдалося зберегти тему: {e}")

    @classmethod
    def load_theme(cls):
        try:
            with open(cls._settings_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                theme_name = data.get('theme', 'dark')
                theme = cls.name_to_theme(theme_name)
                if theme:
                    cls._current_theme = theme
                    theme.apply()
        except Exception:
            pass  # Якщо файл не знайдено або помилка, залишаємо дефолтну тему

    @classmethod
    def _theme_to_name(cls, theme):
        for name, t in cls.available_themes().items():
            if t is theme:
                return name
        return 'dark'

    @classmethod
    def name_to_theme(cls, name):
        return cls.available_themes().get(name, DarkTheme)

    @classmethod
    def current_theme(cls):
        return cls._current_theme

    @classmethod
    def available_themes(cls):
        return {
            'dark': DarkTheme,
            'light': LightTheme,
            'green': GreenTheme,
            'blue': BlueTheme,
            'red': RedTheme,
            'yellow': YellowTheme,
            'modern_dark': ModernDarkTheme
        }
