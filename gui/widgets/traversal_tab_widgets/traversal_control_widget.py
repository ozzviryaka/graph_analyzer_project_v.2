from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel
from gui.additionals.readonly_graph_canvas import ReadOnlyGraphCanvas
from locales.locale_manager import LocaleManager

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
            LocaleManager.get_locale("traversal_control_widget", "bfs_method"),
            LocaleManager.get_locale("traversal_control_widget", "dfs_method"),
            LocaleManager.get_locale("traversal_control_widget", "dijkstra_method"),
            LocaleManager.get_locale("traversal_control_widget", "connected_components_method"),
            LocaleManager.get_locale("traversal_control_widget", "cycle_detection_method")
        ])
        self.start_vertex_combo = QComboBox(self)
        self.update_vertex_list()
        self.start_btn = QPushButton(LocaleManager.get_locale("traversal_control_widget", "start_button"), self)
        self.stop_btn = QPushButton(LocaleManager.get_locale("traversal_control_widget", "stop_button"), self)
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
        hbox.addWidget(QLabel(LocaleManager.get_locale("traversal_control_widget", "method_label"), self))
        hbox.addWidget(self.method_combo)
        hbox.addWidget(QLabel(LocaleManager.get_locale("traversal_control_widget", "start_vertex_label"), self))
        hbox.addWidget(self.start_vertex_combo)
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.stop_btn)
        vbox.addLayout(hbox)
        vbox.addWidget(self.canvas)
        # vbox.addWidget(self.status_label)  # Видалено статус-лейбл
        self.setLayout(vbox)
