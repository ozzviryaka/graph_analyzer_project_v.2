from PyQt5.QtWidgets import QMainWindow, QApplication
from gui.tabs.graph_tabs_widget import GraphTabsWidget
from gui.widgets.graph_settings_widget import GraphSettingsWidget
from core.graph_models.directed_graph import DirectedGraph
from core.graph_models.undirected_graph import UndirectedGraph
# Add theme imports
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyleFactory

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_dark_theme()
        self.setWindowTitle("Граф-аналізатор")
        self.setWindowIcon(QIcon("res/icon.png"))
        self.setMinimumSize(1100, 700)
        # --- Менеджмент графів ---
        self.graphs = []
        g = UndirectedGraph()
        g.name = "Граф 1"
        g.directed = False
        self.graphs.append(g)
        self.graph = g
        # Віджет налаштувань графа (тумблери)
        self.settings_widget = GraphSettingsWidget(self.graph, self.on_graph_changed)
        self.settings_widget.set_graphs_list(self.graphs)
        self.settings_widget.set_graph(self.graph)
        # Додаємо метод для оновлення налаштувань при зміні графа
        # Віджет з вкладками
        self.tabs = GraphTabsWidget(self.graph)
        self.tabs.set_on_graph_changed(self.on_graph_changed)
        # Розміщення: тумблери зверху, вкладки знизу
        from PyQt5.QtWidgets import QWidget, QVBoxLayout
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.settings_widget)
        layout.addWidget(self.tabs)
        central.setLayout(layout)
        self.setCentralWidget(central)
        # Передати список графів у вкладки
        if hasattr(self.tabs.combined_tab.canvas_widget, 'set_graphs_list'):
            self.tabs.combined_tab.canvas_widget.set_graphs_list(self.graphs, self)
        self.settings_widget.auto_vertex_name_switch.toggled.connect(self.on_auto_vertex_name_changed)

    def on_graph_changed(self, new_graph):
        # Якщо новий граф є у списку, зробити його активним
        for i, g in enumerate(self.graphs):
            if g is new_graph:
                self.graph = new_graph
                break
        else:
            # Якщо немає — додати (страховка)
            self.graphs.append(new_graph)
            self.graph = new_graph
        self.tabs.graph = self.graph
        if hasattr(self.tabs, 'combined_tab') and hasattr(self.tabs.combined_tab, 'canvas_widget'):
            self.tabs.combined_tab.canvas_widget.canvas.graph = self.graph
            self.tabs.combined_tab.canvas_widget.canvas._init_node_positions()
            self.tabs.combined_tab.canvas_widget.canvas.update()
        if hasattr(self.tabs.combined_tab.canvas_widget, 'import_export_widget'):
            self.tabs.combined_tab.canvas_widget.import_export_widget.graph = self.graph
        if hasattr(self.settings_widget, 'set_graph'):
            self.settings_widget.set_graph(self.graph)
        if hasattr(self.tabs, 'update_info'):
            self.tabs.update_info(self.graph)
        if hasattr(self.tabs, 'update_matrix'):
            self.tabs.update_matrix(self.graph)
        if hasattr(self.tabs, 'update_nodes'):
            self.tabs.update_nodes()

    def on_auto_vertex_name_changed(self, checked):
        if hasattr(self.tabs.combined_tab.canvas_widget, 'set_auto_vertex_name'):
            self.tabs.combined_tab.canvas_widget.set_auto_vertex_name(checked)

    def set_dark_theme(self):
        app = QApplication.instance()
        app.setStyle(QStyleFactory.create("Fusion"))
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 32, 36))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(24, 26, 30))
        dark_palette.setColor(QPalette.AlternateBase, QColor(36, 38, 43))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(36, 38, 43))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120))
        app.setPalette(dark_palette)
        app.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 13px;
            }
            QMainWindow, QDialog, QMenu, QMenuBar, QToolBar, QTabWidget, QTabBar, QStatusBar {
                background-color: #23252b;
            }
            QPushButton, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton, QGroupBox, QScrollBar, QSlider, QProgressBar, QListWidget, QTreeWidget, QTableWidget, QLabel {
                background-color: #23252b;
                color: #f0f0f0;
                border-radius: 6px;
                border: 1px solid #393b40;
                padding: 4px 8px;
            }
            QPushButton:hover, QComboBox:hover, QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
                background-color: #2d2f36;
                border: 1px solid #4a90e2;
            }
            QPushButton:pressed {
                background-color: #1a1c20;
            }
            QTabBar::tab {
                background: #23252b;
                color: #f0f0f0;
                border: 1px solid #393b40;
                border-bottom: none;
                border-radius: 6px 6px 0 0;
                padding: 8px 20px 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #2d2f36;
                color: #4a90e2;
                border: 1px solid #4a90e2;
                border-bottom: 2px solid #23252b;
            }
            QTabWidget::pane {
                border: 1px solid #393b40;
                border-radius: 0 0 6px 6px;
                top: -1px;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #23252b;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #4a90e2;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                border-radius: 4px;
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background: #4a90e2;
                border: 1px solid #4a90e2;
            }
            QCheckBox::indicator:unchecked, QRadioButton::indicator:unchecked {
                background: #23252b;
                border: 1px solid #393b40;
            }
            QGroupBox {
                border: 1px solid #393b40;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QToolTip {
                background-color: #23252b;
                color: #f0f0f0;
                border: 1px solid #4a90e2;
                border-radius: 6px;
            }
        ''')