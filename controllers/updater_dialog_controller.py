from PySide2 import QtCore
from PySide2.QtWidgets import QDialog

from views import updater_dialog


class UpdaterDialogController(QDialog):
    def __init__(self):
        super(UpdaterDialogController, self).__init__()
        self.ui = updater_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
