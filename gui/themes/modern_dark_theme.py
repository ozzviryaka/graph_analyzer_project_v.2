from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class ModernDarkTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        # Основні кольори
        palette.setColor(QPalette.Window, QColor(28, 28, 34))
        palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.Base, QColor(22, 22, 28))
        palette.setColor(QPalette.AlternateBase, QColor(36, 37, 43))
        palette.setColor(QPalette.ToolTipBase, QColor(40, 40, 48))
        palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
        palette.setColor(QPalette.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.Button, QColor(38, 40, 48))
        palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.BrightText, QColor(255, 85, 85))
        palette.setColor(QPalette.Link, QColor(100, 180, 255))
        palette.setColor(QPalette.Highlight, QColor(100, 180, 255))
        palette.setColor(QPalette.HighlightedText, QColor(28, 28, 34))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #1c1c22;
                color: #e0e0e0;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #23232b;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #23232b;
                color: #e0e0e0;
                border-radius: 8px;
                border: 1px solid #35363a;
                padding: 6px 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #282a36;
                color: #f8f8f2;
                border: 1px solid #44475a;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #44475a;
                color: #50fa7b;
            }
            QPushButton:pressed {
                background-color: #282a36;
                color: #8be9fd;
            }
            QTabBar::tab {
                background: #23232b;
                color: #e0e0e0;
                border-radius: 8px 8px 0 0;
                padding: 8px 20px;
                margin-right: 2px;
                min-width: 120px;
            }
            QTabBar {
                qproperty-drawBase: 0;
                alignment: center;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab:selected {
                background: #282a36;
                color: #50fa7b;
            }
            QTabWidget::pane {
                border-top: 2px solid #44475a;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23232b;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #44475a;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
            QMenu {
                background-color: #23232b;
                color: #e0e0e0;
                border: 1px solid #35363a;
            }
            QMenu::item:selected {
                background-color: #44475a;
                color: #50fa7b;
            }
        ''')
