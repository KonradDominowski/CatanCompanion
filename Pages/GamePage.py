from PySide6.QtCore import Qt, QPropertyAnimation, QTimer
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from Catan.Game import Game
from Catan.PlayerColor import PlayerColor
from MainWindow import MainWindow
from Pages.Page import Page
from Widgets.Buttons.ReturnButton import ReturnButton
from Widgets.Game.Resource import ResourceType
from Widgets.Player import Player
from utils import sort_resource_counts_desc, empty_resources_dict


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

        # Return button
        self.return_button = ReturnButton(main_window, self)
        self.return_button.clicked.connect(self.end_game)

        # Game
        self.game: None | Game = None
        self.main_window.new_game_page.new_game_started.connect(self.new_game)
        self.players: list[Player] = []

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

        # Top bar
        top_bar = QLabel('Bin')
        top_bar.setLayout(QHBoxLayout())
        top_bar.layout().setAlignment(Qt.AlignmentFlag.AlignRight)
        top_bar.setStyleSheet("border: 1px solid rgba(255,255,255, 0.25)")
        top_bar.setFixedHeight(85)
        self.layout.addWidget(top_bar)

        # Reset button - now for development and testing
        reset_button = QPushButton('Reset')
        reset_button.setStyleSheet("color:black; background: white; padding: 5px ")
        reset_button.clicked.connect(self.clear_all_resources)
        top_bar.layout().addWidget(reset_button)

        # Show resources - now for development and testing
        show_resources_button = QPushButton("Show resources")
        show_resources_button.setStyleSheet("color:black; background: white; padding: 5px ")
        show_resources_button.clicked.connect(lambda _: self.show_all_resources())
        top_bar.layout().addWidget(show_resources_button)

        # Players
        for color, player in self.game.get_players().items():
            player = Player(color, player)
            self.players.append(player)
            self.layout.addWidget(player)

        self.setLayout(self.layout)
        self.return_button.raise_()  # Przenosi return_button ponad dodane widgety

        self.show_all_resources()

    def end_game(self):
        # TODO - layout się nie usuwa, trzeba to jako rozwiązać
        self.game = None
        self.layout = None
        self.main_window.slide_to_page(self.index, self.main_window.new_game_page.index, 'right')

    def clear_all_resources(self):
        for player in self.players:
            player.clear_resources()

    def show_all_resources(self):
        animations: list[QPropertyAnimation] = []

        color_resources = empty_resources_dict(self.game.get_colors())

        color_resources['white'].update({
            ResourceType.SHEEP: 5,
            ResourceType.WOOD: 3
        })
        color_resources[PlayerColor.ORANGE][ResourceType.ORE] = 4

        # Sorting to display resources from most to least abundant
        sorted_dict = sort_resource_counts_desc(color_resources)

        for player in self.players:
            player.show_resources(sorted_dict.get(player.get_color()))
            animations.extend(player.get_animations())

        for i, anim in enumerate(animations):
            QTimer.singleShot(i * 10, anim.start)

        if animations:
            animations[-1].finished.connect(animations.clear())
