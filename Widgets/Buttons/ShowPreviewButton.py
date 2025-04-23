from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton
import cv2


class ShowPreviewButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName('ShowPreviewButton')
        self.setFixedSize(QSize(250, 50))
        self.setStyleSheet(f"border-radius: {int(self.height() / 2)}")
        self.clicked.connect(self.show_preview)

    def show_preview(self):
        capture = cv2.VideoCapture(0)

        while True:
            ret, frame = capture.read()

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
