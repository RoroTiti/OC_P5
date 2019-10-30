import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class ProductsTableModel(QAbstractTableModel):
    """
    Model of the data to be displayed on the products table of the main window
    """

    def __init__(self, products: list):
        """
        Initialize a ProductsTableModel object

        :param products: The list of products to display to display on products table
        """
        super().__init__()
        self.products = products

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        """
        Return the data for the corresponding index and role

        :param index: The index of the cell to display
        :param role: The role to display
        :return: If role is DisplayRole, a string. If role is UserRole, a product. Else None.
        """
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
        """
        Return the number of rows to display on table

        :param parent:
        :return: The number of rows to display
        """
        if self.products is None:
            return 0
        return len(self.products)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        """
        Return the number of columns to display on table

        :param parent:
        :return: The number of columns to display
        """
        return 3

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
                    return "Produit"
                elif section == 1:
                    return "NUTRI-SCORE"
                elif section == 2:
                    return "Huile de palme"
            return None
        return None
