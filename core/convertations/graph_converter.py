from core.graph_models.directed_graph import DirectedGraph
from core.graph_models.undirected_graph import UndirectedGraph
from core.graph_components.node import Node
from core.convertations.edge_converter import EdgeConverter
from utils.logger import Logger

class GraphConverter:
    """
    Клас для конвертації між спрямованим та неспрямованим графом.
    """

    @staticmethod
    def directed_to_undirected(directed_graph):
        """
        Конвертує спрямований граф у неспрямований.

        :param directed_graph: Об'єкт DirectedGraph
        :return: Об'єкт UndirectedGraph
        """
        logger = Logger()
        undirected_graph = UndirectedGraph(weighted=directed_graph.is_weighted())
        node_map = {}

        # Додаємо всі вузли
        for node in directed_graph.nodes():
            new_node = Node(node.id, node.data)
            undirected_graph.add_node(new_node)
            node_map[node.id] = new_node

        # Додаємо всі ребра як неспрямовані (унікальні)
        added_edges = set()
        for edge in directed_graph.edges():
            node1 = node_map[edge.source.id]
            node2 = node_map[edge.target.id]
            edge_key = frozenset([node1.id, node2.id])
            if edge_key not in added_edges:
                # Створюємо тимчасове ребро з правильними вузлами
                tmp_edge = type('TmpEdge', (), {
                    'source': node1,
                    'target': node2,
                    'weight': lambda self=edge: edge.weight(directed_graph.is_weighted()),
                    'data': edge.data
                })()
                undirected_edge = EdgeConverter.directed_to_undirected(tmp_edge, weighted=directed_graph.is_weighted())
                undirected_graph.add_edge(undirected_edge)
                added_edges.add(edge_key)
        logger.info("Спрямований граф конвертовано у неспрямований.")
        return undirected_graph

    @staticmethod
    def undirected_to_directed(undirected_graph):
        """
        Конвертує неспрямований граф у спрямований (створює два ребра для кожного неспрямованого).

        :param undirected_graph: Об'єкт UndirectedGraph
        :return: Об'єкт DirectedGraph
        """
        logger = Logger()
        directed_graph = DirectedGraph(weighted=undirected_graph.is_weighted())
        node_map = {}

        # Додаємо всі вузли
        for node in undirected_graph.nodes():
            new_node = Node(node.id, node.data)
            directed_graph.add_node(new_node)
            node_map[node.id] = new_node

        # Додаємо всі ребра як два спрямованих (в обидва боки)
        for edge in undirected_graph.edges():
            node1 = node_map[edge.source.id]
            node2 = node_map[edge.target.id]
            # Створюємо тимчасове ребро для кожного напрямку
            tmp_edge1 = type('TmpEdge', (), {
                'source': node1,
                'target': node2,
                'weight': lambda self=edge: edge.weight(undirected_graph.is_weighted()),
                'data': edge.data
            })()
            tmp_edge2 = type('TmpEdge', (), {
                'source': node2,
                'target': node1,
                'weight': lambda self=edge: edge.weight(undirected_graph.is_weighted()),
                'data': edge.data
            })()
            directed_edge1 = EdgeConverter.undirected_to_directed(tmp_edge1, source_first=True, weighted=undirected_graph.is_weighted())
            directed_edge2 = EdgeConverter.undirected_to_directed(tmp_edge2, source_first=True, weighted=undirected_graph.is_weighted())
            directed_graph.add_edge(directed_edge1)
            directed_graph.add_edge(directed_edge2)
        logger.info("Неспрямований граф конвертовано у спрямований.")
        return directed_graph