from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.flow.ford_fulkerson import FordFulkerson
from core.algorithms.flow.min_cut import MinCut

class FlowAlgorithmsWidget(QWidget):
    """
    Віджет для запуску потокових алгоритмів (Ford-Fulkerson, Min-Cut) на графі.
    """
    def __init__(self, graph, output_textedit, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.output_textedit = output_textedit
        layout = QVBoxLayout()
        # Комбобокси для вибору вершин
        self.source_combo = QComboBox()
        self.source_combo.setCursor(Qt.PointingHandCursor)
        self.sink_combo = QComboBox()
        self.sink_combo.setCursor(Qt.PointingHandCursor)
        self.source_combo.setEditable(False)
        self.sink_combo.setEditable(False)
        layout.addWidget(QLabel("ID джерела (source):"))
        layout.addWidget(self.source_combo)
        layout.addWidget(QLabel("ID стоку (sink):"))
        layout.addWidget(self.sink_combo)
        # Дві кнопки для запуску алгоритмів
        self.run_ff_btn = QPushButton("Ford-Fulkerson (max flow)")
        self.run_ff_btn.setCursor(Qt.PointingHandCursor)
        self.run_ff_btn.clicked.connect(self.run_ford_fulkerson)
        self.run_mc_btn = QPushButton("Min-Cut")
        self.run_mc_btn.setCursor(Qt.PointingHandCursor)
        self.run_mc_btn.clicked.connect(self.run_min_cut)
        layout.addWidget(self.run_ff_btn)
        layout.addWidget(self.run_mc_btn)
        self.setLayout(layout)
        self.update_nodes()

    def update_nodes(self):
        self.source_combo.clear()
        self.sink_combo.clear()
        node_ids = [str(node.id) for node in self.graph.nodes()]
        self.source_combo.addItems(node_ids)
        self.sink_combo.addItems(node_ids)

    def run_ford_fulkerson(self):
        source = self.source_combo.currentText().strip()
        sink = self.sink_combo.currentText().strip()
        if not source or not sink:
            QMessageBox.warning(self, "Помилка", "Оберіть ID джерела та стоку.")
            return
        try:
            algo = FordFulkerson(self.graph)
            max_flow = algo.max_flow(source, sink)
            self.output_textedit.setPlainText(f"Максимальний потік: {max_flow}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_min_cut(self):
        source = self.source_combo.currentText().strip()
        sink = self.sink_combo.currentText().strip()
        if not source or not sink:
            QMessageBox.warning(self, "Помилка", "Оберіть ID джерела та стоку.")
            return
        try:
            algo = MinCut(self.graph)
            min_cut, cut_edges = algo.min_cut(source, sink)
            cut_str = "\n".join([f"{u} -> {v} (c={c})" for u, v, c in cut_edges])
            self.output_textedit.setPlainText(f"Мінімальний розріз: {min_cut}\nРебра розрізу:\n{cut_str}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def set_graph(self, graph):
        self.graph = graph
        self.update_nodes()
