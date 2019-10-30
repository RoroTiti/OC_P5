import typing

import PySide2
from PySide2.QtCore import QAbstractListModel, Qt


class CategoriesComboBoxModel(QAbstractListModel):
    """
    Model of the data to be displayed on the categories combobox of the main window
    """

    def __init__(self, categories: list):
        """
        Initialize a CategoriesComboBoxModel object
        :param categories: The list of the categories to display on the combobox
        """
        super().__init__()
        self.categories = categories

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        """
        Return the data for the corresponding index and role
        :param index: The index of the cell to display
        :param role: The role to display
        :return: If role is DisplayRole, a string. If role is UserRole, a category. Else None.
        """
        if role == Qt.DisplayRole:
            return self.categories[index.row()]["category_name"]

        elif role == Qt.UserRole:
            return self.categories[index.row()]

        return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        """
        Return the number of rows to display on table
        :param parent:
        :return: The number of rows to display
        """
        return len(self.categories)
