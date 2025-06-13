from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.special_paths.simple_path_finder import SimplePathFinder
from core.algorithms.special_paths.longest_path_finder import LongestPathFinder
from core.algorithms.special_paths.hamiltonian_path_finder import HamiltonianPathFinder
from core.algorithms.special_paths.eulerian_path_finder import EulerianPathFinder

class SpecialPathsWidget(QWidget):
    """
    Віджет для запуску спеціальних шляхів (простий, найдовший, гамільтонів, ейлерів).
    """
    def __init__(self, graph, output_textedit, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.output_textedit = output_textedit
        layout = QVBoxLayout()
        # Вибір вершин
        layout.addWidget(QLabel("ID початкової вершини:"))
        self.start_combo = QComboBox()
        self.start_combo.setCursor(Qt.PointingHandCursor)
        self.start_combo.setEditable(False)
        layout.addWidget(self.start_combo)
        layout.addWidget(QLabel("ID кінцевої вершини:"))
        self.end_combo = QComboBox()
        self.end_combo.setCursor(Qt.PointingHandCursor)
        self.end_combo.setEditable(False)
        layout.addWidget(self.end_combo)
        # Кнопки для запуску алгоритмів
        self.simple_btn = QPushButton("Простий шлях (DFS)")
        self.simple_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.simple_btn.setCursor(Qt.PointingHandCursor)
        self.simple_btn.clicked.connect(self.run_simple)
        self.longest_btn = QPushButton("Найдовший простий шлях")
        self.longest_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.longest_btn.setCursor(Qt.PointingHandCursor)
        self.longest_btn.clicked.connect(self.run_longest)
        self.hamiltonian_btn = QPushButton("Гамільтонів шлях")
        self.hamiltonian_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.hamiltonian_btn.setCursor(Qt.PointingHandCursor)
        self.hamiltonian_btn.clicked.connect(self.run_hamiltonian)
        self.eulerian_btn = QPushButton("Ейлерів шлях")
        self.eulerian_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.eulerian_btn.setCursor(Qt.PointingHandCursor)
        self.eulerian_btn.clicked.connect(self.run_eulerian)
        layout.addWidget(self.simple_btn)
        layout.addWidget(self.longest_btn)
        layout.addWidget(self.hamiltonian_btn)
        layout.addWidget(self.eulerian_btn)
        self.setLayout(layout)
        self.update_nodes()

    def update_nodes(self):
        self.start_combo.clear()
        self.end_combo.clear()
        node_ids = [str(node.id) for node in self.graph.nodes()]
        self.start_combo.addItems(node_ids)
        self.end_combo.addItems(node_ids)

    def set_graph(self, graph):
        self.graph = graph
        self.update_nodes()

    def run_simple(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову та кінцеву вершини.")
            return
        try:
            algo = SimplePathFinder(self.graph)
            path = algo.find_simple_path(start, end)
            if path:
                self.output_textedit.setPlainText(f"Простий шлях: {' -> '.join(path)}")
            else:
                self.output_textedit.setPlainText("Шлях не знайдено.")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_longest(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову та кінцеву вершини.")
            return
        try:
            algo = LongestPathFinder(self.graph)
            path = algo.find_longest_path(start, end)
            if path:
                self.output_textedit.setPlainText(f"Найдовший простий шлях: {' -> '.join(path)} (довжина {len(path)})")
            else:
                self.output_textedit.setPlainText("Шлях не знайдено.")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_hamiltonian(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, "Помилка", "Оберіть початкову та кінцеву вершини.")
            return
        try:
            algo = HamiltonianPathFinder(self.graph)
            path = algo.find_hamiltonian_path(start, end)
            if path:
                self.output_textedit.setPlainText(f"Гамільтонів шлях: {' -> '.join(path)}")
            else:
                self.output_textedit.setPlainText("Шлях не знайдено.")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")

    def run_eulerian(self):
        try:
            algo = EulerianPathFinder(self.graph)
            path = algo.find_eulerian_path()
            if path:
                self.output_textedit.setPlainText(f"Ейлерів шлях: {' -> '.join(path)}")
            else:
                self.output_textedit.setPlainText("Ейлерів шлях не знайдено.")
        except Exception as e:
            self.output_textedit.setPlainText(f"Помилка: {e}")
