from PySide6.QtWidgets import QWidget

from MainWindow import MainWindow
from Widgets.Buttons.ReturnButton import ReturnButton


class NewGamePage(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()

        return_button = ReturnButton(main_window, 0, self)
