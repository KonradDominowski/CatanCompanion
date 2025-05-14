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
        font-size: 40px;
        font-weight: 500;
        color: white;
        border-radius: {20}px;
        background-color: rgba(0,0,0,0.6);
        }}""")

        self.color = QFrame()
        self.color.setObjectName('PlayerNameColorFrame')
        self.color.setStyleSheet(f"""QFrame#PlayerNameColorFrame {{
        background-color: {player_color};
        margin: 0px;
        }}""")
        self.color.setFixedHeight(10)

        layout.addWidget(self.line)
        layout.addWidget(self.color)

        self.setLayout(layout)
