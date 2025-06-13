from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from gui.themes.dark_theme import DarkTheme
from gui.themes.light_theme import LightTheme
from gui.themes.green_theme import GreenTheme
from gui.themes.blue_theme import BlueTheme
from gui.themes.theme_manager import ThemeManager

class ThemeSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вибір теми")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Оберіть тему інтерфейсу:"))
        self.combo = QComboBox()
        self.combo.addItem("Темна")
        self.combo.addItem("Світла")
        self.combo.addItem("Зелена")
        self.combo.addItem("Синя")
        layout.addWidget(self.combo)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.apply_theme)
        layout.addWidget(ok_btn)
        self.setLayout(layout)
        # Встановити поточну тему у комбобокс
        current = ThemeManager.current_theme()
        if current is LightTheme:
            self.combo.setCurrentIndex(1)
        elif current is GreenTheme:
            self.combo.setCurrentIndex(2)
        elif current is BlueTheme:
            self.combo.setCurrentIndex(3)
        else:
            self.combo.setCurrentIndex(0)

    def apply_theme(self):
        idx = self.combo.currentIndex()
        if idx == 1:
            ThemeManager.apply_theme(LightTheme)
        elif idx == 2:
            ThemeManager.apply_theme(GreenTheme)
        elif idx == 3:
            ThemeManager.apply_theme(BlueTheme)
        else:
            ThemeManager.apply_theme(DarkTheme)
        self.accept()
