from .graph import BaseGraph
from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge

class DirectedGraph(BaseGraph):
    """
    Клас для представлення спрямованого графа.
    """

    def __init__(self, weighted=True):
        self.weighted = weighted
        self._nodes = {}
        self._edges = []  # було set(), тепер list
        self._adjacency = {}
        self._node_counter = 1  # Для іменування вершин V1, V2, ...

    def add_node(self, node):
        """
        Додає вузол до графа.
        """
        if node.id not in self._nodes:
            self._nodes[node.id] = node
            self._adjacency[node.id] = set()

    def add_edge(self, edge):
        """
        Додає спрямоване ребро до графа.
        """
        if (edge.source.id not in self._nodes) or (edge.target.id not in self._nodes):
            raise ValueError("Обидва вузли ребра мають бути додані до графа перед додаванням ребра.")
        if edge not in self._edges:
            self._edges.append(edge)
            self._adjacency[edge.source.id].add(edge.target.id)

    def remove_edge(self, edge):
        """
        Видаляє спрямоване ребро з графа.
        """
        if edge in self._edges:
            self._edges.remove(edge)
            self._adjacency[edge.source.id].discard(edge.target.id)

    def clear_edges(self):
        """
        Очищає всі ребра в графі.
        """
        self._edges.clear()
        for adj in self._adjacency.values():
            adj.clear()

    def nodes(self):
        """
        Повертає ітератор по всіх вузлах графа.
        """
        return iter(self._nodes.values())

    def edges(self):
        """
        Повертає ітератор по всіх ребрах графа.
        """
        return iter(self._edges)

    def neighbors(self, node_or_id):
        """
        Повертає сусідів заданого вузла (тільки ті, до яких є напрямлене ребро).
        Можна передавати або Node, або id (str).
        """
        node_id = node_or_id.id if hasattr(node_or_id, 'id') else node_or_id
        if node_id not in self._adjacency:
            return iter([])
        return (self._nodes[n_id] for n_id in self._adjacency[node_id])

    def is_weighted(self):
        return self.weighted

    def is_directed(self):
        return True

    def next_node_name(self):
        # Пошук найменшого вільного номера
        used = set()
        for node_id in self._nodes:
            if node_id.startswith('V') and node_id[1:].isdigit():
                used.add(int(node_id[1:]))
        n = 1
        while n in used:
            n += 1
        return f"V{n}"

    def get_edge_weight(self, source_id, target_id):
        """
        Повертає вагу ребра між source_id і target_id, або 1, якщо граф неваговий.
        Якщо ребра немає — повертає float('inf').
        """
        for edge in self._edges:
            if edge.source.id == source_id and edge.target.id == target_id:
                return getattr(edge, 'weight', lambda: 1)() if self.is_weighted() else 1
        return float('inf')