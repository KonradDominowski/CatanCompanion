from PySide6.QtCore import QObject, Signal


class ImportWorker(QObject):
    finished = Signal()

    def run(self):
        global ultralytics, cv2
        import cv2
        import ultralytics

        self.finished.emit()

