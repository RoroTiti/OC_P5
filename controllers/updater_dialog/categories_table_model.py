from typing import Any

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class CategoriesTableModel(QAbstractTableModel):
    def __init__(self, parent, my_list, my_header):
        QAbstractTableModel.__init__(self, parent)
        self.items_list: [] = my_list
        self.header = my_header

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.items_list)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.header)

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        if index.column() == 0:
            return self.items_list[index.row()].name
        elif index.column() == 1:
            return self.items_list[index.row()].products

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        return None
