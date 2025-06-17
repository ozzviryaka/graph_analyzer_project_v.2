from utils.logger import Logger
from locales.locale_manager import LocaleManager

class LongestPathFinder:
    """
    Клас для знаходження найдовшого простого шляху між двома вершинами у графі.

    Найдовший простий шлях — шлях без повторень вершин з максимальною довжиною.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність вузлів та ребер
        if not hasattr(graph, "nodes") or not hasattr(graph, "edges") or not hasattr(graph, "neighbors"):
            self.logger.error(LocaleManager.get_locale("longest_path_finder", "methods_error"))
            raise ValueError(LocaleManager.get_locale("longest_path_finder", "methods_error"))

        self.nodes = list(graph.nodes())
        if not self.nodes:
            self.logger.error(LocaleManager.get_locale("longest_path_finder", "enable_node_error"))
            raise ValueError(LocaleManager.get_locale("longest_path_finder", "enable_node_error"))

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info(LocaleManager.get_locale("longest_path_finder", "init_info"))

    def find_longest_path(self, start_id, end_id):
        """
        Знаходить найдовший простий шлях між start_id та end_id (якщо існує).
        
        :param start_id: id початкової вершини
        :param end_id: id кінцевої вершини
        :return: список id вершин найдовшого шляху або None, якщо шляху не існує
        """
        self.logger.info(LocaleManager.get_locale("longest_path_finder", "longest_start").format(start_id=start_id, end_id=end_id))
        if start_id not in self.node_id_to_node or end_id not in self.node_id_to_node:
            self.logger.error(LocaleManager.get_locale("longest_path_finder", "start_end_error"))
            return None

        longest_path = []
        path = []
        visited = set()

        def dfs(current_id):
            nonlocal longest_path
            visited.add(current_id)
            path.append(current_id)
            if current_id == end_id:
                if len(path) > len(longest_path):
                    longest_path = list(path)
            else:
                for neighbor in self.graph.neighbors(self.node_id_to_node[current_id]):
                    if neighbor.id not in visited:
                        dfs(neighbor.id)
            path.pop()
            visited.remove(current_id)

        dfs(start_id)
        if longest_path:
            self.logger.info(LocaleManager.get_locale("longest_path_finder", "longest_end").format(path_str=' -> '.join(map(str, longest_path)), len_longest_path=len(longest_path)))
            return longest_path
        else:
            self.logger.warning(LocaleManager.get_locale("longest_path_finder", "enable_path_warn").format(start_id=start_id, end_id=end_id))
            return None