from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from gui.widgets.analysis_tab_widgets.traversal_widget import TraversalWidget
from gui.widgets.analysis_tab_widgets.spanning_tree_widget import SpanningTreeWidget
from gui.widgets.analysis_tab_widgets.flow_algorithms_widget import FlowAlgorithmsWidget
from gui.widgets.analysis_tab_widgets.shortest_paths_widget import ShortestPathsWidget
from gui.widgets.analysis_tab_widgets.special_paths_widget import SpecialPathsWidget
from gui.widgets.analysis_tab_widgets.analysis_output_controls import AnalysisOutputControls
from locales.locale_manager import LocaleManager

class GraphAnalysisTab(QWidget):
    """
    Вкладка для аналізу графа з вибором алгоритму, полем для виводу та кнопками керування.
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(LocaleManager.get_locale("graph_analysis_tab", "title")))
        self.alg_combo = QComboBox()
        self.alg_combo.setCursor(Qt.PointingHandCursor)
        self.alg_combo.addItems([
            LocaleManager.get_locale("graph_analysis_tab", "traversal_option"),
            LocaleManager.get_locale("graph_analysis_tab", "spanning_tree_option"),
            LocaleManager.get_locale("graph_analysis_tab", "flow_algorithms_option"),
            LocaleManager.get_locale("graph_analysis_tab", "shortest_paths_option"),
            LocaleManager.get_locale("graph_analysis_tab", "special_paths_option")
        ])
        layout.addWidget(self.alg_combo)
        self.output_textedit = QTextEdit()
        self.output_textedit.setReadOnly(True)
        self.output_textedit.setStyleSheet("")
        layout.addWidget(self.output_textedit)
        self.analysis_controls = AnalysisOutputControls(self.output_textedit)
        layout.addWidget(self.analysis_controls)
        self.setLayout(layout)
        # Алгоритмічні віджети
        self.widgets = [
            TraversalWidget(graph, self.output_textedit),
            SpanningTreeWidget(graph, self.output_textedit),
            FlowAlgorithmsWidget(graph, self.output_textedit),
            ShortestPathsWidget(graph, self.output_textedit),
            SpecialPathsWidget(graph, self.output_textedit)
        ]
        self.current_widget = self.widgets[0]
        layout.insertWidget(2, self.current_widget)
        self.alg_combo.currentIndexChanged.connect(self.switch_widget)

    def switch_widget(self, idx):
        self.layout().removeWidget(self.current_widget)
        self.current_widget.setParent(None)
        self.current_widget = self.widgets[idx]
        self.layout().insertWidget(2, self.current_widget)

    def update_nodes(self):
        """
        Оновлює комбобокси у всіх віджетах-алгоритмах (Traversal, Flow, Shortest, Special).
        """
        for widget in self.widgets:
            if hasattr(widget, 'update_nodes'):
                widget.update_nodes()

    def set_graph(self, graph):
        """
        Оновлює граф у всіх віджетах-алгоритмах
        """
        for widget in self.widgets:
            if hasattr(widget, 'set_graph'):
                widget.set_graph(graph)

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        # Оновлюємо елементи в комбобоксі алгоритмів
        current_index = self.alg_combo.currentIndex()
        self.alg_combo.blockSignals(True)
        self.alg_combo.clear()
        self.alg_combo.addItems([
            LocaleManager.get_locale("graph_analysis_tab", "traversal_option"),
            LocaleManager.get_locale("graph_analysis_tab", "spanning_tree_option"),
            LocaleManager.get_locale("graph_analysis_tab", "flow_algorithms_option"),
            LocaleManager.get_locale("graph_analysis_tab", "shortest_paths_option"),
            LocaleManager.get_locale("graph_analysis_tab", "special_paths_option")
        ])
        self.alg_combo.setCurrentIndex(current_index)
        self.alg_combo.blockSignals(False)
        
        # Оновлюємо текст в дочірніх віджетах
        for widget in self.widgets:
            if hasattr(widget, 'refresh_ui_text'):
                widget.refresh_ui_text()
        
        if hasattr(self.analysis_controls, 'refresh_ui_text'):
            self.analysis_controls.refresh_ui_text()
        
        # Оновлюємо мітку заголовка
        layout = self.layout()
        if layout:
            title_label = layout.itemAt(0).widget()
            if hasattr(title_label, 'setText'):
                title_label.setText(LocaleManager.get_locale("graph_analysis_tab", "title"))
