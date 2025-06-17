from utils.logger import Logger
from locales.locale_manager import LocaleManager

class BellmanFord:
    """
    Клас для знаходження найкоротших шляхів у графі (алгоритм Беллмана-Форда).

    Працює для графів з вагами ребер (можливі від’ємні ваги, але без від’ємних циклів).
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight(self.graph.is_weighted())
            if self.graph.is_weighted() is False:
                self.logger.error(LocaleManager.get_locale("bellman_ford", "weight_error"))
                raise ValueError(LocaleManager.get_locale("bellman_ford", "weight_error"))

        self.logger.info(LocaleManager.get_locale("bellman_ford", "init_info"))

        self.nodes = list(graph.nodes())
        self.node_id_to_node = {node.id: node for node in self.nodes}

    def shortest_path(self, start_id):
        """
        Знаходить найкоротші шляхи від вершини start_id до всіх інших.
        
        :param start_id: id початкової вершини
        :return: (distances, previous) — словник відстаней та попередників
        """
        self.logger.info(LocaleManager.get_locale("bellman_ford", "bellman_ford_start").format(start_id=start_id))
        distances = {node.id: float('inf') for node in self.nodes}
        previous = {node.id: None for node in self.nodes}
        distances[start_id] = 0

        # Основний цикл алгоритму
        for i in range(len(self.nodes) - 1):
            updated = False
            for edge in self.graph.edges():
                u = edge.source.id
                v = edge.target.id
                w = edge.weight(self.graph.is_weighted())
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    previous[v] = u
                    updated = True
                    self.logger.info(LocaleManager.get_locale("bellman_ford", "update_path").format(v=v, d=distances[v], u=u))
                # Для неспрямованого графа — перевіряємо обидва напрямки
                if hasattr(self.graph, "is_directed") and not self.graph.is_directed():
                    if distances[v] + w < distances[u]:
                        distances[u] = distances[v] + w
                        previous[u] = v
                        updated = True
                        self.logger.info(LocaleManager.get_locale("bellman_ford", "update_path").format(v=u, d=distances[u], u=v))
            if not updated:
                break

        # Перевірка на наявність від’ємних циклів
        for edge in self.graph.edges():
            u = edge.source.id
            v = edge.target.id
            w = edge.weight(self.graph.is_weighted())
            if distances[u] + w < distances[v]:
                self.logger.error(LocaleManager.get_locale("bellman_ford", "enable_negative_cycles"))
                raise ValueError(LocaleManager.get_locale("bellman_ford", "enable_negative_cycles"))
            if hasattr(self.graph, "is_directed") and not self.graph.is_directed():
                if distances[v] + w < distances[u]:
                    self.logger.error(LocaleManager.get_locale("bellman_ford", "enable_negative_cycles"))
                    raise ValueError(LocaleManager.get_locale("bellman_ford", "enable_negative_cycles"))

        self.logger.info(LocaleManager.get_locale("bellman_ford", "bellman_ford_end"))
        return distances, previous