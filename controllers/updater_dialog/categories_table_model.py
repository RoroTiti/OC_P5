from typing import Any

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class CategoriesTableModel(QAbstractTableModel):
    def __init__(self, parent, categories):
        super().__init__(parent)
        self.categories = categories

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                if index.column() == 0:
                    return self.categories[index.row()]["name"]
                elif index.column() == 1:
                    return self.categories[index.row()]["products"]

            elif role == Qt.UserRole:
                if index.column() == 0:
                    return self.categories[index.row()]
                elif index.column() == 1:
                    return self.categories[index.row()]

            return None
        return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.categories)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 2

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Catégorie"
                elif section == 1:
                    return "Nombre de produits"
            return None
        return None
