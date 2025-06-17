from utils.logger import Logger
from locales.locale_manager import LocaleManager

class HamiltonianPathFinder:
    """
    Клас для знаходження гамільтонового шляху між двома вершинами у графі.

    Гамільтонів шлях — простий шлях, що проходить через усі вершини графа рівно один раз.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність вузлів та ребер
        if not hasattr(graph, "nodes") or not hasattr(graph, "edges") or not hasattr(graph, "neighbors"):
            self.logger.error(LocaleManager.get_locale("hamiltonian_path_finder", "methods_error"))
            raise ValueError(LocaleManager.get_locale("hamiltonian_path_finder", "methods_error"))

        self.nodes = list(graph.nodes())
        if not self.nodes:
            self.logger.error(LocaleManager.get_locale("hamiltonian_path_finder", "enable_node_error"))
            raise ValueError(LocaleManager.get_locale("hamiltonian_path_finder", "enable_node_error"))

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info(LocaleManager.get_locale("hamiltonian_path_finder", "init_info"))

    def find_hamiltonian_path(self, start_id, end_id):
        """
        Знаходить гамільтонів шлях між start_id та end_id (якщо існує).
        
        :param start_id: id початкової вершини
        :param end_id: id кінцевої вершини
        :return: список id вершин гамільтонового шляху або None, якщо шляху не існує
        """
        self.logger.info(LocaleManager.get_locale("hamiltonian_path_finder", "hamiltonian_start").format(start_id=start_id, end_id=end_id))
        if start_id not in self.node_id_to_node or end_id not in self.node_id_to_node:
            self.logger.error(LocaleManager.get_locale("hamiltonian_path_finder", "start_end_error"))
            return None

        n = len(self.nodes)
        path = []
        visited = set()

        def dfs(current_id):
            visited.add(current_id)
            path.append(current_id)
            if len(path) == n and current_id == end_id:
                return True
            for neighbor in self.graph.neighbors(self.node_id_to_node[current_id]):
                if neighbor.id not in visited:
                    if dfs(neighbor.id):
                        return True
            path.pop()
            visited.remove(current_id)
            return False

        found = dfs(start_id)
        if found:
            self.logger.info(LocaleManager.get_locale("hamiltonian_path_finder", "hamiltonian_end").format(path_str=' -> '.join(map(str, path))))
            return path
        else:
            self.logger.warning(LocaleManager.get_locale("hamiltonian_path_finder", "enable_path_warn"))
            return None