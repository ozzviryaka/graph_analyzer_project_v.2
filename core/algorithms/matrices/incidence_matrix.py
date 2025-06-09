class IncidenceMatrix:
    """
    Клас для створення та отримання матриці інцидентності графа.
    """

    def __init__(self, graph):
        self.graph = graph
        self.nodes = list(graph.nodes())
        self.edges = list(graph.edges())
        self.node_id_to_index = {node.id: idx for idx, node in enumerate(self.nodes)}
        self.matrix = self._build_matrix()

    def _build_matrix(self):
        n = len(self.nodes)
        m = len(self.edges)
        matrix = [[0 for _ in range(m)] for _ in range(n)]

        for j, edge in enumerate(self.edges):
            source_idx = self.node_id_to_index[edge.source.id]
            target_idx = self.node_id_to_index[edge.target.id]
            if hasattr(edge, "weight"):
                value = edge.weight()
            else:
                value = 1

            # Для спрямованого графа: -1 для джерела, +1 для цілі
            # Для неспрямованого: +1 для обох
            if getattr(self.graph, "is_directed", lambda: False)():
                matrix[source_idx][j] = -value
                matrix[target_idx][j] = value
            else:
                matrix[source_idx][j] = value
                matrix[target_idx][j] = value

        return matrix

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        print("   ", end="")
        for j in range(len(self.edges)):
            print(f"e{j+1:2}", end=" ")
        print()
        for i, node in enumerate(self.nodes):
            print(f"{str(node.id):>3}", end=" ")
            for val in self.matrix[i]:
                print(f"{val:2}", end="  ")
            print()