from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui.widgets.graph_tab_widgets.graph_canvas_widget import GraphCanvasWidget
from gui.widgets.graph_tab_widgets.graph_info_export_widget import GraphInfoExportWidget

class GraphCombinedTab(QWidget):
    """
    Віджет-комбінована вкладка з GraphCanvasWidget та GraphInfoExportWidget
    """
    def __init__(self, graph, parent=None, on_graph_changed=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.canvas_widget = GraphCanvasWidget(graph, on_graph_changed=on_graph_changed)
        self.info_widget = GraphInfoExportWidget(graph)
        layout.addWidget(self.canvas_widget)
        layout.addWidget(self.info_widget)
        self.setLayout(layout)

    def update_info(self, graph):
        self.info_widget.set_graph(graph)

    def set_on_graph_changed(self, callback):
        self.canvas_widget.set_on_graph_changed(callback)

    def set_graph(self, graph):
        self.canvas_widget.import_export_widget.set_graph(graph)
        self.info_widget.set_graph(graph)
