import json
from utils.logger import Logger
from core.graph_components.node import Node
from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge

class SessionImporter:
    @staticmethod
    def import_session(filepath, graph_class_map):
        """
        filepath: шлях до файлу сесії
        graph_class_map: dict, наприклад {'Graph': Graph, 'DirectedGraph': DirectedGraph, ...}
        return: список графів
        """
        logger = Logger()
        logger.info(f"Початок імпорту сесії з файлу: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            graphs = []
            for gdata in session_data:
                cls = graph_class_map.get(gdata['class'])
                if not cls:
                    logger.warning(f"Клас графа {gdata['class']} не знайдено у graph_class_map")
                    continue
                g = cls()
                g.name = gdata.get('name')
                g.directed = gdata.get('directed')
                node_map = {}
                # Відновлюємо вузли
                for n in gdata.get('nodes', []):
                    node = Node(n['id'], n.get('data'), n.get('pos'))
                    g.add_node(node)
                    node_map[n['id']] = node
                # Відновлюємо ребра
                for e in gdata.get('edges', []):
                    src = node_map.get(e['source'])
                    tgt = node_map.get(e['target'])
                    if not src or not tgt:
                        logger.warning(f"Не знайдено вузли для ребра: {e}")
                        continue
                    if g.directed:
                        edge = DirectedEdge(src, tgt, e.get('weight', 1), e.get('data'))
                    else:
                        edge = UndirectedEdge(src, tgt, e.get('weight', 1), e.get('data'))
                    g.add_edge(edge)
                graphs.append(g)
            logger.info(f"Сесію успішно імпортовано з файлу: {filepath}")
            return graphs
        except Exception as e:
            logger.error(f"Помилка при імпорті сесії: {e}")
            return []
