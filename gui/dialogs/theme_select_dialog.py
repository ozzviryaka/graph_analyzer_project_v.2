from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from gui.themes.dark_theme import DarkTheme
from gui.themes.modern_dark_theme import ModernDarkTheme
from gui.themes.theme_manager import ThemeManager

class ThemeSelectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вибір теми")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Оберіть тему інтерфейсу:"))
        self.combo = QComboBox()
        self.combo.addItem("Класична темна")
        self.combo.addItem("Сучасна темна")
        layout.addWidget(self.combo)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.apply_theme)
        layout.addWidget(ok_btn)
        self.setLayout(layout)
        # Встановити поточну тему у комбобокс
        current = ThemeManager.current_theme()
        if current is ModernDarkTheme:
            self.combo.setCurrentIndex(1)
        else:
            self.combo.setCurrentIndex(0)

    def apply_theme(self):
        idx = self.combo.currentIndex()
        if idx == 1:
            ThemeManager.apply_theme(ModernDarkTheme)
        else:
            ThemeManager.apply_theme(DarkTheme)
        self.accept()
