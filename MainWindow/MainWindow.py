import os

from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QByteArray, QEasingCurve, QParallelAnimationGroup, QThread
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedLayout
from dotenv import load_dotenv

from Camera.ImportWorker import ImportWorker
from Pages.GamePage import GamePage
from Pages.NewGamePage import NewGamePage
from Pages.Page import Page
from Pages.WelcomePage import WelcomePage
from utils import read_css_file

load_dotenv()


class MainWindow(QMainWindow):
    ANIMATION_DURATION_IN_MILLISECONDS = 400

    def __init__(self, app: QApplication):
        super().__init__()

        self.import_thread = QThread()
        self.import_worker = ImportWorker()

        self.import_libraries()

        self.app = app
        self.setWindowTitle("Catan Companion")
        self.stylesheet = read_css_file('./styles.css')
        self.setStyleSheet(self.stylesheet)
        self.setGeometry(0, 0, 1024, 600)  # 1024 x 600 is the size of the dedicated touch screen display

        env = os.getenv('ENV')
        if env == 'prod':
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        # Pages of the application
        self.pages_layout = QStackedLayout()

        self.welcome_page = self.add_page(WelcomePage)
        self.new_game_page = self.add_page(NewGamePage)
        self.game_page = self.add_page(GamePage)

        self.calculate_pages_dimensions()

        # Animation group for transitions between pages
        self.animation_group: QParallelAnimationGroup | None = None

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
        anim_from.setDuration(self.ANIMATION_DURATION_IN_MILLISECONDS)
        anim_from.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim_from.start()

        anim_to = QPropertyAnimation(to_widget, QByteArray(b"pos"))
        anim_to.setStartValue(to_start_pos)
        anim_to.setEndValue(QPoint(0, 0) + QPoint(9, 9))
        anim_to.setDuration(self.ANIMATION_DURATION_IN_MILLISECONDS)
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

    def add_page(self, page: type[Page]) -> Page:
        """
           Creates an instance of the given page class and adds it to the stacked layout.

           This method takes a page class (which must inherit from `Page`), creates an instance
           of it by passing the `MainWindow` as an argument, and adds the resulting widget
           to the `QStackedLayout`. It returns the created instance for further use.

           :param page: A subclass of `Page` to be instantiated and added to the layout.
           :type page: type[Page]
           :return: The instance of the page that was added to the layout.
           :rtype: Page

           :raises TypeError: If the given argument is not a subclass of `Page`.

           Note:
               This method assumes that all pages accept `MainWindow` as their only constructor argument.
           """
        new_page = page(self)
        self.pages_layout.addWidget(new_page)

        return new_page

    def calculate_pages_dimensions(self):
        """
            Forces layout recalculation for all pages in the QStackedLayout except the first one.

            This method iterates over all pages starting from index 1 and calls their
            `adjust_size()` method to ensure Qt calculates the proper layout size
            before any animations or transitions occur.

            Side effects:
                - Temporarily displays each page off-screen and recalculates its size.

            Note:
                This assumes all widgets in the layout are instances of `Page` or its subclasses.
            """
        widget_count = self.pages_layout.count()
        for i in range(1, widget_count):
            page = self.pages_layout.widget(i)

            if isinstance(page, Page):
                page.adjust_size()

    def import_libraries(self):
        self.import_worker.moveToThread(self.import_thread)

        self.import_thread.started.connect(self.import_worker.run)
        self.import_worker.finished.connect(self.on_import_finished)
        self.import_worker.finished.connect(self.import_thread.quit)
        self.import_worker.finished.connect(self.import_worker.deleteLater)
        self.import_thread.finished.connect(self.import_thread.deleteLater)

        self.import_thread.start()

    def on_import_finished(self):
        print('Import finished')
