from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QPainter, QPolygon, QColor, QRegion
from PySide6.QtCore import QPoint, Qt


class RhombusFrame(QFrame):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self._color = QColor(color)
        self.setFixedSize(120, 7)  # Kwadrat o rozmiarze 60x60

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        points = [
            QPoint(2 * h, 0),      # lewy górny róg
            QPoint(w, 0),      # prawy górny róg
            QPoint(w - 2 * h, h),      # prawy dolny róg
            QPoint(0, h),      # lewy dolny róg
        ]
        polygon = QPolygon(points)

        self.setMask(QRegion(polygon))  # Maska kwadratu
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(self._color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(polygon)
