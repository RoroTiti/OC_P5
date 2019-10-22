import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class NutrimentsTableModel(QAbstractTableModel):
    def __init__(self, nutriments):
        super().__init__()
        self.nutriments = nutriments

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole and index.isValid():
            if index.column() == 0:
                return self.nutriments[index.row()][0]
            elif index.column() == 1:
                return self.nutriments[index.row()][1]

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.nutriments)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 2
