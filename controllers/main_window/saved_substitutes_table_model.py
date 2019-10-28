import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class SavedSubstitutesTableModel(QAbstractTableModel):
    def __init__(self, products_with_substitutes):
        super().__init__()
        self.products_with_substitutes = products_with_substitutes

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.products_with_substitutes[index.row()]["food_name"]
            if index.column() == 1:
                return self.products_with_substitutes[index.row()]["substitute_name"]

        elif role == Qt.UserRole:
            if index.column() == 0:
                return self.products_with_substitutes[index.row()]
            if index.column() == 1:
                return self.products_with_substitutes[index.row()]

        return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        if self.products_with_substitutes is None:
            return 0
        return len(self.products_with_substitutes)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 2

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Produit"
                if section == 1:
                    return "Substitut"
            return None
        return None
