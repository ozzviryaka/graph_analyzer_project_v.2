from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QButtonGroup, QRadioButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from locales.locale_manager import LocaleManager

class LanguageSelectDialog(QDialog):
    """
    Діалог для вибору мови програми
    """
    language_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(LocaleManager.get_locale("language_select_dialog", "title"))
        self.setModal(True)
        self.setFixedSize(300, 200)
        
        # Основний layout
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel(LocaleManager.get_locale("language_select_dialog", "select_language_label"))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Група радіокнопок для вибору мови
        self.language_group = QButtonGroup()
        
        # Українська мова
        self.ukrainian_radio = QRadioButton(LocaleManager.get_locale("language_select_dialog", "ukrainian_language"))
        self.language_group.addButton(self.ukrainian_radio, 0)
        layout.addWidget(self.ukrainian_radio)
        
        # Англійська мова
        self.english_radio = QRadioButton(LocaleManager.get_locale("language_select_dialog", "english_language"))
        self.language_group.addButton(self.english_radio, 1)
        layout.addWidget(self.english_radio)
        
        # Встановлюємо поточну мову
        current_language = LocaleManager.get_current_language()
        if current_language == "uk":
            self.ukrainian_radio.setChecked(True)
        elif current_language == "en":
            self.english_radio.setChecked(True)
        
        # Кнопки OK та Cancel
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton(LocaleManager.get_locale("language_select_dialog", "ok_button"))
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton(LocaleManager.get_locale("language_select_dialog", "cancel_button"))
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def accept(self):
        """Застосовує обрану мову"""
        if self.ukrainian_radio.isChecked():
            new_language = "uk"
        elif self.english_radio.isChecked():
            new_language = "en"
        else:
            new_language = "uk"  # За замовчуванням
        
        # Змінюємо мову
        LocaleManager.set_language(new_language)
        
        # Емітуємо сигнал про зміну мови
        self.language_changed.emit()
        
        super().accept()
    
    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        self.setWindowTitle(LocaleManager.get_locale("language_select_dialog", "title"))
        
        # Оновлюємо заголовок
        layout = self.layout()
        if layout:
            title_label = layout.itemAt(0).widget()
            if hasattr(title_label, 'setText'):
                title_label.setText(LocaleManager.get_locale("language_select_dialog", "select_language_label"))
        
        # Оновлюємо радіокнопки
        self.ukrainian_radio.setText(LocaleManager.get_locale("language_select_dialog", "ukrainian_language"))
        self.english_radio.setText(LocaleManager.get_locale("language_select_dialog", "english_language"))
        
        # Оновлюємо кнопки
        self.ok_button.setText(LocaleManager.get_locale("language_select_dialog", "ok_button"))
        self.cancel_button.setText(LocaleManager.get_locale("language_select_dialog", "cancel_button"))
