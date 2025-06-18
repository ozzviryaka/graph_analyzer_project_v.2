"""
Модуль для алгоритмів обходу графа: BFS, DFS, Dijkstra, пошук компонентів зв'язності, виявлення циклів.
Всі функції повертають повний порядок обходу вершин.
"""
from collections import deque
import heapq
from utils.logger import Logger
from locales.locale_manager import LocaleManager

class GraphTraversal:
    """
    Клас для алгоритмів обходу графа: BFS, DFS, Dijkstra, пошук компонентів зв'язності, виявлення циклів.
    Всі методи повертають повний порядок обходу вершин (або відповідний результат).
    """
    logger = Logger()

    @staticmethod
    def bfs(graph, start_id):
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "bfs_start").format(start_id=start_id))
        visited = set()
        order = []
        queue = deque([start_id])
        while queue:
            node_id = queue.popleft()
            if node_id not in visited:
                visited.add(node_id)
                order.append(node_id)
                GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "bfs_update").format(node_id=node_id))
                for neighbor in graph.neighbors(node_id):
                    if neighbor.id not in visited:
                        queue.append(neighbor.id)
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "bfs_end").format(order=order))
        return order

    @staticmethod
    def dfs(graph, start_id):
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "dfs_start").format(start_id=start_id))
        visited = set()
        order = []
        stack = [start_id]
        while stack:
            node_id = stack.pop()
            if node_id not in visited:
                visited.add(node_id)
                order.append(node_id)
                GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "dfs_update").format(node_id=node_id))
                for neighbor in reversed(list(graph.neighbors(node_id))):
                    if neighbor.id not in visited:
                        stack.append(neighbor.id)
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "bfs_end").format(order=order))
        return order

    @staticmethod
    def dijkstra(graph, start_id):
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "dijkstra_start").format(start_id=start_id))
        visited = set()
        order = []
        heap = [(0, start_id)]
        while heap:
            dist, node_id = heapq.heappop(heap)
            if node_id not in visited:
                visited.add(node_id)
                order.append(node_id)
                GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "dijkstra_update").format(node_id=node_id, dist=dist))
                for neighbor in graph.neighbors(node_id):
                    if neighbor.id not in visited:
                        weight = graph.get_edge_weight(node_id, neighbor.id)
                        heapq.heappush(heap, (dist + weight, neighbor.id))
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "dijkstra_end").format(order=order))
        return order

    @staticmethod
    def connected_components(graph):
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "comp_start"))
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
                GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "comp_update").format(comp=comp))
                components.append(comp)
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "comp_end").format(len_components=len(components)))
        return components

    @staticmethod
    def has_cycle(graph):
        """
        Повертає кортеж (order, cycles), де order — повний порядок обходу,
        cycles — список циклів (кожен цикл — список id вершин).
        """
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "cycle_start"))
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
                        GraphTraversal.logger.warning(LocaleManager.get_locale("traversal_algorithms", "cycle_update").format(cycle=cycle))
            path.pop()
        for node in graph.nodes():
            if node.id not in visited:
                parent[node.id] = None
                dfs_cycle(node.id, None)
        GraphTraversal.logger.info(LocaleManager.get_locale("traversal_algorithms", "cycle_end").format(order=order, len_cycles=len(cycles)))
        return order, cycles
