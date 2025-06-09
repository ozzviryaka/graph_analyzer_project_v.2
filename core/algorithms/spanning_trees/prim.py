import heapq
from utils.logger import Logger

class Prim:
    """
    Клас для знаходження мінімального остовного дерева (алгоритм Прима).

    Працює для зважених НЕСПРЯМОВАНИХ графів без циклів.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на неспрямованість графа
        if hasattr(graph, "is_directed") and graph.is_directed():
            self.logger.error("Алгоритм Прима працює лише для неспрямованих графів.")
            raise ValueError("Алгоритм Прима працює лише для неспрямованих графів.")

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight(self.graph.is_weighted())
            if w < 0:
                self.logger.error("Усі ребра повинні мати невід'ємні ваги для алгоритму Прима.")
                raise ValueError("Усі ребра повинні мати невід'ємні ваги для алгоритму Прима.")

        self.logger.info("Ініціалізація Prim: граф неспрямований, всі ваги ребер коректні.")

        self.nodes = list(graph.nodes())
        self.node_id_to_node = {node.id: node for node in self.nodes}

    def minimum_spanning_tree(self):
        """
        Повертає список ребер MST та його вагу.
        
        :return: (mst_edges, total_weight)
        """
        self.logger.info("Пошук мінімального остовного дерева (MST) розпочато.")
        if not self.nodes:
            return [], 0

        mst_edges = []
        total_weight = 0
        visited = set()
        start_node = self.nodes[0]
        visited.add(start_node.id)
        edge_candidates = []

        # Додаємо всі ребра, що виходять з початкової вершини
        for neighbor in self.graph.neighbors(start_node):
            for edge in self.graph.edges():
                if (edge.source.id == start_node.id and edge.target.id == neighbor.id) or \
                   (edge.target.id == start_node.id and edge.source.id == neighbor.id):
                    heapq.heappush(edge_candidates, (edge.weight(), edge))
                    break

        while edge_candidates and len(visited) < len(self.nodes):
            weight, edge = heapq.heappop(edge_candidates)
            u, v = edge.source.id, edge.target.id
            if v in visited and u in visited:
                continue
            new_node_id = v if u in visited else u
            if new_node_id in visited:
                continue
            mst_edges.append(edge)
            total_weight += weight
            visited.add(new_node_id)
            self.logger.info(f"Додано ребро ({edge.source.id}, {edge.target.id}) з вагою {weight} до MST.")
            # Додаємо нові ребра, що виходять з нової вершини
            for neighbor in self.graph.neighbors(self.node_id_to_node[new_node_id]):
                if neighbor.id not in visited:
                    for e in self.graph.edges():
                        if (e.source.id == new_node_id and e.target.id == neighbor.id) or \
                           (e.target.id == new_node_id and e.source.id == neighbor.id):
                            heapq.heappush(edge_candidates, (e.weight(), e))
                            break

        if len(mst_edges) != len(self.nodes) - 1:
            self.logger.warning("Граф не є зв'язним — MST не існує для всіх вершин.")

        self.logger.info(f"Завершено. MST вага: {total_weight}, кількість ребер: {len(mst_edges)}")
        return mst_edges, total_weight