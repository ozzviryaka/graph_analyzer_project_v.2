from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from gui.widgets.traversal_tab_widgets.traversal_control_widget import TraversalControlWidget
from core.algorithms.traversal.traversal_algorithms import GraphTraversal
from PyQt5.QtCore import QTimer

class TraversalTab(QWidget):
    """
    Вкладка для покрокового обходу графа з вибором алгоритму.
    """
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self.graph = graph
        self.traversal_widget = TraversalControlWidget(graph, self)
        self.traversal_widget.start_btn.clicked.connect(self.start_traversal)
        self.traversal_widget.stop_btn.clicked.connect(self.stop_traversal)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_step)
        self.traversal_order = []
        self.current_step = 0
        self.is_running = False
        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.traversal_widget)
        layout.addWidget(self.text_output)
        self.setLayout(layout)

        # Не створюємо додаткові кнопки undo/redo у вкладці, використовуємо лише ті, що на полотні
        self.history = []
        self.future = []
        self.traversal_widget.canvas.set_undo_redo_callbacks(self.undo_step, self.redo_step)

    def set_status(self, text):
        pass  # status_label видалено, нічого не робимо

    def start_traversal(self):
        method = self.traversal_widget.method_combo.currentText()
        nodes_iter = list(self.graph.nodes())
        if not nodes_iter:
            self.text_output.clear()
            msg = 'Граф порожній'
            self.set_status(msg)
            self.append_text(msg)
            return
        # Вибір початкової вершини з комбобоксу
        start_id = self.traversal_widget.start_vertex_combo.currentText()
        if not start_id:
            msg = 'Оберіть початкову вершину'
            self.set_status(msg)
            self.append_text(msg)
            return
        self.text_output.clear()
        self.traversal_order = []
        self.result_nodes = []
        self.order_to_show = []
        self.cycles = []
        if method.startswith('BFS'):
            result = GraphTraversal.bfs(self.graph, start_id)
            self.order_to_show = list(result)
            self.result_nodes = self.order_to_show.copy()
            if not self.result_nodes:
                msg = 'Жодної досяжної вершини не знайдено.'
                self.set_status(msg)
                self.append_text(msg)
        elif method.startswith('DFS'):
            result = GraphTraversal.dfs(self.graph, start_id)
            self.order_to_show = list(result)
            self.result_nodes = self.order_to_show.copy()
            if not self.result_nodes:
                msg = 'Жодної досяжної вершини не знайдено.'
                self.set_status(msg)
                self.append_text(msg)
        elif method.startswith('Dijkstra'):
            result = GraphTraversal.dijkstra(self.graph, start_id)
            self.order_to_show = list(result)
            self.result_nodes = self.order_to_show.copy()
            if not self.result_nodes:
                msg = 'Жодної досяжної вершини не знайдено.'
                self.set_status(msg)
                self.append_text(msg)
        elif 'Компоненти' in method:
            comps = GraphTraversal.connected_components(self.graph)
            self.order_to_show = [v for comp in comps for v in comp]
            self.result_nodes = comps
            if not comps or all(len(comp) == 0 for comp in comps):
                msg = 'Жодної компоненти звʼязності не знайдено.'
                self.set_status(msg)
                self.append_text(msg)
            else:
                msg = f'Знайдено {len(comps)} компонент(и) звʼязності: ' + ', '.join(str(comp) for comp in comps)
                self.set_status(msg)
                self.append_text(msg)
        elif 'циклів' in method:
            order, cycles = GraphTraversal.has_cycle(self.graph)
            self.order_to_show = order
            self.result_nodes = cycles
            self.cycles = cycles
            if not cycles:
                msg = 'Жодного циклу не знайдено.'
                self.set_status(msg)
                self.append_text(msg)
            else:
                msg = f'Знайдено {len(cycles)} цикл(ів): ' + ', '.join(str(cycle) for cycle in cycles)
                self.set_status(msg)
                self.append_text(msg)
        else:
            self.order_to_show = []
            self.result_nodes = []
            msg = 'Оберіть алгоритм обходу.'
            self.set_status(msg)
            self.append_text(msg)
        self.current_step = 0
        self.is_running = True
        self.traversal_widget.canvas.set_highlighted_nodes([])
        # self.traversal_widget.status_label.setText('')  # status_label видалено
        self.timer.start(700)

    def stop_traversal(self):
        self.timer.stop()
        self.is_running = False
        self.traversal_widget.canvas.set_highlighted_nodes([])
        msg = 'Зупинено'
        self.set_status(msg)
        self.append_text(msg)

    def next_step(self):
        # Додаємо поточний стан у історію для undo
        if self.is_running and self.current_step < len(self.order_to_show):
            self.history.append((self.current_step, list(self.traversal_widget.canvas._highlighted_nodes)))
            self.future.clear()
        # Спочатку підсвічуємо порядок обходу, потім результат
        if self.current_step < len(self.order_to_show):
            highlight = self.order_to_show[:self.current_step+1]
            self.traversal_widget.canvas.set_highlighted_nodes(highlight)
            msg = f'Порядок обходу: {self.order_to_show[self.current_step]}'
            self.set_status(msg)
            self.append_text(msg)
            self.current_step += 1
        elif self.current_step == len(self.order_to_show):
            # Після обходу підсвічуємо результат
            if self.traversal_widget.method_combo.currentText().startswith('BFS') or \
               self.traversal_widget.method_combo.currentText().startswith('DFS') or \
               self.traversal_widget.method_combo.currentText().startswith('Dijkstra'):
                self.traversal_widget.canvas.set_highlighted_nodes(self.result_nodes)
                msg = f'Отримані вершини: {", ".join(map(str, self.result_nodes))}'
                self.set_status(msg)
                self.append_text(msg)
            elif 'Компоненти' in self.traversal_widget.method_combo.currentText():
                for i, comp in enumerate(self.result_nodes, 1):
                    self.traversal_widget.canvas.set_highlighted_nodes(comp)
                    msg = f'Компонента {i}: {", ".join(map(str, comp))}'
                    self.set_status(msg)
                    self.append_text(msg)
            elif 'циклів' in self.traversal_widget.method_combo.currentText():
                if not self.cycles:
                    msg = 'Жодного циклу не знайдено.'
                    self.set_status(msg)
                    self.append_text(msg)
                else:
                    for i, cycle in enumerate(self.cycles, 1):
                        self.traversal_widget.canvas.set_highlighted_nodes(cycle)
                        msg = f'Цикл {i}: {", ".join(map(str, cycle))}'
                        self.set_status(msg)
                        self.append_text(msg)
            self.current_step += 1
        else:
            self.timer.stop()
            self.is_running = False
            msg = 'Обхід завершено'
            self.set_status(msg)
            self.append_text(msg)

    def set_graph(self, graph):
        self.graph = graph
        self.traversal_widget.set_graph(graph)
        self.traversal_widget.canvas.graph = graph
        self.traversal_widget.canvas._init_node_positions()
        self.traversal_widget.canvas.update()
        self.traversal_widget.update_vertex_list()

    def append_text(self, text):
        self.text_output.append(text)

    def undo_step(self):
        if self.history:
            self.timer.stop()
            self.is_running = False
            self.future.append((self.current_step, list(self.traversal_widget.canvas._highlighted_nodes)))
            self.current_step, highlighted = self.history.pop()
            self.traversal_widget.canvas.set_highlighted_nodes(highlighted)

    def redo_step(self):
        if self.future:
            self.history.append((self.current_step, list(self.traversal_widget.canvas._highlighted_nodes)))
            self.current_step, highlighted = self.future.pop()
            self.traversal_widget.canvas.set_highlighted_nodes(highlighted)
