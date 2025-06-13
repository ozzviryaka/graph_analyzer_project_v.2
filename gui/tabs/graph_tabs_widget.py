from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QObject, QEvent
from gui.tabs.graph_combined_tab import GraphCombinedTab
from gui.tabs.matrix_tabs_widget import MatrixTabsWidget
from gui.tabs.graph_analysis_tab import GraphAnalysisTab

class TabBarEventFilter(QObject):
    def __init__(self, tab_widget):
        super().__init__(tab_widget)
        self.tab_widget = tab_widget

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverMove:
            tabbar = self.tab_widget.tabBar()
            index = tabbar.tabAt(event.pos())
            if index != -1:
                tabbar.setCursor(Qt.PointingHandCursor)
            else:
                tabbar.setCursor(Qt.ArrowCursor)
        elif event.type() == QEvent.Leave:
            self.tab_widget.tabBar().setCursor(Qt.ArrowCursor)
        return False

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
        self.tabs.tabBar().setMouseTracking(True)
        # Add event filter to tab bar for hand cursor only on inactive tabs
        self._tabbar_filter = TabBarEventFilter(self.tabs)
        self.tabs.tabBar().installEventFilter(self._tabbar_filter)

    def update_analysis_graph(self, graph):
        if hasattr(self.analysis_tab, 'set_graph'):
            self.analysis_tab.set_graph(graph)

    def update_info(self, graph):
        self.combined_tab.set_graph(graph)
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
