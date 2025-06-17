from utils.logger import Logger
from locales.locale_manager import LocaleManager

class FloydWarshall:
    """
    Клас для знаходження найкоротших шляхів між усіма парами вершин (алгоритм Флойда-Уоршелла).

    Працює для графів з невід'ємними вагами ребер.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight(self.graph.is_weighted())
            if w < 0:
                self.logger.error(LocaleManager.get_locale("floyd_warshall", "weight_error"))
                raise ValueError(LocaleManager.get_locale("floyd_warshall", "weight_error"))

        self.logger.info(LocaleManager.get_locale("floyd_warshall", "init_info"))

        self.nodes = list(graph.nodes())
        self.node_id_to_index = {node.id: idx for idx, node in enumerate(self.nodes)}
        self.index_to_node_id = {idx: node.id for idx, node in enumerate(self.nodes)}

    def shortest_paths(self):
        """
        Знаходить найкоротші шляхи між усіма парами вершин.
        
        :return: матриця відстаней dist[i][j], де i, j — індекси вузлів
        """
        n = len(self.nodes)
        INF = float('inf')
        dist = [[INF for _ in range(n)] for _ in range(n)]
        next_node = [[None for _ in range(n)] for _ in range(n)]

        # Ініціалізація матриці відстаней
        for i in range(n):
            dist[i][i] = 0
            next_node[i][i] = self.index_to_node_id[i]
        for edge in self.graph.edges():
            u = self.node_id_to_index[edge.source.id]
            v = self.node_id_to_index[edge.target.id]
            w = edge.weight(self.graph.is_weighted())
            dist[u][v] = min(dist[u][v], w)
            next_node[u][v] = self.index_to_node_id[v]
            # Для неспрямованого графа — симетрично
            if hasattr(self.graph, "is_directed") and not self.graph.is_directed():
                dist[v][u] = min(dist[v][u], w)
                next_node[v][u] = self.index_to_node_id[u]

        # Основний цикл алгоритму
        self.logger.info(LocaleManager.get_locale("floyd_warshall", "floyd_warshall_start"))
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
                        self.logger.info(LocaleManager.get_locale(
                            "floyd_warshall", "update_path").format(
                            from_node=self.index_to_node_id[i],
                            to_node=self.index_to_node_id[j],
                            via_node=self.index_to_node_id[k],
                            distance=dist[i][j]
                        ))
        self.logger.info(LocaleManager.get_locale("floyd_warshall", "floyd_warshall_end"))
        return dist, next_node