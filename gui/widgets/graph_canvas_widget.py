from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from gui.additionals.graph_canvas import GraphCanvas
from data_utils.graph_saver import GraphSaver
from data_utils.graph_loader import GraphLoader
from gui.widgets.graph_import_export_widget import GraphImportExportWidget

class GraphCanvasWidget(QWidget):
    """
    Віджет-обгортка для GraphCanvas з кнопкою очищення графа та віджетом імпорту/експорту.
    """
    def __init__(self, graph, parent=None, on_graph_changed=None):
        super().__init__(parent)
        self.canvas = GraphCanvas(graph, on_graph_changed=on_graph_changed)
        self.clear_btn = QPushButton("Очистити граф")
        self.clear_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.clear_btn.clicked.connect(self.canvas.clear_graph)

        self.import_export_widget = GraphImportExportWidget(self.canvas.graph)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.import_export_widget)
        self.setLayout(layout)

    def set_on_graph_changed(self, callback):
        self.canvas.on_graph_changed = callback
