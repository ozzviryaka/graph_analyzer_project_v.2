import json
from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge
from utils.logger import Logger

class GraphLoader:
    """
    Клас для завантаження графа з файлу .json.
    """

    @staticmethod
    def load(filepath, directed_graph_class, undirected_graph_class, directed_edge_class, undirected_edge_class):
        """
        Завантажує граф з файлу .json.

        :param filepath: Шлях до файлу
        :param directed_graph_class: Клас спрямованого графа
        :param undirected_graph_class: Клас неспрямованого графа
        :param directed_edge_class: Клас спрямованого ребра
        :param undirected_edge_class: Клас неспрямованого ребра
        :return: Об'єкт графа
        """
        logger = Logger()
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"Файл графа успішно завантажено: {filepath}")
        except Exception as e:
            logger.error(f"Помилка при завантаженні графа: {e}")
            raise

        is_directed = data.get("directed", False)
        if is_directed:
            graph = directed_graph_class()
            edge_class = directed_edge_class
        else:
            graph = undirected_graph_class()
            edge_class = undirected_edge_class

        node_map = {}

        for node_data in data["nodes"]:
            node = Node(node_data["id"], node_data.get("data"))
            graph.add_node(node)
            node_map[node.id] = node

        for edge_data in data["edges"]:
            source = node_map[edge_data["source"]]
            target = node_map[edge_data["target"]]
            weight = edge_data.get("weight", 1)
            edge = edge_class(source, target, weight, edge_data.get("data"))
            graph.add_edge(edge)

        logger.info("Граф успішно відновлено з даних.")
        return graph