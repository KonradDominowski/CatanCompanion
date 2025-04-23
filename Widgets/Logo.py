from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class Logo(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumHeight(250)

        image_label = QLabel(self)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        original_pixmap = QPixmap("./assets/catan_logo.png")
        scaled_pixmap = original_pixmap.scaledToWidth(600, Qt.SmoothTransformation)

        image_label.setPixmap(scaled_pixmap)

        layout = QVBoxLayout()
        layout.addWidget(image_label)
        self.setLayout(layout)
        self.setContentsMargins(0, 20, 0, 0)
