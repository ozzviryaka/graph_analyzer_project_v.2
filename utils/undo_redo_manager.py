class UndoRedoManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        self._is_enabled = True

    def push(self, action, inverse_action):
        if not self._is_enabled:
            return
        self.undo_stack.append((action, inverse_action))
        self.redo_stack.clear()

    def undo(self):
        if not self.can_undo():
            return
        action, inverse_action = self.undo_stack.pop()
        self._is_enabled = False
        inverse_action()
        self._is_enabled = True
        self.redo_stack.append((action, inverse_action))

    def redo(self):
        if not self.can_redo():
            return
        action, inverse_action = self.redo_stack.pop()
        self._is_enabled = False
        action()
        self._is_enabled = True
        self.undo_stack.append((action, inverse_action))

    def can_undo(self):
        return len(self.undo_stack) > 0

    def can_redo(self):
        return len(self.redo_stack) > 0
