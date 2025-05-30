from PySide6.QtCore import Qt, QParallelAnimationGroup, QPauseAnimation, QSequentialAnimationGroup, QPropertyAnimation, \
    QTimer
from PySide6.QtWidgets import QHBoxLayout, QLabel, QFrame, QVBoxLayout

from Catan.PlayerColor import PlayerColor
from Widgets.Game.Resource import Resource, ResourceType


class Player(QFrame):
    def __init__(self, color: PlayerColor, player: str):
        super().__init__()

        self.animations: list[QPropertyAnimation] = list()

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

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def clear_resources(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget().objectName() == 'resContainer':
                self.layout.takeAt(i).widget().setParent(None)

    def show_resources(self, count):
        for res_type in ResourceType:
            resource_container = QFrame()
            resource_container.setObjectName('resContainer')
            # resource_container.setStyleSheet('QFrame#resContainer {border: 1px solid yellow}')

            resource_container.setLayout(QVBoxLayout())
            resource_container.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resource_container.layout().setSpacing(0)
            resource_container.layout().setContentsMargins(0, 0, 0, 0)

            resources_row_1 = QFrame()
            resources_row_1.setObjectName('resRow1')
            resources_row_1.setLayout(QHBoxLayout())
            resources_row_1.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resources_row_1.layout().setSpacing(0)
            resources_row_1.layout().setContentsMargins(0, 0, 0, 0)

            resources_row_2 = QFrame()
            resources_row_2.setObjectName('resRow2')
            resources_row_2.setLayout(QHBoxLayout())
            resources_row_2.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resources_row_2.layout().setSpacing(0)
            resources_row_2.layout().setContentsMargins(0, 0, 0, 0)

            if count > 0:
                for j in range(1, count + 1):
                    resource = Resource(res_type)
                    self.animations.append(resource.get_animation())

                    if j <= 2:
                        resources_row_1.layout().addWidget(resource)
                    elif j <= 4:
                        resources_row_2.layout().addWidget(resource)
                    elif j % 2 != 0:
                        resources_row_1.layout().addWidget(resource)
                    else:
                        resources_row_2.layout().addWidget(resource)

            if count > 2:
                resource_container.layout().addWidget(resources_row_2)

            resource_container.layout().addWidget(resources_row_1)

            self.layout.addWidget(resource_container)

    def get_animations(self) -> list[QPropertyAnimation]:
        anims = self.animations.copy()
        self.animations.clear()
        return anims
