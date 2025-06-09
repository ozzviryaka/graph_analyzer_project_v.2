from abc import ABC, abstractmethod

class BaseGraph(ABC):
    """
    Абстрактний базовий клас для графа.
    """

    @abstractmethod
    def add_node(self, node):
        """
        Додає вузол до графа.
        """
        pass

    @abstractmethod
    def add_edge(self, edge):
        """
        Додає ребро до графа.
        """
        pass

    @abstractmethod
    def nodes(self):
        """
        Повертає ітератор по всіх вузлах графа.
        """
        pass

    @abstractmethod
    def edges(self):
        """
        Повертає ітератор по всіх ребрах графа.
        """
        pass

    @abstractmethod
    def neighbors(self, node):
        """
        Повертає сусідів заданого вузла.
        """
        pass