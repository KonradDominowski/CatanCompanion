from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton
import cv2
from picamera2 import Picamera2
import os
from datetime import datetime


class ShowPreviewButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName('ShowPreviewButton')
        self.setFixedSize(QSize(250, 50))
        self.setStyleSheet(f"border-radius: {int(self.height() / 2)}")
        self.clicked.connect(self.show_preview)

    def show_preview(self):
        path = "Photos"
        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        command = f'libcamera-still -q 99 -o "{path}/{date}.jpg"'
        os.system(command)
#         picam2 = Picamera2()
#         picam2.preview_configuration.main.size = (640, 480)
#         picam2.preview_configuration.main.format = "RGB888"
#         picam2.configure("preview")
#         picam2.start()
# 
#         while True:
#             frame = picam2.capture_array()
#             cv2.imshow("Pi Camera Preview", frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
# 
#         cv2.destroyAllWindows()
# 


