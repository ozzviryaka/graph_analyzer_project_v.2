from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class RedTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(48, 28, 28))
        palette.setColor(QPalette.WindowText, QColor(255, 220, 220))
        palette.setColor(QPalette.Base, QColor(38, 22, 22))
        palette.setColor(QPalette.AlternateBase, QColor(58, 36, 36))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 220, 220))
        palette.setColor(QPalette.ToolTipText, QColor(48, 28, 28))
        palette.setColor(QPalette.Text, QColor(255, 220, 220))
        palette.setColor(QPalette.Button, QColor(58, 36, 36))
        palette.setColor(QPalette.ButtonText, QColor(255, 220, 220))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(200, 0, 0))
        palette.setColor(QPalette.Highlight, QColor(200, 0, 0))
        palette.setColor(QPalette.HighlightedText, QColor(48, 28, 28))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(180, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(180, 120, 120))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #301c1c;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #3a2222;
                color: #ffdcdc;
                border-radius: 6px;
                border: 1px solid #ae3f3f;
                padding: 4px 8px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #ae3f3f;
                border: 1px solid #ae3f3f;
            }
            QPushButton:pressed {
                background-color: #4d2e2e;
            }
            QTabBar::tab {
                background: #3a2222;
                color: #ffdcdc;
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
                background: #ae3f3f;
                color: #301c1c;
                border: 2px solid #ae3f3f;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1px solid #ae3f3f;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabWidget::pane {
                border: 1px solid #ae3f3f;
                border-radius: 0 0 6px 6px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #301c1c;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #ae3f3f;
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
                background: #ae3f3f;
                border: 1px solid #ae3f3f;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #3a2222;
                border: 1px solid #ae3f3f;
            }
            QGroupBox {
                border: 1px solid #ae3f3f;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #3a2222;
                color: #ffdcdc;
                border: 1px solid #ae3f3f;
                border-radius: 6px;
            }
        ''')
