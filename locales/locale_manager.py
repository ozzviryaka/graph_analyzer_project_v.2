import json
import os
from typing import Any, Optional

class LocaleManager:
    _locale = {}
    _current_path = None

    @classmethod
    def load_locale(cls, path: Optional[str] = None):
        if path is None:
            path = os.path.join(os.path.dirname(__file__), "uk_locale.json")
        cls._current_path = path
        with open(path, "r", encoding="utf-8") as f:
            cls._locale = json.load(f)

    @classmethod
    def set_locale(cls, locale_filename: str):
        """
        Змінити поточний файл локалізації (наприклад, 'uk_locale.json', 'en_locale.json').
        """
        path = os.path.join(os.path.dirname(__file__), locale_filename)
        cls.load_locale(path)

    @classmethod
    def get_locale(cls, section: str, key: str, **kwargs) -> str:
        value = cls._locale.get(section, {}).get(key, [key])
        if isinstance(value, str) and kwargs:
            try:
                return value.format(**kwargs)
            except Exception:
                return value  # fallback if formatting fails
        return value

    @classmethod
    def reload_locale(cls):
        if cls._current_path:
            cls.load_locale(cls._current_path)
