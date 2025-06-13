from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class BlueTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(28, 36, 48))
        palette.setColor(QPalette.WindowText, QColor(220, 230, 255))
        palette.setColor(QPalette.Base, QColor(22, 28, 38))
        palette.setColor(QPalette.AlternateBase, QColor(36, 44, 58))
        palette.setColor(QPalette.ToolTipBase, QColor(220, 230, 255))
        palette.setColor(QPalette.ToolTipText, QColor(28, 36, 48))
        palette.setColor(QPalette.Text, QColor(220, 230, 255))
        palette.setColor(QPalette.Button, QColor(36, 44, 58))
        palette.setColor(QPalette.ButtonText, QColor(220, 230, 255))
        palette.setColor(QPalette.BrightText, QColor(0, 170, 255))
        palette.setColor(QPalette.Link, QColor(0, 120, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 255))
        palette.setColor(QPalette.HighlightedText, QColor(28, 36, 48))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 140, 180))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 140, 180))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #1c2330;
                color: #b6cfff;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #1c2330;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #223355;
                color: #b6cfff;
                border-radius: 8px;
                border: 1px solid #3f7fae;
                padding: 6px 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2e3d5d;
                color: #b6cfff;
                border: 1px solid #3f7fae;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #3f7fae;
                color: #1c2330;
            }
            QPushButton:pressed {
                background-color: #2e3d5d;
            }
            QTabBar {
                qproperty-drawBase: 0;
                alignment: center;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background: #223355;
                color: #b6cfff;
                border-radius: 8px 8px 0 0;
                padding: 8px 20px;
                margin-right: 2px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background: #3f7fae;
                color: #1c2330;
                border: 2px solid #3f7fae;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1px solid #3f7fae;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabWidget::pane {
                border-top: 2px solid #3f7fae;
                top: -1px;
            }
        ''')
