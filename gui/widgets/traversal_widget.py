from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from core.algorithms.traversal.bfs import BFS
from core.algorithms.traversal.dfs import DFS

class TraversalWidget(QWidget):
    """
    Віджет для запуску обходу графа (BFS, DFS).
    """
    def __init__(self, graph, output_textedit, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.output_textedit = output_textedit
        layout = QVBoxLayout()
        # Вибір стартової вершини
        layout.addWidget(QLabel("ID стартової вершини:"))
        self.start_combo = QComboBox()
        self.start_combo.setEditable(False)
        layout.addWidget(self.start_combo)
        # Кнопки для запуску обходу
        self.bfs_btn = QPushButton("Обхід у ширину (BFS)")
        self.bfs_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.bfs_btn.clicked.connect(self.run_bfs)
        self.dfs_btn = QPushButton("Обхід у глибину (DFS)")
        self.dfs_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.dfs_btn.clicked.connect(self.run_dfs)
        layout.addWidget(self.bfs_btn)
        layout.addWidget(self.dfs_btn)
        self.setLayout(layout)
        self.update_nodes()

    def update_nodes(self):
        self.start_combo.clear()
        node_ids = [str(node.id) for node in self.graph.nodes()]
        self.start_combo.addItems(node_ids)

    def run_bfs(self):
        start = self.start_combo.currentText().strip()
        if not start:
            QMessageBox.warning(self, "Помилка", "Оберіть стартову вершину.")
            return
        try:
            algo = BFS(self.graph)
            order = algo.traverse(start)
            self.output_textedit.setPlainText(f"BFS порядок обходу: {' -> '.join(map(str, order))}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_dfs(self):
        start = self.start_combo.currentText().strip()
        if not start:
            QMessageBox.warning(self, "Помилка", "Оберіть стартову вершину.")
            return
        try:
            algo = DFS(self.graph)
            order = algo.traverse(start)
            self.output_textedit.setPlainText(f"DFS порядок обходу: {' -> '.join(map(str, order))}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def set_graph(self, graph):
        self.graph = graph
        self.update_nodes()
