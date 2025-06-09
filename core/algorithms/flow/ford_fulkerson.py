from collections import deque, defaultdict
from utils.logger import Logger

class FordFulkerson:
    """
    Клас для знаходження максимальної потужності потоку у графі (алгоритм Форда-Фалкерсона).
    Працює для орієнтованих графів з невід'ємними вагами ребер.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на орієнтованість графа
        if not hasattr(graph, "is_directed") or not graph.is_directed():
            self.logger.error("Алгоритм Форда-Фалкерсона працює лише для орієнтованих графів.")
            raise ValueError("Алгоритм Форда-Фалкерсона працює лише для орієнтованих графів.")

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight(self.graph.is_weighted())
            if w < 0:
                self.logger.error("Усі ребра повинні мати невід'ємні ваги для алгоритму Форда-Фалкерсона.")
                raise ValueError("Усі ребра повинні мати невід'ємні ваги для алгоритму Форда-Фалкерсона.")

        self.logger.info("Ініціалізація FordFulkerson: граф орієнтований, всі ваги ребер коректні.")

        self.nodes = list(graph.nodes())
        self.node_ids = [node.id for node in self.nodes]
        self.capacity = self._build_capacity()

    def _build_capacity(self):
        capacity = defaultdict(lambda: defaultdict(int))
        for edge in self.graph.edges():
            u = edge.source.id
            v = edge.target.id
            w = edge.weight(self.graph.is_weighted())
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

    def max_flow(self, source_id, sink_id):
        """
        Знаходить максимальний потік між source_id та sink_id.
        :param source_id: id початкової вершини
        :param sink_id: id кінцевої вершини
        :return: максимальний потік (int)
        """
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

        self.logger.info(f"Максимальний потік між {source_id} та {sink_id}: {max_flow}")
        return max_flow