import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt
from PySide2.QtWidgets import QMainWindow


class CategoriesTableModel(QAbstractTableModel):
    """
    Model of the data to be displayed on the categories lists of the data updater window
    """

    def __init__(self, parent: QMainWindow, categories: list):
        """
        Initialize a CategoriesTableModel object

        :param parent:
        :param categories:
        """
        super().__init__(parent)
        self.categories = categories

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        """
        Return the data for the corresponding index and role

        :param index: The index of the cell to display
        :param role: The role to display
        :return: If role is DisplayRole, a string. If role is UserRole, a product. Else None.
        """
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
        """
        Return the number of rows to display on table

        :param parent:
        :return: The number of rows to display
        """
        return len(self.categories)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        """
        Return the number of columns to display on table

        :param parent:
        :return: The number of columns to display
        """
        return 2

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        """
        Return the header of the column to display

        :param section: The index of the column
        :param orientation: The orientation of the header to display
        :param role: The role to display
        :return: The header of the column
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Catégorie"
                elif section == 1:
                    return "Nombre de produits"
            return None
        return None
