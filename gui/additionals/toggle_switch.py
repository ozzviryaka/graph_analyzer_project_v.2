from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush

class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, checked=False):
        super().__init__(parent)
        self.setFixedSize(50, 27)
        self._checked = checked
        self.setCursor(Qt.PointingHandCursor)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.toggled.emit(self._checked)
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self._checked)
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Background
        bg_color = QColor(170, 170, 170) if not self._checked else QColor(100, 200, 100)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        rect = QRectF(2, 2, self.width()-4, self.height()-4)
        painter.drawRoundedRect(rect, self.height()/2, self.height()/2)
        # Handle
        handle_radius = self.height() - 8
        handle_x = 4 if not self._checked else self.width() - handle_radius - 4
        painter.setBrush(QBrush(Qt.white))
        painter.drawEllipse(handle_x, 4, handle_radius, handle_radius)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self.size()
