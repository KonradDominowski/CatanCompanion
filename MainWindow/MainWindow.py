import os

from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QByteArray, QEasingCurve, QParallelAnimationGroup, QMargins, \
    QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedLayout, QComboBox
from dotenv import load_dotenv

from Pages.NewGamePage import NewGamePage
from Pages.WelcomePage import WelcomePage
from utils import read_css_file

load_dotenv()


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app
        self.stylesheet = read_css_file('./styles.css')
        self.setStyleSheet(self.stylesheet)

        self.animation_group: QParallelAnimationGroup | None = None
        self.animation_duration_in_milliseconds = 250

        env = os.getenv('ENV')
        if env == 'dev':
            self.setGeometry(-500, 0, 1024, 600)
        elif env == 'prod':
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        self.welcome_page = WelcomePage(self)
        self.new_game_page = NewGamePage(self)

        QTimer.singleShot(100, self.new_game_page.adjust_size)

        self.pages_layout = QStackedLayout()
        self.pages_layout.addWidget(self.welcome_page)
        self.pages_layout.addWidget(self.new_game_page)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.pages_layout)

        self.container = QWidget()
        self.container.setLayout(main_layout)
        self.setCentralWidget(self.container)

    def slide_to_page(self, from_index: int, to_index: int, direction: str = "left"):
        """
        Animates a sliding transition between pages in the application.

        This function performs a smooth animated transition between two pages
        managed by a QStackedLayout. The transition can be in one of four directions:
        ``'left'``, ``'right'``, ``'up'``, or ``'down'``. The currently visible page (at ``from_index``)
        slides out of view, while the target page (at ``to_index``) slides in.

        :param from_index: Index of the currently visible page in the QStackedLayout.
        :type from_index: int
        :param to_index: Index of the target page to transition to.
        :type to_index: int
        :param direction: Direction of the animation. Must be one of:
                          ``"left"``, ``"right"``, ``"up"``, or ``"down"``.
        :type direction: str
        :raises ValueError: If the direction is not one of the accepted values.

        :Side effects:
            - Starts a QParallelAnimationGroup to animate both outgoing and incoming widgets.
            - Updates the current index of the stacked layout after the animation finishes.
            - Ensures widgets are reset to correct positions after the animation.
        """

        self.animation_group = QParallelAnimationGroup()

        left, top, right, bottom = self.container.layout().getContentsMargins()
        margin = QPoint(right, top)

        from_widget = self.pages_layout.widget(from_index)
        to_widget = self.pages_layout.widget(to_index)
        page_width = self.container.width()

        directions = {
            "left": (QPoint(-page_width, 0), QPoint(page_width, 0)),
            "right": (QPoint(page_width, 0), QPoint(-page_width, 0)),
            "up": (QPoint(0, -page_width), QPoint(0, page_width)),
            "down": (QPoint(0, page_width), QPoint(0, -page_width)),
        }

        if direction in directions:
            from_end_pos, to_start_pos = directions[direction]
            from_end_pos += margin
            to_start_pos += margin
        else:
            raise ValueError("Direction must be 'left', 'right', 'up', or 'down'")

        to_widget.move(to_start_pos)
        to_widget.show()

        anim_from = QPropertyAnimation(from_widget, QByteArray(b"pos"))
        anim_from.setEndValue(from_end_pos)
        anim_from.setDuration(self.animation_duration_in_milliseconds)
        anim_from.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_from.start()

        anim_to = QPropertyAnimation(to_widget, QByteArray(b"pos"))
        anim_to.setStartValue(to_start_pos)
        anim_to.setEndValue(QPoint(0, 0) + QPoint(9, 9))
        anim_to.setDuration(self.animation_duration_in_milliseconds)
        anim_to.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.animation_group.addAnimation(anim_from)
        self.animation_group.addAnimation(anim_to)

        def on_finished():
            self.pages_layout.setCurrentIndex(to_index)
            from_widget.move(0, 0)  # reset for reuse
            to_widget.move(0, 0)
            self.animation_group = None

        self.animation_group.finished.connect(on_finished)
        self.animation_group.start()
