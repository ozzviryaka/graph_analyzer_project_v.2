from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel, QMessageBox, QInputDialog, QComboBox
from PyQt5.QtCore import Qt

class GraphSelectDialog(QDialog):
    def __init__(self, graph_list, current_graph, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вибір графа")
        self.selected_graph = None
        self.graph_list = graph_list  # список об'єктів графів
        self.current_graph = current_graph
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.refresh_list()
        layout.addWidget(QLabel("Оберіть граф для роботи:"))
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton("Новий граф")
        self.btn_delete = QPushButton("Видалити граф")
        self.btn_select = QPushButton("Вибрати")
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_select)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_new.clicked.connect(self.create_new_graph)
        self.btn_delete.clicked.connect(self.delete_graph)
        self.btn_select.clicked.connect(self.select_graph)

        # Встановити поточний граф як вибраний
        self.set_current_graph_selected()

    def refresh_list(self):
        self.list_widget.clear()
        for g in self.graph_list:
            desc = self.graph_description(g)
            self.list_widget.addItem(desc)

    def graph_description(self, g):
        name = getattr(g, 'name', str(id(g)))
        directed = getattr(g, 'directed', hasattr(g, 'is_directed') and g.is_directed())
        weighted = getattr(g, 'weighted', False)
        return f"{name} | {'Орієнтований' if directed else 'Неорієнтований'} | {'Ваговий' if weighted else 'Неваговий'}"

    def set_current_graph_selected(self):
        for i, g in enumerate(self.graph_list):
            if g is self.current_graph:
                self.list_widget.setCurrentRow(i)
                break

    def create_new_graph(self):
        # Діалог для вибору типу графа
        types = ["Орієнтований", "Неорієнтований"]
        type_idx, ok = QInputDialog.getItem(self, "Тип графа", "Оберіть тип графа:", types, 0, False)
        if not ok:
            return
        weighted, ok2 = QInputDialog.getItem(self, "Ваговість", "Граф ваговий?", ["Так", "Ні"], 0, False)
        if not ok2:
            return
        auto_name, ok4 = QInputDialog.getItem(self, "Автоматична назва вершин", "Використовувати автоназви для вершин?", ["Так", "Ні"], 0, False)
        if not ok4:
            return
        name, ok3 = QInputDialog.getText(self, "Назва графа", "Введіть назву графа:")
        if not ok3 or not name.strip():
            return
        from core.graph_models.directed_graph import DirectedGraph
        from core.graph_models.undirected_graph import UndirectedGraph
        if type_idx == "Орієнтований":
            g = DirectedGraph(weighted=(weighted=="Так"))
            g.directed = True
        else:
            g = UndirectedGraph(weighted=(weighted=="Так"))
            g.directed = False
        g.name = name.strip()
        g.auto_vertex_name = (auto_name == "Так")
        # Оновити чекбокс у налаштуваннях, якщо є
        main_window = self.parent()
        if hasattr(main_window, 'settings_widget'):
            main_window.settings_widget.set_auto_vertex_name(g.auto_vertex_name)
            # Також оновити GraphCanvas, якщо потрібно
            if hasattr(main_window.tabs.combined_tab.canvas_widget, 'set_auto_vertex_name'):
                main_window.tabs.combined_tab.canvas_widget.set_auto_vertex_name(g.auto_vertex_name)
        self.graph_list.append(g)
        self.refresh_list()
        self.list_widget.setCurrentRow(len(self.graph_list)-1)

    def delete_graph(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            if self.graph_list[row] is self.current_graph:
                QMessageBox.warning(self, "Видалення", "Неможливо видалити активний граф. Спочатку виберіть інший.")
                return
            del self.graph_list[row]
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Видалення", "Оберіть граф для видалення.")

    def select_graph(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.selected_graph = self.graph_list[row]
            self.accept()
        else:
            QMessageBox.warning(self, "Вибір", "Оберіть граф зі списку.")
