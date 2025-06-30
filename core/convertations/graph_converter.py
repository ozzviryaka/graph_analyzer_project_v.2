from core.graph_models.directed_graph import DirectedGraph
from core.graph_models.undirected_graph import UndirectedGraph
from core.graph_components.node import Node
from core.convertations.edge_converter import EdgeConverter
from utils.logger import Logger
from locales.locale_manager import LocaleManager

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
        # Зберігаємо ім'я та додаткові атрибути
        if hasattr(directed_graph, 'name'):
            undirected_graph.name = directed_graph.name
        if hasattr(directed_graph, 'directed'):
            undirected_graph.directed = False
        # Зберігаємо позиції вершин, якщо вони є
        if hasattr(directed_graph, 'node_positions'):
            undirected_graph.node_positions = dict(directed_graph.node_positions)
        node_map = {}

        # Додаємо всі вузли
        for node in directed_graph.nodes():
            new_node = Node(node.id, node.data)
            undirected_graph.add_node(new_node)
            node_map[node.id] = new_node

        # Додаємо всі ребра як неспрямовані (унікальні)
        from core.graph_components.directed_edge import DirectedEdge
        added_edges = set()
        for edge in directed_graph.edges():
            node1 = node_map[edge.source.id]
            node2 = node_map[edge.target.id]
            edge_key = frozenset([node1.id, node2.id])
            if edge_key not in added_edges:
                # Визначаємо вагу: якщо є _original_weight, беремо її, інакше _weight
                weight = getattr(edge, '_original_weight', edge._weight)
                directed_edge = DirectedEdge(node1, node2, weight=weight, data=edge.data)
                undirected_edge = EdgeConverter.directed_to_undirected(directed_edge, weighted=True)
                undirected_graph.add_edge(undirected_edge)
                added_edges.add(edge_key)
        logger.info(LocaleManager.get_locale("graph_converter", "directed_to_undirected_info"))
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
        # Зберігаємо ім'я та додаткові атрибути
        if hasattr(undirected_graph, 'name'):
            directed_graph.name = undirected_graph.name
        if hasattr(undirected_graph, 'directed'):
            directed_graph.directed = True
        # Зберігаємо позиції вершин, якщо вони є
        if hasattr(undirected_graph, 'node_positions'):
            directed_graph.node_positions = dict(undirected_graph.node_positions)
        node_map = {}

        # Додаємо всі вузли
        for node in undirected_graph.nodes():
            new_node = Node(node.id, node.data)
            directed_graph.add_node(new_node)
            node_map[node.id] = new_node

        # Додаємо всі ребра як два спрямованих (в обидва боки)
        from core.graph_components.undirected_edge import UndirectedEdge
        for edge in undirected_graph.edges():
            node1 = node_map[edge.source.id]
            node2 = node_map[edge.target.id]
            weight = getattr(edge, '_original_weight', edge._weight)
            undirected_edge = UndirectedEdge(node1, node2, weight=weight, data=edge.data)
            directed_edge = EdgeConverter.undirected_to_directed(undirected_edge, source_first=True, weighted=True)
            directed_graph.add_edge(directed_edge)
        logger.info(LocaleManager.get_locale("graph_converter", "undirected_to_directed_info"))
        return directed_graph