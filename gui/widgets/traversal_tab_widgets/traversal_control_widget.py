from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
from gui.additionals.readonly_graph_canvas import ReadOnlyGraphCanvas

class TraversalControlWidget(QWidget):
    """
    Віджет для вибору методу обходу графа, початкової вершини та керування запуском/зупинкою анімації обходу.
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.canvas = ReadOnlyGraphCanvas(graph, self)
        self.method_combo = QComboBox(self)
        self.method_combo.addItems([
            'BFS (у ширину)',
            'DFS (у глибину)',
            'Dijkstra',
            'Компоненти звʼязності',
            'Пошук циклів'
        ])
        self.start_vertex_combo = QComboBox(self)
        self.update_vertex_list()
        self.start_btn = QPushButton('Запустити', self)
        self.stop_btn = QPushButton('Стоп', self)
        self.status_label = None  # Видалено статус-лейбл
        self._setup_layout()
        # Тут можна додати підключення сигналів до методів запуску/зупинки

    def update_vertex_list(self):
        current = self.start_vertex_combo.currentText()
        self.start_vertex_combo.blockSignals(True)
        self.start_vertex_combo.clear()
        for node in self.graph.nodes():
            self.start_vertex_combo.addItem(str(node.id))
        # Відновлюємо попередній вибір, якщо він ще є
        idx = self.start_vertex_combo.findText(current)
        if idx >= 0:
            self.start_vertex_combo.setCurrentIndex(idx)
        self.start_vertex_combo.blockSignals(False)

    def set_graph(self, graph):
        self.graph = graph
        self.canvas.graph = graph
        self.canvas._init_node_positions()
        self.canvas.update()
        self.update_vertex_list()

    def on_graph_changed(self, *args, **kwargs):
        self.update_vertex_list()

    def _setup_layout(self):
        vbox = QVBoxLayout(self)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('Метод:', self))
        hbox.addWidget(self.method_combo)
        hbox.addWidget(QLabel('Початкова вершина:', self))
        hbox.addWidget(self.start_vertex_combo)
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.stop_btn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        # vbox.addWidget(self.status_label)  # Видалено статус-лейбл
        self.setLayout(vbox)
