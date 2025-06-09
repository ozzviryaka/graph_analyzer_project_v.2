from .graph import BaseGraph
from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge

class DirectedGraph(BaseGraph):
    """
    Клас для представлення спрямованого графа.
    """

    def __init__(self):
        self._nodes = {}
        self._edges = set()
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
        Додає спрямоване ребро до графа.
        """
        if (edge.source.id not in self._nodes) or (edge.target.id not in self._nodes):
            raise ValueError("Обидва вузли ребра мають бути додані до графа перед додаванням ребра.")
        self._edges.add(edge)
        self._adjacency[edge.source.id].add(edge.target.id)

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
        Повертає сусідів заданого вузла (тільки ті, до яких є напрямлене ребро).
        """
        if node.id not in self._adjacency:
            return iter([])
        return (self._nodes[n_id] for n_id in self._adjacency[node.id])