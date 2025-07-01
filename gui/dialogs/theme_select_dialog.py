from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import pyqtSignal
from gui.themes.classic.dark_theme import DarkTheme
from gui.themes.classic.light_theme import LightTheme
from gui.themes.classic.green_theme import GreenTheme
from gui.themes.classic.blue_theme import BlueTheme
from gui.themes.classic.red_theme import RedTheme
from gui.themes.classic.yellow_theme import YellowTheme
from gui.themes.theme_manager import ThemeManager
from gui.themes.modern.modern_dark_theme import ModernDarkTheme
from gui.themes.modern.modern_light_theme import ModernLightTheme
from gui.themes.modern.modern_green_theme import ModernGreenTheme
from gui.themes.modern.modern_blue_theme import ModernBlueTheme
from gui.themes.modern.modern_red_theme import ModernRedTheme
from gui.themes.modern.modern_yellow_theme import ModernYellowTheme
from locales.locale_manager import LocaleManager

class ThemeSelectDialog(QDialog):
    language_changed = pyqtSignal()  # Сигнал для повідомлення про зміну мови
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(LocaleManager.get_locale("theme_select_dialog", "window_title"))
        self.setFixedSize(300, 280)
        layout = QVBoxLayout()
        
        # Вибір стилю теми
        layout.addWidget(QLabel(LocaleManager.get_locale("theme_select_dialog", "style_label")))
        self.style_combo = QComboBox()
        self.style_combo.addItems([LocaleManager.get_locale("theme_select_dialog", "modern"), LocaleManager.get_locale("theme_select_dialog", "classic")])
        layout.addWidget(self.style_combo)
        
        # Вибір кольору теми
        layout.addWidget(QLabel(LocaleManager.get_locale("theme_select_dialog", "color_label")))
        self.color_combo = QComboBox()
        self.color_combo.addItems([
            LocaleManager.get_locale("theme_select_dialog", "dark"), LocaleManager.get_locale("theme_select_dialog", "light"), LocaleManager.get_locale("theme_select_dialog", "green"), LocaleManager.get_locale("theme_select_dialog", "blue"), LocaleManager.get_locale("theme_select_dialog", "red"), LocaleManager.get_locale("theme_select_dialog", "yellow")
        ])
        layout.addWidget(self.color_combo)
        
        # Вибір мови
        layout.addWidget(QLabel(LocaleManager.get_locale("theme_select_dialog", "language_label")))
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            LocaleManager.get_locale("theme_select_dialog", "ukrainian"),
            LocaleManager.get_locale("theme_select_dialog", "english")
        ])
        layout.addWidget(self.language_combo)
        
        # Кнопка OK
        ok_btn = QPushButton(LocaleManager.get_locale("theme_select_dialog", "ok_button"))
        ok_btn.clicked.connect(self.apply_changes)
        layout.addWidget(ok_btn)
        
        self.setLayout(layout)
        self.style_combo.currentIndexChanged.connect(self.update_color_combo)
        self.update_color_combo()
        
        # Встановити поточні значення у комбобоксах
        self._set_current_values()

    def _set_current_values(self):
        # Встановити поточну тему у комбобоксах
        current = ThemeManager.current_theme()
        modern_map = {
            ModernDarkTheme: (0, 0), ModernLightTheme: (0, 1), ModernGreenTheme: (0, 2), ModernBlueTheme: (0, 3), ModernRedTheme: (0, 4), ModernYellowTheme: (0, 5)
        }
        classic_map = {
            DarkTheme: (1, 0), LightTheme: (1, 1), GreenTheme: (1, 2), BlueTheme: (1, 3), RedTheme: (1, 4), YellowTheme: (1, 5)
        }
        idxs = modern_map.get(current) or classic_map.get(current) or (0, 0)
        self.style_combo.setCurrentIndex(idxs[0])
        self.color_combo.setCurrentIndex(idxs[1])
        
        # Встановити поточну мову
        current_locale = LocaleManager.get_current_locale_code()
        if current_locale == "uk":
            self.language_combo.setCurrentIndex(0)
        else:
            self.language_combo.setCurrentIndex(1)

    def update_color_combo(self):
        style = self.style_combo.currentIndex()
        self.color_combo.clear()
        if style == 0:
            self.color_combo.addItems([LocaleManager.get_locale("theme_select_dialog", "dark"), LocaleManager.get_locale("theme_select_dialog", "light"), LocaleManager.get_locale("theme_select_dialog", "green"), LocaleManager.get_locale("theme_select_dialog", "blue"), LocaleManager.get_locale("theme_select_dialog", "red"), LocaleManager.get_locale("theme_select_dialog", "yellow")])
        else:
            self.color_combo.addItems([LocaleManager.get_locale("theme_select_dialog", "dark"), LocaleManager.get_locale("theme_select_dialog", "light"), LocaleManager.get_locale("theme_select_dialog", "green"), LocaleManager.get_locale("theme_select_dialog", "blue"), LocaleManager.get_locale("theme_select_dialog", "red"), LocaleManager.get_locale("theme_select_dialog", "yellow")])

    def apply_changes(self):
        # Застосувати тему
        style = self.style_combo.currentIndex()
        color = self.color_combo.currentIndex()
        if style == 0:
            theme_list = [ModernDarkTheme, ModernLightTheme, ModernGreenTheme, ModernBlueTheme, ModernRedTheme, ModernYellowTheme]
        else:
            theme_list = [DarkTheme, LightTheme, GreenTheme, BlueTheme, RedTheme, YellowTheme]
        ThemeManager.apply_theme(theme_list[color])
        
        # Застосувати мову
        language_index = self.language_combo.currentIndex()
        current_locale = LocaleManager.get_current_locale_code()
        new_locale = "uk" if language_index == 0 else "en"
        
        if current_locale != new_locale:
            available_locales = LocaleManager.get_available_locales()
            LocaleManager.set_locale(available_locales[new_locale])
            self.language_changed.emit()  # Сигналізувати про зміну мови
        
        self.accept()

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            for btn in self.findChildren(QPushButton):
                if btn.text().lower() in [LocaleManager.get_locale("common_dialogs", "ok_text"), LocaleManager.get_locale("common_dialogs", "select_text")]:
                    btn.click()
                    return
        super().keyPressEvent(event)
