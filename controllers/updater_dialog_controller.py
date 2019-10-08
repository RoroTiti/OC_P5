from PySide2 import QtCore
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide2.QtWidgets import QDialog

from views import updater_dialog


class UpdaterDialogController(QDialog):
    def __init__(self):
        super(UpdaterDialogController, self).__init__()
        self.manager = QNetworkAccessManager()
        self.ui = updater_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.ui.btn_load_list.clicked.connect(self.fetch_categories)

    def fetch_categories(self):
        request = QNetworkRequest(QtCore.QUrl("https://fr.openfoodfacts.org/categories.jon"))
        self.manager.finished.connect(self.handle_api_categories)
        self.manager.get(request)

    def handle_api_categories(self, reply: QNetworkReply):
        er = reply.error()

        if er == QNetworkReply.NoError:
            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))

        else:
            print("Error occured: ", er)
            print(reply.errorString())
