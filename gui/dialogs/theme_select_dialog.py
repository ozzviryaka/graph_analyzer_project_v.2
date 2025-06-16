from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
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

class ThemeSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вибір теми")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Оберіть стиль теми:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["Сучасна", "Класична"])
        layout.addWidget(self.style_combo)
        layout.addWidget(QLabel("Оберіть колір теми:"))
        self.color_combo = QComboBox()
        self.color_combo.addItems([
            "Темна", "Світла", "Зелена", "Синя", "Червона", "Жовта"
        ])
        layout.addWidget(self.color_combo)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.apply_theme)
        layout.addWidget(ok_btn)
        self.setLayout(layout)
        self.style_combo.currentIndexChanged.connect(self.update_color_combo)
        self.update_color_combo()
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

    def update_color_combo(self):
        style = self.style_combo.currentIndex()
        self.color_combo.clear()
        if style == 0:
            self.color_combo.addItems(["Темна", "Світла", "Зелена", "Синя", "Червона", "Жовта"])
        else:
            self.color_combo.addItems(["Темна", "Світла", "Зелена", "Синя", "Червона", "Жовта"])

    def apply_theme(self):
        style = self.style_combo.currentIndex()
        color = self.color_combo.currentIndex()
        if style == 0:
            theme_list = [ModernDarkTheme, ModernLightTheme, ModernGreenTheme, ModernBlueTheme, ModernRedTheme, ModernYellowTheme]
        else:
            theme_list = [DarkTheme, LightTheme, GreenTheme, BlueTheme, RedTheme, YellowTheme]
        ThemeManager.apply_theme(theme_list[color])
        self.accept()

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            for btn in self.findChildren(QPushButton):
                if btn.text().lower() in ["ok", "вибрати"]:
                    btn.click()
                    return
        super().keyPressEvent(event)
