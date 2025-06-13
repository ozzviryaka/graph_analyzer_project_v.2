from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class InstructionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Інструкція")
        layout = QVBoxLayout()
        text = (
            "\u2139  Інструкція: створення та редагування графа\n"
            "\n"
            "- Додати вершину: ЛКМ по порожньому місцю\n"
            "- Видалити вершину: ПКМ по вершині\n"
            "- Додати ребро: виділіть вершину, потім ЛКМ+Ctrl по іншій вершині\n"
            "- Видалити ребро: ПКМ по середині ребра\n"
            "- Редагувати вагу ребра: подвійний ЛКМ по середині ребра (лише для вагового графа)\n"
            "- Переміщення вершини: ЛКМ по вершині та тягнути мишею\n"
            "- Зміна орієнтованості/ваговості/автоназв: тумблери над полотном\n"
            "- Експорт/імпорт графа: відповідні кнопки під полотном\n"
            "- Інструкція: кнопка під полотном\n"
            "\n"
            "Почніть з додавання вершин!"
        )
        label = QLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
        self.setLayout(layout)
