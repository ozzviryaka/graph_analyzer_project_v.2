from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from utils.txt_exporter import TxtExporter
from locales.locale_manager import LocaleManager

class AnalysisOutputControls(QWidget):
    """
    Віджет з кнопками для експорту результатів у .txt та очищення поля результатів.
    """
    def __init__(self, output_textedit, parent=None):
        super().__init__(parent)
        self.output_textedit = output_textedit
        layout = QHBoxLayout()
        self.export_btn = QPushButton(LocaleManager.get_locale("analysis_output_controls", "export_txt_button"))
        self.export_btn.setCursor(Qt.PointingHandCursor)
        self.export_btn.clicked.connect(self.export_txt)
        self.clear_btn = QPushButton(LocaleManager.get_locale("analysis_output_controls", "clear_results_button"))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_output)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.clear_btn)
        self.setLayout(layout)

    def export_txt(self):
        from PyQt5.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(self, LocaleManager.get_locale("analysis_output_controls", "save_dialog_title"), "", "Text Files (*.txt)")
        if filepath:
            TxtExporter.export(self.output_textedit, filepath)

    def clear_output(self):
        self.output_textedit.clear()

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        self.export_btn.setText(LocaleManager.get_locale("analysis_output_controls", "export_txt_button"))
        self.clear_btn.setText(LocaleManager.get_locale("analysis_output_controls", "clear_results_button"))
