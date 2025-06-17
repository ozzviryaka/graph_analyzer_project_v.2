import heapq
from utils.logger import Logger
from locales.locale_manager import LocaleManager

class Dijkstra:
    """
    Клас для знаходження найкоротших шляхів у графі (алгоритм Дейкстри).

    Працює для графів з невід'ємними вагами ребер.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight(self.graph.is_weighted())
            if w < 0:
                self.logger.error(LocaleManager.get_locale("dijkstra", "weight_error"))
                raise ValueError(LocaleManager.get_locale("dijkstra", "weight_error"))

        self.logger.info(LocaleManager.get_locale("dijkstra", "init_info"))

        self.nodes = list(graph.nodes())
        self.node_id_to_node = {node.id: node for node in self.nodes}

    def shortest_path(self, start_id):
        """
        Знаходить найкоротші шляхи від вершини start_id до всіх інших.
        
        :param start_id: id початкової вершини
        :return: словник {id_вершини: (відстань, попередник)}
        """
        self.logger.info(LocaleManager.get_locale("dijkstra", "dijkstra_start").format(start_id=start_id))
        distances = {node.id: float('inf') for node in self.nodes}
        previous = {node.id: None for node in self.nodes}
        distances[start_id] = 0

        queue = [(0, start_id)]
        visited = set()

        while queue:
            dist_u, u_id = heapq.heappop(queue)
            if u_id in visited:
                continue
            visited.add(u_id)

            for neighbor in self.graph.neighbors(self.node_id_to_node[u_id]):
                v_id = neighbor.id
                # Знаходимо вагу ребра між u та v
                weight = None
                for edge in self.graph.edges():
                    if edge.source.id == u_id and edge.target.id == v_id:
                        weight = edge.weight(self.graph.is_weighted())
                        break
                    # Для неспрямованого графа перевіряємо обидва напрямки
                    if hasattr(self.graph, "is_directed") and not self.graph.is_directed():
                        if edge.source.id == v_id and edge.target.id == u_id:
                            weight = edge.weight(self.graph.is_weighted())
                            break
                if self.graph.is_weighted() is False:
                    continue
                alt = dist_u + weight
                if alt < distances[v_id]:
                    distances[v_id] = alt
                    previous[v_id] = u_id
                    heapq.heappush(queue, (alt, v_id))
                    self.logger.info(LocaleManager.get_locale("dijkstra", "update_path").format(v_id=v_id, alt=alt, u_id=u_id))

        self.logger.info(LocaleManager.get_locale("dijkstra", "dijkstra_end"))
        return {node_id: (distances[node_id], previous[node_id]) for node_id in distances}