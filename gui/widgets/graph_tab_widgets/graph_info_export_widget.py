from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt
from utils.txt_exporter import TxtExporter
from core.algorithms.graph_info import GraphInfo
from locales.locale_manager import LocaleManager

class GraphInfoExportWidget(QWidget):
    """
    Віджет для відображення інформації про граф та експорту у .txt
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("")
        self.export_btn = QPushButton(LocaleManager.get_locale("graph_info_export_widget", "export_txt_button"))
        self.export_btn.setCursor(Qt.PointingHandCursor)
        # self.export_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")  # REMOVE custom style
        self.export_btn.clicked.connect(self.export_txt)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.export_btn)
        self.setLayout(layout)

        self.update_info()

    def update_info(self):
        info = GraphInfo(self.graph).get_all_info()
        text = "\n".join(f"{k}: {v}" for k, v in info.items())
        self.text_edit.setPlainText(text)

    def set_graph(self, graph):
        self.graph = graph
        self.update_info()

    def export_txt(self):
        filepath, _ = QFileDialog.getSaveFileName(self, LocaleManager.get_locale("graph_info_export_widget", "save_txt_dialog_title"), "", "Text Files (*.txt)")
        if filepath:
            TxtExporter.export(self.text_edit, filepath)

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        self.export_btn.setText(LocaleManager.get_locale("graph_info_export_widget", "export_txt_button"))
        # Оновлюємо інформацію про граф в текстовому полі
        self.update_info()
