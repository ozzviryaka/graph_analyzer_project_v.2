from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from data_utils.graph_saver import GraphSaver
from data_utils.graph_loader import GraphLoader
from locales.locale_manager import LocaleManager

class GraphImportExportWidget(QWidget):
    """
    Віджет з двома кнопками для експорту та імпорту графа у .json
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.export_btn = QPushButton(LocaleManager.get_locale("graph_import_export_widget", "export_json_button"))
        self.export_btn.setCursor(Qt.PointingHandCursor)
        # self.export_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")  # REMOVE custom style
        self.export_btn.clicked.connect(self.export_graph)

        self.import_btn = QPushButton(LocaleManager.get_locale("graph_import_export_widget", "import_json_button"))
        self.import_btn.setCursor(Qt.PointingHandCursor)
        # self.import_btn.setStyleSheet("background-color: #444; color: #fff; border-radius: 6px; padding: 6px; font-size: 14px;")  # REMOVE custom style
        self.import_btn.clicked.connect(self.import_graph)

        layout = QVBoxLayout()
        layout.addWidget(self.export_btn)
        layout.addWidget(self.import_btn)
        self.setLayout(layout)

    def export_graph(self):
        filepath, _ = QFileDialog.getSaveFileName(self, LocaleManager.get_locale("graph_import_export_widget", "save_graph_dialog_title"), "", "JSON Files (*.json)")
        if filepath:
            GraphSaver.save(self.graph, filepath)

    def import_graph(self):
        filepath, _ = QFileDialog.getOpenFileName(self, LocaleManager.get_locale("graph_import_export_widget", "open_graph_dialog_title"), "", "JSON Files (*.json)")
        if filepath:
            new_graph = GraphLoader.load(filepath)
            if new_graph:
                self.graph.__dict__.update(new_graph.__dict__)

    def set_graph(self, graph):
        self.graph = graph

    def refresh_ui_text(self):
        """Оновлює текст інтерфейсу після зміни мови"""
        self.export_btn.setText(LocaleManager.get_locale("graph_import_export_widget", "export_json_button"))
        self.import_btn.setText(LocaleManager.get_locale("graph_import_export_widget", "import_json_button"))
