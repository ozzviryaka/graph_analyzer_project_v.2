from .base_edge import BaseEdge
from utils.logger import Logger

class UndirectedEdge(BaseEdge):
    """
    Клас для неспрямованого ребра графа.
    """

    def __init__(self, node1, node2, weight=1, data=None):
        """
        Ініціалізує неспрямоване ребро між двома вузлами.

        :param node1: Перша вершина
        :param node2: Друга вершина
        :param weight: Вага ребра (за замовчуванням 1)
        :param data: Додаткові дані, пов'язані з ребром (за замовчуванням None)
        """
        super().__init__(node1, node2, data)
        self._weight = weight

        Logger().info(
            f"Створено неспрямоване ребро: node1={self.source.id}, node2={self.target.id}, weight={self._weight}, data={self.data}"
        )

    def weight(self):
        """
        Повертає вагу ребра.
        """
        return self._weight

    def __eq__(self, other):
        """
        Перевіряє рівність ребер незалежно від порядку вузлів.
        """
        if not isinstance(other, UndirectedEdge):
            return False
        return {self.source, self.target} == {other.source, other.target} and self._weight == other._weight

    def __hash__(self):
        """
        Хеш для використання в множинах та словниках.
        """
        return hash(frozenset([self.source, self.target])) ^ hash(self._weight)