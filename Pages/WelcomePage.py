from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout

from MainWindow import MainWindow
from Pages.Page import Page
from Widgets.Buttons.NewGameButton import NewGameButton
from Widgets.Buttons.ShowPreviewButton import ShowPreviewButton
from Widgets.Logo import Logo


class WelcomePage(Page):
    def __init__(self, main_window: MainWindow):
        super().__init__(main_window)

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
        self.main_window.slide_to_page(from_index=self.index,
                                       to_index=self.main_window.new_game_page.index,
                                       direction="left")
