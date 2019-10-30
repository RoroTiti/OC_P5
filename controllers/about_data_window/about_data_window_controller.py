from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog

from controllers.about_data_window.data_fetcher_thread import DataFetcherThread
from controllers.about_data_window.data_information_table_model import DataInformationTableModel
from views import about_data_dialog


class AboutDataDialogController(QDialog):

    def __init__(self, parent):
        super(AboutDataDialogController, self).__init__(parent)

        self.ui = about_data_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModal)

        self.data_information = []
        self.ui.table_informations.setModel(DataInformationTableModel(self.data_information))
        self.ui.table_informations.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.table_informations.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.data_fetcher_thread = DataFetcherThread()
        self.data_fetcher_thread.result.connect(self.set_table_data_information)
        self.data_fetcher_thread.start()

    def set_table_data_information(self, data_information):
        self.ui.table_informations.model().beginResetModel()
        self.data_information.clear()
        self.data_information += data_information
        self.ui.table_informations.model().endResetModel()
