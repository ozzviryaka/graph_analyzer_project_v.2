import json
import os
from typing import Any, Optional

class LocaleManager:
    _locale = {}
    _current_path = None

    @classmethod
    def load_locale(cls, path: Optional[str] = None):
        if path is None:
            # Спробувати завантажити збережену мову з settings.json
            saved_locale = cls._load_saved_locale()
            if saved_locale:
                filename = f"{saved_locale}_locale.json"
                path = os.path.join(os.path.dirname(__file__), filename)
            else:
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
        # Зберегти вибрану мову в settings.json
        cls._save_locale_to_settings()

    @classmethod
    def _load_saved_locale(cls) -> Optional[str]:
        """Завантажити збережену мову з settings.json"""
        try:
            settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    return settings.get("locale", None)
        except Exception:
            pass
        return None

    @classmethod
    def _save_locale_to_settings(cls):
        """Зберегти поточну мову в settings.json"""
        try:
            settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")
            current_locale = cls.get_current_locale_code()
            
            # Завантажити існуючі налаштування
            settings = {}
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            
            # Оновити мову
            settings["locale"] = current_locale
            
            # Зберегти налаштування
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    @classmethod
    def get_current_locale_code(cls) -> str:
        """
        Повертає код поточної мови (uk або en).
        """
        if cls._current_path:
            filename = os.path.basename(cls._current_path)
            if filename.startswith("uk_"):
                return "uk"
            elif filename.startswith("en_"):
                return "en"
        return "uk"  # за замовчуванням

    @classmethod
    def get_available_locales(cls) -> dict:
        """
        Повертає словник доступних мов у форматі {код: назва_файлу}.
        """
        return {
            "uk": "uk_locale.json",
            "en": "en_locale.json"
        }

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
