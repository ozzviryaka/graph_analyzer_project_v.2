from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from gui.additionals.graph_canvas import GraphCanvas
from data_utils.graph_saver import GraphSaver
from data_utils.graph_loader import GraphLoader
from gui.widgets.graph_tab_widgets.graph_import_export_widget import GraphImportExportWidget
from gui.dialogs.graph_select_dialog import GraphSelectDialog
from gui.dialogs.instruction_dialog import InstructionDialog
from utils.undo_redo_event_filter import UndoRedoEventFilter
from locales.locale_manager import LocaleManager

class GraphCanvasWidget(QWidget):
    """
    Віджет-обгортка для GraphCanvas з кнопкою очищення графа та віджетом імпорту/експорту.
    """
    def __init__(self, graph, parent=None, on_graph_changed=None):
        super().__init__(parent)
        self.canvas = GraphCanvas(graph, on_graph_changed=on_graph_changed)
        self.import_export_widget = GraphImportExportWidget(self.canvas.graph)
        self.import_export_widget.import_graph_with_undo = self.import_graph_with_undo.__get__(self.import_export_widget)
        self.import_export_widget.import_btn.clicked.disconnect()
        self.import_export_widget.import_btn.clicked.connect(self.import_export_widget.import_graph_with_undo)
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.canvas.setFocus()
        # Передаємо менеджер з canvas
        self.undo_redo = UndoRedoEventFilter(self.canvas, manager=self.canvas.undo_redo_manager)
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

    def import_graph_with_undo(self):
        # Додаємо undo для імпорту графа
        from utils.undo_redo_manager import UndoRedoManager
        from copy import deepcopy
        filepath, _ = QFileDialog.getOpenFileName(self, LocaleManager.get_locale("graph_canvas_widget", "open_graph_dialog_title"), "", "JSON Files (*.json)")
        if filepath:
            old_graph_state = deepcopy(self.canvas.graph)
            new_graph = GraphLoader.load(filepath)
            if new_graph:
                self.canvas.graph.__dict__.update(new_graph.__dict__)
                self.canvas._init_node_positions()
                self.canvas.update()
                if hasattr(self.canvas, 'on_graph_changed') and self.canvas.on_graph_changed:
                    self.canvas.on_graph_changed(self.canvas.graph)
                def undo():
                    self.canvas.graph.__dict__.update(deepcopy(old_graph_state.__dict__))
                    self.canvas._init_node_positions()
                    self.canvas.update()
                    if hasattr(self.canvas, 'on_graph_changed') and self.canvas.on_graph_changed:
                        self.canvas.on_graph_changed(self.canvas.graph)
                def redo():
                    self.canvas.graph.__dict__.update(deepcopy(new_graph.__dict__))
                    self.canvas._init_node_positions()
                    self.canvas.update()
                    if hasattr(self.canvas, 'on_graph_changed') and self.canvas.on_graph_changed:
                        self.canvas.on_graph_changed(self.canvas.graph)
                self.canvas.undo_redo_manager.push(redo, undo)

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        # Оновлюємо текст у дочірніх віджетах
        if hasattr(self.import_export_widget, 'refresh_ui_text'):
            self.import_export_widget.refresh_ui_text()
