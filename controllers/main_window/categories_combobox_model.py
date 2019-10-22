import typing

import PySide2
from PySide2.QtCore import QAbstractListModel, Qt


class CategoriesComboBoxModel(QAbstractListModel):

    def __init__(self, categories):
        super().__init__()
        self.categories = categories

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.categories[index.row()].category_name

        elif role == Qt.UserRole:
            return self.categories[index.row()]

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.categories)
