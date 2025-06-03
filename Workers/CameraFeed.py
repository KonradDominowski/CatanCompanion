import platform
import cv2

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None


class CameraFeedBase:
    def read_frame(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError


class RPiCameraFeed(CameraFeedBase):
    def __init__(self):
        self.cam = Picamera2()
        self.cam.preview_configuration.main.size = (640, 480)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.configure("preview")
        self.cam.start()

    def read_frame(self):
        return self.cam.capture_array()

    def release(self):
        self.cam.stop()


class CvCameraFeed(CameraFeedBase):
    def __init__(self, index=0):
        self.cam = cv2.VideoCapture(index)

    def read_frame(self):
        ret, frame = self.cam.read()
        return frame if ret else None

    def release(self):
        self.cam.release()


def create_camera_feed() -> CameraFeedBase:
    is_rpi = platform.machine().startswith("arm")
    if is_rpi:
        return RPiCameraFeed()
    else:
        return CvCameraFeed()
