import os

from PySide6.QtCore import Qt
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

        env = os.getenv('ENV')
        if env == 'dev':
            self.setGeometry(-500, 0, 1024, 600)
        elif env == 'prod':
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        welcome_page = WelcomePage(self)
        new_game_page = NewGamePage(self)

        self.pages_layout = QStackedLayout()
        self.pages_layout.addWidget(welcome_page)
        self.pages_layout.addWidget(new_game_page)

        self.page_combo_box = QComboBox()
        self.page_combo_box.addItem("Welcome Page")
        self.page_combo_box.addItem("New Game Page")
        self.page_combo_box.activated.connect(
            self.pages_layout.setCurrentIndex)

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.pages_layout)

        self.container = QWidget()
        self.container.setLayout(main_layout)
        self.setCentralWidget(self.container)
