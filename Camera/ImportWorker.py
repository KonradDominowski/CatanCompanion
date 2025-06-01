from PySide6.QtCore import QObject, Signal, QThread


class ImportWorker(QObject):
    finished = Signal()

    def run(self):
        print('importing')
        global ultralytics
        import ultralytics
        self.finished.emit()

