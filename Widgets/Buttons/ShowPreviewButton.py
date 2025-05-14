from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton
from picamera2 import Picamera2
import cv2
import time

class ShowPreviewButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName('ShowPreviewButton')
        self.setFixedSize(QSize(250, 50))
        self.setStyleSheet(f"border-radius: {int(self.height() / 2)}")
        self.clicked.connect(self.show_preview)

    def show_preview(self):
        picam2 = Picamera2()
        picam2.preview_configuration.main.size = (640, 480)
        picam2.preview_configuration.main.format = "RGB888"
        picam2.configure("preview")

        picam2.start()
        # ~ time.sleep(1)  # chwilka na uruchomienie kamery

        while True:
            frame = picam2.capture_array()

            cv2.imshow("Preview", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()
        picam2.stop()
    
    
    # ~ def show_preview(self):
                # ~ capture = cv2.VideoCapture(0)

        # ~ while True:
            # ~ ret, frame = capture.read()

            # ~ cv2.imshow('frame', frame)
            # ~ if cv2.waitKey(1) == ord('q'):
                # ~ break

        # ~ capture.release()
        # ~ cv2.destroyAllWindows()
