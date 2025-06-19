from locales.locale_manager import LocaleManager

class GraphInfo:
    """
    Клас для отримання характеристик графа.
    """

    def __init__(self, graph):
        self.graph = graph
        self._degrees = None

    def num_nodes(self):
        return sum(1 for _ in self.graph.nodes())

    def num_edges(self):
        return sum(1 for _ in self.graph.edges())

    def degrees(self):
        if self._degrees is None:
            self._degrees = [sum(1 for _ in self.graph.neighbors(node)) for node in self.graph.nodes()]
        return self._degrees

    def min_degree(self):
        degs = self.degrees()
        return min(degs) if degs else 0

    def max_degree(self):
        degs = self.degrees()
        return max(degs) if degs else 0

    def avg_degree(self):
        degs = self.degrees()
        return sum(degs) / len(degs) if degs else 0

    def is_connected(self):
        nodes = list(self.graph.nodes())
        if not nodes:
            return True
        visited = set()
        stack = [nodes[0]]
        while stack:
            node = stack.pop()
            if node.id not in visited:
                visited.add(node.id)
                stack.extend(n for n in self.graph.neighbors(node) if n.id not in visited)
        return len(visited) == self.num_nodes()

    def structural_redundancy(self):
        n = self.num_nodes()
        m = self.num_edges()
        if n <= 1:
            return 0
        return (m - (n - 1)) / (n - 1)

    def degree_inequality(self):
        degs = self.degrees()
        if not degs:
            return 0
        avg = self.avg_degree()
        return sum(abs(d - avg) for d in degs) / len(degs)

    def structural_compactness(self):
        n = self.num_nodes()
        m = self.num_edges()
        if n <= 1:
            return 0
        return m / (n * (n - 1) / 2) if n > 1 else 0

    def relative_compactness(self):
        n = self.num_nodes()
        m = self.num_edges()
        if n <= 2:
            return 0
        max_edges = n * (n - 1) / 2
        min_edges = n - 1
        if max_edges == min_edges:
            return 1
        return (m - min_edges) / (max_edges - min_edges)

    def degree_centralization(self):
        degs = self.degrees()
        if not degs:
            return 0
        max_deg = max(degs)
        n = len(degs)
        denom = (n - 1) * (n - 2)
        if denom == 0:
            return 0
        return sum(max_deg - d for d in degs) / denom

    def get_all_info(self):
        return {
            LocaleManager.get_locale("graph_info", "num_nodes"): self.num_nodes(),
            LocaleManager.get_locale("graph_info", "num_edges"): self.num_edges(),
            LocaleManager.get_locale("graph_info", "min_degree"): self.min_degree(),
            LocaleManager.get_locale("graph_info", "max_degree"): self.max_degree(),
            LocaleManager.get_locale("graph_info", "avg_degree"): self.avg_degree(),
            LocaleManager.get_locale("graph_info", "is_connected"): LocaleManager.get_locale("graph_info", "yes") if self.is_connected() else LocaleManager.get_locale("graph_info", "no"),
            LocaleManager.get_locale("graph_info", "structural_redundancy"): self.structural_redundancy(),
            LocaleManager.get_locale("graph_info", "degree_inequality"): self.degree_inequality(),
            LocaleManager.get_locale("graph_info", "structural_compactness"): self.structural_compactness(),
            LocaleManager.get_locale("graph_info", "relative_compactness"): self.relative_compactness(),
            LocaleManager.get_locale("graph_info", "degree_centralization"): self.degree_centralization()
        }