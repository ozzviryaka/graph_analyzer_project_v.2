from PyQt5.QtWidgets import QMainWindow, QApplication
from gui.tabs.graph_tabs_widget import GraphTabsWidget
from gui.widgets.graph_settings_widget import GraphSettingsWidget
from core.graph_models.directed_graph import DirectedGraph
from core.graph_models.undirected_graph import UndirectedGraph
# Add theme imports
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory
from gui.themes.classic.dark_theme import DarkTheme
from gui.themes.theme_manager import ThemeManager
from gui.additionals.tab_shortcut_event_filter import TabShortcutEventFilter
from utils.logger import Logger

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Logger().info("Запущено програму")
        ThemeManager.load_theme()  # Завантажити тему з settings.json
        # ThemeManager.apply_theme(DarkTheme)  # Видалено, тепер тема зберігається
        self.setWindowTitle("G_A_P_V.2")
        self.setWindowIcon(QIcon("res/icon.png"))
        self.setMinimumSize(1100, 700)
        # --- Менеджмент графів ---
        self.graphs = []
        g = UndirectedGraph()
        g.name = "Граф 1"
        g.directed = False
        self.graphs.append(g)
        self.graph = g
        # Віджет налаштувань графа (тумблери)
        self.settings_widget = GraphSettingsWidget(self.graph, self.on_graph_changed)
        self.settings_widget.set_graphs_list(self.graphs)
        self.settings_widget.set_graph(self.graph)
        # Додаємо метод для оновлення налаштувань при зміні графа
        # Віджет з вкладками
        self.tabs = GraphTabsWidget(self.graph)
        self.tabs.set_on_graph_changed(self.on_graph_changed)
        # Розміщення: тумблери зверху, вкладки знизу
        from PyQt5.QtWidgets import QWidget, QVBoxLayout
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.settings_widget)
        layout.addWidget(self.tabs)
        central.setLayout(layout)
        self.setCentralWidget(central)
        # Передати список графів у вкладки
        if hasattr(self.tabs.combined_tab.canvas_widget, 'set_graphs_list'):
            self.tabs.combined_tab.canvas_widget.set_graphs_list(self.graphs, self)
        self.settings_widget.auto_vertex_name_switch.toggled.connect(self.on_auto_vertex_name_changed)
        # Додаємо фільтр для Alt+1..9
        tab_widget = self.tabs.tabs if hasattr(self.tabs, 'tabs') else None
        if tab_widget:
            self.tab_shortcut_filter = TabShortcutEventFilter(self, tab_widget)
            self.installEventFilter(self.tab_shortcut_filter)

    def on_graph_changed(self, new_graph):
        # Якщо новий граф є у списку, зробити його активним
        for i, g in enumerate(self.graphs):
            if g is new_graph:
                self.graph = new_graph
                break
        else:
            # Якщо немає — додати (страховка)
            self.graphs.append(new_graph)
            self.graph = new_graph
        self.tabs.graph = self.graph
        if hasattr(self.tabs, 'combined_tab') and hasattr(self.tabs.combined_tab, 'canvas_widget'):
            self.tabs.combined_tab.canvas_widget.canvas.graph = self.graph
            self.tabs.combined_tab.canvas_widget.canvas._init_node_positions()
            self.tabs.combined_tab.canvas_widget.canvas.update()
        if hasattr(self.tabs.combined_tab.canvas_widget, 'import_export_widget'):
            self.tabs.combined_tab.canvas_widget.import_export_widget.graph = self.graph
        if hasattr(self.settings_widget, 'set_graph'):
            self.settings_widget.set_graph(self.graph)
        if hasattr(self.tabs, 'update_info'):
            self.tabs.update_info(self.graph)
        if hasattr(self.tabs, 'update_matrix'):
            self.tabs.update_matrix(self.graph)
        if hasattr(self.tabs, 'update_nodes'):
            self.tabs.update_nodes()

    def on_auto_vertex_name_changed(self, checked):
        if hasattr(self.tabs.combined_tab.canvas_widget, 'set_auto_vertex_name'):
            self.tabs.combined_tab.canvas_widget.set_auto_vertex_name(checked)
