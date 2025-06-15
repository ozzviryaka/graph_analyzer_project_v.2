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
            # Серіалізуємо вузли та ребра у прості словники
            nodes = []
            for n in g.nodes():
                nodes.append({
                    'id': getattr(n, 'id', None),
                    'data': getattr(n, 'data', None),
                    'pos': getattr(n, 'pos', None)
                })
            edges = []
            for e in g.edges():
                edges.append({
                    'source': getattr(e, 'source').id if hasattr(e, 'source') else None,
                    'target': getattr(e, 'target').id if hasattr(e, 'target') else None,
                    'weight': getattr(e, '_weight', None),
                    'data': getattr(e, 'data', None)
                })
            session_data.append({
                'class': g.__class__.__name__,
                'name': getattr(g, 'name', None),
                'directed': getattr(g, 'directed', None),
                'nodes': nodes,
                'edges': edges,
            })
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
