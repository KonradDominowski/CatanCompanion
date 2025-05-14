from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QGridLayout, QPushButton, QVBoxLayout, QLabel, QGroupBox, \
    QFormLayout, QLineEdit

from Camera.CameraFeed import create_camera_feed
from MainWindow import MainWindow
from Widgets.Buttons.ReturnButton import ReturnButton
from Widgets.Camera.Preview import Preview
from Widgets.PlayerName import PlayerName


class NewGamePage(QWidget):
    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.main_window = main_window
        self.index = 1
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
        # players.setStyleSheet("QWidget#players {border: 1px solid white}")

        layout = QVBoxLayout()
        for color in ['white', 'orange', 'blue', 'red']:
            layout.addWidget(PlayerName(color))

        players.setLayout(layout)

        # Preview
        self.preview_container = QWidget()

        start_game_button = QPushButton("New Game")
        start_game_button.setStyleSheet("background-color: white")

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
        QTimer.singleShot(0, self.adjustSize)

    def showEvent(self, event):
        print(self.preview_container.size())
        event.accept()
