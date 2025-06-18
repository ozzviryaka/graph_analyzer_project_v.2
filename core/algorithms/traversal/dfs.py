from utils.logger import Logger
from locales.locale_manager import LocaleManager

class DFS:
    """
    Клас для обходу графа в глибину (DFS).
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність вузлів та neighbors
        if not hasattr(graph, "nodes") or not hasattr(graph, "neighbors"):
            self.logger.error(LocaleManager.get_locale("dfs", "methods_error"))
            raise ValueError(LocaleManager.get_locale("dfs", "methods_error"))

        self.nodes = list(graph.nodes())
        if not self.nodes:
            self.logger.error(LocaleManager.get_locale("dfs", "nodes_error"))
            raise ValueError(LocaleManager.get_locale("dfs", "nodes_error"))

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info(LocaleManager.get_locale("dfs", "init_info"))

    def traverse(self, start_id):
        """
        Виконує DFS від заданої вершини.
        
        :param start_id: id початкової вершини
        :return: список id вершин у порядку обходу
        """
        self.logger.info(LocaleManager.get_locale("dfs", "dfs_start").format(start_id=start_id))
        if start_id not in self.node_id_to_node:
            self.logger.error(LocaleManager.get_locale("dfs", "start_error"))
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
        self.logger.info(LocaleManager.get_locale("dfs", "dfs_end").format(path_str=' -> '.join(map(str, order))))
        return order