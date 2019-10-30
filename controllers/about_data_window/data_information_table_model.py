import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class DataInformationTableModel(QAbstractTableModel):

    def __init__(self, data_information):
        super().__init__()
        self.data_information = data_information

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                return self.data_information[index.row()][index.column()]

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.data_information)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 2
