from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton
import cv2
import time
from datetime import datetime
from PIL import Image


class ShowPreviewButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName('ShowPreviewButton')
        self.setFixedSize(QSize(250, 50))
        self.setStyleSheet(f"border-radius: {int(self.height() / 2)}")
        self.clicked.connect(self.show_preview)

    def show_preview(self):
        picam2 = Picamera2()

        # Konfiguracja z maksymalną rozdzielczością
        still_config = picam2.create_still_configuration()
        picam2.configure(still_config)

        picam2.start()

        # Ustawienie autofokusa – tylko jeśli Twoja kamera to obsługuje!
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        time.sleep(2)

        # Opcjonalnie wymuszenie wyostrzenia przed zdjęciem
        picam2.set_controls({"AfTrigger": 0})  # Start autofocus
        time.sleep(2)  # Poczekaj aż ustawi ostrość

        # Zrobienie zdjęcia
        image = picam2.capture_array()
        name = datetime.now()
        Image.fromarray(image).save(f"photos/{name}.jpg")
        
        self.setText('Photo taken')

        picam2.stop()
        picam2.close()
