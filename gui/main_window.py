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
from locales.locale_manager import LocaleManager

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Logger().info(LocaleManager.get_locale("main_window", "app_started"))
        ThemeManager.load_theme()  # Завантажити тему з settings.json
        # ThemeManager.apply_theme(DarkTheme)  # Видалено, тепер тема зберігається
        self.setWindowTitle(LocaleManager.get_locale("main_window", "app_title"))
        self.setWindowIcon(QIcon("res/icon.png"))
        self.setMinimumSize(1100, 700)
        # --- Менеджмент графів ---
        self.graphs = []
        g = UndirectedGraph()
        g.name = LocaleManager.get_locale("main_window", "default_graph_name")
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

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        # Оновити заголовок вікна
        self.setWindowTitle(LocaleManager.get_locale("main_window", "app_title"))
        
        # Оновити назву графа за замовчуванням для нових графів
        for graph in self.graphs:
            if hasattr(graph, 'name') and graph.name in ["Граф 1", "Graph 1"]:
                graph.name = LocaleManager.get_locale("main_window", "default_graph_name")
        
        # Оновити віджети
        if hasattr(self.settings_widget, 'refresh_ui_text'):
            self.settings_widget.refresh_ui_text()
        
        if hasattr(self.tabs, 'refresh_ui_text'):
            self.tabs.refresh_ui_text()
        
        # Перемалювати інтерфейс
        self.update()
