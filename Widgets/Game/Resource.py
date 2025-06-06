from enum import Enum

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget


class ResourceType(Enum):
    WOOD = 'wood'
    BRICK = 'brick'
    WHEAT = 'wheat'
    SHEEP = 'sheep'
    ORE = 'ore'


class Resource(QWidget):
    def __init__(self, resource_type: ResourceType, parent=None):
        super().__init__(parent)

        size = 50

        self.setFixedSize(size, size)  # STAŁY rozmiar widoczny w layoucie

        self.type = resource_type
        # self.icon_path = f"./assets/res_{self.type.value}.png"
        self.icon_path = f"./assets/res_{self.type.value}_glow_subtle.png"

        # QLabel wewnątrz - będzie animowany
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap(self.icon_path))
        self.icon_label.setScaledContents(True)
        self.icon_label.setGeometry(10, 10, 0, 0)  # Start w centrum

        # Animacja rozmiaru QLabel (geometry)
        self.animation = QPropertyAnimation(self.icon_label, b"geometry")
        self.animation.setDuration(750)
        # self.animation.setStartValue(QRect(margin, margin, start_size, start_size))
        self.animation.setEndValue(QRect(0, 0, size, size))  # rozciąga się do pełnego rozmiaru rodzica
        self.animation.setEasingCurve(QEasingCurve.Type.OutBack)

    def resize_icon(self):
        self.icon_label.setPixmap(QPixmap(self.icon_path).scaled(
            self.size(),
            aspectMode=Qt.AspectRatioMode.KeepAspectRatio,
            mode=Qt.TransformationMode.SmoothTransformation
        ))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_icon()

    def get_animation(self):
        return self.animation
