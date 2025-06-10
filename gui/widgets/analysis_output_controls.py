from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from utils.txt_exporter import TxtExporter

class AnalysisOutputControls(QWidget):
    """
    Віджет з кнопками для експорту результатів у .txt та очищення поля результатів.
    """
    def __init__(self, output_textedit, parent=None):
        super().__init__(parent)
        self.output_textedit = output_textedit
        layout = QHBoxLayout()
        self.export_btn = QPushButton("Експортувати у .txt")
        self.export_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.export_btn.clicked.connect(self.export_txt)
        self.clear_btn = QPushButton("Очистити результати")
        self.clear_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")
        self.clear_btn.clicked.connect(self.clear_output)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.clear_btn)
        self.setLayout(layout)

    def export_txt(self):
        from PyQt5.QtWidgets import QFileDialog
        filepath, _ = QFileDialog.getSaveFileName(self, "Зберегти як .txt", "", "Text Files (*.txt)")
        if filepath:
            TxtExporter.export(self.output_textedit, filepath)

    def clear_output(self):
        self.output_textedit.clear()
