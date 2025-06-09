from collections import deque
from utils.logger import Logger

class BFS:
    """
    Клас для обходу графа в ширину (BFS).
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність вузлів та neighbors
        if not hasattr(graph, "nodes") or not hasattr(graph, "neighbors"):
            self.logger.error("Граф повинен мати методи nodes та neighbors.")
            raise ValueError("Граф повинен мати методи nodes та neighbors.")

        self.nodes = list(graph.nodes())
        if not self.nodes:
            self.logger.error("Граф не містить жодної вершини.")
            raise ValueError("Граф не містить жодної вершини.")

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info("Ініціалізація BFS: граф коректний.")

    def traverse(self, start_id):
        """
        Виконує BFS від заданої вершини.
        
        :param start_id: id початкової вершини
        :return: список id вершин у порядку обходу
        """
        self.logger.info(f"Початок BFS з вершини {start_id}.")
        if start_id not in self.node_id_to_node:
            self.logger.error("Початкова вершина відсутня у графі.")
            return []

        visited = set()
        order = []
        queue = deque([start_id])
        visited.add(start_id)

        while queue:
            current_id = queue.popleft()
            order.append(current_id)
            for neighbor in self.graph.neighbors(self.node_id_to_node[current_id]):
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    queue.append(neighbor.id)
        self.logger.info(f"BFS завершено. Порядок обходу: {' -> '.join(map(str, order))}")
        return order