from collections import deque
from utils.logger import Logger
from locales.locale_manager import LocaleManager

class BFS:
    """
    Клас для обходу графа в ширину (BFS).
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність вузлів та neighbors
        if not hasattr(graph, "nodes") or not hasattr(graph, "neighbors"):
            self.logger.error(LocaleManager.get_locale("bfs", "methods_error"))
            raise ValueError(LocaleManager.get_locale("bfs", "methods_error"))

        self.nodes = list(graph.nodes())
        if not self.nodes:
            self.logger.error(LocaleManager.get_locale("bfs", "nodes_error"))
            raise ValueError(LocaleManager.get_locale("bfs", "nodes_error"))

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info(LocaleManager.get_locale("bfs", "init_info"))

    def traverse(self, start_id):
        """
        Виконує BFS від заданої вершини.
        
        :param start_id: id початкової вершини
        :return: список id вершин у порядку обходу
        """
        self.logger.info(LocaleManager.get_locale("bfs", "bfs_start").format(start_id=start_id))
        if start_id not in self.node_id_to_node:
            self.logger.error(LocaleManager.get_locale("bfs", "start_error"))
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
        self.logger.info(LocaleManager.get_locale("bfs", "bfs_end").format(path_str=' -> '.join(map(str, order))))
        return order