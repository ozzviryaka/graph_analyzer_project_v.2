from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFontMetrics
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette

from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge
from gui.dialogs.edge_edit_dialog import EdgeEditDialog
from gui.dialogs.vertex_edit_dialog import VertexEditDialog
from utils.undo_redo_manager import UndoRedoManager
from locales.locale_manager import LocaleManager

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
        self.auto_vertex_name = True  # За замовчуванням автоназва
        self._hovered_node_id = None  # Для локального tooltip
        self.undo_redo_manager = UndoRedoManager()
        # Додаємо кнопки безпосередньо на полотно
        self.undo_btn = QPushButton('↶', self)
        self.redo_btn = QPushButton('↷', self)
        self.undo_btn.setToolTip('Undo (Ctrl+Z)')
        self.redo_btn.setToolTip('Redo (Ctrl+Y)')
        self.undo_btn.setFixedSize(24, 24)
        self.redo_btn.setFixedSize(24, 24)
        self.undo_btn.setToolTip(LocaleManager.get_locale("graph_canvas", "undo_tooltip"))
        self.redo_btn.setToolTip(LocaleManager.get_locale("graph_canvas", "redo_tooltip"))
        self.undo_btn.clicked.connect(lambda: (self.undo_redo_manager.undo(), self.update(), self._update_undo_redo_buttons()))
        self.redo_btn.clicked.connect(lambda: (self.undo_redo_manager.redo(), self.update(), self._update_undo_redo_buttons()))
        self.undo_btn.raise_()
        self.redo_btn.raise_()
        # Викликаємо оновлення кнопок після їх створення
        self._update_undo_redo_buttons()
        self.undo_btn.setStyleSheet('color: #f5f5f5; background: #23232a; border-radius: 6px; border: 1.5px solid #23232a; padding: 0 2px; font-size: 14px; min-width: 0; min-height: 0;')
        self.redo_btn.setStyleSheet('color: #f5f5f5; background: #23232a; border-radius: 6px; border: 1.5px solid #23232a; padding: 0 2px; font-size: 14px; min-width: 0; min-height: 0;')

    def _init_node_positions(self):
        # Якщо у графа вже є node_positions — використовуємо їх
        nodes = list(self.graph.nodes())
        n = len(nodes)
        # Відновлюємо позиції з node.pos, якщо є
        for node in nodes:
            if hasattr(node, 'pos') and node.pos is not None:
                self.node_positions[node.id] = QPointF(*node.pos)
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
                node.set_pos((x, y))

    def set_auto_vertex_name(self, value: bool):
        self.auto_vertex_name = value

    def add_node(self, node_id=None, data=None, pos=None):
        if not self.auto_vertex_name:
            # Відкрити діалог для введення назви
            from gui.dialogs.vertex_edit_dialog import VertexEditDialog
            dlg = VertexEditDialog(data=None, editable_data=False, parent=self)
            dlg.setWindowTitle("Введіть назву вершини")
            if dlg.exec_() == dlg.Accepted:
                node_id = dlg.get_vertex_name()
                data = dlg.get_data()
            else:
                return  # Користувач скасував
        if node_id is None:
            # Якщо граф має next_node_name, використовуємо його для унікального імені
            if hasattr(self.graph, 'next_node_name'):
                node_id = self.graph.next_node_name()
            else:
                # Знаходимо найменший вільний Vn
                used = set()
                for k in self.node_positions:
                    if k.startswith('V') and k[1:].isdigit():
                        used.add(int(k[1:]))
                n = 1
                while n in used:
                    n += 1
                node_id = f"V{n}"
        node = Node(node_id, data, (pos.x(), pos.y()) if pos is not None else None)
        prev_graph_state = self.graph.copy() if hasattr(self.graph, 'copy') else None
        self.graph.add_node(node)
        if pos is not None:
            self.node_positions[node_id] = QPointF(pos)
            node.set_pos((pos.x(), pos.y()))
        else:
            self._init_node_positions()
        self.update_graph_positions()
        self.update()
        if self.on_graph_changed:
            self.on_graph_changed(self.graph)
        def undo():
            self.graph._nodes.pop(node_id, None)
            self.node_positions.pop(node_id, None)
            self.update_graph_positions()
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        def redo():
            self.graph.add_node(node)
            self.node_positions[node_id] = QPointF(pos) if pos is not None else self.node_positions[node_id]
            self.update_graph_positions()
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        self.undo_redo_manager.push(redo, undo)
        self._update_undo_redo_buttons()

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
                        if self.graph.is_weighted():
                            dlg = EdgeEditDialog(weight=None, data=None, editable_weight=True, editable_data=True, parent=self)
                            if dlg.exec_() == dlg.Accepted:
                                weight, data = dlg.get_values()
                                if weight is None:
                                    weight = 1
                                self.add_edge(self.selected_node.id, node_id, weight, data)
                                self.selected_node = None
                                self.update()
                        else:
                            # Для невагового графа одразу додаємо ребро з вагою 1 без діалогу
                            self.add_edge(self.selected_node.id, node_id, 1, None)
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
                    dist = self._distance_point_to_segment(pos, src, tgt)
                    if dist < self.radius:
                        return
            # Якщо клік не по вершині і не по ребру — додаємо нову вершину
            result = self.add_node(pos=pos)
            if result is not None:
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
        super().mouseMoveEvent(event)
        if self._dragging_node_id is not None:
            self.node_positions[self._dragging_node_id] = event.pos() - self._drag_offset
            # Оновлюємо pos у Node
            node = next((n for n in self.graph.nodes() if n.id == self._dragging_node_id), None)
            if node is not None:
                node.set_pos((self.node_positions[self._dragging_node_id].x(), self.node_positions[self._dragging_node_id].y()))
            self.update_graph_positions()
            self.update()

    def mouseReleaseEvent(self, event):
        if self._dragging_node_id is not None:
            self._dragging_node_id = None
            self._drag_offset = QPointF(0, 0)
            self.update()

    def _distance_point_to_segment(self, p, a, b):
        # p, a, b — QPointF
        ap = p - a
        ab = b - a
        ab_len_squared = ab.x() ** 2 + ab.y() ** 2
        if ab_len_squared == 0:
            return (p - a).manhattanLength()
        t = max(0, min(1, (ap.x() * ab.x() + ap.y() * ab.y()) / ab_len_squared))
        proj = a + ab * t
        return (p - proj).manhattanLength()

    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        # Редагування ваги/даних ребра по дабл-кліку по будь-якій частині ребра
        for edge in self.graph.edges():
            src = self.node_positions.get(edge.source.id)
            tgt = self.node_positions.get(edge.target.id)
            if src and tgt:
                dist = self._distance_point_to_segment(pos, src, tgt)
                if dist < self.radius:
                    dlg = EdgeEditDialog(weight=edge.weight(self.graph.is_weighted()), data=edge.data if isinstance(edge.data, dict) else None, editable_weight=self.graph.is_weighted(), editable_data=True, parent=self)
                    if dlg.exec_() == dlg.Accepted:
                        weight, data = dlg.get_values()
                        if self.graph.is_weighted() and weight is not None:
                            self.edit_edge_weight(edge.source.id, edge.target.id, weight)
                        if data:
                            edge.data = data
                        self.update()
                    return
        # Дабл-клік по вершині — редагування даних вершини
        for node_id, node_pos in self.node_positions.items():
            if (pos - node_pos).manhattanLength() < self.radius:
                node = next((n for n in self.graph.nodes() if n.id == node_id), None)
                if node is not None:
                    dlg = VertexEditDialog(data=node.data if isinstance(node.data, dict) else None, editable_data=True, parent=self, node_id=node.id)
                    if dlg.exec_() == dlg.Accepted:
                        data = dlg.get_data()
                        if data:
                            node.data = data
                            self.update()
                return

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.palette().color(self.backgroundRole()))  # Use palette background
        # Draw a visible border around the canvas using theme color
        border_color = self.palette().color(QPalette.Highlight)
        border_pen = QPen(border_color, 2)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.rect().adjusted(1, 1, -2, -2))
        painter.setRenderHint(QPainter.Antialiasing)
        if not list(self.graph.nodes()):
            painter.setPen(self.palette().color(QPalette.Highlight))
            painter.setFont(self.font())
            # text = (
            #     "\u2139  Інструкція: створення та редагування графа\n"
            #     "\n"
            #     "- Додати вершину: ЛКМ по порожньому місцю\n"
            #     "- Видалити вершину: ПКМ по вершині\n"
            #     "- Додати ребро: виділіть вершину, потім ЛКМ+Ctrl по іншій вершині\n"
            #     "- Видалити ребро: ПКМ по середині ребра\n"
            #     "- Редагувати вагу ребра: подвійний ЛКМ по середині ребра\n"
            #     "- Переміщення вершини: ЛКМ по вершині та тягнути мишею\n"
            #     "- Зміна орієнтованості/ваговості: тумблери над полотном\n"
            #     "\n"
            #     "Почніть з додавання вершин!"
            # )
            # rect = self.rect().adjusted(40, 40, -40, -40)
            # painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, text)
            return
        # Draw edges
        for edge in self.graph.edges():
            src = self.node_positions.get(edge.source.id)
            tgt = self.node_positions.get(edge.target.id)
            if src and tgt:
                pen = QPen(self.palette().color(QPalette.Mid), 2)
                if edge == self.selected_edge:
                    pen.setColor(self.palette().color(QPalette.BrightText))
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
                if self.graph.is_weighted():
                    mid = (src + tgt) / 2
                    painter.setPen(QColor(180, 180, 255))
                    painter.drawText(mid + QPointF(0, -8), str(edge.weight(self.graph.is_weighted())))
        # Draw nodes
        for node in self.graph.nodes():
            pos = self.node_positions.get(node.id)
            if not pos:
                continue
            node_color = self.palette().color(QPalette.Button)
            brush = QBrush(node_color)
            if node == self.selected_node:
                pen = QPen(self.palette().color(QPalette.BrightText), 3)
                pen.setStyle(Qt.DashLine)
            else:
                pen = QPen(self.palette().color(QPalette.Mid), 2)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawEllipse(pos, self.radius, self.radius)
            painter.setPen(self.palette().color(QPalette.ButtonText))
            # Центрований текст у межах вершини, автоматичне зменшення розміру шрифту
            text_rect = QRectF(pos.x() - self.radius + 2, pos.y() - self.radius + 2, 2 * self.radius - 4, 2 * self.radius - 4)
            text = str(node.id)
            font = painter.font()
            max_width = int(2 * self.radius - 8)
            max_height = int(2 * self.radius - 8)
            min_point_size = 6
            point_size = font.pointSize()
            # Зменшуємо розмір шрифту, поки текст не влізе по ширині і висоті, але не менше мінімального
            while point_size > min_point_size:
                font.setPointSize(point_size)
                metrics = QFontMetrics(font)
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()
                if text_width <= max_width and text_height <= max_height:
                    break
                point_size -= 1
            if point_size < min_point_size:
                point_size = min_point_size
                font.setPointSize(point_size)
            painter.setFont(font)
            # Якщо навіть мінімальний шрифт не допомагає — обрізаємо текст з крапками
            metrics = QFontMetrics(font)
            elided = metrics.elidedText(text, Qt.ElideRight, max_width)
            painter.drawText(text_rect, Qt.AlignCenter, elided)
            # self.setToolTip(f"{node.id}")  # Видалено, щоб не було глобальної підказки

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
        def undo():
            self.graph._edges = [e for e in self.graph._edges if not ((e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id))]
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        def redo():
            if hasattr(self.graph, 'is_directed') and self.graph.is_directed():
                edge = DirectedEdge(src, tgt, weight, data)
            else:
                edge = UndirectedEdge(src, tgt, weight, data)
            self.graph.add_edge(edge)
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        self.undo_redo_manager.push(redo, undo)
        self._update_undo_redo_buttons()

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
                        if self.graph.is_weighted():
                            dlg = EdgeEditDialog(weight=None, data=None, editable_weight=True, editable_data=True, parent=self)
                            if dlg.exec_() == dlg.Accepted:
                                weight, data = dlg.get_values()
                                if weight is None:
                                    weight = 1
                                self.add_edge(self.selected_node.id, node_id, weight, data)
                                self.selected_node = None
                                self.update()
                        else:
                            # Для невагового графа одразу додаємо ребро з вагою 1 без діалогу
                            self.add_edge(self.selected_node.id, node_id, 1, None)
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
                    dist = self._distance_point_to_segment(pos, src, tgt)
                    if dist < self.radius:
                        return
            # Якщо клік не по вершині і не по ребру — додаємо нову вершину
            result = self.add_node(pos=pos)
            if result is not None:
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
        super().mouseMoveEvent(event)
        if self._dragging_node_id is not None:
            self.node_positions[self._dragging_node_id] = event.pos() - self._drag_offset
            # Оновлюємо pos у Node
            node = next((n for n in self.graph.nodes() if n.id == self._dragging_node_id), None)
            if node is not None:
                node.set_pos((self.node_positions[self._dragging_node_id].x(), self.node_positions[self._dragging_node_id].y()))
            self.update_graph_positions()
            self.update()

    def mouseReleaseEvent(self, event):
        if self._dragging_node_id is not None:
            self._dragging_node_id = None
            self._drag_offset = QPointF(0, 0)
            self.update()

    def _distance_point_to_segment(self, p, a, b):
        # p, a, b — QPointF
        ap = p - a
        ab = b - a
        ab_len_squared = ab.x() ** 2 + ab.y() ** 2
        if ab_len_squared == 0:
            return (p - a).manhattanLength()
        t = max(0, min(1, (ap.x() * ab.x() + ap.y() * ab.y()) / ab_len_squared))
        proj = a + ab * t
        return (p - proj).manhattanLength()

    def mouseDoubleClickEvent(self, event):
        pos = event.pos()
        # Редагування ваги/даних ребра по дабл-кліку по будь-якій частині ребра
        for edge in self.graph.edges():
            src = self.node_positions.get(edge.source.id)
            tgt = self.node_positions.get(edge.target.id)
            if src and tgt:
                dist = self._distance_point_to_segment(pos, src, tgt)
                if dist < self.radius:
                    dlg = EdgeEditDialog(weight=edge.weight(self.graph.is_weighted()), data=edge.data if isinstance(edge.data, dict) else None, editable_weight=self.graph.is_weighted(), editable_data=True, parent=self)
                    if dlg.exec_() == dlg.Accepted:
                        weight, data = dlg.get_values()
                        if self.graph.is_weighted() and weight is not None:
                            self.edit_edge_weight(edge.source.id, edge.target.id, weight)
                        if data:
                            edge.data = data
                        self.update()
                    return
        # Дабл-клік по вершині — редагування даних вершини
        for node_id, node_pos in self.node_positions.items():
            if (pos - node_pos).manhattanLength() < self.radius:
                node = next((n for n in self.graph.nodes() if n.id == node_id), None)
                if node is not None:
                    dlg = VertexEditDialog(data=node.data if isinstance(node.data, dict) else None, editable_data=True, parent=self, node_id=node.id)
                    if dlg.exec_() == dlg.Accepted:
                        data = dlg.get_data()
                        if data:
                            node.data = data
                            self.update()
                return

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.palette().color(self.backgroundRole()))  # Use palette background
        # Draw a visible border around the canvas using theme color
        border_color = self.palette().color(QPalette.Highlight)
        border_pen = QPen(border_color, 2)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.rect().adjusted(1, 1, -2, -2))
        painter.setRenderHint(QPainter.Antialiasing)
        if not list(self.graph.nodes()):
            painter.setPen(self.palette().color(QPalette.Highlight))
            painter.setFont(self.font())
            # text = (
            #     "\u2139  Інструкція: створення та редагування графа\n"
            #     "\n"
            #     "- Додати вершину: ЛКМ по порожньому місцю\n"
            #     "- Видалити вершину: ПКМ по вершині\n"
            #     "- Додати ребро: виділіть вершину, потім ЛКМ+Ctrl по іншій вершині\n"
            #     "- Видалити ребро: ПКМ по середині ребра\n"
            #     "- Редагувати вагу ребра: подвійний ЛКМ по середині ребра\n"
            #     "- Переміщення вершини: ЛКМ по вершині та тягнути мишею\n"
            #     "- Зміна орієнтованості/ваговості: тумблери над полотном\n"
            #     "\n"
            #     "Почніть з додавання вершин!"
            # )
            # rect = self.rect().adjusted(40, 40, -40, -40)
            # painter.drawText(rect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, text)
            return
        # Draw edges
        for edge in self.graph.edges():
            src = self.node_positions.get(edge.source.id)
            tgt = self.node_positions.get(edge.target.id)
            if src and tgt:
                pen = QPen(self.palette().color(QPalette.Mid), 2)
                if edge == self.selected_edge:
                    pen.setColor(self.palette().color(QPalette.BrightText))
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
                if self.graph.is_weighted():
                    mid = (src + tgt) / 2
                    painter.setPen(QColor(180, 180, 255))
                    painter.drawText(mid + QPointF(0, -8), str(edge.weight(self.graph.is_weighted())))
        # Draw nodes
        for node in self.graph.nodes():
            pos = self.node_positions.get(node.id)
            if not pos:
                continue
            node_color = self.palette().color(QPalette.Button)
            brush = QBrush(node_color)
            if node == self.selected_node:
                pen = QPen(self.palette().color(QPalette.BrightText), 3)
                pen.setStyle(Qt.DashLine)
            else:
                pen = QPen(self.palette().color(QPalette.Mid), 2)
            painter.setBrush(brush)
            painter.setPen(pen)
            painter.drawEllipse(pos, self.radius, self.radius)
            painter.setPen(self.palette().color(QPalette.ButtonText))
            # Центрований текст у межах вершини, автоматичне зменшення розміру шрифту
            text_rect = QRectF(pos.x() - self.radius + 2, pos.y() - self.radius + 2, 2 * self.radius - 4, 2 * self.radius - 4)
            text = str(node.id)
            font = painter.font()
            max_width = int(2 * self.radius - 8)
            max_height = int(2 * self.radius - 8)
            min_point_size = 6
            point_size = font.pointSize()
            # Зменшуємо розмір шрифту, поки текст не влізе по ширині і висоті, але не менше мінімального
            while point_size > min_point_size:
                font.setPointSize(point_size)
                metrics = QFontMetrics(font)
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()
                if text_width <= max_width and text_height <= max_height:
                    break
                point_size -= 1
            if point_size < min_point_size:
                point_size = min_point_size
                font.setPointSize(point_size)
            painter.setFont(font)
            # Якщо навіть мінімальний шрифт не допомагає — обрізаємо текст з крапками
            metrics = QFontMetrics(font)
            elided = metrics.elidedText(text, Qt.ElideRight, max_width)
            painter.drawText(text_rect, Qt.AlignCenter, elided)
            # self.setToolTip(f"{node.id}")  # Видалено, щоб не було глобальної підказки

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
        def undo():
            self.graph._edges = [e for e in self.graph._edges if not ((e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id))]
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        def redo():
            if hasattr(self.graph, 'is_directed') and self.graph.is_directed():
                edge = DirectedEdge(src, tgt, weight, data)
            else:
                edge = UndirectedEdge(src, tgt, weight, data)
            self.graph.add_edge(edge)
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        self.undo_redo_manager.push(redo, undo)
        self._update_undo_redo_buttons()

    def remove_node(self, node_id):
        # Видалення вузла (та всіх інцидентних ребер)
        import copy
        node = next((n for n in self.graph.nodes() if n.id == node_id), None)
        if node is not None:
            node_copy = copy.deepcopy(node)
            edges_copy = [copy.deepcopy(e) for e in self.graph.edges() if e.source.id == node_id or e.target.id == node_id]
        else:
            node_copy = None
            edges_copy = []
        if hasattr(self.graph, '_nodes') and node_id in self.graph._nodes:
            del self.graph._nodes[node_id]
            if hasattr(self.graph, '_adjacency'):
                self.graph._adjacency.pop(node_id, None)
                for adj in self.graph._adjacency.values():
                    adj.discard(node_id)
            # Видалити ребра
            if hasattr(self.graph, '_edges'):
                self.graph._edges = [e for e in self.graph._edges if e.source.id != node_id and e.target.id != node_id]
            self.node_positions.pop(node_id, None)
            # Видаляємо pos у Node
            if node is not None:
                node.set_pos(None)
            self.update_graph_positions()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        def undo():
            if node_copy is not None:
                self.graph.add_node(node_copy)
                if hasattr(self.graph, '_adjacency'):
                    for n_id in self.graph._nodes:
                        if n_id not in self.graph._adjacency:
                            self.graph._adjacency[n_id] = set()
                self.node_positions[node_id] = QPointF(*node_copy.pos) if hasattr(node_copy, 'pos') and node_copy.pos else QPointF(0,0)
                self.update_graph_positions()
                for e in edges_copy:
                    if e.source.id in self.graph._nodes and e.target.id in self.graph._nodes:
                        if e not in self.graph.edges():
                            self.graph.add_edge(e)
                        if hasattr(self.graph, '_adjacency'):
                            self.graph._adjacency.setdefault(e.source.id, set()).add(e.target.id)
                            self.graph._adjacency.setdefault(e.target.id, set()).add(e.source.id)
                self.sanitize_adjacency()
                self.update()
                if self.on_graph_changed:
                    self.on_graph_changed(self.graph)
        def redo():
            if hasattr(self.graph, '_nodes') and node_id in self.graph._nodes:
                del self.graph._nodes[node_id]
                if hasattr(self.graph, '_adjacency'):
                    self.graph._adjacency.pop(node_id, None)
                    for adj in self.graph._adjacency.values():
                        adj.discard(node_id)
                if hasattr(self.graph, '_edges'):
                    self.graph._edges = [e for e in self.graph._edges if e.source.id != node_id and e.target.id != node_id]
                self.node_positions.pop(node_id, None)
                self.update_graph_positions()
                self.sanitize_adjacency()
                self.update()
                if self.on_graph_changed:
                    self.on_graph_changed(self.graph)
        self.undo_redo_manager.push(undo, redo)
        self._update_undo_redo_buttons()

    def remove_edge(self, source_id, target_id):
        # Видаляє ребро між source_id і target_id
        if hasattr(self.graph, '_edges'):
            self.graph._edges = [e for e in self.graph._edges if not ((e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id))]
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        edge = next((e for e in self.graph.edges() if (e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id)), None)
        import copy
        edge_copy = copy.deepcopy(edge) if edge else None
        def undo():
            if edge_copy:
                self.graph.add_edge(edge_copy)
                self.sanitize_adjacency()
                self.update()
                if self.on_graph_changed:
                    self.on_graph_changed(self.graph)
        def redo():
            self.graph._edges = [e for e in self.graph._edges if not ((e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id))]
            self.sanitize_adjacency()
            self.update()
            if self.on_graph_changed:
                self.on_graph_changed(self.graph)
        self.undo_redo_manager.push(redo, undo)
        self._update_undo_redo_buttons()

    def edit_edge_weight(self, source_id, target_id, new_weight):
        # Редагує вагу ребра
        for edge in self.graph.edges():
            if (edge.source.id == source_id and edge.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (edge.source.id == target_id and edge.target.id == source_id):
                edge._weight = new_weight
        self.update()
        if self.on_graph_changed:
            self.on_graph_changed(self.graph)
        edge = next((e for e in self.graph.edges() if (e.source.id == source_id and e.target.id == target_id) or (not hasattr(self.graph, 'is_directed') or not self.graph.is_directed()) and (e.source.id == target_id and e.target.id == source_id)), None)
        old_weight = edge._weight if edge else None
        def undo():
            if edge:
                edge._weight = old_weight
                self.sanitize_adjacency()
                self.update()
                if self.on_graph_changed:
                    self.on_graph_changed(self.graph)
        def redo():
            if edge:
                edge._weight = new_weight
                self.sanitize_adjacency()
                self.update()
                if self.on_graph_changed:
                    self.on_graph_changed(self.graph)
        self.undo_redo_manager.push(redo, undo)
        self._update_undo_redo_buttons()

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

    def update_graph_positions(self):
        # Зберігає позиції вершин у node.pos
        for node_id, pos in self.node_positions.items():
            node = next((n for n in self.graph.nodes() if n.id == node_id), None)
            if node is not None:
                node.set_pos((pos.x(), pos.y()))

    def sanitize_adjacency(self):
        if hasattr(self.graph, '_adjacency'):
            for n_id, neighbors in self.graph._adjacency.items():
                self.graph._adjacency[n_id] = {x for x in neighbors if x in self.graph._nodes}

    def _update_undo_redo_buttons(self):
        if hasattr(self, 'undo_btn') and hasattr(self, 'redo_btn'):
            self.undo_btn.setEnabled(self.undo_redo_manager.can_undo())
            self.redo_btn.setEnabled(self.undo_redo_manager.can_redo())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Розміщуємо кнопки у правому верхньому куті
        margin = 8
        self.undo_btn.move(self.width() - 2*24 - margin*2, margin)
        self.redo_btn.move(self.width() - 24 - margin, margin)
        self.undo_btn.show()
        self.redo_btn.show()