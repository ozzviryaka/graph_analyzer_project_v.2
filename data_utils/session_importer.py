import json

class SessionImporter:
    @staticmethod
    def import_session(filepath, graph_class_map):
        """
        filepath: шлях до файлу сесії
        graph_class_map: dict, наприклад {'Graph': Graph, 'DirectedGraph': DirectedGraph, ...}
        return: список графів
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        graphs = []
        for gdata in session_data:
            cls = graph_class_map.get(gdata['class'])
            if not cls:
                continue
            g = cls()
            g.name = gdata.get('name')
            g.directed = gdata.get('directed')
            # Відновлення вузлів та ребер користувач має реалізувати згідно своєї моделі
            graphs.append(g)
        return graphs
