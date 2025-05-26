from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QFrame, QLayout

from Catan.PlayerColor import PlayerColor
from Widgets.RhombusFrame import RhombusFrame


class PlayerName(QWidget):
    def __init__(self, player_color: PlayerColor):
        super().__init__()
        layout = QVBoxLayout()

        self.color = player_color
        self.line = QLineEdit()
        self.line.setPlaceholderText("Player name")
        self.line.setObjectName('PlayerNameLineEdit')
        self.line.setStyleSheet(f"""QLineEdit#PlayerNameLineEdit {{ 
        font-family: arno;
        padding: 15px;
        margin: 0px;
        font-size: 30px;
        font-weight: 500;
        color: white;
        border-radius: {20}px;
        background-color: rgba(0,0,0,0.3);
        }}""")

        color_frame = RhombusFrame(player_color, self)

        layout.addWidget(self.line)
        layout.addWidget(color_frame)
        layout.setSpacing(0)

        self.setLayout(layout)

        # Only for developing
        if self.color == PlayerColor.WHITE:
            self.line.setText('Długa nazwa testowa')
        elif self.color == PlayerColor.RED:
            self.line.setText('Test 2')
        elif self.color == PlayerColor.ORANGE:
            self.line.setText('Test 3')
        else:
            self.line.setText('Test 4')

    def get_player_name(self) -> tuple[PlayerColor, str]:
        return self.color, self.line.text()
