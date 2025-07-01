from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.shortest_paths.dijkstra import Dijkstra
from core.algorithms.shortest_paths.bellman_ford import BellmanFord
from core.algorithms.shortest_paths.floyd_warshall import FloydWarshall
from locales.locale_manager import LocaleManager

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
        layout.addWidget(QLabel(LocaleManager.get_locale("shortest_paths_widget", "start_vertex_label")))
        self.start_combo = QComboBox()
        self.start_combo.setCursor(Qt.PointingHandCursor)
        self.start_combo.setEditable(False)
        layout.addWidget(self.start_combo)
        layout.addWidget(QLabel(LocaleManager.get_locale("shortest_paths_widget", "end_vertex_label")))
        self.end_combo = QComboBox()
        self.end_combo.setCursor(Qt.PointingHandCursor)
        self.end_combo.setEditable(False)
        layout.addWidget(self.end_combo)
        # Кнопки для запуску алгоритмів
        self.dijkstra_btn = QPushButton(LocaleManager.get_locale("shortest_paths_widget", "dijkstra_all_button"))
        self.dijkstra_btn.setCursor(Qt.PointingHandCursor)
        self.dijkstra_btn.clicked.connect(self.run_dijkstra)
        self.bellman_btn = QPushButton(LocaleManager.get_locale("shortest_paths_widget", "bellman_all_button"))
        self.bellman_btn.setCursor(Qt.PointingHandCursor)
        self.bellman_btn.clicked.connect(self.run_bellman)
        self.floyd_btn = QPushButton(LocaleManager.get_locale("shortest_paths_widget", "floyd_all_button"))
        self.floyd_btn.setCursor(Qt.PointingHandCursor)
        self.floyd_btn.clicked.connect(self.run_floyd)
        self.dijkstra_path_btn = QPushButton(LocaleManager.get_locale("shortest_paths_widget", "dijkstra_path_button"))
        self.dijkstra_path_btn.setCursor(Qt.PointingHandCursor)
        self.dijkstra_path_btn.clicked.connect(self.run_dijkstra_path)
        self.bellman_path_btn = QPushButton(LocaleManager.get_locale("shortest_paths_widget", "bellman_path_button"))
        self.bellman_path_btn.setCursor(Qt.PointingHandCursor)
        self.bellman_path_btn.clicked.connect(self.run_bellman_path)
        self.floyd_path_btn = QPushButton(LocaleManager.get_locale("shortest_paths_widget", "floyd_path_button"))
        self.floyd_path_btn.setCursor(Qt.PointingHandCursor)
        self.floyd_path_btn.clicked.connect(self.run_floyd_path)
        # self.floyd_all_btn = QPushButton("Флойд-Уоршелл (всі найкоротші шляхи)")
        # self.floyd_all_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        # self.floyd_all_btn.setCursor(Qt.PointingHandCursor)
        # self.floyd_all_btn.clicked.connect(self.run_floyd_all)
        # layout.addWidget(self.dijkstra_btn)  # Від однієї до всіх - видалено
        # layout.addWidget(self.bellman_btn)   # Від однієї до всіх - видалено
        layout.addWidget(self.floyd_btn)     # Всі до всіх - повернуто
        layout.addWidget(self.dijkstra_path_btn)
        layout.addWidget(self.bellman_path_btn)
        layout.addWidget(self.floyd_path_btn)
        # layout.addWidget(self.floyd_all_btn) # Всі найкоротші шляхи - видалено
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
            QMessageBox.warning(self, LocaleManager.get_locale("shortest_paths_widget", "error_title"), LocaleManager.get_locale("shortest_paths_widget", "select_start_vertex"))
            return
        try:
            algo = Dijkstra(self.graph)
            result = algo.shortest_path(start)
            text = LocaleManager.get_locale("shortest_paths_widget", "dijkstra_distances") + "\n" + "\n".join([f"{k}: {v[0]}" for k, v in result.items()])
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def run_bellman(self):
        start = self.start_combo.currentText().strip()
        if not start:
            QMessageBox.warning(self, LocaleManager.get_locale("shortest_paths_widget", "error_title"), LocaleManager.get_locale("shortest_paths_widget", "select_start_vertex"))
            return
        try:
            algo = BellmanFord(self.graph)
            distances, previous = algo.shortest_path(start)
            text = LocaleManager.get_locale("shortest_paths_widget", "bellman_distances") + "\n" + "\n".join([f"{k}: {v}" for k, v in distances.items()])
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def run_floyd(self):
        try:
            algo = FloydWarshall(self.graph)
            dist, _ = algo.shortest_paths()
            text = LocaleManager.get_locale("shortest_paths_widget", "floyd_matrix") + "\n"
            for row in dist:
                text += " ".join([str(x) if x != float('inf') else '∞' for x in row]) + "\n"
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def run_dijkstra_path(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, LocaleManager.get_locale("shortest_paths_widget", "error_title"), LocaleManager.get_locale("shortest_paths_widget", "select_start_end_vertices"))
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
                self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "dijkstra_path").format(path=' -> '.join(path), length=result[end][0]))
            else:
                self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "path_not_found"))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def run_bellman_path(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, LocaleManager.get_locale("shortest_paths_widget", "error_title"), LocaleManager.get_locale("shortest_paths_widget", "select_start_end_vertices"))
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
                self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "bellman_path").format(path=' -> '.join(path), length=distances[end]))
            else:
                self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "path_not_found"))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def run_floyd_path(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, LocaleManager.get_locale("shortest_paths_widget", "error_title"), LocaleManager.get_locale("shortest_paths_widget", "select_start_end_vertices"))
            return
        try:
            algo = FloydWarshall(self.graph)
            dist, next_node = algo.shortest_paths()
            node_ids = [str(node.id) for node in self.graph.nodes()]
            idx_map = {str(node.id): i for i, node in enumerate(self.graph.nodes())}
            if start not in idx_map or end not in idx_map:
                self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "vertex_not_found"))
                return
            i, j = idx_map[start], idx_map[end]
            if dist[i][j] == float('inf'):
                self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "path_not_found"))
                return
            # Відновлення шляху
            path = [start]
            current = start
            while current != end:
                next_step = next_node[idx_map[current]][j]
                if next_step is None or next_step == current:
                    self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "path_not_found"))
                    return
                path.append(next_step)
                current = next_step
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "floyd_path").format(path=' -> '.join(path), length=dist[i][j]))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def run_floyd_all(self):
        try:
            algo = FloydWarshall(self.graph)
            dist, next_node = algo.shortest_paths()
            node_ids = [str(node.id) for node in self.graph.nodes()]
            n = len(node_ids)
            text = LocaleManager.get_locale("shortest_paths_widget", "floyd_all_paths") + "\n"
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    if dist[i][j] == float('inf'):
                        text += LocaleManager.get_locale("shortest_paths_widget", "path_not_exists").format(from_node=node_ids[i], to_node=node_ids[j]) + "\n"
                        continue
                    # Відновлення шляху
                    path = [node_ids[i]]
                    cur = node_ids[i]
                    while cur != node_ids[j]:
                        cur = next_node[i][j]
                        if cur is None:
                            break
                        path.append(cur)
                    text += LocaleManager.get_locale("shortest_paths_widget", "path_result").format(
                        from_node=node_ids[i], 
                        to_node=node_ids[j], 
                        path=' -> '.join(path), 
                        length=dist[i][j]
                    ) + "\n"
            self.output_textedit.setPlainText(text)
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("shortest_paths_widget", "error_result").format(error=str(e)))

    def set_graph(self, graph):
        self.graph = graph
        self.update_nodes()
