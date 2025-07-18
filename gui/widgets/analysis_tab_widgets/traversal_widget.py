from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.traversal.bfs import BFS
from core.algorithms.traversal.dfs import DFS
from locales.locale_manager import LocaleManager

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
        layout.addWidget(QLabel(LocaleManager.get_locale("traversal_widget", "start_vertex_label")))
        self.start_combo = QComboBox()
        self.start_combo.setCursor(Qt.PointingHandCursor)
        self.start_combo.setEditable(False)
        layout.addWidget(self.start_combo)
        # Кнопки для запуску обходу
        self.bfs_btn = QPushButton(LocaleManager.get_locale("traversal_widget", "bfs_button"))
        self.bfs_btn.setCursor(Qt.PointingHandCursor)
        self.bfs_btn.clicked.connect(self.run_bfs)
        self.dfs_btn = QPushButton(LocaleManager.get_locale("traversal_widget", "dfs_button"))
        self.dfs_btn.setCursor(Qt.PointingHandCursor)
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
            QMessageBox.warning(self, LocaleManager.get_locale("traversal_widget", "error_title"), LocaleManager.get_locale("traversal_widget", "select_start_vertex"))
            return
        try:
            algo = BFS(self.graph)
            order = algo.traverse(start)
            self.output_textedit.setPlainText(LocaleManager.get_locale("traversal_widget", "bfs_result").format(order=' -> '.join(map(str, order))))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("traversal_widget", "error_result").format(error=str(e)))

    def run_dfs(self):
        start = self.start_combo.currentText().strip()
        if not start:
            QMessageBox.warning(self, LocaleManager.get_locale("traversal_widget", "error_title"), LocaleManager.get_locale("traversal_widget", "select_start_vertex"))
            return
        try:
            algo = DFS(self.graph)
            order = algo.traverse(start)
            self.output_textedit.setPlainText(LocaleManager.get_locale("traversal_widget", "dfs_result").format(order=' -> '.join(map(str, order))))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("traversal_widget", "error_result").format(error=str(e)))

    def set_graph(self, graph):
        self.graph = graph
        self.update_nodes()

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        self.bfs_btn.setText(LocaleManager.get_locale("traversal_widget", "bfs_button"))
        self.dfs_btn.setText(LocaleManager.get_locale("traversal_widget", "dfs_button"))
        
        # Оновлюємо мітку (потрібно знайти її в layout)
        layout = self.layout()
        if layout:
            # Оновлюємо мітку початкової вершини
            start_label = layout.itemAt(0).widget()
            if hasattr(start_label, 'setText'):
                start_label.setText(LocaleManager.get_locale("traversal_widget", "start_vertex_label"))
