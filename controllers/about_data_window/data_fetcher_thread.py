from PySide2.QtCore import QThread, Signal


class DataFetcherThread(QThread):
    result = Signal()

    def run(self):
        pass
