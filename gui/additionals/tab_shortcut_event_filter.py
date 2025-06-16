from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QApplication

class TabShortcutEventFilter(QObject):
    """
    Фільтр для відстеження натиску Alt+1, Alt+2, ... Alt+9 для перемикання вкладок.
    """
    def __init__(self, main_window, tab_widget):
        super().__init__(main_window)
        self.main_window = main_window
        self.tab_widget = tab_widget

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress and event.modifiers() & Qt.AltModifier:
            key = event.key()
            if Qt.Key_1 <= key <= Qt.Key_9:
                idx = key - Qt.Key_1
                if idx < self.tab_widget.count():
                    self.tab_widget.setCurrentIndex(idx)
                    return True
        return super().eventFilter(obj, event)
