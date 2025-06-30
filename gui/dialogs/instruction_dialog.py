from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from locales.locale_manager import LocaleManager

class InstructionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(LocaleManager.get_locale("instruction_dialog", "window_title"))
        layout = QVBoxLayout()
        text = LocaleManager.get_locale("instruction_dialog", "instruction_text")
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        ok_btn = QPushButton(LocaleManager.get_locale("instruction_dialog", "ok_button"))
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            for btn in self.findChildren(QPushButton):
                if btn.text().lower() in [LocaleManager.get_locale("common_dialogs", "ok_text"), LocaleManager.get_locale("common_dialogs", "select_text")]:
                    btn.click()
                    return
        super().keyPressEvent(event)
