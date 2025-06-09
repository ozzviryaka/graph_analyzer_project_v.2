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
            "Кількість вершин": self.num_nodes(),
            "Кількість ребер": self.num_edges(),
            "Мінімальний ступінь": self.min_degree(),
            "Максимальний ступінь": self.max_degree(),
            "Середній ступінь": self.avg_degree(),
            "Зв'язний граф": "Так" if self.is_connected() else "Ні",
            "Структурна надмірність": self.structural_redundancy(),
            "Нерівномірність розподілу зв'язків": self.degree_inequality(),
            "Структурна компактність": self.structural_compactness(),
            "Відносний показник компактності": self.relative_compactness(),
            "Ступінь централізації": self.degree_centralization()
        }