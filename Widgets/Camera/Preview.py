import cv2
from PySide6.QtCore import QThread, Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy

from Camera.CameraWorker import CameraWorker


class Preview(QLabel):
    layout_calculated = False

    def __init__(self):
        super().__init__()

        self.setStyleSheet("border: 10px solid rgba(0, 0, 0, 1)")

        self.thread = None
        self.worker = None
        self._camera_active = False

    def start_camera(self):
        if self._camera_active:
            return

        self._camera_active = True
        self.thread = QThread()
        
        self.worker = CameraWorker()
        self.worker.moveToThread(self.thread)

        self.worker.frame_ready.connect(self.update_frame)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def stop_camera(self):
        if not self._camera_active:
            return

        self._camera_active = False
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()
        
        del self.worker
        self.worker = None
        self.thread = None

    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled_image = image.scaled(494, 406, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        pix = QPixmap.fromImage(scaled_image)
        # pix = QPixmap.fromImage(image)
        self.setPixmap(pix)

    def showEvent(self, event):
        super().showEvent(event)

        # The first time it's showed it only is shown to calculate the layout, no need for the camera to activate
        self.start_camera()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stop_camera()

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()
