from PySide6.QtCore import Qt, QPropertyAnimation
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

        # Player Name
        self.label = QLabel(self.player)
        self.layout.addWidget(self.label)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def get_color(self) -> PlayerColor:
        return self.color

    def clear_resources(self):
        """
        Removes all resource containers (widgets with objectName 'resContainer') from the player's layout.

        This is typically used before redrawing the resources with new values.
        """
        # reversed() allows to simultaneously iterate and remove widgets from layout
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget().objectName() == 'resContainer':
                self.layout.takeAt(i).widget().setParent(None)

    def show_resources(self, resources_dict: dict[ResourceType, int]):
        """
        Displays the player's resources visually using Resource widgets arranged in two rows
        per resource type. Resources are animated when added.

        Each resource type (e.g., wood, brick) is represented as a separate vertical container,
        ensuring consistent layout even when the resource count is zero.

        Row logic:
            - The lower row (`resources_row_1`) is shown at the bottom.
            - The upper row (`resources_row_2`) is shown above the lower row only if needed.
            - Resources are added in this order:
                1–2  → lower row (bottom),
                3–4  → upper row (top),
                5+   → alternately: odd to lower row, even to upper row.

        :param resources_dict: A dictionary mapping each ResourceType to the number of such
                               resources the player currently has.
        """
        for res_type, res_count in resources_dict.items():

            # Main vertical layout to hold both rows
            resource_container = QFrame()
            resource_container.setObjectName('resContainer')
            resource_container.setLayout(QVBoxLayout())
            resource_container.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resource_container.layout().setSpacing(0)
            resource_container.layout().setContentsMargins(0, 0, 0, 0)

            # Lower row – always added to the container layout
            resources_row_1 = QFrame()
            resources_row_1.setObjectName('resRow1')
            resources_row_1.setLayout(QHBoxLayout())
            resources_row_1.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resources_row_1.layout().setSpacing(0)
            resources_row_1.layout().setContentsMargins(0, 0, 0, 0)

            # Upper row – added conditionally if more than 2 resources
            resources_row_2 = QFrame()
            resources_row_2.setObjectName('resRow2')
            resources_row_2.setLayout(QHBoxLayout())
            resources_row_2.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
            resources_row_2.layout().setSpacing(0)
            resources_row_2.layout().setContentsMargins(0, 0, 0, 0)

            if res_count > 0:
                for j in range(1, res_count + 1):
                    resource = Resource(res_type)
                    self.animations.append(resource.get_animation())

                    # Distribution logic:
                    # - 1–2: lower row
                    # - 3–4: upper row
                    # - 5+: odd → lower, even → upper
                    if j <= 2:
                        resources_row_1.layout().addWidget(resource)
                    elif j <= 4:
                        resources_row_2.layout().addWidget(resource)
                    elif j % 2 != 0:
                        resources_row_1.layout().addWidget(resource)
                    else:
                        resources_row_2.layout().addWidget(resource)

                # Add upper row only if it contains any widgets
                if res_count > 2:
                    resource_container.layout().addWidget(resources_row_2)

            # Add lower row (even if empty)
            resource_container.layout().addWidget(resources_row_1)

            # Add the full resource container to the player's layout
            self.layout.addWidget(resource_container)

    def get_animations(self) -> list[QPropertyAnimation]:
        """
        Returns all collected resource animations and clears the internal animation list.
        This is used to allow batch starting of all animations from outside the class
        (e.g. from the game page controller).

        :return: A list of QPropertyAnimation instances representing resource animations.
        """

        anims = self.animations.copy()
        self.animations.clear()
        return anims
