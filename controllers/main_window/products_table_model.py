import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class ProductsTableModel(QAbstractTableModel):
    def __init__(self, products):
        super().__init__()
        self.products = products

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return f"{self.products[index.row()]['food_name']}, {self.products[index.row()]['brand_name']}"
            if index.column() == 1:
                return self.products[index.row()]["nutriscore"]
            if index.column() == 2:
                return "Oui" if self.products[index.row()]["ingredients_from_palm_oil_n"] > 0 else "Non"

        elif role == Qt.UserRole:
            return self.products[index.row()]

        else:
            return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        if self.products is None:
            return 0
        return len(self.products)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 3

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Produit"
                elif section == 1:
                    return "NUTRI-SCORE"
                elif section == 2:
                    return "Huile de palme"
            return None
        return None
