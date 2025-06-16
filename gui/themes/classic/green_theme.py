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
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #1e281e;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #223322;
                color: #b6ffb6;
                border-radius: 6px;
                border: 1px solid #3fae3f;
                padding: 4px 8px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #3fae3f;
                border: 1px solid #3fae3f;
            }
            QPushButton:pressed {
                background-color: #2e4d2e;
            }
            QTabBar::tab {
                background: #223322;
                color: #b6ffb6;
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
                border: 1px solid #3fae3f;
                border-radius: 0 0 6px 6px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #1e281e;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #3fae3f;
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
                background: #3fae3f;
                border: 1px solid #3fae3f;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #223322;
                border: 1px solid #3fae3f;
            }
            QGroupBox {
                border: 1px solid #3fae3f;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #223322;
                color: #b6ffb6;
                border: 1px solid #3fae3f;
                border-radius: 6px;
            }
        ''')
