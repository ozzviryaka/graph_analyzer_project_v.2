from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
from typing import List, Optional
from data_utils.adjacency_matrix_exporter import AdjacencyMatrixExporter
import pprint

class AdjacencyMatrixExportWidget(QWidget):
    def __init__(self, matrix: List[List[int]], row_names: Optional[List[str]] = None, col_names: Optional[List[str]] = None, parent=None):
        super().__init__(parent)
        self.matrix = matrix if isinstance(matrix, list) and all(isinstance(row, list) for row in matrix) else []
        self.row_names = row_names if row_names else []
        self.col_names = col_names if col_names else []
        self.init_ui()
        # Додаємо MatrixWidget для відображення та експорту
        from gui.widgets.matrix_tab_widgets.matrix_widget import MatrixWidget
        self.matrix_widget = MatrixWidget(self.matrix, self.row_names, self.col_names)

    def init_ui(self):
        layout = QHBoxLayout()
        self.csv_btn = QPushButton('Експортувати у CSV')
        # self.png_btn = QPushButton('Експортувати у PNG')
        self.csv_btn.clicked.connect(self.export_csv)
        # self.png_btn.clicked.connect(self.export_png)
        layout.addWidget(self.csv_btn)
        # layout.addWidget(self.png_btn)
        self.setLayout(layout)

    def export_csv(self):
        if not self.matrix or not isinstance(self.matrix, list) or not all(isinstance(row, list) for row in self.matrix):
            QMessageBox.critical(self, 'Помилка', 'Матриця порожня або некоректна!')
            return
        file_path, _ = QFileDialog.getSaveFileName(self, 'Зберегти як CSV', '', 'CSV files (*.csv)')
        if file_path:
            try:
                AdjacencyMatrixExporter.export(self.matrix, file_path, self.row_names, self.col_names)
                QMessageBox.information(self, 'Успіх', 'Матриця суміжності збережена у CSV!')
            except Exception as e:
                QMessageBox.critical(self, 'Помилка', str(e))
