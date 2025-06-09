from utils.logger import Logger

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
            self.logger.error("Граф повинен мати методи nodes, edges та neighbors.")
            raise ValueError("Граф повинен мати методи nodes, edges та neighbors.")

        self.nodes = list(graph.nodes())
        if not self.nodes:
            self.logger.error("Граф не містить жодної вершини.")
            raise ValueError("Граф не містить жодної вершини.")

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info("Ініціалізація LongestPathFinder: граф коректний.")

    def find_longest_path(self, start_id, end_id):
        """
        Знаходить найдовший простий шлях між start_id та end_id (якщо існує).
        
        :param start_id: id початкової вершини
        :param end_id: id кінцевої вершини
        :return: список id вершин найдовшого шляху або None, якщо шляху не існує
        """
        self.logger.info(f"Пошук найдовшого простого шляху між {start_id} та {end_id} розпочато.")
        if start_id not in self.node_id_to_node or end_id not in self.node_id_to_node:
            self.logger.error("Початкова або кінцева вершина відсутня у графі.")
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
            self.logger.info(f"Знайдено найдовший простий шлях: {' -> '.join(map(str, longest_path))} (довжина {len(longest_path)})")
            return longest_path
        else:
            self.logger.warning(f"Найдовшого простого шляху між {start_id} та {end_id} не існує.")
            return None