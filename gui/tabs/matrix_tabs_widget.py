from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QTableWidgetItem
from core.algorithms.matrices.adjacency_matrix import AdjacencyMatrix
from core.algorithms.matrices.incidence_matrix import IncidenceMatrix
from gui.widgets.matrix_tab_widgets.matrix_widget import MatrixWidget
from gui.widgets.matrix_tab_widgets.adjacency_matrix_export_widget import AdjacencyMatrixExportWidget
from gui.widgets.matrix_tab_widgets.incidence_matrix_export_widget import IncidenceMatrixExportWidget
from locales.locale_manager import LocaleManager

class MatrixTabsWidget(QWidget):
    """
    Віджет з вкладками для матриці суміжності та інцидентності.
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.tabs = QTabWidget()
        # Матриця суміжності
        adj_matrix_obj = AdjacencyMatrix(graph)
        adj_matrix = adj_matrix_obj.get_matrix()
        adj_labels = [node.id for node in adj_matrix_obj.nodes]
        self.adj_widget = MatrixWidget(adj_matrix, row_labels=adj_labels, col_labels=adj_labels, title=LocaleManager.get_locale("matrix_tabs_widget", "adjacency_matrix_title"))
        self.adj_export_widget = AdjacencyMatrixExportWidget(adj_matrix, row_names=adj_labels, col_names=adj_labels)
        # Матриця інцидентності
        inc_matrix_obj = IncidenceMatrix(graph)
        inc_matrix = inc_matrix_obj.get_matrix()
        inc_row_labels = [node.id for node in inc_matrix_obj.nodes]
        inc_col_labels = [LocaleManager.get_locale("matrix_tabs_widget", "edge_label").format(index=i+1) for i in range(len(inc_matrix_obj.edges))] if hasattr(inc_matrix_obj, 'edges') else None
        self.inc_widget = MatrixWidget(inc_matrix, row_labels=inc_row_labels, col_labels=inc_col_labels, title=LocaleManager.get_locale("matrix_tabs_widget", "incidence_matrix_title"))
        self.inc_export_widget = IncidenceMatrixExportWidget(inc_matrix, row_names=inc_row_labels, col_names=inc_col_labels)
        # Додаємо віджети у вкладки
        adj_tab = QWidget()
        adj_layout = QVBoxLayout()
        adj_layout.addWidget(self.adj_widget)
        adj_layout.addWidget(self.adj_export_widget)
        adj_tab.setLayout(adj_layout)
        inc_tab = QWidget()
        inc_layout = QVBoxLayout()
        inc_layout.addWidget(self.inc_widget)
        inc_layout.addWidget(self.inc_export_widget)
        inc_tab.setLayout(inc_layout)
        self.tabs.addTab(adj_tab, LocaleManager.get_locale("matrix_tabs_widget", "adjacency_tab"))
        self.tabs.addTab(inc_tab, LocaleManager.get_locale("matrix_tabs_widget", "incidence_tab"))
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def update_matrix(self, graph):
        # Оновити матрицю суміжності
        adj_matrix_obj = AdjacencyMatrix(graph)
        adj_matrix = adj_matrix_obj.get_matrix()
        adj_labels = [node.id for node in adj_matrix_obj.nodes]
        self.adj_widget.table.setRowCount(len(adj_matrix))
        self.adj_widget.table.setColumnCount(len(adj_matrix[0]) if adj_matrix else 0)
        if adj_labels:
            self.adj_widget.table.setVerticalHeaderLabels([str(l) for l in adj_labels])
            self.adj_widget.table.setHorizontalHeaderLabels([str(l) for l in adj_labels])
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[0])):
                item = self.adj_widget.table.item(i, j)
                if not item:
                    item = QTableWidgetItem()
                    self.adj_widget.table.setItem(i, j, item)
                item.setText(str(adj_matrix[i][j]))
        self.adj_widget.table.resizeColumnsToContents()
        self.adj_widget.table.resizeRowsToContents()
        # Оновити дані експорту для матриці суміжності
        self.adj_export_widget.matrix = adj_matrix
        self.adj_export_widget.row_names = adj_labels
        self.adj_export_widget.col_names = adj_labels
        # Оновити матрицю інцидентності
        inc_matrix_obj = IncidenceMatrix(graph)
        inc_matrix = inc_matrix_obj.get_matrix()
        inc_row_labels = [node.id for node in inc_matrix_obj.nodes]
        inc_col_labels = [LocaleManager.get_locale("matrix_tabs_widget", "edge_label").format(index=i+1) for i in range(len(inc_matrix_obj.edges))] if hasattr(inc_matrix_obj, 'edges') else None
        self.inc_widget.table.setRowCount(len(inc_matrix))
        self.inc_widget.table.setColumnCount(len(inc_matrix[0]) if inc_matrix else 0)
        if inc_row_labels:
            self.inc_widget.table.setVerticalHeaderLabels([str(l) for l in inc_row_labels])
        if inc_col_labels:
            self.inc_widget.table.setHorizontalHeaderLabels([str(l) for l in inc_col_labels])
        for i in range(len(inc_matrix)):
            for j in range(len(inc_matrix[0])):
                item = self.inc_widget.table.item(i, j)
                if not item:
                    item = QTableWidgetItem()
                    self.inc_widget.table.setItem(i, j, item)
                item.setText(str(inc_matrix[i][j]))
        self.inc_widget.table.resizeColumnsToContents()
        self.inc_widget.table.resizeRowsToContents()
        # Оновити дані експорту для матриці інцидентності
        self.inc_export_widget.matrix = inc_matrix
        self.inc_export_widget.row_names = inc_row_labels
        self.inc_export_widget.col_names = inc_col_labels

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        # Оновлюємо назви вкладок
        self.tabs.setTabText(0, LocaleManager.get_locale("matrix_tabs_widget", "adjacency_tab"))
        self.tabs.setTabText(1, LocaleManager.get_locale("matrix_tabs_widget", "incidence_tab"))
        
        # Оновлюємо заголовки матриць
        adj_layout = self.adj_widget.layout()
        if adj_layout:
            title_label = adj_layout.itemAt(0).widget()
            if hasattr(title_label, 'setText'):
                title_label.setText(f"<b>{LocaleManager.get_locale('matrix_tabs_widget', 'adjacency_matrix_title')}</b>")
        
        inc_layout = self.inc_widget.layout()
        if inc_layout:
            title_label = inc_layout.itemAt(0).widget()
            if hasattr(title_label, 'setText'):
                title_label.setText(f"<b>{LocaleManager.get_locale('matrix_tabs_widget', 'incidence_matrix_title')}</b>")
        
        # Оновлюємо мітки колонок для матриці інцидентності
        if hasattr(self.inc_widget, 'table') and hasattr(self.inc_export_widget, 'col_names'):
            col_count = self.inc_widget.table.columnCount()
            if col_count > 0:
                new_col_labels = [LocaleManager.get_locale("matrix_tabs_widget", "edge_label").format(index=i+1) for i in range(col_count)]
                self.inc_widget.table.setHorizontalHeaderLabels(new_col_labels)
                self.inc_export_widget.col_names = new_col_labels
        
        # Оновлюємо текст в експорт віджетах
        if hasattr(self.adj_export_widget, 'refresh_ui_text'):
            self.adj_export_widget.refresh_ui_text()
        if hasattr(self.inc_export_widget, 'refresh_ui_text'):
            self.inc_export_widget.refresh_ui_text()
