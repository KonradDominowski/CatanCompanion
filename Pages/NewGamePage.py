from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QPushButton, QVBoxLayout

from MainWindow import MainWindow
from Pages.Page import Page
from Widgets.Buttons.ReturnButton import ReturnButton
from Widgets.Camera.Preview import Preview
from Widgets.PlayerName import PlayerName


class NewGamePage(Page):
    def __init__(self, main_window: MainWindow):
        super().__init__(main_window)

        self.background = QWidget(self)
        self.background.setObjectName("background")
        self.background.setStyleSheet("""
            QWidget#background {
                background-color: rgba(0, 0, 0, 0.6);
                border-radius: 50px;
            }
        """)
        self.background.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return_button = ReturnButton(main_window, self)
        return_button.clicked.connect(
            lambda _: main_window.slide_to_page(self.index, 0, 'right'))

        # Layout
        grid_layout = QGridLayout()  # Grid 16 x 11

        # Players form
        players = QWidget()
        players.setObjectName('players')

        layout = QVBoxLayout()
        for color in ['white', 'orange', 'blue', 'red']:
            layout.addWidget(PlayerName(color))

        players.setLayout(layout)

        # Preview
        self.preview_container = QWidget()

        start_game_button = QPushButton("New Game")
        start_game_button.setObjectName('start_game_button')
        start_game_button.setStyleSheet("""
          QPushButton#start_game_button {
             background-color: white;
             font-family: arno;
          }""")

        spacer = QWidget()
        spacer.setVisible(False)

        grid_layout.addWidget(spacer, 0, 0, 2, 2)
        grid_layout.addWidget(players, 2, 0, 14, 6)
        grid_layout.addWidget(self.preview_container, 2, 6, 12, 6)
        grid_layout.addWidget(start_game_button, 14, 9, 2, 3)

        preview_layout = QVBoxLayout()
        self.preview_label = Preview()
        preview_layout.addWidget(self.preview_label)
        self.preview_container.setLayout(preview_layout)

        self.background.setLayout(grid_layout)

    def adjust_size(self):
        self.background.resize(self.main_window.size().width() - 18, self.main_window.size().height() - 18)
        super().adjust_size()
