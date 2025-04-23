from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton

from MainWindow import MainWindow


class ReturnButton(QToolButton):
    def __init__(self, main_window: MainWindow, target_index: int, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.move(10, 10)
        self.setFixedSize(75, 75)

        self.setIcon(QIcon("./assets/left_arrow.svg"))
        self.setIconSize(QSize(self.height(), self.width()))
        self.setStyleSheet(f"border-radius: {self.height() / 2}")

        self.clicked.connect(
            lambda i: self.main_window.pages_layout.setCurrentIndex(target_index)
        )
