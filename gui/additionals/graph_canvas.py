from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF

from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge

import math

class GraphCanvas(QWidget):
    """
    Віджет для візуалізації та редагування графа (підтримує DirectedGraph, UndirectedGraph тощо).
    """
    def __init__(self, graph, parent=None, on_graph_changed=None):
        super().__init__(parent)
        self.graph = graph
        self.node_positions = {}  # id: QPointF
        self.selected_node = None
        self.selected_edge = None
        self.radius = 20
        self.setMinimumSize(600, 400)
        self._init_node_positions()
        self.setMouseTracking(True)
        self.node_counter = 1  # Лічильник для автоматичних ID
        self._dragging_node_id = None
        self._drag_offset = QPointF(0, 0)
        self.on_graph_changed = on_graph_changed

    def _init_node_positions(self):
        # Розташування вершин по колу лише для ініціалізації, не для додавання нових
        nodes = list(self.graph.nodes())
        n = len(nodes)
        # Якщо вже є позиції для всіх вершин — нічого не робимо
        if n == len(self.node_positions):
            return
        cx, cy, r = 300, 200, 150
        for i, node in enumerate(nodes):
            if node.id not in self.node_positions:
                angle = 2 * math.pi * i / n
                x = cx + r * math.cos(angle)
                y = cy + r * math.sin(angle)
                self.node_positions[node.id] = QPointF(x, y)

    def add_node(self, node_id=None, data=None, pos=None):
        if node_id is None:
            # Знаходимо найменший вільний Vn
            used = set()
            for k in self.node_positions:
                if k.startswith('V') and k[1:].isdigit():
                    used.add(int(k[1:]))
            n = 1
            while n in used:
                n += 1
            node_id = f"V{n}"
        node = Node(node_id, data)
        self.graph.add_node(node)
        if pos is not None:
            self.node_positions[node_id] = QPointF(pos)
        # Не викликаємо _init_node_positions() при додаванні вершини з pos
        else:
            # Якщо це ініціалізація (додавання всіх вершин), тоді розташовуємо по колу
            self._init_node_positions()
        self.update()
        if self.on_graph_changed:
            self.on_graph_changed(self.graph)

    def mousePressEvent(self, event):
        pos = event.pos()
        self._mouse_press_pos = pos
        self._mouse_press_node_id = None
        if event.button() == Qt.LeftButton:
            for node_id, node_pos in self.node_positions.items():
                if (pos - node_pos).manhattanLength() < self.radius:
                    self._mouse_press_node_id = node_id
                    # Додавання ребра — тільки якщо є selected_node, клік по іншій вершині і натиснуто Ctrl
                    if (self.selected_node and self.selected_node.id != node_id and (event.modifiers() & Qt.ControlModifier)):
                        weight = 1
                        if self.graph.is_weighted():
                            w, ok = QInputDialog.getInt(self, "Вага ребра", f"Введіть вагу ребра {self.selected_node.id} → {node_id}", 1, 1, 10000)
                            if ok:
                                weight = w
                            else:
                                return
                        self.add_edge(self.selected_node.id, node_id, weight)
                        self.selected_node = None
                        self.update()
                        return
                    # Drag дозволяється завжди по будь-якій вершині
                    self.selected_node = next((n for n in self.graph.nodes() if n.id == node_id), None)
                    self.selected_edge = None
                    self._dragging_node_id = node_id
                    self._drag_offset = pos - self.node_positions[node_id]
                    self.update()
                    return
            # Якщо клік по ребру — нічого не робимо (для doubleClick)
            for edge in self.graph.edges():
                src = self.node_positions.get(edge.source.id)
                tgt = self.node_positions.get(edge.target.id)
                if src and tgt:
                    mid = (src + tgt) / 2
                    if (pos - mid).manhattanLength() < self.radius:
                        return
            # Якщо клік не по вершині і не по ребру — додаємо нову вершину
            self.add_node(pos=pos)
            last_id = max(self.node_positions, key=lambda k: int(k[1:]) if k.startswith('V') and k[1:].isdigit() else -1)
            self.selected_node = next((n for n in self.graph.nodes() if n.id == last_id), None)
            self.update()
        elif event.button() == Qt.RightButton:
            # Видалення вершини або ребра
            for node_id, node_pos in self.node_positions.items():
                if (pos - node_pos).manhattanLength() < self.radius:
                    self.remove_node(node_id)
                    self.selected_node = None
                    self.update()
                    return
            for edge in self.graph.edges():
                src = self.node_positions.get(edge.source.id)
                tgt = self.node_positions.get(edge.target.id)
                if src and tgt:
                    mid = (src + tgt) / 2
                    if (pos - mid).manhattanLength() < self.radius:
                        self.remove_edge(edge.source.id, edge.target.id)
                        self.selected_edge = None
                        self.update()
                        return
        self.selected_node = None
        self.selected_edge = None
        self.update()

    def mouseMoveEvent(self, event):
        if self._dragging_node_id is not None:
            self.node_positions[self._dragging_node_id] = event.pos() - self._drag_offset
            self.update()

    def mouseReleaseEvent(self, event):
        if self._dragging_node_id is not None:
            self._dragging_node_id = None
            self._drag_offset = QPointF(0, 0)
            self.update()

    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        # Редагування ваги ребра по дабл-кліку по середині ребра
        for edge in self.graph.edges():
            src = self.node_positions.get(edge.source.id)
            tgt = self.node_positions.get(edge.target.id)
            if src and tgt:
                mid = (src + tgt) / 2
                if (pos - mid).manhattanLength() < self.radius:
                    if self.graph.is_weighted():
                        w, ok = QInputDialog.getInt(self, "Редагувати вагу", f"Нова вага ребра {edge.source.id} → {edge.target.id}", edge.weight(self.graph.is_weighted()), 1, 10000)
                        if ok:
                            self.edit_edge_weight(edge.source.id, edge.target.id, w)
                    return

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 32, 36))  # Dark background
        painter.setRenderHint(QPainter.Antialiasing)
        if not list(self.graph.nodes()):
            painter.setPen(QColor(120, 160, 255))
            painter.setFont(self.font())
            text = (
                "\u2139  Інструкція: створення та редагування графа\n"
                "\n"
                "- Додати вершину: ЛКМ по порожньому місцю\n"
                "- Видалити вершину: ПКМ по вершині\n"
                "- Додати ребро: виділіть вершину, потім ЛКМ+Ctrl по іншій вершині\n"
                "- Видалити ребро: ПКМ по середині ребра\n"
                "- Редагувати вагу ребра: подвійний ЛКМ по середині ребра\n"
                "- Переміщення вершини: ЛКМ по вершині та тягнути мишею\n"
                "- Зміна орієнтованості/ваговості: тумблери над полотном\n"
                "\n"
                "Почніть з додавання вершин!"
            )
            rect = self.rect().adjusted(40, 40, -40, -40)
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, text)
            return
        # Draw edges
        for edge in self.graph.edges():
            src = self.node_positions.get(edge.source.id)
            tgt = self.node_positions.get(edge.target.id)
            if src and tgt:
                pen = QPen(QColor(80, 80, 120), 2)
                if edge == self.selected_edge:
                    pen.setColor(QColor(255, 85, 85))
                painter.setPen(pen)
                # Якщо граф орієнтований — малюємо стрілку
                is_directed = hasattr(self.graph, 'is_directed') and self.graph.is_directed()
                if is_directed:
                    # Відступаємо від центру вершини на радіус
                    dx = tgt.x() - src.x()
                    dy = tgt.y() - src.y()
                    length = math.hypot(dx, dy)
                    if length == 0:
                        continue
                    offset_x = self.radius * dx / length
                    offset_y = self.radius * dy / length
                    start = QPointF(src.x() + offset_x, src.y() + offset_y)
                    end = QPointF(tgt.x() - offset_x, tgt.y() - offset_y)
                    painter.drawLine(start, end)
                    # Малюємо стрілку
                    arrow_size = 14
                    angle = math.atan2(dy, dx)
                    p1 = QPointF(
                        end.x() - arrow_size * math.cos(angle - math.pi / 7),
                        end.y() - arrow_size * math.sin(angle - math.pi / 7)
                    )
                    p2 = QPointF(
                        end.x() - arrow_size * math.cos(angle + math.pi / 7),
                        end.y() - arrow_size * math.sin(angle + math.pi / 7)
                    )
                    arrow_head = [end, p1, p2]
                    painter.setBrush(QColor(80, 80, 120))
                    painter.drawPolygon(*arrow_head)
                else:
                    painter.drawLine(src, tgt)
                # Draw weight
                mid = (src + tgt) / 2
                painter.setPen(QColor(180, 180, 255))
                painter.drawText(mid + QPointF(0, -8), str(edge.weight(self.graph.is_weighted())))
        # Draw nodes
        for node in self.graph.nodes():
            pos = self.node_positions.get(node.id)
            if not pos:
                continue
            brush = QBrush(QColor(44, 47, 51))  # Завжди один колір
            if node == self.selected_node:
                pen = QPen(QColor(255, 0, 0), 3)
                pen.setStyle(Qt.DashLine)  # Червона штрихована лінія
            else:
                pen = QPen(QColor(120, 120, 160), 2)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawEllipse(pos, self.radius, self.radius)
            painter.setPen(QColor(220, 220, 220))
            painter.drawText(pos + QPointF(-8, 5), str(node.id))

    def add_edge(self, source_id, target_id, weight=1, data=None):
        # Додає ребро відповідного типу
        src = next((n for n in self.graph.nodes() if n.id == source_id), None)
        tgt = next((n for n in self.graph.nodes() if n.id == target_id), None)
        if not src or not tgt:
            return
        if hasattr(self.graph, 'is_directed') and self.graph.is_directed():
            edge = DirectedEdge(src, tgt, weight, data)
        else:
            edge = UndirectedEdge(src, tgt, weight, data)
        self.graph.add_edge(edge)
        self.update()
        if self.on_graph_changed:
            self.on_graph_changed(self.graph)

    def remove_node(self, node_id):
        # Видалення вузла (та всіх інцидентних ребер)
        if hasattr(self.graph, '_nodes') and node_id in self.graph._nodes:
            del self.graph._nodes[node_id]
            if hasattr(self.graph, '_adjacency'):
                self.graph._adjacency.pop(node_id, None)
                for adj in self.graph._adjacency.values():
                    adj.discard(node_id)
            # Видалити ребра
            if hasattr(self.graph, '_edges'):
                self.graph._edges = set(e for e in self.graph._edges if e.source.id != node_id and e.target.id != node_id)
            self.node_positions.pop(node_id, None)
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)

    def remove_edge(self, source_id, target_id):
        # Видаляє ребро між source_id і target_id
        if hasattr(self.graph, '_edges'):
            self.graph._edges = set(e for e in self.graph._edges if not ((e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id)))
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)

    def edit_edge_weight(self, source_id, target_id, new_weight):
        # Редагує вагу ребра
        for edge in self.graph.edges():
            if (edge.source.id == source_id and edge.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (edge.source.id == target_id and edge.target.id == source_id):
                edge._weight = new_weight
        self.update()
        if self.on_graph_changed:
            self.on_graph_changed(self.graph)

    def show_instruction(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Інструкція")
        msg.setText(
            """
            Інструкція з використання графового полотна:
            - Клік по вершині: вибір вершини
            - Додавання вершини: add_node(node_id)
            - Видалення вершини: remove_node(node_id)
            - Додавання ребра: add_edge(source_id, target_id, weight)
            - Видалення ребра: remove_edge(source_id, target_id)
            - Редагування ваги ребра: edit_edge_weight(source_id, target_id, new_weight)
            - Відображення графа: автоматично
            """
        )
        msg.exec_()

    def clear_graph(self):
        """
        Очищає граф: видаляє всі вершини, ребра та позиції.
        """
        if hasattr(self.graph, '_nodes'):
            self.graph._nodes.clear()
        if hasattr(self.graph, '_edges'):
            self.graph._edges.clear()
        if hasattr(self.graph, '_adjacency'):
            self.graph._adjacency.clear()
        self.node_positions.clear()
        self.selected_node = None
        self.selected_edge = None
        self.update()
        if self.on_graph_changed:
            self.on_graph_changed(self.graph)