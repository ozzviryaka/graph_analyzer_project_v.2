import json
from copy import deepcopy

class SessionExporter:
    @staticmethod
    def export_session(graphs, filepath):
        """
        graphs: список графів (об'єктів Graph/DirectedGraph/UndirectedGraph)
        filepath: шлях до файлу для збереження сесії
        """
        session_data = []
        for g in graphs:
            session_data.append({
                'class': g.__class__.__name__,
                'name': getattr(g, 'name', None),
                'directed': getattr(g, 'directed', None),
                'nodes': [n.__dict__ for n in g.nodes()],
                'edges': [e.__dict__ for e in g.edges()],
            })
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
