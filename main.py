import sys

from PySide2 import QtCore
from PySide2.QtCore import SIGNAL, SLOT
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog

from views import updaterdialog, mainwindow, dataupdater


class UpdaterWindow(QMainWindow):
    def __init__(self):
        super(UpdaterWindow, self).__init__()
        self.ui = dataupdater.Ui_MainWindow()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.listWidget.clear()
        self.ui.listWidget.addItems(["lol", "lol2"])

        self.ui.listWidget.currentItemChanged.connect(self.item_selected)

        self.ui.lineEdit.textChanged.connect(self.setName)

        print(self.ui.listWidget.items)

        self.connect(self.ui.action_update, SIGNAL("triggered()"), self, SLOT("open_dialog()"))

    def push_button_clicked(self):
        pass

    def item_selected(self, current, previous):
        print(current)
        print(previous)
        print(self.ui.listWidget.currentItem().text())

    def setName(self, name):
        print(name)

    def open_dialog(self):
        dialog = QDialog()
        dialog.ui = updaterdialog.Ui_Dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
