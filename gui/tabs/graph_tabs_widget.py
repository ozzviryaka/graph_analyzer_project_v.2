from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from gui.tabs.graph_combined_tab import GraphCombinedTab
from gui.tabs.matrix_tabs_widget import MatrixTabsWidget
from gui.tabs.graph_analysis_tab import GraphAnalysisTab
from gui.tabs.traversal_tab import TraversalTab
from locales.locale_manager import LocaleManager

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
        self.traversal_tab = TraversalTab(graph)
        self.tabs.addTab(self.combined_tab, LocaleManager.get_locale("graph_tabs_widget", "graph_info_tab"))
        self.tabs.addTab(self.matrix_tab, LocaleManager.get_locale("graph_tabs_widget", "matrices_tab"))
        self.tabs.addTab(self.analysis_tab, LocaleManager.get_locale("graph_tabs_widget", "analysis_tab"))
        self.tabs.addTab(self.traversal_tab, LocaleManager.get_locale("graph_tabs_widget", "traversal_tab"))
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.widgets = [self.analysis_tab, self.traversal_tab]  # Додаємо вкладку обходу
        self.tabs.tabBar().setMouseTracking(True)

    def update_analysis_graph(self, graph):
        if hasattr(self.analysis_tab, 'set_graph'):
            self.analysis_tab.set_graph(graph)

    def update_traversal_graph(self, graph):
        if hasattr(self.traversal_tab, 'set_graph'):
            self.traversal_tab.set_graph(graph)

    def update_info(self, graph):
        self.combined_tab.set_graph(graph)
        self.update_analysis_graph(graph)
        self.update_traversal_graph(graph)

    def update_matrix(self, graph):
        self.matrix_tab.update_matrix(graph)
        self.update_analysis_graph(graph)
        self.update_traversal_graph(graph)

    def set_on_graph_changed(self, callback):
        self.combined_tab.set_on_graph_changed(callback)

    def update_nodes(self):
        """
        Оновлює комбобокси у вкладці аналізу графа (і відповідних віджетах-алгоритмах).
        """
        if hasattr(self.analysis_tab, 'update_nodes'):
            self.analysis_tab.update_nodes()
