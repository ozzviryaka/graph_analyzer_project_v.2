import json
from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge
from core.graph_models.directed_graph import DirectedGraph
from core.graph_models.undirected_graph import UndirectedGraph
from utils.logger import Logger

class GraphLoader:
    """
    Клас для завантаження графа з файлу .json.
    """

    @staticmethod
    def load(filepath):
        """
        Завантажує граф з файлу .json.

        :param filepath: Шлях до файлу
        :return: Об'єкт графа (DirectedGraph або UndirectedGraph)
        """
        logger = Logger()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            is_directed = data.get("directed", False)
            is_weighted = data.get("weighted", True)
            nodes_data = data.get("nodes", [])
            edges_data = data.get("edges", [])

            if is_directed:
                graph = DirectedGraph(weighted=is_weighted)
                edge_class = DirectedEdge
            else:
                graph = UndirectedGraph(weighted=is_weighted)
                edge_class = UndirectedEdge

            node_map = {}
            for node_info in nodes_data:
                node = Node(node_info["id"], node_info.get("data"))
                graph.add_node(node)
                node_map[node.id] = node

            for edge_info in edges_data:
                source = node_map[edge_info["source"]]
                target = node_map[edge_info["target"]]
                weight = edge_info.get("weight", 1)
                data_field = edge_info.get("data")
                edge = edge_class(source, target, weight, data_field)
                graph.add_edge(edge)

            logger.info(f"Граф успішно завантажено з файлу {filepath}")
            return graph
        except Exception as e:
            logger.error(f"Помилка при завантаженні графа: {e}")
            return None