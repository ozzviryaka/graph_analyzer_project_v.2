from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea
from PyQt5.QtGui import QIcon
from locales.locale_manager import LocaleManager

class EdgeEditDialog(QDialog):
    """
    Діалог для додавання або редагування ребра (вага + довільна кількість додаткових даних).
    """
    def __init__(self, weight=None, data=None, editable_weight=True, editable_data=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(LocaleManager.get_locale("edge_edit_dialog", "window_title"))
        self.setWindowIcon(QIcon("res/settings_icon.png"))
        layout = QVBoxLayout()

        # Вага
        if editable_weight:
            hlayout = QHBoxLayout()
            hlayout.addWidget(QLabel(LocaleManager.get_locale("edge_edit_dialog", "weight_label")))
            self.weight_edit = QLineEdit(str(weight) if weight is not None else "")
            hlayout.addWidget(self.weight_edit)
            layout.addLayout(hlayout)
        else:
            self.weight_edit = None

        # Додаткові дані (key-value)
        self.data_edits = []
        self.data_area = QVBoxLayout()
        self.data_widget = QWidget()
        self.data_widget.setLayout(self.data_area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.data_widget)
        layout.addWidget(QLabel(LocaleManager.get_locale("edge_edit_dialog", "additional_data_label")))
        layout.addWidget(scroll)

        if editable_data:
            if isinstance(data, dict):
                for k, v in data.items():
                    self._add_data_row(str(k), str(v))
            elif data is not None:
                self._add_data_row("key", str(data))
        self._add_data_row()  # Порожній рядок для додавання нового

        # btn_layout, OK/Cancel як було
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton(LocaleManager.get_locale("edge_edit_dialog", "ok_button"))
        cancel_btn = QPushButton(LocaleManager.get_locale("edge_edit_dialog", "cancel_button"))
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _add_data_row(self, key="", value=""):
        # Перетворення на str, якщо key/value не str
        key = str(key) if not isinstance(key, str) else key
        value = str(value) if not isinstance(value, str) else value
        hlayout = QHBoxLayout()
        key_edit = QLineEdit(key)
        value_edit = QLineEdit(value)
        remove_btn = QPushButton("-")
        remove_btn.setFixedWidth(24)
        hlayout.addWidget(QLabel(LocaleManager.get_locale("edge_edit_dialog", "key_label")))
        hlayout.addWidget(key_edit)
        hlayout.addWidget(QLabel(LocaleManager.get_locale("edge_edit_dialog", "value_label")))
        hlayout.addWidget(value_edit)
        hlayout.addWidget(remove_btn)
        self.data_area.addLayout(hlayout)
        self.data_edits.append((hlayout, key_edit, value_edit, remove_btn))
        remove_btn.clicked.connect(lambda: self._remove_data_row(hlayout))
        # Додаємо автододавання нового поля, якщо це останній рядок і він заповнений
        key_edit.textChanged.connect(lambda: self._auto_add_row(key_edit, value_edit))
        value_edit.textChanged.connect(lambda: self._auto_add_row(key_edit, value_edit))

    def _auto_add_row(self, key_edit, value_edit):
        # Якщо це останній рядок і обидва поля не порожні — додати ще один порожній рядок
        if self.data_edits and (self.data_edits[-1][1] is key_edit or self.data_edits[-1][2] is value_edit):
            k = self.data_edits[-1][1].text().strip()
            v = self.data_edits[-1][2].text().strip()
            if k and v:
                # Перевіряємо, чи вже немає порожнього поля в кінці
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

    def get_values(self):
        weight = None
        if self.weight_edit is not None:
            try:
                weight = float(self.weight_edit.text())
            except ValueError:
                weight = self.weight_edit.text()
        data = {}
        for hl, key_edit, value_edit, _ in self.data_edits:
            k = key_edit.text().strip()
            v = value_edit.text().strip()
            if k:
                data[k] = v
        return weight, data

    def keyPressEvent(self, event):
        from PyQt5.QtCore import Qt
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            for btn in self.findChildren(QPushButton):
                if btn.text().lower() in [LocaleManager.get_locale("common_dialogs", "ok_text"), LocaleManager.get_locale("common_dialogs", "select_text")]:
                    btn.click()
                    return
        super().keyPressEvent(event)
