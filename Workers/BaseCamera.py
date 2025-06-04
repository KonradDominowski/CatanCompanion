from PySide6.QtCore import QObject, Signal
import platform
import cv2
import time

try:
    from picamera2 import Picamera2
    from libcamera import controls
except ImportError:
    Picamera2 = None
    controls = None

class BaseCamera(QObject):
    """
    Abstract base class for camera handling, supporting both Raspberry Pi (Picamera2)
    and standard desktops/laptops using OpenCV.

    Designed to be subclassed by classes like CameraWorker or PhotoTaker.
    """
    frame_ready = Signal(object)
    finished = Signal()

    def __init__(self, index=0):
        super().__init__()
        self._running = True
        self._is_rpi = platform.machine().startswith("aarch")  # Check if host machine is Pi

	# Set camera backend for Pi or for cv2 capture
	# TODO - Picamera2 od razu sie otwiera i zaczyna nagrywanie, cv2 sie inicjalizuje ale nie od razu startuje
        if self._is_rpi and Picamera2:
            self.cam = Picamera2()
            self.configure()  # Configure for video or still picture
            self.start()
            self.read_func = self.cam.capture_array
        else:
            self.cam = cv2.VideoCapture(index)
            self.read_func = self._read_cv

    def configure(self):
        raise NotImplementedError("configure method not implemented")
	
    def run(self):
        raise NotImplementedError("run method not implemented")
    
    def _read_cv(self):
        ret, frame = self.cam.read()
        return frame if ret else None
    
    def start(self):
        self.cam.start()
	
	# Enable autofocus if it's available, on Raspberry Pi Camera
	# autofocus doesn't turn on automatically, so it has to be done manually
        if controls:
            try:
                self.cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})
                time.sleep(0.1)
                self.cam.set_controls({"AfTrigger": controls.AfTriggerEnum.Start})
            except Exception as e:
                print(f"⚠️ Autofokus nieaktywny: {e}")
		
    def stop(self):
        self._running = False

    def _release(self):
        if self._is_rpi:
            self.cam.stop()
            self.cam.close()
        else:
            self.cam.release()
