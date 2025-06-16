from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory, QApplication

class ModernDarkTheme:
    @staticmethod
    def apply():
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        # Глибокий темний фон
        palette.setColor(QPalette.Window, QColor(18, 20, 24))
        palette.setColor(QPalette.WindowText, QColor(245, 245, 245))
        palette.setColor(QPalette.Base, QColor(24, 26, 30))
        palette.setColor(QPalette.AlternateBase, QColor(28, 30, 36))
        palette.setColor(QPalette.ToolTipBase, QColor(30, 32, 36))
        palette.setColor(QPalette.ToolTipText, QColor(245, 245, 245))
        palette.setColor(QPalette.Text, QColor(245, 245, 245))
        palette.setColor(QPalette.Button, QColor(24, 26, 30))
        palette.setColor(QPalette.ButtonText, QColor(245, 245, 245))
        palette.setColor(QPalette.BrightText, QColor(255, 60, 60))  # Яскравий червоний для помилок
        palette.setColor(QPalette.Link, QColor(70, 160, 255))  # Синій акцент
        palette.setColor(QPalette.Highlight, QColor(70, 160, 255))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        app.setPalette(palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
                background-color: #18181c;
                color: #f5f5f5;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #18181c;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #23232a;
                color: #f5f5f5;
                border-radius: 7px;
                border: 1.5px solid #23232a;
                padding: 5px 10px;
                transition: border 0.2s;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #232a36;
                border: 1.5px solid #46a0ff;
            }
            QPushButton:pressed {
                background-color: #18181c;
            }
            QPushButton:focus {
                border: 1.5px solid #23232a;
            }
            QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
                border: 1.5px solid #ff3c3c;
            }
            QTabBar::tab {
                background: #23232a;
                color: #f5f5f5;
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
                background: #232a36;
                color: #46a0ff;
                border: 2px solid #46a0ff;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabBar::tab:!selected {
                border: 1.5px solid #23232a;
                border-bottom: none;
                border-radius: 10px 10px 0 0;
            }
            QTabWidget::pane {
                border: 1.5px solid #23232a;
                border-radius: 0 0 8px 8px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #18181c;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #46a0ff;
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
                background: #46a0ff;
                border: 1.5px solid #46a0ff;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #23232a;
                border: 1.5px solid #393b40;
            }
            QGroupBox {
                border: 1.5px solid #23232a;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #23232a;
                color: #f5f5f5;
                border: 1.5px solid #46a0ff;
                border-radius: 7px;
            }
            QProgressBar {
                background-color: #23232a;
                color: #f5f5f5;
                border: 1.5px solid #23232a;
                border-radius: 7px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #46a0ff;
                border-radius: 7px;
            }
            QSlider::groove:horizontal, QSlider::groove:vertical {
                background: #23232a;
                border: 1.5px solid #23232a;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal, QSlider::handle:vertical {
                background: #46a0ff;
                border: 1.5px solid #46a0ff;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
                background: #46a0ff;
                color: #fff;
            }
            QListWidget::item:hover, QTreeWidget::item:hover, QTableWidget::item:hover {
                background: #ff3c3c;
                color: #fff;
            }
        ''')
