from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class YellowTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 250, 220))
        palette.setColor(QPalette.WindowText, QColor(80, 60, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 230))
        palette.setColor(QPalette.AlternateBase, QColor(255, 245, 180))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 200))
        palette.setColor(QPalette.ToolTipText, QColor(80, 60, 0))
        palette.setColor(QPalette.Text, QColor(80, 60, 0))
        palette.setColor(QPalette.Button, QColor(255, 245, 180))
        palette.setColor(QPalette.ButtonText, QColor(80, 60, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 200, 0))
        palette.setColor(QPalette.Link, QColor(255, 180, 0))
        palette.setColor(QPalette.Highlight, QColor(255, 200, 0))
        palette.setColor(QPalette.HighlightedText, QColor(80, 60, 0))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(180, 160, 80))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(180, 160, 80))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #fffadc;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #fff5b4;
                color: #805c00;
                border-radius: 6px;
                border: 1px solid #e2b800;
                padding: 4px 8px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #ffe066;
                border: 1px solid #e2b800;
            }
            QPushButton:pressed {
                background-color: #fff5b4;
            }
            QTabBar::tab {
                background: #fff5b4;
                color: #805c00;
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
                background: #ffe066;
                color: #805c00;
                border: 2px solid #e2b800;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1px solid #e2b800;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
            }
            QTabWidget::pane {
                border: 1px solid #e2b800;
                border-radius: 0 0 6px 6px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #fffadc;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #e2b800;
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
                background: #e2b800;
                border: 1px solid #e2b800;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #fff5b4;
                border: 1px solid #e2b800;
            }
            QGroupBox {
                border: 1px solid #e2b800;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #fff5b4;
                color: #805c00;
                border: 1px solid #e2b800;
                border-radius: 6px;
            }
        ''')
