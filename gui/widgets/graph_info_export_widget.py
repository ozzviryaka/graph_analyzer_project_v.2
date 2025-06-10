from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog
from utils.txt_exporter import TxtExporter
from core.algorithms.graph_info import GraphInfo

class GraphInfoExportWidget(QWidget):
    """
    Віджет для відображення інформації про граф та експорту у .txt
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("background-color: #23272e; color: #e0e0e0; font-size: 14px;")
        self.export_btn = QPushButton("Експортувати у .txt")
        self.export_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
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
        filepath, _ = QFileDialog.getSaveFileName(self, "Зберегти як .txt", "", "Text Files (*.txt)")
        if filepath:
            TxtExporter.export(self.text_edit, filepath)
