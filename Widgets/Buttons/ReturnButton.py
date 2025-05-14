from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolButton

from MainWindow import MainWindow


class ReturnButton(QToolButton):
    def __init__(self, main_window: MainWindow, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.move(15, 15)
        self.setFixedSize(60, 60)

        self.setIcon(QIcon("./assets/left_arrow.svg"))
        self.setIconSize(QSize(self.height(), self.width()))
        self.setStyleSheet(f"border-radius: {self.height() / 2}")
