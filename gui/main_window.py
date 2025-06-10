from PyQt5.QtWidgets import QMainWindow, QApplication
from gui.tabs.graph_tabs_widget import GraphTabsWidget
from gui.widgets.graph_settings_widget import GraphSettingsWidget
from core.graph_models.undirected_graph import UndirectedGraph

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Граф-аналізатор")
        self.setMinimumSize(1100, 700)
        # Створюємо новий порожній граф для роботи (можна змінити на DirectedGraph за потреби)
        self.graph = UndirectedGraph()
        # Віджет налаштувань графа (тумблери)
        self.settings_widget = GraphSettingsWidget(self.graph, self.on_graph_changed)
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

    def on_graph_changed(self, new_graph):
        self.graph = new_graph
        self.tabs.graph = new_graph
        # Оновити вкладки/віджети, якщо потрібно (наприклад, перерисувати canvas, оновити комбобокси тощо)
        if hasattr(self.tabs, 'combined_tab') and hasattr(self.tabs.combined_tab, 'canvas_widget'):
            self.tabs.combined_tab.canvas_widget.canvas.graph = new_graph
            self.tabs.combined_tab.canvas_widget.canvas._init_node_positions()
            self.tabs.combined_tab.canvas_widget.canvas.update()
        # Оновити інформацію про граф
        if hasattr(self.tabs, 'update_info'):
            self.tabs.update_info(new_graph)
        # Оновити матриці
        if hasattr(self.tabs, 'update_matrix'):
            self.tabs.update_matrix(new_graph)
        # Оновити комбобокси у всіх віджетах, якщо є метод update_nodes
        for tab in getattr(self.tabs, 'widgets', []):
            if hasattr(tab, 'update_nodes'):
                tab.update_nodes()

# Для запуску як standalone (опціонально):
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
