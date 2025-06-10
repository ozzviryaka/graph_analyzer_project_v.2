from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge
from utils.logger import Logger

class EdgeConverter:
    """
    Клас для конвертації спрямованого ребра у неспрямоване та навпаки.
    """

    @staticmethod
    def directed_to_undirected(directed_edge, weighted=True):
        """
        Конвертує спрямоване ребро у неспрямоване.

        :param directed_edge: Об'єкт DirectedEdge
        :param weighted: Чи враховувати вагу (True/False)
        :return: Об'єкт UndirectedEdge
        """
        if not isinstance(directed_edge, DirectedEdge):
            Logger().error("Передане ребро не є спрямованим.")
            raise TypeError("Передане ребро не є спрямованим.")

        undirected_edge = UndirectedEdge(
            directed_edge.source,
            directed_edge.target,
            weight=directed_edge.weight(True),
            data=directed_edge.data
        )
        Logger().info(
            f"Конвертовано спрямоване ребро ({directed_edge.source.id} -> {directed_edge.target.id}) у неспрямоване."
        )
        return undirected_edge

    @staticmethod
    def undirected_to_directed(undirected_edge, source_first=True, weighted=True):
        """
        Конвертує неспрямоване ребро у спрямоване.

        :param undirected_edge: Об'єкт UndirectedEdge
        :param source_first: Якщо True, source=node1, target=node2, інакше навпаки
        :param weighted: Чи враховувати вагу (True/False)
        :return: Об'єкт DirectedEdge
        """
        if not isinstance(undirected_edge, UndirectedEdge):
            Logger().error("Передане ребро не є неспрямованим.")
            raise TypeError("Передане ребро не є неспрямованим.")

        source = undirected_edge.source if source_first else undirected_edge.target
        target = undirected_edge.target if source_first else undirected_edge.source

        directed_edge = DirectedEdge(
            source,
            target,
            weight=undirected_edge.weight(True),
            data=undirected_edge.data
        )
        Logger().info(
            f"Конвертовано неспрямоване ребро ({undirected_edge.source.id} -- {undirected_edge.target.id}) у спрямоване ({source.id} -> {target.id})."
        )
        return directed_edge