from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QSizePolicy

from MainWindow import MainWindow
from Widgets.Buttons.ReturnButton import ReturnButton


class NewGamePage(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.main_window = main_window
        self.index = 1
        self.background = QWidget(self)
        self.background.setStyleSheet("background-color: rgba(0, 0, 0, 0.6); border-radius: 50px")
        self.background.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return_button = ReturnButton(main_window, self)
        return_button.clicked.connect(
            lambda _: main_window.slide_to_page(self.index, 0, 'right'))

    def adjust_size(self):
        self.background.resize(self.main_window.size().width() - 18, self.main_window.size().height() - 18)
        QTimer.singleShot(0, self.adjustSize)
