from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QFrame, QLayout

from Widgets.RhombusFrame import RhombusFrame


class PlayerName(QWidget):
    def __init__(self, player_color):
        super().__init__()
        layout = QVBoxLayout()

        self.line = QLineEdit()
        self.line.setPlaceholderText("Long placeholder")
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

        self.color = RhombusFrame(player_color, self)

        layout.addWidget(self.line)
        layout.addWidget(self.color)
        layout.setSpacing(0)

        self.setLayout(layout)
