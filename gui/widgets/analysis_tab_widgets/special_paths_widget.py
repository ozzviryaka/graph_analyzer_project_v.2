from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.special_paths.simple_path_finder import SimplePathFinder
from core.algorithms.special_paths.longest_path_finder import LongestPathFinder
from core.algorithms.special_paths.hamiltonian_path_finder import HamiltonianPathFinder
from core.algorithms.special_paths.eulerian_path_finder import EulerianPathFinder
from locales.locale_manager import LocaleManager

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
        layout.addWidget(QLabel(LocaleManager.get_locale("special_paths_widget", "start_vertex_label")))
        self.start_combo = QComboBox()
        self.start_combo.setCursor(Qt.PointingHandCursor)
        self.start_combo.setEditable(False)
        layout.addWidget(self.start_combo)
        layout.addWidget(QLabel(LocaleManager.get_locale("special_paths_widget", "end_vertex_label")))
        self.end_combo = QComboBox()
        self.end_combo.setCursor(Qt.PointingHandCursor)
        self.end_combo.setEditable(False)
        layout.addWidget(self.end_combo)
        # Кнопки для запуску алгоритмів
        self.simple_btn = QPushButton(LocaleManager.get_locale("special_paths_widget", "simple_path_button"))
        self.simple_btn.setCursor(Qt.PointingHandCursor)
        self.simple_btn.clicked.connect(self.run_simple)
        self.longest_btn = QPushButton(LocaleManager.get_locale("special_paths_widget", "longest_path_button"))
        self.longest_btn.setCursor(Qt.PointingHandCursor)
        self.longest_btn.clicked.connect(self.run_longest)
        self.hamiltonian_btn = QPushButton(LocaleManager.get_locale("special_paths_widget", "hamiltonian_path_button"))
        self.hamiltonian_btn.setCursor(Qt.PointingHandCursor)
        self.hamiltonian_btn.clicked.connect(self.run_hamiltonian)
        self.eulerian_btn = QPushButton(LocaleManager.get_locale("special_paths_widget", "eulerian_path_button"))
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
            QMessageBox.warning(self, LocaleManager.get_locale("special_paths_widget", "error_title"), LocaleManager.get_locale("special_paths_widget", "select_start_end_vertices"))
            return
        try:
            algo = SimplePathFinder(self.graph)
            path = algo.find_simple_path(start, end)
            if path:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "simple_path_result").format(path=' -> '.join(path)))
            else:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "path_not_found"))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "error_result").format(error=str(e)))

    def run_longest(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, LocaleManager.get_locale("special_paths_widget", "error_title"), LocaleManager.get_locale("special_paths_widget", "select_start_end_vertices"))
            return
        try:
            algo = LongestPathFinder(self.graph)
            path = algo.find_longest_path(start, end)
            if path:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "longest_path_result").format(path=' -> '.join(path), length=len(path)))
            else:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "path_not_found"))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "error_result").format(error=str(e)))

    def run_hamiltonian(self):
        start = self.start_combo.currentText().strip()
        end = self.end_combo.currentText().strip()
        if not start or not end:
            QMessageBox.warning(self, LocaleManager.get_locale("special_paths_widget", "error_title"), LocaleManager.get_locale("special_paths_widget", "select_start_end_vertices"))
            return
        try:
            algo = HamiltonianPathFinder(self.graph)
            path = algo.find_hamiltonian_path(start, end)
            if path:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "hamiltonian_path_result").format(path=' -> '.join(path)))
            else:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "path_not_found"))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "error_result").format(error=str(e)))

    def run_eulerian(self):
        try:
            algo = EulerianPathFinder(self.graph)
            path = algo.find_eulerian_path()
            if path:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "eulerian_path_result").format(path=' -> '.join(path)))
            else:
                self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "eulerian_path_not_found"))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("special_paths_widget", "error_result").format(error=str(e)))
