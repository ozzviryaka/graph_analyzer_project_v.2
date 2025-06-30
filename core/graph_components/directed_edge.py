from .base_edge import BaseEdge
from utils.logger import Logger
from locales.locale_manager import LocaleManager

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
            LocaleManager.get_locale("directed_edge", "created_info").format(
                source_id=self.source.id, target_id=self.target.id, weight=self._weight, data=self.data
            )
        )

    def weight(self, use_weight=True):
        """
        Повертає вагу ребра, або 1 якщо use_weight=False (граф неваговий).
        """
        return self._weight if use_weight else 1