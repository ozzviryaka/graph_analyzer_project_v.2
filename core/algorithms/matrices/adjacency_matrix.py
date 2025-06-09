class AdjacencyMatrix:
    """
    Клас для створення та отримання матриці суміжності графа.
    """

    def __init__(self, graph):
        self.graph = graph
        self.nodes = list(graph.nodes())
        self.node_id_to_index = {node.id: idx for idx, node in enumerate(self.nodes)}
        self.matrix = self._build_matrix()

    def _build_matrix(self):
        n = len(self.nodes)
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for edge in self.graph.edges():
            i = self.node_id_to_index[edge.source.id]
            j = self.node_id_to_index[edge.target.id]
            value = edge.weight(self.graph.is_weighted())

            matrix[i][j] += value
            # Якщо граф неспрямований — симетрично
            if not getattr(self.graph, "is_directed", lambda: False)():
                matrix[j][i] += value

        return matrix

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        print("    ", end="")
        for node in self.nodes:
            print(f"{str(node.id):>3}", end=" ")
        print()
        for i, node in enumerate(self.nodes):
            print(f"{str(node.id):>3}", end=" ")
            for val in self.matrix[i]:
                print(f"{val:3}", end=" ")
            print()