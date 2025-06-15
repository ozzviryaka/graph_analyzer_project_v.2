from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject
from utils.undo_redo_manager import UndoRedoManager

class UndoRedoEventFilter(QObject):
    def __init__(self, canvas, manager=None, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.manager = manager if manager is not None else UndoRedoManager()
        self._install(canvas)

    def _install(self, widget):
        widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        from PyQt5.QtCore import Qt
        if event.type() == event.KeyPress:
            if event.modifiers() == Qt.ControlModifier:
                if event.key() == Qt.Key_Z:
                    self.manager.undo()
                    self.canvas.update()
                    return True
                elif event.key() == Qt.Key_Y:
                    self.manager.redo()
                    self.canvas.update()
                    return True
        return False
