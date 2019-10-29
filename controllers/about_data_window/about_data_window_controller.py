from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog

from views import about_data_dialog


class AboutDataDialogController(QDialog):

    def __init__(self, parent):
        super(AboutDataDialogController, self).__init__(parent)

        self.ui = about_data_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModal)
        