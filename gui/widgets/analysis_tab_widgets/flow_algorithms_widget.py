from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from core.algorithms.flow.ford_fulkerson import FordFulkerson
from core.algorithms.flow.min_cut import MinCut
from locales.locale_manager import LocaleManager

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
        layout.addWidget(QLabel(LocaleManager.get_locale("flow_algorithms_widget", "source_label")))
        layout.addWidget(self.source_combo)
        layout.addWidget(QLabel(LocaleManager.get_locale("flow_algorithms_widget", "sink_label")))
        layout.addWidget(self.sink_combo)
        # Дві кнопки для запуску алгоритмів
        self.run_ff_btn = QPushButton(LocaleManager.get_locale("flow_algorithms_widget", "ford_fulkerson_button"))
        self.run_ff_btn.setCursor(Qt.PointingHandCursor)
        self.run_ff_btn.clicked.connect(self.run_ford_fulkerson)
        self.run_mc_btn = QPushButton(LocaleManager.get_locale("flow_algorithms_widget", "min_cut_button"))
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
            QMessageBox.warning(self, LocaleManager.get_locale("flow_algorithms_widget", "error_title"), LocaleManager.get_locale("flow_algorithms_widget", "select_source_sink"))
            return
        try:
            algo = FordFulkerson(self.graph)
            max_flow = algo.max_flow(source, sink)
            self.output_textedit.setPlainText(LocaleManager.get_locale("flow_algorithms_widget", "max_flow_result").format(flow=max_flow))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("flow_algorithms_widget", "error_result").format(error=str(e)))

    def run_min_cut(self):
        source = self.source_combo.currentText().strip()
        sink = self.sink_combo.currentText().strip()
        if not source or not sink:
            QMessageBox.warning(self, LocaleManager.get_locale("flow_algorithms_widget", "error_title"), LocaleManager.get_locale("flow_algorithms_widget", "select_source_sink"))
            return
        try:
            algo = MinCut(self.graph)
            min_cut, cut_edges = algo.min_cut(source, sink)
            cut_str = "\n".join([f"{u} -> {v} (c={c})" for u, v, c in cut_edges])
            self.output_textedit.setPlainText(LocaleManager.get_locale("flow_algorithms_widget", "min_cut_result").format(cut=min_cut, edges=cut_str))
        except Exception as e:
            self.output_textedit.setPlainText(LocaleManager.get_locale("flow_algorithms_widget", "error_result").format(error=str(e)))

    def set_graph(self, graph):
        self.graph = graph
        self.update_nodes()

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        self.run_ff_btn.setText(LocaleManager.get_locale("flow_algorithms_widget", "ford_fulkerson_button"))
        self.run_mc_btn.setText(LocaleManager.get_locale("flow_algorithms_widget", "min_cut_button"))
        
        # Оновлюємо мітки в layout
        layout = self.layout()
        if layout:
            # Оновлюємо мітку джерела
            source_label = layout.itemAt(0).widget()
            if hasattr(source_label, 'setText'):
                source_label.setText(LocaleManager.get_locale("flow_algorithms_widget", "source_label"))
            
            # Оновлюємо мітку стоку
            sink_label = layout.itemAt(2).widget()
            if hasattr(sink_label, 'setText'):
                sink_label.setText(LocaleManager.get_locale("flow_algorithms_widget", "sink_label"))
