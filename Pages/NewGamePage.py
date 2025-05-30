from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QPushButton, QVBoxLayout, QLabel

from Catan.PlayerColor import PlayerColor
from MainWindow import MainWindow
from Pages.Page import Page
from Widgets.Buttons.ReturnButton import ReturnButton
from Widgets.Camera.Preview import Preview
from Widgets.PlayerName import PlayerName


class NewGamePage(Page):
    # Using Signal(object) because Signal(dict) may convert keys to str,
    # causing loss of PlayerColor type when the signal is received.
    new_game_started = Signal(object)

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
            lambda _: main_window.slide_to_page(self.index,
                                                self.main_window.welcome_page.index,
                                                'right'))

        # Layout
        grid_layout = QGridLayout()  # Grid 16 x 11

        # Players form
        self.players = QWidget()
        self.players.setObjectName('players')

        layout = QVBoxLayout()
        for color in PlayerColor:
            layout.addWidget(PlayerName(PlayerColor(color)))

        self.players.setLayout(layout)

        # Preview
        self.preview_container = QWidget()

        start_game_button = QPushButton("START")
        start_game_button.setObjectName('start_game_button')
        start_game_button.setStyleSheet(f"""
          QPushButton#start_game_button {{
             background-color: rgb(255, 255, 100);
             font-family: arno;
             padding: 30px;
             border-radius: {40};
             border: 2px solid black ;
          }}""")
        start_game_button.clicked.connect(self.start_new_game)

        spacer = QWidget()
        spacer.setVisible(False)

        info_text = QLabel("Upewnij się że cała plansza jest widoczna")
        info_text.setObjectName('info_text')
        info_text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        info_text.setStyleSheet("""
        QLabel#info_text{
            font-weight: 400;
            background: #F1E1C6;
            border: 1px solid black;
            padding: 5px;
            border-radius: 5px;
        }""")

        grid_layout.addWidget(spacer, 0, 0, 2, 2)
        grid_layout.addWidget(self.players, 2, 0, 14, 6)
        grid_layout.addWidget(info_text, 1, 7, 1, 4)
        grid_layout.addWidget(self.preview_container, 2, 6, 12, 6)
        grid_layout.addWidget(start_game_button, 12, 7, 4, 4)

        preview_layout = QVBoxLayout()
        self.preview_label = Preview()
        preview_layout.addWidget(self.preview_label)
        self.preview_container.setLayout(preview_layout)

        self.background.setLayout(grid_layout)

    def adjust_size(self):
        self.background.resize(self.main_window.size().width() - 18, self.main_window.size().height() - 18)
        super().adjust_size()

    @Slot()
    def start_new_game(self):
        player_names = [child for child in self.players.children() if isinstance(child, PlayerName)]
        players = dict()

        for child in player_names:
            key, value = child.get_player_name()

            if value:
                players[key] = value

        self.new_game_started.emit(players)
        self.main_window.slide_to_page(self.index, self.main_window.game_page.index, 'left')
