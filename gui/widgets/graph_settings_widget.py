from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
from gui.additionals.toggle_switch import ToggleSwitch
from core.convertations.graph_converter import GraphConverter
from gui.dialogs.graph_select_dialog import GraphSelectDialog
from gui.dialogs.instruction_dialog import InstructionDialog
from gui.dialogs.theme_select_dialog import ThemeSelectDialog

class GraphSettingsWidget(QWidget):
    """
    Віджет з тумблерами для орієнтованості та ваговості графа.
    """
    def __init__(self, graph, on_graph_changed, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.on_graph_changed = on_graph_changed
        self.graphs = None  # буде встановлено з MainWindow
        layout = QHBoxLayout()
        # Кнопка вибору графа
        self.select_graph_btn = QPushButton("Вибрати граф")
        self.select_graph_btn.setCursor(Qt.PointingHandCursor)
        # self.select_graph_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")  # REMOVE custom style
        self.select_graph_btn.clicked.connect(self.open_graph_select_dialog)
        layout.addWidget(self.select_graph_btn)
        # Тумблер орієнтованості
        self.directed_switch = ToggleSwitch(checked=hasattr(graph, 'is_directed') and graph.is_directed())
        self.directed_label = QLabel("Орієнтований граф")
        self.directed_label.setCursor(Qt.PointingHandCursor)
        self.directed_switch.toggled.connect(self.toggle_directed)
        self.directed_label.mousePressEvent = lambda event: self.directed_switch.setChecked(not self.directed_switch.isChecked())
        layout.addWidget(self.directed_label)
        layout.addWidget(self.directed_switch)
        # Тумблер ваговості
        self.weighted_switch = ToggleSwitch(checked=getattr(graph, 'weighted', True))
        self.weighted_label = QLabel("Ваговий граф")
        self.weighted_label.setCursor(Qt.PointingHandCursor)
        self.weighted_switch.toggled.connect(self.toggle_weighted)
        self.weighted_label.mousePressEvent = lambda event: self.weighted_switch.setChecked(not self.weighted_switch.isChecked())
        layout.addWidget(self.weighted_label)
        layout.addWidget(self.weighted_switch)
        # Тумблер автоматичної назви вершини
        self.auto_vertex_name_switch = ToggleSwitch(checked=True)
        self.auto_vertex_name_label = QLabel("Автоматична назва вершини")
        self.auto_vertex_name_label.setCursor(Qt.PointingHandCursor)
        self.auto_vertex_name_switch.toggled.connect(self.on_auto_vertex_name_toggled)
        self.auto_vertex_name_label.mousePressEvent = lambda event: self.auto_vertex_name_switch.setChecked(not self.auto_vertex_name_switch.isChecked())
        layout.addWidget(self.auto_vertex_name_label)
        layout.addWidget(self.auto_vertex_name_switch)
        # Кнопка вибору теми
        self.theme_btn = QPushButton("Вибрати тему")
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.show_theme_dialog)
        layout.addWidget(self.theme_btn)
        layout.addStretch()
        self.setLayout(layout)
        # Кнопка інструкції
        self.instruction_btn = QPushButton("Інструкція")
        self.instruction_btn.setCursor(Qt.PointingHandCursor)
        self.instruction_btn.clicked.connect(self.show_instruction_dialog)
        layout.addWidget(self.instruction_btn)

    def set_graphs_list(self, graphs):
        self.graphs = graphs

    def set_graph(self, graph):
        self.graph = graph
        self.directed_switch.blockSignals(True)
        self.weighted_switch.blockSignals(True)
        self.directed_switch.setChecked(hasattr(graph, 'is_directed') and graph.is_directed())
        self.weighted_switch.setChecked(getattr(graph, 'weighted', True))
        self.directed_switch.blockSignals(False)
        self.weighted_switch.blockSignals(False)

    def is_auto_vertex_name(self):
        return self.auto_vertex_name_switch.isChecked()

    def on_auto_vertex_name_toggled(self, checked):
        if hasattr(self.parent(), 'on_auto_vertex_name_changed'):
            self.parent().on_auto_vertex_name_changed(checked)

    def toggle_directed(self, checked):
        is_directed = checked
        if hasattr(self.graph, 'is_directed') and self.graph.is_directed() == is_directed:
            return
        # Конвертація графа
        if is_directed:
            from core.graph_models.undirected_graph import UndirectedGraph
            if isinstance(self.graph, UndirectedGraph):
                from core.convertations.graph_converter import GraphConverter
                new_graph = GraphConverter.undirected_to_directed(self.graph)
                if self.graphs is not None:
                    for i, g in enumerate(self.graphs):
                        if g is self.graph:
                            self.graphs[i] = new_graph
                            break
                self.graph = new_graph
        else:
            from core.graph_models.directed_graph import DirectedGraph
            if isinstance(self.graph, DirectedGraph):
                from core.convertations.graph_converter import GraphConverter
                new_graph = GraphConverter.directed_to_undirected(self.graph)
                if self.graphs is not None:
                    for i, g in enumerate(self.graphs):
                        if g is self.graph:
                            self.graphs[i] = new_graph
                            break
                self.graph = new_graph
        self.on_graph_changed(self.graph)

    def toggle_weighted(self, checked):
        weighted = checked
        if getattr(self.graph, 'weighted', True) == weighted:
            return
        # Міняємо ваговість у графа
        self.graph.weighted = weighted
        # Міняємо ваговість у всіх ребер
        if hasattr(self.graph, '_edges'):
            for edge in self.graph._edges:
                if hasattr(edge, '_weight'):
                    if weighted:
                        if getattr(edge, '_original_weight', None) is not None:
                            edge._weight = edge._original_weight
                    else:
                        # Зберігаємо оригінальну вагу, якщо ще не збережено
                        if not hasattr(edge, '_original_weight'):
                            edge._original_weight = edge._weight
                        edge._weight = 1
        self.on_graph_changed(self.graph)

    def open_graph_select_dialog(self):
        if hasattr(self.parent(), 'graphs'):
            graphs = self.parent().graphs
        else:
            graphs = self.graphs
        dialog = GraphSelectDialog(graphs, self.graph, self)
        if dialog.exec_() == dialog.Accepted:
            selected = dialog.selected_graph
            if selected is not self.graph:
                self.graph = selected
                if hasattr(self.parent(), 'on_graph_changed'):
                    self.parent().on_graph_changed(selected)
                if hasattr(self, 'on_graph_changed'):
                    self.on_graph_changed(selected)

    def show_instruction_dialog(self):
        dlg = InstructionDialog(self)
        dlg.exec_()

    def show_theme_dialog(self):
        dlg = ThemeSelectDialog(self)
        dlg.exec_()

    def set_auto_vertex_name(self, value: bool):
        self.auto_vertex_name_switch.blockSignals(True)
        self.auto_vertex_name_switch.setChecked(value)
        self.auto_vertex_name_switch.blockSignals(False)
