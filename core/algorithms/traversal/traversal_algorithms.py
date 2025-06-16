"""
Модуль для алгоритмів обходу графа: BFS, DFS, Dijkstra, пошук компонентів зв'язності, виявлення циклів.
Всі функції повертають повний порядок обходу вершин.
"""
from collections import deque
import heapq

class GraphTraversal:
    """
    Клас для алгоритмів обходу графа: BFS, DFS, Dijkstra, пошук компонентів зв'язності, виявлення циклів.
    Всі методи повертають повний порядок обходу вершин (або відповідний результат).
    """
    @staticmethod
    def bfs(graph, start_id):
        visited = set()
        order = []
        queue = deque([start_id])
        while queue:
            node_id = queue.popleft()
            if node_id not in visited:
                visited.add(node_id)
                order.append(node_id)
                for neighbor in graph.neighbors(node_id):
                    if neighbor.id not in visited:
                        queue.append(neighbor.id)
        return order

    @staticmethod
    def dfs(graph, start_id):
        visited = set()
        order = []
        stack = [start_id]
        while stack:
            node_id = stack.pop()
            if node_id not in visited:
                visited.add(node_id)
                order.append(node_id)
                for neighbor in reversed(list(graph.neighbors(node_id))):
                    if neighbor.id not in visited:
                        stack.append(neighbor.id)
        return order

    @staticmethod
    def dijkstra(graph, start_id):
        visited = set()
        order = []
        heap = [(0, start_id)]
        while heap:
            dist, node_id = heapq.heappop(heap)
            if node_id not in visited:
                visited.add(node_id)
                order.append(node_id)
                for neighbor in graph.neighbors(node_id):
                    if neighbor.id not in visited:
                        weight = graph.get_edge_weight(node_id, neighbor.id)
                        heapq.heappush(heap, (dist + weight, neighbor.id))
        return order

    @staticmethod
    def connected_components(graph):
        visited = set()
        components = []
        for node in graph.nodes():
            if node.id not in visited:
                comp = []
                queue = deque([node.id])
                while queue:
                    nid = queue.popleft()
                    if nid not in visited:
                        visited.add(nid)
                        comp.append(nid)
                        for neighbor in graph.neighbors(nid):
                            if neighbor.id not in visited:
                                queue.append(neighbor.id)
                components.append(comp)
        return components

    @staticmethod
    def has_cycle(graph):
        """
        Повертає кортеж (order, cycles), де order — повний порядок обходу,
        cycles — список циклів (кожен цикл — список id вершин).
        """
        visited = set()
        parent = {}
        order = []
        cycles = []
        path = []
        def dfs_cycle(u, p):
            visited.add(u)
            order.append(u)
            path.append(u)
            for neighbor in graph.neighbors(u):
                v = neighbor.id
                if v not in visited:
                    parent[v] = u
                    dfs_cycle(v, u)
                elif parent.get(u) != v and v in path:
                    # Знайдено цикл
                    idx = path.index(v)
                    cycle = path[idx:] + [v]
                    if cycle not in cycles:
                        cycles.append(cycle)
            path.pop()
        for node in graph.nodes():
            if node.id not in visited:
                parent[node.id] = None
                dfs_cycle(node.id, None)
        return order, cycles
