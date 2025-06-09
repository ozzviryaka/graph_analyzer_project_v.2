from utils.logger import Logger

class Kruskal:
    """
    Клас для знаходження мінімального остовного дерева (алгоритм Краскала).
    Працює для зважених НЕСПРЯМОВАНИХ графів без циклів.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на неспрямованість графа
        if hasattr(graph, "is_directed") and graph.is_directed():
            self.logger.error("Алгоритм Краскала працює лише для неспрямованих графів.")
            raise ValueError("Алгоритм Краскала працює лише для неспрямованих графів.")

        # Перевірка на наявність ваг у всіх ребер
        for edge in graph.edges():
            w = edge.weight(self.graph.is_weighted())
            if w < 0:
                self.logger.error("Усі ребра повинні мати невід'ємні ваги для алгоритму Краскала.")
                raise ValueError("Усі ребра повинні мати невід'ємні ваги для алгоритму Краскала.")

        self.logger.info("Ініціалізація Kruskal: граф неспрямований, всі ваги ребер коректні.")

        self.nodes = list(graph.nodes())
        self.node_id_to_node = {node.id: node for node in self.nodes}

    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def minimum_spanning_tree(self):
        """
        Повертає список ребер MST та його вагу.
        :return: (mst_edges, total_weight)
        """
        self.logger.info("Пошук мінімального остовного дерева розпочато.")
        edges = sorted(self.graph.edges(), key=lambda e: e.weight())
        parent = {node.id: node.id for node in self.nodes}
        rank = {node.id: 0 for node in self.nodes}
        mst_edges = []
        total_weight = 0

        for edge in edges:
            u = edge.source.id
            v = edge.target.id
            set_u = self.find(parent, u)
            set_v = self.find(parent, v)
            if set_u != set_v:
                mst_edges.append(edge)
                total_weight += edge.weight()
                self.logger.info(f"Додано ребро ({u}, {v}) з вагою {edge.weight()} до MST.")
                self.union(parent, rank, set_u, set_v)
            if len(mst_edges) == len(self.nodes) - 1:
                break

        if len(mst_edges) != len(self.nodes) - 1:
            self.logger.warning("Граф не є зв'язним — MST не існує для всіх вершин.")

        self.logger.info(f"Завершено. MST вага: {total_weight}, кількість ребер: {len(mst_edges)}")
        return mst_edges, total_weight