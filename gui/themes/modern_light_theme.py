from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class ModernLightTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        # Сучасний світлий контрастний фон
        palette.setColor(QPalette.Window, QColor(245, 247, 250))
        palette.setColor(QPalette.WindowText, QColor(30, 30, 30))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 242, 245))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ToolTipText, QColor(30, 30, 30))
        palette.setColor(QPalette.Text, QColor(30, 30, 30))
        palette.setColor(QPalette.Button, QColor(240, 242, 245))
        palette.setColor(QPalette.ButtonText, QColor(30, 30, 30))
        palette.setColor(QPalette.BrightText, QColor(255, 60, 60))  # Яскравий червоний для помилок
        palette.setColor(QPalette.Link, QColor(0, 120, 255))  # Яскравий синій
        palette.setColor(QPalette.Highlight, QColor(0, 120, 255))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(180, 180, 180))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(180, 180, 180))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #f5f7fa;
                color: #1e1e1e;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #f5f7fa;
            }
            QPushButton, QPushButton:flat, QPushButton[flat="true"] {
                color: #1e1e1e !important;
                background: #f0f2f5;
                border-radius: 7px;
                border: 1.5px solid #e0e3e8;
                padding: 5px 10px;
            }
            QPushButton:flat, QPushButton[flat="true"] {
                background: transparent;
                border: none;
            }
            QGraphicsView QPushButton, QGraphicsWidget QPushButton {
                color: #1e1e1e !important;
                background: #f0f2f5;
            }
            QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #fff;
                color: #1e1e1e;
                border-radius: 7px;
                border: 1.5px solid #e0e3e8;
                padding: 5px 10px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #e6f0ff;
                border: 1.5px solid #0078ff;
            }
            QPushButton:pressed {
                background-color: #e0e3e8;
            }
            QPushButton:focus {
                border: 1.5px solid #e0e3e8;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 1.5px solid #ff3c3c;
            }
            QTabBar::tab {
                background: #f0f2f5;
                color: #1e1e1e;
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
                background: #e6f0ff;
                color: #0078ff;
                border: 2px solid #0078ff;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1.5px solid #e0e3e8;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabWidget::pane {
                border: 1.5px solid #e0e3e8;
                border-radius: 0 0 8px 8px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #f5f7fa;
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
                border: 1.5px solid #b0b3b8;
            }
            QGroupBox {
                border: 1.5px solid #e0e3e8;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #f0f2f5;
                color: #1e1e1e;
                border: 1.5px solid #0078ff;
                border-radius: 7px;
            }
            QProgressBar {
                background-color: #fff;
                color: #1e1e1e;
                border: 1.5px solid #e0e3e8;
                border-radius: 7px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0078ff;
                border-radius: 7px;
            }
            QSlider::groove:horizontal, QSlider::groove:vertical {
                background: #f0f2f5;
                border: 1.5px solid #e0e3e8;
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
