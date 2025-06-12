from utils.logger import Logger

class Node:
    """
    Клас, що представляє вузол (вершину) графа.
    """

    def __init__(self, node_id, data=None, pos=None):
        """
        Ініціалізує вузол з унікальним ідентифікатором та додатковими даними.

        :param node_id: Унікальний ідентифікатор вузла
        :param data: Додаткові дані, пов'язані з вузлом (за замовчуванням None)
        """
        self.id = node_id
        self.data = data if data is not None else {}
        self.pos = pos  # координати (x, y) або None

        Logger().info(f"Створено вузол: id={self.id}, data={self.data}, pos={self.pos}")

    def __repr__(self):
        return f"Node(id={self.id}, data={self.data}, pos={self.pos})"

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos