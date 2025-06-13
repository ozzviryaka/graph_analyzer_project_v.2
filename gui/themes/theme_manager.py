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
        cls._current_theme = theme
        theme.apply()

    @classmethod
    def current_theme(cls):
        return cls._current_theme
