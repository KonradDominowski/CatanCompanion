from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QSizePolicy

from MainWindow import MainWindow
from Widgets.Buttons.ReturnButton import ReturnButton


class NewGamePage(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.index = 1
        background = QWidget(self)
        background.resize(main_window.size().width() - 18, main_window.size().height() - 18)
        background.setStyleSheet("background-color: rgba(0, 0, 0, 0.7); border-radius: 50px")
        background.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return_button = ReturnButton(main_window, self)
        return_button.clicked.connect(
            lambda _: main_window.slide_to_page(self.index, 0, 'right'))

        # Ensure layout is recalculated after widget size is set
        QTimer.singleShot(0, self.adjustSize)
