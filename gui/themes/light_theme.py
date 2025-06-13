from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class LightTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(245, 245, 250))
        palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(235, 235, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.Button, QColor(235, 235, 245))
        palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.BrightText, QColor(255, 85, 85))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(100, 180, 255))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(180, 180, 180))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(180, 180, 180))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #f5f5fa;
                color: #222;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #f5f5fa;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #fff;
                color: #222;
                border-radius: 8px;
                border: 1px solid #d0d0e0;
                padding: 6px 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #f8f8ff;
                color: #222;
                border: 1px solid #b0b0c0;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0e0f0;
                color: #0078d7;
            }
            QPushButton:pressed {
                background-color: #d0d0e0;
                color: #005fa3;
            }
            QTabBar::tab {
                background: #f5f5fa;
                color: #222;
                border-radius: 8px 8px 0 0;
                padding: 8px 20px;
                margin-right: 2px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: #f0f0f0;
                color: #1976d2;
                border: 2px solid #1976d2;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1px solid #cccccc;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar {
                qproperty-drawBase: 0;
                alignment: center;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QMenu {
                background-color: #fff;
                color: #222;
                border: 1px solid #d0d0e0;
            }
            QMenu::item:selected {
                background-color: #e0e0f0;
                color: #0078d7;
            }
        ''')
