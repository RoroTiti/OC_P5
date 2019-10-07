import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QFile
from mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(["lol", "lol2"])

        self.ui.listWidget.currentItemChanged.connect(self.item_selected)

        self.ui.lineEdit.textChanged.connect(self.setName)

        print(self.ui.listWidget.items)

    def push_button_clicked(self):
        pass

    def item_selected(self, current, previous):
        print(current)
        print(previous)
        print(self.ui.listWidget.currentItem().text())

    def setName(self, name):
        print(name)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
