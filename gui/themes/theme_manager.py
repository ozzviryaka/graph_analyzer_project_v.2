from utils.logger import Logger
from .dark_theme import DarkTheme
from .light_theme import LightTheme
from .green_theme import GreenTheme
from .blue_theme import BlueTheme
from .red_theme import RedTheme
from .yellow_theme import YellowTheme

class ThemeManager:
    _current_theme = DarkTheme

    @classmethod
    def apply_theme(cls, theme):
        logger = Logger()
        logger.info(f"Зміна теми на: {theme.__name__ if hasattr(theme, '__name__') else str(theme)}")
        cls._current_theme = theme
        theme.apply()

    @classmethod
    def current_theme(cls):
        return cls._current_theme
