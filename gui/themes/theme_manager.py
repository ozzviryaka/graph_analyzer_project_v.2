class ThemeManager:
    _current_theme = None

    @staticmethod
    def apply_theme(theme_class):
        ThemeManager._current_theme = theme_class
        theme_class.apply()

    @staticmethod
    def current_theme():
        return ThemeManager._current_theme
