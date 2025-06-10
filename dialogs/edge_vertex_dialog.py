from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class EdgeDialog(QDialog):
    """
    Діалог для редагування/додавання ваги та даних ребра.
    """
    def __init__(self, weight=None, data=None, editable_weight=True, editable_data=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редагування ребра")
        layout = QVBoxLayout()

        if editable_weight:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Вага ребра:"))
            self.weight_edit = QLineEdit(str(weight) if weight is not None else "")
            hlayout.addWidget(self.weight_edit)
            layout.addLayout(hlayout)
        else:
            self.weight_edit = None

        if editable_data:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Дані:"))
            self.data_edit = QLineEdit(str(data) if data is not None else "")
            hlayout.addWidget(self.data_edit)
            layout.addLayout(hlayout)
        else:
            self.data_edit = None

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Скасувати")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def get_values(self):
        weight = None
        data = None
        if self.weight_edit is not None:
            try:
                weight = float(self.weight_edit.text())
            except ValueError:
                weight = self.weight_edit.text()
        if self.data_edit is not None:
            data = self.data_edit.text()
        return weight, data

class VertexDialog(QDialog):
    """
    Діалог для редагування/додавання даних вершини.
    """
    def __init__(self, data=None, editable_data=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редагування вершини")
        layout = QVBoxLayout()

        if editable_data:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel("Дані вершини:"))
            self.data_edit = QLineEdit(str(data) if data is not None else "")
            hlayout.addWidget(self.data_edit)
            layout.addLayout(hlayout)
        else:
            self.data_edit = None

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Скасувати")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def get_value(self):
        if self.data_edit is not None:
            return self.data_edit.text()
        return None
