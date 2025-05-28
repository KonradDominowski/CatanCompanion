from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel

from Catan.Game import Game
from Catan.PlayerColor import PlayerColor
from MainWindow import MainWindow
from Pages.Page import Page
from Widgets.Buttons.ReturnButton import ReturnButton
from Widgets.Player import Player


class GamePage(Page):
    def __init__(self, main_window: MainWindow):
        super().__init__(main_window)

        # Background
        self.background = QWidget(self)
        self.background.setObjectName("background")
        self.background.setStyleSheet("""
                    QWidget#background {
                        background-color: rgba(0, 0, 0, 0.6);
                        border-radius: 50px;
                    }
                """)
        self.background.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.return_button = ReturnButton(main_window, self)
        self.return_button.clicked.connect(self.end_game)

        # Game
        self.game: None | Game = None
        self.main_window.new_game_page.new_game_started.connect(self.new_game)

        # Layout
        self.layout = None

    def adjust_size(self):
        self.background.resize(self.main_window.size().width() - 18, self.main_window.size().height() - 18)
        super().adjust_size()

    def new_game(self, players: dict[PlayerColor, str]):
        self.game = Game(players)
        self.setup_game_ui()

    def setup_game_ui(self):
        self.game.get_players()

        self.layout = QVBoxLayout(self)

        top_bar = QLabel('Bin')
        top_bar.setStyleSheet("border: 1px solid rgba(255,255,255, 0.25)")
        top_bar.setFixedHeight(85)
        self.layout.addWidget(top_bar)

        for color, player in self.game.get_players().items():
            player = Player(color, player)
            self.layout.addWidget(player)

        self.setLayout(self.layout)
        self.return_button.raise_()  # Przenosi return_button ponad dodane widgety

    def end_game(self):
        self.game = None
        self.layout = None
        self.main_window.slide_to_page(self.index, 1, 'right')
