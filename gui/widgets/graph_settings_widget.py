from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox
from core.convertations.graph_converter import GraphConverter

class GraphSettingsWidget(QWidget):
    """
    Віджет з тумблерами для орієнтованості та ваговості графа.
    """
    def __init__(self, graph, on_graph_changed, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.on_graph_changed = on_graph_changed  # callback для оновлення інтерфейсу
        layout = QHBoxLayout()
        # Тумблер орієнтованості
        self.directed_checkbox = QCheckBox("Орієнтований граф")
        self.directed_checkbox.setChecked(hasattr(graph, 'is_directed') and graph.is_directed())
        self.directed_checkbox.stateChanged.connect(self.toggle_directed)
        layout.addWidget(self.directed_checkbox)
        # Тумблер ваговості
        self.weighted_checkbox = QCheckBox("Ваговий граф")
        self.weighted_checkbox.setChecked(getattr(graph, 'weighted', True))
        self.weighted_checkbox.stateChanged.connect(self.toggle_weighted)
        layout.addWidget(self.weighted_checkbox)
        layout.addStretch()
        self.setLayout(layout)

    def toggle_directed(self, state):
        is_directed = state == 2
        if hasattr(self.graph, 'is_directed') and self.graph.is_directed() == is_directed:
            return
        # Конвертація графа
        if is_directed:
            from core.graph_models.undirected_graph import UndirectedGraph
            if isinstance(self.graph, UndirectedGraph):
                self.graph = GraphConverter.undirected_to_directed(self.graph)
        else:
            from core.graph_models.directed_graph import DirectedGraph
            if isinstance(self.graph, DirectedGraph):
                self.graph = GraphConverter.directed_to_undirected(self.graph)
        self.on_graph_changed(self.graph)

    def toggle_weighted(self, state):
        weighted = state == 2
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
