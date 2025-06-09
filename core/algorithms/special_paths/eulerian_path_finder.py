from utils.logger import Logger

class EulerianPathFinder:
    """
    Клас для знаходження ейлерового шляху у графі.

    Ейлерів шлях — шлях, який проходить кожне ребро графа рівно один раз.

    Працює для орієнтованих та неорієнтованих графів.
    """

    def __init__(self, graph):
        self.graph = graph
        self.logger = Logger()

        # Перевірка на наявність вузлів та ребер
        if not hasattr(graph, "nodes") or not hasattr(graph, "edges") or not hasattr(graph, "neighbors"):
            self.logger.error("Граф повинен мати методи nodes, edges та neighbors.")
            raise ValueError("Граф повинен мати методи nodes, edges та neighbors.")

        self.nodes = list(graph.nodes())
        self.edges = list(graph.edges())
        if not self.nodes or not self.edges:
            self.logger.error("Граф повинен містити хоча б одну вершину та ребро.")
            raise ValueError("Граф повинен містити хоча б одну вершину та ребро.")

        self.node_id_to_node = {node.id: node for node in self.nodes}
        self.logger.info("Ініціалізація EulerianPathFinder: граф коректний.")

    def _is_eulerian(self):
        """
        Перевіряє, чи існує ейлерів шлях у графі.

        Для неорієнтованого: не більше двох вершин непарного ступеня.

        Для орієнтованого: не більше однієї вершини з out-in=1 та однієї з in-out=1.
        """
        if hasattr(self.graph, "is_directed") and self.graph.is_directed():
            in_deg = {}
            out_deg = {}
            for node in self.nodes:
                in_deg[node.id] = 0
                out_deg[node.id] = 0
            for edge in self.edges:
                out_deg[edge.source.id] += 1
                in_deg[edge.target.id] += 1
            start_nodes = end_nodes = 0
            for node_id in in_deg:
                if out_deg[node_id] - in_deg[node_id] == 1:
                    start_nodes += 1
                elif in_deg[node_id] - out_deg[node_id] == 1:
                    end_nodes += 1
                elif in_deg[node_id] != out_deg[node_id]:
                    return False
            return (start_nodes == 1 and end_nodes == 1) or (start_nodes == 0 and end_nodes == 0)
        else:
            odd = 0
            for node in self.nodes:
                deg = sum(1 for _ in self.graph.neighbors(node))
                if deg % 2 != 0:
                    odd += 1
            return odd == 0 or odd == 2

    def find_eulerian_path(self):
        """
        Знаходить ейлерів шлях (якщо існує).
        
        :return: список id вершин у порядку проходження або None, якщо шляху не існує
        """
        self.logger.info("Пошук ейлерового шляху розпочато.")
        if not self._is_eulerian():
            self.logger.warning("Ейлерового шляху у графі не існує.")
            return None

        # Копія списку ребер для обходу
        edge_list = list(self.edges)
        used = set()
        path = []

        # Для орієнтованого графа
        if hasattr(self.graph, "is_directed") and self.graph.is_directed():
            in_deg = {}
            out_deg = {}
            for node in self.nodes:
                in_deg[node.id] = 0
                out_deg[node.id] = 0
            for edge in self.edges:
                out_deg[edge.source.id] += 1
                in_deg[edge.target.id] += 1
            start_id = self.nodes[0].id
            for node in self.nodes:
                if out_deg[node.id] - in_deg[node.id] == 1:
                    start_id = node.id
                    break
            def visit(u):
                for i, edge in enumerate(edge_list):
                    if i in used:
                        continue
                    if edge.source.id == u:
                        used.add(i)
                        visit(edge.target.id)
                path.append(u)
            visit(start_id)
            path.reverse()
        else:
            # Для неорієнтованого графа
            from collections import defaultdict
            adj = defaultdict(list)
            for idx, edge in enumerate(edge_list):
                adj[edge.source.id].append((edge.target.id, idx))
                adj[edge.target.id].append((edge.source.id, idx))
            start_id = self.nodes[0].id
            for node in self.nodes:
                deg = len(adj[node.id])
                if deg % 2 == 1:
                    start_id = node.id
                    break
            def visit(u):
                while adj[u]:
                    v, idx = adj[u].pop()
                    if idx in used:
                        continue
                    used.add(idx)
                    # Видаляємо зворотне ребро
                    adj[v] = [(n, i) for n, i in adj[v] if i != idx]
                    visit(v)
                path.append(u)
            visit(start_id)
            path.reverse()

        if len(used) != len(edge_list):
            self.logger.warning("Не всі ребра використані — ейлерового шляху не існує.")
            return None

        self.logger.info(f"Знайдено ейлерів шлях: {' -> '.join(map(str, path))}")
        return path