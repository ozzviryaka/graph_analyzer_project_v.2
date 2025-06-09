from utils.logger import Logger

class DFS:
    """
    Клас для обходу графа в глибину (DFS).
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
        self.logger.info("Ініціалізація DFS: граф коректний.")

    def traverse(self, start_id):
        """
        Виконує DFS від заданої вершини.
        :param start_id: id початкової вершини
        :return: список id вершин у порядку обходу
        """
        self.logger.info(f"Початок DFS з вершини {start_id}.")
        if start_id not in self.node_id_to_node:
            self.logger.error("Початкова вершина відсутня у графі.")
            return []

        visited = set()
        order = []

        def dfs(current_id):
            visited.add(current_id)
            order.append(current_id)
            for neighbor in self.graph.neighbors(self.node_id_to_node[current_id]):
                if neighbor.id not in visited:
                    dfs(neighbor.id)

        dfs(start_id)
        self.logger.info(f"DFS завершено. Порядок обходу: {' -> '.join(map(str, order))}")
        return order