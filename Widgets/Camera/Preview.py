import cv2
from PySide6.QtCore import QTimer, QThread
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QSizePolicy

from Camera.CameraFeed import create_camera_feed
from Camera.CameraWorker import CameraWorker


# class Preview(QLabel):
#     def __init__(self):
#         super().__init__()
#
#         self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
#
#         # 📷 Kamera
#         self.camera_feed = create_camera_feed()  # automatycznie Picamera2 lub OpenCV
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.update_frame)
#         self.timer.start(30)
#
#     def update_frame(self):
#         frame = self.camera_feed.read_frame()
#         if frame is not None:
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             h, w, ch = rgb.shape
#             bytes_per_line = ch * w
#             image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
#             pix = QPixmap.fromImage(image)
#             self.setPixmap(pix)
#
#     def closeEvent(self, event):
#         self.camera_feed.release()
#         event.accept()

class Preview(QLabel):
    def __init__(self):
        super().__init__()

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

        self.worker = None
        self.thread = None

    def update_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pix = QPixmap.fromImage(image)
        self.setPixmap(pix)

    def showEvent(self, event):
        super().showEvent(event)
        self.start_camera()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stop_camera()

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()