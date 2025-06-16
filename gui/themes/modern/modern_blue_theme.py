from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class ModernBlueTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        palette.setColor(QPalette.WindowText, QColor(20, 40, 80))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(230, 240, 255))
        palette.setColor(QPalette.ToolTipBase, QColor(240, 248, 255))
        palette.setColor(QPalette.ToolTipText, QColor(20, 40, 80))
        palette.setColor(QPalette.Text, QColor(20, 40, 80))
        palette.setColor(QPalette.Button, QColor(230, 240, 255))
        palette.setColor(QPalette.ButtonText, QColor(20, 40, 80))
        palette.setColor(QPalette.BrightText, QColor(255, 60, 60))
        palette.setColor(QPalette.Link, QColor(0, 120, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 255))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(180, 200, 220))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(180, 200, 220))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #f0f8ff;
                color: #142850;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #f0f8ff;
            }
            QPushButton, QPushButton:flat, QPushButton[flat="true"] {
                color: #142850 !important;
                background: #e6f0ff;
                border-radius: 7px;
                border: 1.5px solid #b2c6e6;
                padding: 5px 10px;
            }
            QPushButton:flat, QPushButton[flat="true"] {
                background: transparent;
                border: none;
            }
            QGraphicsView QPushButton, QGraphicsWidget QPushButton {
                color: #142850 !important;
                background: #e6f0ff;
            }
            QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #fff;
                color: #142850;
                border-radius: 7px;
                border: 1.5px solid #b2c6e6;
                padding: 5px 10px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #d0e6ff;
                border: 1.5px solid #0078ff;
            }
            QPushButton:pressed {
                background-color: #b2c6e6;
            }
            QPushButton:focus {
                border: 1.5px solid #b2c6e6;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 1.5px solid #ff3c3c;
            }
            QTabBar::tab {
                background: #e6f0ff;
                color: #142850;
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
                background: #d0e6ff;
                color: #0078ff;
                border: 2px solid #0078ff;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1.5px solid #b2c6e6;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabWidget::pane {
                border: 1.5px solid #b2c6e6;
                border-radius: 0 0 8px 8px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #f0f8ff;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #0078ff;
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
                background: #0078ff;
                border: 1.5px solid #0078ff;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #fff;
                border: 1.5px solid #b2c6e6;
            }
            QGroupBox {
                border: 1.5px solid #b2c6e6;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #e6f0ff;
                color: #142850;
                border: 1.5px solid #0078ff;
                border-radius: 7px;
            }
            QProgressBar {
                background-color: #fff;
                color: #142850;
                border: 1.5px solid #b2c6e6;
                border-radius: 7px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078ff;
                border-radius: 7px;
            }
            QSlider::groove:horizontal, QSlider::groove:vertical {
                background: #e6f0ff;
                border: 1.5px solid #b2c6e6;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal, QSlider::handle:vertical {
                background: #0078ff;
                border: 1.5px solid #0078ff;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
                background: #0078ff;
                color: #fff;
            }
            QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover {
                background: #ff3c3c;
                color: #fff;
            }
        ''')
