from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from data_utils.graph_saver import GraphSaver
from data_utils.graph_loader import GraphLoader

class GraphImportExportWidget(QWidget):
    """
    Віджет з двома кнопками для експорту та імпорту графа у .json
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.export_btn = QPushButton("Експортувати у .json")
        self.export_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.export_btn.clicked.connect(self.export_graph)

        self.import_btn = QPushButton("Імпортувати з .json")
        self.import_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.import_btn.clicked.connect(self.import_graph)

        layout = QVBoxLayout()
        layout.addWidget(self.export_btn)
        layout.addWidget(self.import_btn)
        self.setLayout(layout)

    def export_graph(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Зберегти граф як .json", "", "JSON Files (*.json)")
        if filepath:
            GraphSaver.save(self.graph, filepath)

    def import_graph(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Відкрити граф з .json", "", "JSON Files (*.json)")
        if filepath:
            new_graph = GraphLoader.load(filepath)
            if new_graph:
                self.graph.__dict__.update(new_graph.__dict__)
