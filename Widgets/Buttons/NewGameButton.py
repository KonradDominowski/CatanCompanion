from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton


class NewGameButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Start a new game")
        self.setObjectName('NewGameButton')
        self.setFixedSize(QSize(400, 90))
        self.setStyleSheet(f"border-radius: {int(self.height() / 2)}")
