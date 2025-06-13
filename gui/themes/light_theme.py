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
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #f5f5fa;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #fff;
                color: #222;
                border-radius: 6px;
                border: 1px solid #d0d0e0;
                padding: 4px 8px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #e0e0f0;
                border: 1px solid #1976d2;
            }
            QPushButton:pressed {
                background-color: #d0d0e0;
            }
            QTabBar::tab {
                background: #f5f5fa;
                color: #222;
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
            QTabWidget::pane {
                border: 1px solid #d0d0e0;
                border-radius: 0 0 6px 6px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #f5f5fa;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #1976d2;
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
                background: #1976d2;
                border: 1px solid #1976d2;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #fff;
                border: 1px solid #d0d0e0;
            }
            QGroupBox {
                border: 1px solid #d0d0e0;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #fff;
                color: #222;
                border: 1px solid #1976d2;
                border-radius: 6px;
            }
        ''')
