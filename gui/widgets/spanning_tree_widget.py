from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.spanning_trees.prim import Prim
from core.algorithms.spanning_trees.kruskal import Kruskal

class SpanningTreeWidget(QWidget):
    """
    Віджет для запуску алгоритмів остовних дерев (Прима, Краскала) на графі.
    """
    def __init__(self, graph, output_textedit, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.output_textedit = output_textedit
        layout = QVBoxLayout()
        # Кнопки для запуску алгоритмів
        self.prim_btn = QPushButton("Остовне дерево (Прим)")
        self.prim_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.prim_btn.setCursor(Qt.PointingHandCursor)
        self.prim_btn.clicked.connect(self.run_prim)
        self.kruskal_btn = QPushButton("Остовне дерево (Краскал)")
        self.kruskal_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.kruskal_btn.setCursor(Qt.PointingHandCursor)
        self.kruskal_btn.clicked.connect(self.run_kruskal)
        layout.addWidget(self.prim_btn)
        layout.addWidget(self.kruskal_btn)
        self.setLayout(layout)

    def run_prim(self):
        try:
            algo = Prim(self.graph)
            mst_edges, total_weight = algo.minimum_spanning_tree()
            if not mst_edges:
                self.output_textedit.setPlainText("Остовне дерево не знайдено (граф не зв'язний або некоректний).")
                return
            edges_str = "\n".join([f"{e.source.id} -- {e.target.id} (w={e.weight()})" for e in mst_edges])
            self.output_textedit.setPlainText(f"Остовне дерево (Прим):\n{edges_str}\nЗагальна вага: {total_weight}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_kruskal(self):
        try:
            algo = Kruskal(self.graph)
            mst_edges, total_weight = algo.minimum_spanning_tree()
            if not mst_edges:
                self.output_textedit.setPlainText("Остовне дерево не знайдено (граф не зв'язний або некоректний).")
                return
            edges_str = "\n".join([f"{e.source.id} -- {e.target.id} (w={e.weight()})" for e in mst_edges])
            self.output_textedit.setPlainText(f"Остовне дерево (Краскал):\n{edges_str}\nЗагальна вага: {total_weight}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def set_graph(self, graph):
        self.graph = graph
