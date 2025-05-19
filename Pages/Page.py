from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from MainWindow import MainWindow


class Page(QWidget):
    """
        Base class for all application pages.

        This class extends `QWidget` and serves as a template for pages managed
        by the `MainWindow`. Each page holds a reference to the main window
        and provides a method to ensure its size is correctly adjusted.

        :param main_window: The main application window managing this page.
        :type main_window: MainWindow
        """

    def __init__(self, main_window: MainWindow):
        super().__init__()

        self.main_window = main_window
        self.index = main_window.pages_layout.count()

    def adjust_size(self):
        """
           Temporarily displays the page off-screen to allow Qt to calculate its proper size.

           Qt cannot automatically determine the correct size of invisible widgets.
           This method briefly shows the page far off-screen (`move(-10000, -10000)`) so that Qt can compute its layout size. It then schedules `adjustSize()` to resize the widget to fit its content, and hides the widget again.

           Side effects:
               - Sets the page's parent to `main_window` if it isn't already.
               - Moves the widget off-screen and shows it briefly.
               - Hides the widget after 50 ms.
               - Calls `adjustSize()` after 50 ms to recalculate its size.

           Note:
               This method should only be called during initialization or setup.
               Do not call it while animations are running or for visible pages.
           """
        self.setParent(self.main_window)
        self.move(-10000, -10000)
        self.show()

        QTimer.singleShot(50, self.hide)
        QTimer.singleShot(50, self.adjustSize)
