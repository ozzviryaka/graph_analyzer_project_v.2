from gui.additionals.graph_canvas import GraphCanvas
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFontMetrics
from PyQt5.QtCore import QRectF, Qt

class ReadOnlyGraphCanvas(GraphCanvas):
    """
    Віджет для перегляду графа без можливості редагування та без додаткових кнопок.
    """
    def __init__(self, graph, parent=None):
        super().__init__(graph, parent)
        # Додаємо кнопки Undo/Redo на саме полотно
        self.undo_btn = QPushButton('↶', self)
        self.redo_btn = QPushButton('↷', self)
        self.undo_btn.setToolTip('Undo (Ctrl+Z)')
        self.redo_btn.setToolTip('Redo (Ctrl+Y)')
        self.undo_btn.setFixedSize(28, 28)
        self.redo_btn.setFixedSize(28, 28)
        self.undo_btn.show()
        self.redo_btn.show()
        self._highlighted_nodes = set()  # Множина id вершин для підсвічування
        self._node_numbers = dict()      # id вершини -> номер

    def set_highlighted_nodes(self, node_ids):
        self._highlighted_nodes = set(node_ids)
        self.update()

    def set_node_numbers(self, node_number_map):
        """
        node_number_map: dict {node_id: number}
        """
        self._node_numbers = dict(node_number_map)
        self.update()

    def mousePressEvent(self, event):
        # Забороняємо будь-які зміни
        pass

    def mouseMoveEvent(self, event):
        # Дозволяємо лише підсвічування (tooltip)
        pos = event.pos()
        hovered = None
        for node_id, node_pos in self.node_positions.items():
            if (pos - node_pos).manhattanLength() < self.radius:
                hovered = node_id
                break
        if hovered != self._hovered_node_id:
            self._hovered_node_id = hovered
            if hovered is not None:
                self.setToolTip(str(hovered))
            else:
                self.setToolTip("")
        # Не викликаємо super(QWidget, self).mouseMoveEvent(event), бо це некоректно
        # Якщо потрібно, можна викликати super().mouseMoveEvent(event) для GraphCanvas
        # super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        pass

    def add_node(self, *args, **kwargs):
        pass

    def add_edge(self, *args, **kwargs):
        pass

    def remove_node(self, *args, **kwargs):
        pass

    def remove_edge(self, *args, **kwargs):
        pass

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for node in self.graph.nodes():
            pos = self.node_positions.get(node.id)
            if not pos:
                continue
            # Підсвічування
            if node.id in getattr(self, '_highlighted_nodes', set()):
                highlight_pen = QPen(QColor(255, 140, 0), 4)
                painter.setPen(highlight_pen)
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(pos, self.radius + 4, self.radius + 4)
            # Номер біля вершини
            if node.id in getattr(self, '_node_numbers', {}):
                number = self._node_numbers[node.id]
                font = painter.font()
                font.setPointSize(max(8, font.pointSize() - 1))
                painter.setFont(font)
                painter.setPen(QColor(0, 120, 255))
                metrics = QFontMetrics(font)
                text = str(number)
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()
                # Малюємо номер справа вгорі від вершини
                offset_x = self.radius + 8
                offset_y = -self.radius // 2
                painter.drawText(pos.x() + offset_x, pos.y() + offset_y + text_height // 2, text)

    def set_undo_redo_callbacks(self, undo_callback, redo_callback):
        self.undo_btn.clicked.connect(undo_callback)
        self.redo_btn.clicked.connect(redo_callback)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Переміщуємо кнопки при зміні розміру
        margin = 10
        btn_space = 8
        w = self.width()
        self.undo_btn.move(w - self.undo_btn.width() * 2 - btn_space - margin, margin)
        self.redo_btn.move(w - self.redo_btn.width() - margin, margin)
