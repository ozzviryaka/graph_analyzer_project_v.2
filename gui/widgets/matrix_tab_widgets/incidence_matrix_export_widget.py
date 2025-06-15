from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
from typing import List, Optional
from data_utils.incidence_matrix_exporter import IncidenceMatrixExporter
from gui.additionals.incidence_matrix_image_exporter import IncidenceMatrixImageExporter

class IncidenceMatrixExportWidget(QWidget):
    def __init__(self, matrix: List[List[int]], row_names: Optional[List[str]] = None, col_names: Optional[List[str]] = None, parent=None):
        super().__init__(parent)
        self.matrix = matrix
        self.row_names = row_names
        self.col_names = col_names
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.csv_btn = QPushButton('Експортувати у CSV')
        self.png_btn = QPushButton('Експортувати у PNG')
        self.csv_btn.clicked.connect(self.export_csv)
        self.png_btn.clicked.connect(self.export_png)
        layout.addWidget(self.csv_btn)
        layout.addWidget(self.png_btn)
        self.setLayout(layout)

    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Зберегти як CSV', '', 'CSV files (*.csv)')
        if file_path:
            try:
                IncidenceMatrixExporter.export(self.matrix, file_path, self.row_names, self.col_names)
                QMessageBox.information(self, 'Успіх', 'Матриця інцидентості збережена у CSV!')
            except Exception as e:
                QMessageBox.critical(self, 'Помилка', str(e))

    def export_png(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Зберегти як PNG', '', 'PNG files (*.png)')
        if file_path:
            try:
                IncidenceMatrixImageExporter.export(self.matrix, file_path, self.row_names, self.col_names)
                QMessageBox.information(self, 'Успіх', 'Матриця інцидентості збережена у PNG!')
            except Exception as e:
                QMessageBox.critical(self, 'Помилка', str(e))
