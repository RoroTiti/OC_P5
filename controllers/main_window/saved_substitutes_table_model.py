import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class SavedSubstitutesTableModel(QAbstractTableModel):
    """
    Model of the data to be displayed on the saved substitutes table of the main window
    """

    def __init__(self, products_with_substitutes):
        """
        Initialize a SavedSubstitutesTableModel object

        :param products_with_substitutes: The list of product ID + substitute ID to save into the database
        """
        super().__init__()
        self.products_with_substitutes = products_with_substitutes

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        """
        Return the data for the corresponding index and role

        :param index: The index of the cell to display
        :param role: The role to display
        :return: If role is DisplayRole, a string. If role is UserRole, a product. Else None.
        """

        product_with_substitute = self.products_with_substitutes[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return \
                    f"{product_with_substitute['product']['food_name']}\r\n" \
                    f"   {product_with_substitute['product']['brand_name']}\r\n" \
                    f"   Nutriscore : {product_with_substitute['product']['nutriscore']}\r\n" \
                    f"   Huile de palme : {'Oui' if product_with_substitute['product']['ingredients_from_palm_oil_n'] > 0 else 'Non'}"

            if index.column() == 1:
                return \
                    f"{product_with_substitute['substitute']['food_name']}\r\n" \
                    f"   {product_with_substitute['substitute']['brand_name']}\r\n" \
                    f"   Nutriscore : {product_with_substitute['substitute']['nutriscore']}\r\n" \
                    f"   Huile de palme : {'Oui' if product_with_substitute['substitute']['ingredients_from_palm_oil_n'] > 0 else 'Non'}"

        elif role == Qt.UserRole:
            if index.column() == 0:
                return product_with_substitute["product"]
            if index.column() == 1:
                return product_with_substitute["substitute"]

        return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        """
        Return the number of rows to display on table

        :param parent:
        :return: The number of rows to display
        """
        if self.products_with_substitutes is None:
            return 0
        return len(self.products_with_substitutes)

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
                    return "Produit"
                if section == 1:
                    return "Substitut"
            return None
        return None
