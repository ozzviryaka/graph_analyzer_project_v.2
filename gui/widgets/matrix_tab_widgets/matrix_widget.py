from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QAbstractScrollArea, QLabel
from PyQt5.QtCore import Qt

class MatrixWidget(QWidget):
    """
    Віджет для відображення матриці з прокруткою, якщо вона велика.
    """
    def __init__(self, matrix, row_labels=None, col_labels=None, title=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        if title:
            layout.addWidget(QLabel(f"<b>{title}</b>"))
        self.table = QTableWidget()
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        n_rows = len(matrix)
        n_cols = len(matrix[0]) if n_rows > 0 else 0
        self.table.setRowCount(n_rows)
        self.table.setColumnCount(n_cols)
        # Set labels if provided
        if row_labels:
            self.table.setVerticalHeaderLabels([str(l) for l in row_labels])
        if col_labels:
            self.table.setHorizontalHeaderLabels([str(l) for l in col_labels])
        # Fill table
        for i in range(n_rows):
            for j in range(n_cols):
                item = QTableWidgetItem(str(matrix[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setMinimumSize(400, 200)
        # self.table.setStyleSheet("")
        layout.addWidget(self.table)
        self.setLayout(layout)

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        # Оновлюємо заголовок, якщо він є
        layout = self.layout()
        if layout and layout.count() > 0:
            first_item = layout.itemAt(0).widget()
            if hasattr(first_item, 'setText') and hasattr(first_item, 'text'):
                # Це QLabel з заголовком
                current_text = first_item.text()
                if current_text and '<b>' in current_text:
                    # Заголовок потрібно оновити в батьківському класі
                    pass
