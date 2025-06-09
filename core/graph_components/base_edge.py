from abc import ABC, abstractmethod

class BaseEdge(ABC):
    """
    Абстрактний базовий клас для ребра графа.
    """

    @abstractmethod
    def __init__(self, source, target, data=None):
        """
        Ініціалізує ребро між двома вузлами.

        :param source: Вершина-джерело
        :param target: Вершина-призначення
        :param data: Додаткові дані, пов'язані з ребром (за замовчуванням None)
        """
        self.source = source
        self.target = target
        self.data = data if data is not None else {}

    @abstractmethod
    def weight(self):
        """
        Повертає вагу ребра (якщо застосовується).
        """
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(source={self.source}, target={self.target}, data={self.data})"