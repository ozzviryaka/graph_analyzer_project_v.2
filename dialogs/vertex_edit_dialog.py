from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea
from utils.logger import Logger

class VertexEditDialog(QDialog):
    """
    Діалог для редагування/додавання довільної кількості додаткових даних вершини (ключ-значення).
    """
    def __init__(self, data=None, editable_data=True, parent=None, node_id=None):
        super().__init__(parent)
        self.node_id = node_id
        self.setWindowTitle("Редагування вершини")
        layout = QVBoxLayout()

        self.data_edits = []
        self.data_area = QVBoxLayout()
        self.data_widget = QWidget()
        self.data_widget.setLayout(self.data_area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.data_widget)
        layout.addWidget(QLabel("Додаткові дані вершини (ключ-значення):"))
        layout.addWidget(scroll)

        if editable_data:
            if isinstance(data, dict):
                for k, v in data.items():
                    self._add_data_row(str(k), str(v))
            elif data is not None:
                self._add_data_row("key", str(data))
        self._add_data_row()  # Порожній рядок для додавання нового

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Скасувати")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _add_data_row(self, key="", value=""):
        key = str(key) if not isinstance(key, str) else key
        value = str(value) if not isinstance(value, str) else value
        hlayout = QHBoxLayout()
        key_edit = QLineEdit(key)
        value_edit = QLineEdit(value)
        remove_btn = QPushButton("-")
        remove_btn.setFixedWidth(24)
        hlayout.addWidget(QLabel("Ключ:"))
        hlayout.addWidget(key_edit)
        hlayout.addWidget(QLabel("Значення:"))
        hlayout.addWidget(value_edit)
        hlayout.addWidget(remove_btn)
        self.data_area.addLayout(hlayout)
        self.data_edits.append((hlayout, key_edit, value_edit, remove_btn))
        remove_btn.clicked.connect(lambda: self._remove_data_row(hlayout))
        key_edit.textChanged.connect(lambda: self._auto_add_row(key_edit, value_edit))
        value_edit.textChanged.connect(lambda: self._auto_add_row(key_edit, value_edit))

    def _auto_add_row(self, key_edit, value_edit):
        if self.data_edits and (self.data_edits[-1][1] is key_edit or self.data_edits[-1][2] is value_edit):
            k = self.data_edits[-1][1].text().strip()
            v = self.data_edits[-1][2].text().strip()
            if k and v:
                self._add_data_row()

    def _remove_data_row(self, layout):
        for i, (hl, key_edit, value_edit, remove_btn) in enumerate(self.data_edits):
            if hl == layout:
                for j in reversed(range(hl.count())):
                    w = hl.itemAt(j).widget()
                    if w is not None:
                        w.setParent(None)
                self.data_area.removeItem(hl)
                self.data_edits.pop(i)
                break

    def get_data(self):
        data = {}
        for hl, key_edit, value_edit, _ in self.data_edits:
            k = key_edit.text().strip()
            v = value_edit.text().strip()
            if k:
                data[k] = v
        return data

    def accept(self):
        data = self.get_data()
        node_info = f" (id: {self.node_id})" if self.node_id is not None else ""
        Logger().info(f"Дані вершини{node_info} після редагування: {data}")
        super().accept()
