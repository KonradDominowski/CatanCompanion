from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QFrame


class PlayerName(QWidget):
    def __init__(self, player_color):
        super().__init__()
        layout = QVBoxLayout()

        self.line = QLineEdit()
        self.line.setPlaceholderText("Long placeholder")
        self.line.setObjectName('PlayerNameLineEdit')
        self.line.setStyleSheet(f"""QLineEdit#PlayerNameLineEdit {{ 
        padding: 15px;
        margin: 0px;
        font-size: 30px;
        font-weight: 400;
        color: white;
        border-radius: {20}px;
        background-color: rgba(0,0,0,0.3);
        }}""")

        self.color = QFrame()
        self.color.setObjectName('PlayerNameColorFrame')
        self.color.setStyleSheet(f"""QFrame#PlayerNameColorFrame {{
        background-color: {player_color};
        margin: 0px;
        }}""")
        self.color.setFixedHeight(7)

        layout.addWidget(self.line)
        layout.addWidget(self.color)

        self.setLayout(layout)
