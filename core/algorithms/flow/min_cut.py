from collections import deque, defaultdict
from utils.logger import Logger

class MinCut:
    """
    Клас для знаходження мінімального розрізу у графі (алгоритм Форда-Фалкерсона).
    Працює для орієнтованих графів з невід'ємними вагами ребер.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на орієнтованість графа
        if not hasattr(graph, "is_directed") or not graph.is_directed():
            self.logger.error("Алгоритм мінімального розрізу працює лише для орієнтованих графів.")
            raise ValueError("Алгоритм мінімального розрізу працює лише для орієнтованих графів.")

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight() if hasattr(edge, "weight") else None
            if w is None or w < 0:
                self.logger.error("Усі ребра повинні мати невід'ємні ваги для алгоритму мінімального розрізу.")
                raise ValueError("Усі ребра повинні мати невід'ємні ваги для алгоритму мінімального розрізу.")

        self.logger.info("Ініціалізація MinCut: граф орієнтований, всі ваги ребер коректні.")

        self.nodes = list(graph.nodes())
        self.node_ids = [node.id for node in self.nodes]
        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.capacity = self._build_capacity()

    def _build_capacity(self):
        capacity = defaultdict(lambda: defaultdict(int))
        for edge in self.graph.edges():
            u = edge.source.id
            v = edge.target.id
            w = edge.weight() if hasattr(edge, "weight") else 1
            capacity[u][v] += w
        return capacity

    def _bfs(self, residual, s, t, parent):
        visited = set()
        queue = deque([s])
        visited.add(s)
        while queue:
            u = queue.popleft()
            for v in residual[u]:
                if v not in visited and residual[u][v] > 0:
                    parent[v] = u
                    if v == t:
                        return True
                    visited.add(v)
                    queue.append(v)
        return False

    def min_cut(self, source_id, sink_id):
        """
        Знаходить мінімальний розріз між source_id та sink_id.
        :param source_id: id початкової вершини
        :param sink_id: id кінцевої вершини
        :return: (min_cut_value, cut_edges) — вага розрізу та список ребер розрізу
        """
        self.logger.info(f"Пошук мінімального розрізу між {source_id} та {sink_id} розпочато.")
        residual = defaultdict(lambda: defaultdict(int))
        for u in self.capacity:
            for v in self.capacity[u]:
                residual[u][v] = self.capacity[u][v]

        parent = {}
        max_flow = 0

        # Алгоритм Форда-Фалкерсона (Edmonds-Karp)
        while self._bfs(residual, source_id, sink_id, parent):
            path_flow = float('inf')
            v = sink_id
            while v != source_id:
                u = parent[v]
                path_flow = min(path_flow, residual[u][v])
                v = u
            v = sink_id
            while v != source_id:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                v = u
            max_flow += path_flow
            self.logger.info(f"Знайдено шлях з потоком {path_flow}. Поточний max_flow: {max_flow}")

        # Визначаємо розріз
        visited = set()
        queue = deque([source_id])
        while queue:
            u = queue.popleft()
            visited.add(u)
            for v in residual[u]:
                if residual[u][v] > 0 and v not in visited:
                    queue.append(v)

        cut_edges = []
        for u in self.capacity:
            for v in self.capacity[u]:
                if u in visited and v not in visited and self.capacity[u][v] > 0:
                    cut_edges.append((u, v, self.capacity[u][v]))

        self.logger.info(f"Мінімальний розріз: {max_flow}, кількість ребер у розрізі: {len(cut_edges)}")
        return max_flow, cut_edges