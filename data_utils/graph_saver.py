import json
from utils.logger import Logger

class GraphSaver:
    """
    Клас для збереження графа у файл .json.
    """

    @staticmethod
    def save(graph, filepath):
        """
        Зберігає граф у файл .json.

        :param graph: Об'єкт графа (DirectedGraph або UndirectedGraph)
        :param filepath: Шлях до файлу для збереження
        """
        logger = Logger()
        try:
            is_directed = hasattr(graph, "is_directed") and graph.is_directed()
            is_weighted = getattr(graph, "weighted", True)
            data = {
                "directed": is_directed,
                "weighted": is_weighted,
                "nodes": [
                    {"id": node.id, "data": node.data}
                    for node in graph.nodes()
                ],
                "edges": [
                    {
                        "source": edge.source.id,
                        "target": edge.target.id,
                        "weight": edge.weight(is_weighted),
                        "data": edge.data
                    }
                    for edge in graph.edges()
                ]
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Граф успішно збережено у файл {filepath}")
        except Exception as e:
            logger.error(f"Помилка при збереженні графа: {e}")