from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton
import cv2
from datetime import datetime
from picamera2 import Picamera2
import os


class ShowPreviewButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setObjectName('ShowPreviewButton')
        self.setFixedSize(QSize(250, 50))
        self.setStyleSheet(f"border-radius: {int(self.height() / 2)}")
        # self.clicked.connect(self.show_preview)
        self.clicked.connect(self.take_photo)

    def show_preview(self):
        capture = cv2.VideoCapture(0)

        while True:
            ret, frame = capture.read()

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()

    def take_photo(self):
        # Inicjalizacja kamery
        picam2 = Picamera2()
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

        config = picam2.create_still_configuration()
        picam2.configure(config)
    
        picam2.start()
        picam2.sleep(2)  # Poczekaj, aż obraz się ustabilizuje
    
        # Utworzenie nazwy pliku ze znacznikiem czasu
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"photos/photo_{timestamp}.jpg"
    
        # Zapis zdjęcia
        picam2.capture_file(filepath)
        print(f"Zapisano zdjęcie: {filepath}")
    
        # Zwolnienie zasobów
        picam2.stop()

        self.setText(f"{timestamp}")
        self.setDisabled(True)

        QTimer.singleShot(2000, self.restore_button)

    def restore_button(self):
        self.setText(self.original_text)
        self.setDisabled(False)
