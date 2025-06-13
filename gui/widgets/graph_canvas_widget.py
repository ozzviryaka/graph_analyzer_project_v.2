from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from gui.additionals.graph_canvas import GraphCanvas
from data_utils.graph_saver import GraphSaver
from data_utils.graph_loader import GraphLoader
from gui.widgets.graph_import_export_widget import GraphImportExportWidget
from gui.dialogs.graph_select_dialog import GraphSelectDialog
from gui.dialogs.instruction_dialog import InstructionDialog

class GraphCanvasWidget(QWidget):
    """
    Віджет-обгортка для GraphCanvas з кнопкою очищення графа та віджетом імпорту/експорту.
    """
    def __init__(self, graph, parent=None, on_graph_changed=None):
        super().__init__(parent)
        self.canvas = GraphCanvas(graph, on_graph_changed=on_graph_changed)
        self.import_export_widget = GraphImportExportWidget(self.canvas.graph)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.import_export_widget)
        self.setLayout(layout)

    def show_instruction_dialog(self):
        dlg = InstructionDialog(self)
        dlg.exec_()

    def set_graphs_list(self, graphs, main_window):
        self.graphs = graphs
        self.main_window = main_window

    def replace_graph(self, old_graph, new_graph):
        # Замінити старий граф у списку на новий
        for i, g in enumerate(self.graphs):
            if g is old_graph:
                self.graphs[i] = new_graph
                break

    def open_graph_select_dialog(self):
        dialog = GraphSelectDialog(self.graphs, self.canvas.graph, self)
        if dialog.exec_() == dialog.Accepted:
            selected = dialog.selected_graph
            if selected is not self.canvas.graph:
                self.canvas.graph = selected
                if hasattr(self, 'main_window'):
                    self.main_window.on_graph_changed(selected)
                if hasattr(self.import_export_widget, 'graph'):
                    self.import_export_widget.graph = selected
                self.canvas._init_node_positions()
                self.canvas.update()

    def set_on_graph_changed(self, callback):
        self.canvas.on_graph_changed = callback

    def set_auto_vertex_name(self, value: bool):
        self.canvas.set_auto_vertex_name(value)
