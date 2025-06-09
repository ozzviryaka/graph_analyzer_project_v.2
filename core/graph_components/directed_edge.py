from .base_edge import BaseEdge
from utils.logger import Logger

class DirectedEdge(BaseEdge):
    """
    Клас для спрямованого ребра графа.
    """

    def __init__(self, source, target, weight=1, data=None):
        """
        Ініціалізує спрямоване ребро між двома вузлами.

        :param source: Вершина-джерело
        :param target: Вершина-призначення
        :param weight: Вага ребра (за замовчуванням 1)
        :param data: Додаткові дані, пов'язані з ребром (за замовчуванням None)
        """
        super().__init__(source, target, data)
        self._weight = weight

        Logger().info(
            f"Створено спрямоване ребро: source={self.source.id}, target={self.target.id}, weight={self._weight}, data={self.data}"
        )

    def weight(self):
        """
        Повертає вагу ребра.
        """
        return self._weight