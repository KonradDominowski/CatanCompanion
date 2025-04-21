import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPalette, QBrush
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from dotenv import load_dotenv

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
            self.setGeometry(1000, 1000, 1024, 600)
        elif env == 'prod':
            self.setWindowState(Qt.WindowState.WindowFullScreen)

        center = QWidget(self)
        self.setCentralWidget(center)

        button = QPushButton('Test', self)
        button2 = QPushButton('Test', self)

        main_layout = QVBoxLayout()
        main_layout.addWidget(button)
        main_layout.addWidget(button2)
        center.setLayout(main_layout)