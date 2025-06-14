from PyQt5.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QTableWidgetItem
from core.algorithms.matrices.adjacency_matrix import AdjacencyMatrix
from core.algorithms.matrices.incidence_matrix import IncidenceMatrix
from gui.widgets.matrix_tab_widgets.matrix_widget import MatrixWidget

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
        self.adj_widget = MatrixWidget(adj_matrix, row_labels=adj_labels, col_labels=adj_labels, title="Матриця суміжності")
        # Матриця інцидентності
        inc_matrix_obj = IncidenceMatrix(graph)
        inc_matrix = inc_matrix_obj.get_matrix()
        inc_row_labels = [node.id for node in inc_matrix_obj.nodes]
        inc_col_labels = [f"e{i+1}" for i in range(len(inc_matrix_obj.edges))] if hasattr(inc_matrix_obj, 'edges') else None
        self.inc_widget = MatrixWidget(inc_matrix, row_labels=inc_row_labels, col_labels=inc_col_labels, title="Матриця інцидентності")
        self.tabs.addTab(self.adj_widget, "Суміжності")
        self.tabs.addTab(self.inc_widget, "Інцидентності")
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
        # Оновити матрицю інцидентності
        inc_matrix_obj = IncidenceMatrix(graph)
        inc_matrix = inc_matrix_obj.get_matrix()
        inc_row_labels = [node.id for node in inc_matrix_obj.nodes]
        inc_col_labels = [f"E{i+1}" for i in range(len(inc_matrix_obj.edges))] if hasattr(inc_matrix_obj, 'edges') else None
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
