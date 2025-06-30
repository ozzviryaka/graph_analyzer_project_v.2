from core.graph_components.directed_edge import DirectedEdge
from core.graph_components.undirected_edge import UndirectedEdge
from utils.logger import Logger
from locales.locale_manager import LocaleManager

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
            Logger().error(LocaleManager.get_locale("edge_converter", "not_directed_error"))
            raise TypeError(LocaleManager.get_locale("edge_converter", "not_directed_error"))

        undirected_edge = UndirectedEdge(
            directed_edge.source,
            directed_edge.target,
            weight=directed_edge.weight(True),
            data=directed_edge.data
        )
        Logger().info(
            LocaleManager.get_locale("edge_converter", "directed_to_undirected_info").format(source_id=directed_edge.source, target_id=directed_edge.target))
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
            Logger().error(LocaleManager.get_locale("edge_converter", "not_undirected_error"))
            raise TypeError(LocaleManager.get_locale("edge_converter", "not_undirected_error"))

        source = undirected_edge.source if source_first else undirected_edge.target
        target = undirected_edge.target if source_first else undirected_edge.source

        directed_edge = DirectedEdge(
            source,
            target,
            weight=undirected_edge.weight(True),
            data=undirected_edge.data
        )
        Logger().info(
            LocaleManager.get_locale("edge_converter", "undirected_to_directed_info").format(source_id=undirected_edge.source, target_id=undirected_edge.target,new_source_id=source, new_target_id=target))
        
        return directed_edge