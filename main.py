import sys

from PySide2.QtGui import QColor, QPalette
from PySide2.QtWidgets import QApplication

from controllers.main_window.main_window_controller import MainWindowController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.Highlight, QColor(41, 128, 185))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))

    app.setPalette(palette)

    window = MainWindowController()
    window.show()
    sys.exit(app.exec_())
