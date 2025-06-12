from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from gui.tabs.graph_combined_tab import GraphCombinedTab
from gui.tabs.matrix_tabs_widget import MatrixTabsWidget
from gui.tabs.graph_analysis_tab import GraphAnalysisTab

class GraphTabsWidget(QWidget):
    """
    Віджет з вкладками: граф+інфо, матриці, аналіз графа.
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.tabs = QTabWidget()
        self.combined_tab = GraphCombinedTab(graph)
        self.matrix_tab = MatrixTabsWidget(graph)
        self.analysis_tab = GraphAnalysisTab(graph)
        self.tabs.addTab(self.combined_tab, "Граф та інформація")
        self.tabs.addTab(self.matrix_tab, "Матриці")
        self.tabs.addTab(self.analysis_tab, "Аналіз графа")
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.widgets = [self.analysis_tab]  # Додаємо список для зручного доступу до вкладок з алгоритмами

    def update_analysis_graph(self, graph):
        if hasattr(self.analysis_tab, 'set_graph'):
            self.analysis_tab.set_graph(graph)

    def update_info(self, graph):
        self.combined_tab.update_info(graph)
        self.update_analysis_graph(graph)

    def update_matrix(self, graph):
        self.matrix_tab.update_matrix(graph)
        self.update_analysis_graph(graph)

    def set_on_graph_changed(self, callback):
        self.combined_tab.set_on_graph_changed(callback)

    def update_nodes(self):
        """
        Оновлює комбобокси у вкладці аналізу графа (і відповідних віджетах-алгоритмах).
        """
        if hasattr(self.analysis_tab, 'update_nodes'):
            self.analysis_tab.update_nodes()
