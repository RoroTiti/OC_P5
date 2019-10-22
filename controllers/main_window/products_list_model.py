import typing

import PySide2
from PySide2.QtCore import QAbstractListModel, Qt


class ProductsListModel(QAbstractListModel):

    def __init__(self, products):
        super().__init__()
        self.products = products

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.products[index.row()].food_name

        elif role == Qt.UserRole:
            return self.products[index.row()]

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.products)
