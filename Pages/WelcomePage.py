from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QGridLayout

from MainWindow import MainWindow
from Widgets.Buttons.ShowPreviewButton import ShowPreviewButton
from Widgets.Buttons.NewGameButton import NewGameButton
from Widgets.Logo import Logo


class WelcomePage(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.main_window = main_window

        logo = Logo()
        new_game_button = NewGameButton()
        preview_button = ShowPreviewButton("Show preview")

        grid = QGridLayout()
        grid.addWidget(logo, 0, 0)
        grid.addWidget(new_game_button, 2, 0, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(preview_button, 3, 0, 2, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(grid)

        new_game_button.clicked.connect(self.start_new_game)

    def start_new_game(self):
        self.main_window.pages_layout.setCurrentIndex(1)
