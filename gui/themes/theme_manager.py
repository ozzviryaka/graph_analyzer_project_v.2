from utils.logger import Logger
from locales.locale_manager import LocaleManager
from .classic.dark_theme import DarkTheme
from .classic.light_theme import LightTheme
from .classic.green_theme import GreenTheme
from .classic.blue_theme import BlueTheme
from .classic.red_theme import RedTheme
from .classic.yellow_theme import YellowTheme
from .modern.modern_dark_theme import ModernDarkTheme
from .modern.modern_light_theme import ModernLightTheme
from .modern.modern_green_theme import ModernGreenTheme
from .modern.modern_blue_theme import ModernBlueTheme
from .modern.modern_red_theme import ModernRedTheme
from .modern.modern_yellow_theme import ModernYellowTheme
import os
import json

class ThemeManager:
    _current_theme = DarkTheme
    _settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'settings.json')

    @classmethod
    def apply_theme(cls, theme):
        logger = Logger()
        theme_name = theme.__name__ if hasattr(theme, '__name__') else str(theme)
        logger.info(LocaleManager.get_locale("theme_manager", "theme_change_info").format(theme_name=theme_name))
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
            Logger().error(LocaleManager.get_locale("theme_manager", "theme_save_error").format(error=str(e)))

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
            'modern_dark': ModernDarkTheme,
            'modern_light': ModernLightTheme,
            'modern_green': ModernGreenTheme,
            'modern_blue': ModernBlueTheme,
            'modern_red': ModernRedTheme,
            'modern_yellow': ModernYellowTheme
        }
