from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class DarkTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 32, 36))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(24, 26, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(36, 38, 43))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(36, 38, 43))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        app.setPalette(dark_palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #23252b;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #23252b;
                color: #f0f0f0;
                border-radius: 6px;
                border: 1px solid #393b40;
                padding: 4px 8px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #2d2f36;
                border: 1px solid #4a90e2;
            }
            QPushButton:pressed {
                background-color: #1e1f23;
            }
            QTabBar::tab {
                background: #23252b;
                color: #f0f0f0;
                border-radius: 6px 6px 0 0;
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
                background: #2d2f36;
                color: #4a90e2;
                border: 2px solid #4a90e2;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1px solid #393b40;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabWidget::pane {
                border: 1px solid #393b40;
                border-radius: 0 0 6px 6px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23252b;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #4a90e2;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                border-radius: 4px;
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background: #4a90e2;
                border: 1px solid #4a90e2;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #23252b;
                border: 1px solid #393b40;
            }
            QGroupBox {
                border: 1px solid #393b40;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #23252b;
                color: #f0f0f0;
                border: 1px solid #4a90e2;
                border-radius: 6px;
            }
        ''')
