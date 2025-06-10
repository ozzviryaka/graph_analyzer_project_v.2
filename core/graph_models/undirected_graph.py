from .graph import BaseGraph
from core.graph_components.node import Node
from core.graph_components.undirected_edge import UndirectedEdge

class UndirectedGraph(BaseGraph):
    """
    Клас для представлення неспрямованого графа.
    """

    def __init__(self, weighted=True):
        self.weighted = weighted
        self._nodes = {}
        self._edges = []  # було set(), тепер list
        self._adjacency = {}

    def add_node(self, node):
        """
        Додає вузол до графа.
        """
        if node.id not in self._nodes:
            self._nodes[node.id] = node
            self._adjacency[node.id] = set()

    def add_edge(self, edge):
        """
        Додає неспрямоване ребро до графа.
        """
        if (edge.source.id not in self._nodes) or (edge.target.id not in self._nodes):
            raise ValueError("Обидва вузли ребра мають бути додані до графа перед додаванням ребра.")
        if edge not in self._edges:
            self._edges.append(edge)
            self._adjacency[edge.source.id].add(edge.target.id)
            self._adjacency[edge.target.id].add(edge.source.id)

    def remove_edge(self, edge):
        """
        Видаляє неспрямоване ребро з графа.
        """
        if edge in self._edges:
            self._edges.remove(edge)
            self._adjacency[edge.source.id].discard(edge.target.id)
            self._adjacency[edge.target.id].discard(edge.source.id)

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

    def neighbors(self, node):
        """
        Повертає сусідів заданого вузла (усі вузли, з'єднані ребром).
        """
        if node.id not in self._adjacency:
            return iter([])
        return (self._nodes[n_id] for n_id in self._adjacency[node.id])

    def is_weighted(self):
        return self.weighted

    def clear_edges(self):
        """
        Очищає всі ребра в графі.
        """
        self._edges.clear()
        for adj in self._adjacency.values():
            adj.clear()

    def is_directed(self):
        """
        Повертає False, оскільки граф є неспрямованим.
        """
        return False