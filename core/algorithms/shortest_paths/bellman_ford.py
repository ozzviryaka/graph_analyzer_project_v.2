from utils.logger import Logger

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
            w = edge.weight() if hasattr(edge, "weight") else None
            if w is None:
                self.logger.error("Усі ребра повинні мати вагу для алгоритму Беллмана-Форда.")
                raise ValueError("Усі ребра повинні мати вагу для алгоритму Беллмана-Форда.")

        self.logger.info("Ініціалізація BellmanFord: всі ваги ребер коректні.")

        self.nodes = list(graph.nodes())
        self.node_id_to_node = {node.id: node for node in self.nodes}

    def shortest_path(self, start_id):
        """
        Знаходить найкоротші шляхи від вершини start_id до всіх інших.
        :param start_id: id початкової вершини
        :return: (distances, previous) — словник відстаней та попередників
        """
        self.logger.info(f"Пошук найкоротших шляхів від вершини {start_id} розпочато.")
        distances = {node.id: float('inf') for node in self.nodes}
        previous = {node.id: None for node in self.nodes}
        distances[start_id] = 0

        # Основний цикл алгоритму
        for i in range(len(self.nodes) - 1):
            updated = False
            for edge in self.graph.edges():
                u = edge.source.id
                v = edge.target.id
                w = edge.weight() if hasattr(edge, "weight") else 1
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    previous[v] = u
                    updated = True
                    self.logger.info(f"Оновлено шлях до {v}: відстань {distances[v]}, попередник {u}")
                # Для неспрямованого графа — перевіряємо обидва напрямки
                if hasattr(self.graph, "is_directed") and not self.graph.is_directed():
                    if distances[v] + w < distances[u]:
                        distances[u] = distances[v] + w
                        previous[u] = v
                        updated = True
                        self.logger.info(f"Оновлено шлях до {u}: відстань {distances[u]}, попередник {v}")
            if not updated:
                break

        # Перевірка на наявність від’ємних циклів
        for edge in self.graph.edges():
            u = edge.source.id
            v = edge.target.id
            w = edge.weight() if hasattr(edge, "weight") else 1
            if distances[u] + w < distances[v]:
                self.logger.error("Граф містить від’ємний цикл.")
                raise ValueError("Граф містить від’ємний цикл.")
            if hasattr(self.graph, "is_directed") and not self.graph.is_directed():
                if distances[v] + w < distances[u]:
                    self.logger.error("Граф містить від’ємний цикл.")
                    raise ValueError("Граф містить від’ємний цикл.")

        self.logger.info("Пошук найкоротших шляхів завершено.")
        return distances, previous