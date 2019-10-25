import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class SubstitutesTableModel(QAbstractTableModel):
    def __init__(self, substitutes):
        super().__init__()
        self.substitutes = substitutes

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return f"{self.substitutes[index.row()]['food_name']}, {self.substitutes[index.row()]['brand_name']}"
            if index.column() == 1:
                return self.substitutes[index.row()]["nutriscore"]
            if index.column() == 2:
                return "Oui" if self.substitutes[index.row()]["ingredients_from_palm_oil_n"] > 0 else "Non"

        elif role == Qt.UserRole:
            return self.substitutes[index.row()]

        else:
            return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        if self.substitutes is None:
            return 0
        else:
            return len(self.substitutes)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 3

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Produit"
                if section == 1:
                    return "NUTRI-SCORE"
                if section == 2:
                    return "Huile de palme"
            return None
        return None
