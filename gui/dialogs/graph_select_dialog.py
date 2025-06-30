from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QHBoxLayout, QLabel, QMessageBox, QInputDialog, QComboBox
from PyQt5.QtCore import Qt
from locales.locale_manager import LocaleManager

class GraphSelectDialog(QDialog):
    def __init__(self, graph_list, current_graph, parent=None):
        super().__init__(parent)
        self.setWindowTitle(LocaleManager.get_locale("graph_select_dialog", "window_title"))
        self.selected_graph = None
        self.graph_list = graph_list  # список об'єктів графів
        self.current_graph = current_graph
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.refresh_list()
        layout.addWidget(QLabel(LocaleManager.get_locale("graph_select_dialog", "select_graph_label")))
        layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton(LocaleManager.get_locale("graph_select_dialog", "new_graph_button"))
        self.btn_delete = QPushButton(LocaleManager.get_locale("graph_select_dialog", "delete_graph_button"))
        self.btn_select = QPushButton(LocaleManager.get_locale("graph_select_dialog", "select_button"))
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_select)
        # Додаємо кнопки для експорту та імпорту сесії
        self.btn_export_session = QPushButton(LocaleManager.get_locale("graph_select_dialog", "export_session_button"))
        self.btn_import_session = QPushButton(LocaleManager.get_locale("graph_select_dialog", "import_session_button"))
        btn_layout.addWidget(self.btn_export_session)
        btn_layout.addWidget(self.btn_import_session)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_new.clicked.connect(self.create_new_graph)
        self.btn_delete.clicked.connect(self.delete_graph)
        self.btn_select.clicked.connect(self.select_graph)
        self.btn_export_session.clicked.connect(self.export_session)
        self.btn_import_session.clicked.connect(self.import_session)

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
        directed_text = LocaleManager.get_locale("graph_select_dialog", "directed") if directed else LocaleManager.get_locale("graph_select_dialog", "undirected")
        weighted_text = LocaleManager.get_locale("graph_select_dialog", "weighted") if weighted else LocaleManager.get_locale("graph_select_dialog", "unweighted")
        return f"{name} | {directed_text} | {weighted_text}"

    def set_current_graph_selected(self):
        for i, g in enumerate(self.graph_list):
            if g is self.current_graph:
                self.list_widget.setCurrentRow(i)
                break

    def create_new_graph(self):
        # Діалог для вибору типу графа
        types = [LocaleManager.get_locale("graph_select_dialog", "directed"), LocaleManager.get_locale("graph_select_dialog", "undirected")]
        type_idx, ok = QInputDialog.getItem(self, LocaleManager.get_locale("graph_select_dialog", "graph_type_title"), LocaleManager.get_locale("graph_select_dialog", "graph_type_label"), types, 0, False)
        if not ok:
            return
        weighted, ok2 = QInputDialog.getItem(self, LocaleManager.get_locale("graph_select_dialog", "weight_title"), LocaleManager.get_locale("graph_select_dialog", "weight_label"), [LocaleManager.get_locale("graph_select_dialog", "yes"), LocaleManager.get_locale("graph_select_dialog", "no")], 0, False)
        if not ok2:
            return
        auto_name, ok4 = QInputDialog.getItem(self, LocaleManager.get_locale("graph_select_dialog", "auto_name_title"), LocaleManager.get_locale("graph_select_dialog", "auto_name_label"), [LocaleManager.get_locale("graph_select_dialog", "yes"), LocaleManager.get_locale("graph_select_dialog", "no")], 0, False)
        if not ok4:
            return
        name, ok3 = QInputDialog.getText(self, LocaleManager.get_locale("graph_select_dialog", "graph_name_title"), LocaleManager.get_locale("graph_select_dialog", "graph_name_label"))
        if not ok3 or not name.strip():
            return
        from core.graph_models.directed_graph import DirectedGraph
        from core.graph_models.undirected_graph import UndirectedGraph
        if type_idx == LocaleManager.get_locale("graph_select_dialog", "directed"):
            g = DirectedGraph(weighted=(weighted==LocaleManager.get_locale("graph_select_dialog", "yes")))
            g.directed = True
        else:
            g = UndirectedGraph(weighted=(weighted==LocaleManager.get_locale("graph_select_dialog", "yes")))
            g.directed = False
        g.name = name.strip()
        g.auto_vertex_name = (auto_name == LocaleManager.get_locale("graph_select_dialog", "yes"))
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
                QMessageBox.warning(self, LocaleManager.get_locale("graph_select_dialog", "delete_warning_title"), LocaleManager.get_locale("graph_select_dialog", "delete_active_graph"))
                return
            del self.graph_list[row]
            self.refresh_list()
        else:
            QMessageBox.warning(self, LocaleManager.get_locale("graph_select_dialog", "delete_warning_title"), LocaleManager.get_locale("graph_select_dialog", "delete_no_selection"))

    def select_graph(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.selected_graph = self.graph_list[row]
            self.accept()
        else:
            QMessageBox.warning(self, LocaleManager.get_locale("graph_select_dialog", "select_warning_title"), LocaleManager.get_locale("graph_select_dialog", "select_no_selection"))

    def export_session(self):
        from data_utils.session_exporter import SessionExporter
        from PyQt5.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(self, LocaleManager.get_locale("graph_select_dialog", "export_session_title"), "", LocaleManager.get_locale("graph_select_dialog", "session_files"))
        if filepath:
            SessionExporter.export_session(self.graph_list, filepath)

    def import_session(self):
        from data_utils.session_importer import SessionImporter
        from core.graph_models.directed_graph import DirectedGraph
        from core.graph_models.undirected_graph import UndirectedGraph
        from PyQt5.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getOpenFileName(self, LocaleManager.get_locale("graph_select_dialog", "import_session_title"), "", LocaleManager.get_locale("graph_select_dialog", "session_files"))
        if filepath:
            graph_class_map = {
                'DirectedGraph': DirectedGraph,
                'UndirectedGraph': UndirectedGraph,
                'Graph': UndirectedGraph  # fallback
            }
            imported_graphs = SessionImporter.import_session(filepath, graph_class_map)
            if imported_graphs:
                self.graph_list.clear()
                self.graph_list.extend(imported_graphs)
                self.refresh_list()
                self.set_current_graph_selected()

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            for btn in self.findChildren(QPushButton):
                if btn.text().lower() in [LocaleManager.get_locale("common_dialogs", "ok_text"), LocaleManager.get_locale("common_dialogs", "select_text")]:
                    btn.click()
                    return
        super().keyPressEvent(event)
