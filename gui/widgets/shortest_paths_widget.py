from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from core.algorithms.shortest_paths.dijkstra import Dijkstra
from core.algorithms.shortest_paths.bellman_ford import BellmanFord
from core.algorithms.shortest_paths.floyd_warshall import FloydWarshall

class ShortestPathsWidget(QWidget):
    """
    Віджет для запуску алгоритмів пошуку найкоротших шляхів (Дейкстра, Беллман-Форд, Флойд-Уоршелл).
    """
    def __init__(self, graph, output_textedit, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.output_textedit = output_textedit
        layout = QVBoxLayout()
        # Вибір вершин
        layout.addWidget(QLabel("ID початкової вершини:"))
        self.start_combo = QComboBox()
        self.start_combo.setEditable(False)
        layout.addWidget(self.start_combo)
        layout.addWidget(QLabel("ID кінцевої вершини:"))
        self.end_combo = QComboBox()
        self.end_combo.setEditable(False)
        layout.addWidget(self.end_combo)
        # Кнопки для запуску алгоритмів
        self.dijkstra_btn = QPushButton("Дейкстра (від однієї до всіх)")
        self.dijkstra_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.dijkstra_btn.clicked.connect(self.run_dijkstra)
        self.bellman_btn = QPushButton("Беллман-Форд (від однієї до всіх)")
        self.bellman_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.bellman_btn.clicked.connect(self.run_bellman)
        self.floyd_btn = QPushButton("Флойд-Уоршелл (всі до всіх)")
        self.floyd_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.floyd_btn.clicked.connect(self.run_floyd)
        self.dijkstra_path_btn = QPushButton("Дейкстра (шлях між двома)")
        self.dijkstra_path_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.dijkstra_path_btn.clicked.connect(self.run_dijkstra_path)
        self.bellman_path_btn = QPushButton("Беллман-Форд (шлях між двома)")
        self.bellman_path_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.bellman_path_btn.clicked.connect(self.run_bellman_path)
        self.floyd_path_btn = QPushButton("Флойд-Уоршелл (шлях між двома)")
        self.floyd_path_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.floyd_path_btn.clicked.connect(self.run_floyd_path)
        self.floyd_all_btn = QPushButton("Флойд-Уоршелл (всі найкоротші шляхи)")
        self.floyd_all_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.floyd_all_btn.clicked.connect(self.run_floyd_all)
        layout.addWidget(self.dijkstra_btn)
        layout.addWidget(self.bellman_btn)
        layout.addWidget(self.floyd_btn)
        layout.addWidget(self.dijkstra_path_btn)
        layout.addWidget(self.bellman_path_btn)
        layout.addWidget(self.floyd_path_btn)
        layout.addWidget(self.floyd_all_btn)
        self.setLayout(layout)
        self.update_nodes()

    def update_nodes(self):
        self.start_combo.clear()
        self.end_combo.clear()
        node_ids = [str(node.id) for node in self.graph.nodes()]
        self.start_combo.addItems(node_ids)
        self.end_combo.addItems(node_ids)

    def run_dijkstra(self):
        start = self.start_combo.currentText().strip()
        if not start:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову вершину.")
            return
        try:
            algo = Dijkstra(self.graph)
            result = algo.shortest_path(start)
            text = "Найкоротші відстані (Дейкстра):\n" + "\n".join([f"{k}: {v[0]}" for k, v in result.items()])
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_bellman(self):
        start = self.start_combo.currentText().strip()
        if not start:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову вершину.")
            return
        try:
            algo = BellmanFord(self.graph)
            distances, previous = algo.shortest_path(start)
            text = "Найкоротші відстані (Беллман-Форд):\n" + "\n".join([f"{k}: {v}" for k, v in distances.items()])
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_floyd(self):
        try:
            algo = FloydWarshall(self.graph)
            dist, _ = algo.shortest_paths()
            text = "Матриця найкоротших відстаней (Флойд-Уоршелл):\n"
            for row in dist:
                text += " ".join([str(x) if x != float('inf') else '∞' for x in row]) + "\n"
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_dijkstra_path(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову та кінцеву вершини.")
            return
        try:
            algo = Dijkstra(self.graph)
            result = algo.shortest_path(start)
            # Відновлення шляху
            path = []
            current = end
            while current and current != start:
                path.append(current)
                current = result[current][1]
            if current == start:
                path.append(start)
                path.reverse()
                self.output_textedit.setPlainText(f"Шлях (Дейкстра): {' -> '.join(path)}\nДовжина: {result[end][0]}")
            else:
                self.output_textedit.setPlainText("Шлях не знайдено.")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_bellman_path(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову та кінцеву вершини.")
            return
        try:
            algo = BellmanFord(self.graph)
            distances, previous = algo.shortest_path(start)
            # Відновлення шляху
            path = []
            current = end
            while current and current != start:
                path.append(current)
                current = previous[current]
            if current == start:
                path.append(start)
                path.reverse()
                self.output_textedit.setPlainText(f"Шлях (Беллман-Форд): {' -> '.join(path)}\nДовжина: {distances[end]}")
            else:
                self.output_textedit.setPlainText("Шлях не знайдено.")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_floyd_path(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову та кінцеву вершини.")
            return
        try:
            algo = FloydWarshall(self.graph)
            dist, next_node = algo.shortest_paths()
            node_ids = [node.id for node in self.graph.nodes()]
            idx_map = {str(node.id): i for i, node in enumerate(self.graph.nodes())}
            i, j = idx_map[start], idx_map[end]
            if dist[i][j] == float('inf'):
                self.output_textedit.setPlainText("Шлях не знайдено.")
                return
            # Відновлення шляху
            path = [start]
            while start != end:
                start = next_node[idx_map[path[-1]]][j]
                if start is None:
                    self.output_textedit.setPlainText("Шлях не знайдено.")
                    return
                path.append(start)
            self.output_textedit.setPlainText(f"Шлях (Флойд-Уоршелл): {' -> '.join(path)}\nДовжина: {dist[i][j]}")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_floyd_all(self):
        try:
            algo = FloydWarshall(self.graph)
            dist, next_node = algo.shortest_paths()
            node_ids = [str(node.id) for node in self.graph.nodes()]
            n = len(node_ids)
            text = "Всі найкоротші шляхи (Флойд-Уоршелл):\n"
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    if dist[i][j] == float('inf'):
                        text += f"{node_ids[i]} -> {node_ids[j]}: шлях не існує\n"
                        continue
                    # Відновлення шляху
                    path = [node_ids[i]]
                    cur = node_ids[i]
                    while cur != node_ids[j]:
                        cur = next_node[i][j]
                        if cur is None:
                            break
                        path.append(cur)
                    text += f"{node_ids[i]} -> {node_ids[j]}: {' -> '.join(path)} (довжина {dist[i][j]})\n"
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")
