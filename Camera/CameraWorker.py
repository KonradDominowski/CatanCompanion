from PySide6.QtCore import QObject, Signal, QThread
import platform
import cv2
import time

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None


class CameraWorker(QObject):
    frame_ready = Signal(object)
    finished = Signal()

    def __init__(self, index=0):
        super().__init__()
        self._running = True
        self._is_rpi = platform.machine().startswith("arm")
        if self._is_rpi and Picamera2:
            self.cam = Picamera2()
            self.cam.preview_configuration.main.size = (640, 480)
            self.cam.preview_configuration.main.format = "RGB888"
            self.cam.configure("preview")
            self.cam.start()
            self.read_func = self.cam.capture_array
        else:
            self.cam = cv2.VideoCapture(index)
            self.read_func = self._read_cv

    def _read_cv(self):
        ret, frame = self.cam.read()
        return frame if ret else None

    def run(self):
        while self._running:
            frame = self.read_func()
            if frame is not None:
                self.frame_ready.emit(frame)
            time.sleep(0.03)  # ~30 FPS

        self._release()
        self.finished.emit()

    def stop(self):
        self._running = False

    def _release(self):
        if self._is_rpi:
            self.cam.stop()
        else:
            self.cam.release()
