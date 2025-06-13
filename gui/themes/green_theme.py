from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class GreenTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 40, 30))
        palette.setColor(QPalette.WindowText, QColor(220, 255, 220))
        palette.setColor(QPalette.Base, QColor(24, 36, 24))
        palette.setColor(QPalette.AlternateBase, QColor(36, 48, 36))
        palette.setColor(QPalette.ToolTipBase, QColor(220, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(30, 40, 30))
        palette.setColor(QPalette.Text, QColor(220, 255, 220))
        palette.setColor(QPalette.Button, QColor(36, 48, 36))
        palette.setColor(QPalette.ButtonText, QColor(220, 255, 220))
        palette.setColor(QPalette.BrightText, QColor(0, 255, 0))
        palette.setColor(QPalette.Link, QColor(0, 200, 100))
        palette.setColor(QPalette.Highlight, QColor(0, 200, 100))
        palette.setColor(QPalette.HighlightedText, QColor(30, 40, 30))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 160, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 160, 120))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #1e281e;
                color: #b6ffb6;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #1e281e;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #223322;
                color: #b6ffb6;
                border-radius: 8px;
                border: 1px solid #3fae3f;
                padding: 6px 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2e4d2e;
                color: #b6ffb6;
                border: 1px solid #3fae3f;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3fae3f;
                color: #1e281e;
            }
            QPushButton:pressed {
                background-color: #2e4d2e;
            }
            QTabBar {
                qproperty-drawBase: 0;
                alignment: center;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #223322;
                color: #b6ffb6;
                border-radius: 8px 8px 0 0;
                padding: 8px 20px;
                margin-right: 2px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: #3fae3f;
                color: #1e281e;
                border: 2px solid #3fae3f;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1px solid #3fae3f;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabWidget::pane {
                border-top: 2px solid #3fae3f;
                top: -1px;
            }
        ''')
