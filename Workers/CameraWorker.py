import time

from Workers.BaseCamera import BaseCamera


class CameraWorker(BaseCamera):
    def __init__(self, index=0):
        super().__init__()

    def configure(self):
        self.cam.preview_configuration.main.size = (640, 480)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.configure("preview")

    def run(self):
        while self._running:
            frame = self.read_func()
            if frame is not None:
                self.frame_ready.emit(frame)
            time.sleep(0.03)  # ~30 FPS

        self._release()
        self.finished.emit()

