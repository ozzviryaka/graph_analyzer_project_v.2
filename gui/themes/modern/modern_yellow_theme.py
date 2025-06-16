from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class ModernYellowTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 252, 230))
        palette.setColor(QPalette.WindowText, QColor(80, 70, 20))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(255, 250, 200))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 252, 230))
        palette.setColor(QPalette.ToolTipText, QColor(80, 70, 20))
        palette.setColor(QPalette.Text, QColor(80, 70, 20))
        palette.setColor(QPalette.Button, QColor(255, 250, 200))
        palette.setColor(QPalette.ButtonText, QColor(80, 70, 20))
        palette.setColor(QPalette.BrightText, QColor(255, 60, 60))
        palette.setColor(QPalette.Link, QColor(255, 200, 0))
        palette.setColor(QPalette.Highlight, QColor(255, 200, 0))
        palette.setColor(QPalette.HighlightedText, QColor(80, 70, 20))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(220, 210, 180))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(220, 210, 180))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #fffce6;
                color: #504614;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #fffce6;
            }
            QPushButton, QPushButton:flat, QPushButton[flat="true"] {
                color: #504614 !important;
                background: #fff6b2;
                border-radius: 7px;
                border: 1.5px solid #e6dcb2;
                padding: 5px 10px;
            }
            QPushButton:flat, QPushButton[flat="true"] {
                background: transparent;
                border: none;
            }
            QGraphicsView QPushButton, QGraphicsWidget QPushButton {
                color: #504614 !important;
                background: #fff6b2;
            }
            QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #fff;
                color: #504614;
                border-radius: 7px;
                border: 1.5px solid #e6dcb2;
                padding: 5px 10px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #fff0b2;
                border: 1.5px solid #ffd700;
            }
            QPushButton:pressed {
                background-color: #e6dcb2;
            }
            QPushButton:focus {
                border: 1.5px solid #e6dcb2;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 1.5px solid #ff3c3c;
            }
            QTabBar::tab {
                background: #fff6b2;
                color: #504614;
                border-radius: 8px 8px 0 0;
                padding: 8px 22px;
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
                background: #fff0b2;
                color: #ffd700;
                border: 2px solid #ffd700;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1.5px solid #e6dcb2;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabWidget::pane {
                border: 1.5px solid #e6dcb2;
                border-radius: 0 0 8px 8px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #fffce6;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #ffd700;
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
                background: #ffd700;
                border: 1.5px solid #ffd700;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #fff;
                border: 1.5px solid #e6dcb2;
            }
            QGroupBox {
                border: 1.5px solid #e6dcb2;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #fff6b2;
                color: #504614;
                border: 1.5px solid #ffd700;
                border-radius: 7px;
            }
            QProgressBar {
                background-color: #fff;
                color: #504614;
                border: 1.5px solid #e6dcb2;
                border-radius: 7px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #ffd700;
                border-radius: 7px;
            }
            QSlider::groove:horizontal, QSlider::groove:vertical {
                background: #fff6b2;
                border: 1.5px solid #e6dcb2;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal, QSlider::handle:vertical {
                background: #ffd700;
                border: 1.5px solid #ffd700;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
                background: #ffd700;
                color: #fff;
            }
            QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover {
                background: #ffecb3;
                color: #fff;
            }
        ''')
