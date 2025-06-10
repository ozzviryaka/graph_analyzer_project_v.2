from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QLabel, QTextEdit
from gui.widgets.traversal_widget import TraversalWidget
from gui.widgets.spanning_tree_widget import SpanningTreeWidget
from gui.widgets.flow_algorithms_widget import FlowAlgorithmsWidget
from gui.widgets.shortest_paths_widget import ShortestPathsWidget
from gui.widgets.special_paths_widget import SpecialPathsWidget
from gui.widgets.analysis_output_controls import AnalysisOutputControls

class GraphAnalysisTab(QWidget):
    """
    Вкладка для аналізу графа з вибором алгоритму, полем для виводу та кнопками керування.
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Аналіз графа</h2>"))
        self.alg_combo = QComboBox()
        self.alg_combo.addItems([
            "Обхід графа (BFS/DFS)",
            "Остовні дерева (Прим/Краскал)",
            "Потокові алгоритми (Ford-Fulkerson/Min-Cut)",
            "Найкоротші шляхи (Дейкстра/Беллман-Форд/Флойд-Уоршелл)",
            "Спеціальні шляхи (простий/найдовший/гамільтонів/ейлерів)"
        ])
        layout.addWidget(self.alg_combo)
        self.output_textedit = QTextEdit()
        self.output_textedit.setReadOnly(True)
        self.output_textedit.setStyleSheet("background-color: #23272e; color: #e0e0e0; font-size: 13px;")
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
