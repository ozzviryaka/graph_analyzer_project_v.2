from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from gui.themes.dark_theme import DarkTheme
from gui.themes.light_theme import LightTheme
from gui.themes.green_theme import GreenTheme
from gui.themes.blue_theme import BlueTheme
from gui.themes.red_theme import RedTheme
from gui.themes.yellow_theme import YellowTheme
from gui.themes.theme_manager import ThemeManager
from gui.themes.modern_dark_theme import ModernDarkTheme
from gui.themes.modern_light_theme import ModernLightTheme
from gui.themes.modern_green_theme import ModernGreenTheme
from gui.themes.modern_blue_theme import ModernBlueTheme
from gui.themes.modern_red_theme import ModernRedTheme
from gui.themes.modern_yellow_theme import ModernYellowTheme

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
        self.combo.addItem("Червона")
        self.combo.addItem("Жовта")
        self.combo.addItem("Сучасна темна")
        self.combo.addItem("Сучасна світла")
        self.combo.addItem("Сучасна зелена")
        self.combo.addItem("Сучасна синя")
        self.combo.addItem("Сучасна червона")
        self.combo.addItem("Сучасна жовта")
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
        elif current is RedTheme:
            self.combo.setCurrentIndex(4)
        elif current is YellowTheme:
            self.combo.setCurrentIndex(5)
        elif current is ModernDarkTheme:
            self.combo.setCurrentIndex(6)
        elif current is ModernLightTheme:
            self.combo.setCurrentIndex(7)
        elif current is ModernGreenTheme:
            self.combo.setCurrentIndex(8)
        elif current is ModernBlueTheme:
            self.combo.setCurrentIndex(9)
        elif current is ModernRedTheme:
            self.combo.setCurrentIndex(10)
        elif current is ModernYellowTheme:
            self.combo.setCurrentIndex(11)
        else:
            self.combo.setCurrentIndex(0)

    def apply_theme(self):
        idx = self.combo.currentIndex()
        if idx == 0:
            ThemeManager.apply_theme(ModernDarkTheme)
        elif idx == 1:
            ThemeManager.apply_theme(ModernLightTheme)
        elif idx == 2:
            ThemeManager.apply_theme(ModernGreenTheme)
        elif idx == 3:
            ThemeManager.apply_theme(ModernBlueTheme)
        elif idx == 4:
            ThemeManager.apply_theme(ModernRedTheme)
        elif idx == 5:
            ThemeManager.apply_theme(ModernYellowTheme)
        else:
            ThemeManager.apply_theme(DarkTheme)
        self.accept()

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            for btn in self.findChildren(QPushButton):
                if btn.text().lower() in ["ok", "вибрати"]:
                    btn.click()
                    return
        super().keyPressEvent(event)
