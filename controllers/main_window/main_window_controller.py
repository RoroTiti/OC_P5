from PySide2.QtCore import SIGNAL, SLOT
from PySide2.QtWidgets import QMainWindow

from controllers.updater_dialog.updater_dialog_controller import UpdaterDialogController
from views import main_window


class MainWindowController(QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect(self.ui.action_update, SIGNAL("triggered()"), self, SLOT("open_updater_dialog()"))

    def open_updater_dialog(self):
        dialog = UpdaterDialogController(self)
        dialog.exec_()
