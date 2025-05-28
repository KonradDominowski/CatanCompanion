from PySide6.QtCore import QMargins, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame, QVBoxLayout

from Catan.PlayerColor import PlayerColor


class Player(QFrame):
    def __init__(self, color: PlayerColor, player: str):
        super().__init__()

        self.layout = QHBoxLayout()

        self.color = color
        self.player = player
        self.setObjectName('playerInfo')
        border_gradient = f"""2px solid qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                        stop:0 rgba({color.r}, {color.g}, {color.b}, 1),
                                                        stop:0.85 rgba({color.r}, {color.g}, {color.b}, 0)
                                                        );"""
        self.setStyleSheet(f"""
            QFrame#{self.objectName()} {{
            border-top: {border_gradient};
            border-bottom: {border_gradient};
            border-left: 2px solid {color.hex};
            }}
            
            QWidget {{
            color: white;
            font-size: 24px;
            }}
        """)

        """
                    QFrame#resContainer {{
            border: 1px solid white
            }}"""

        # Player Name
        self.label = QLabel(self.player)
        # self.label.setStyleSheet('border: 1px solid yellow')
        self.layout.addWidget(self.label)

        resources_amount = 5

        # Resources gained
        for i in range(5):
            resource_container = QFrame()
            resource_container.setObjectName('resContainer')

            resource_container.setLayout(QVBoxLayout())
            resource_container.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resource_container.layout().setSpacing(0)
            resource_container.layout().setContentsMargins(0, 0, 0, 0)

            resources_row_1 = QFrame()
            resources_row_1.setObjectName('resContainer')
            resources_row_1.setLayout(QHBoxLayout())
            resources_row_1.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resources_row_1.layout().setSpacing(0)
            resources_row_1.layout().setContentsMargins(0, 0, 0, 0)

            resources_row_2 = QFrame()
            resources_row_2.setObjectName('resContainer')
            resources_row_2.setLayout(QHBoxLayout())
            resources_row_2.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resources_row_2.layout().setSpacing(0)
            resources_row_2.layout().setContentsMargins(0, 0, 0, 0)

            if resources_amount > 0:
                for j in range(1, resources_amount + 1):
                    resource = QLabel()
                    resource.setPixmap(QPixmap("./assets/res_wheat.png").scaled(40, 40))
                    # resource.setStyleSheet('border: 1px solid green')

                    if j <= 2:
                        resources_row_1.layout().addWidget(resource)
                    elif j <= 4:
                        resources_row_2.layout().addWidget(resource)
                    elif j % 2 != 0:
                        resources_row_1.layout().addWidget(resource)
                    else:
                        resources_row_2.layout().addWidget(resource)

            if resources_amount > 2:
                resource_container.layout().addWidget(resources_row_2)

            resource_container.layout().addWidget(resources_row_1)

            self.layout.addWidget(resource_container)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
