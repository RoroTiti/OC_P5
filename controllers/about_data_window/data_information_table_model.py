import typing

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt


class DataInformationTableModel(QAbstractTableModel):
    """
    Model of the data information to be displayed on the table in the data information dialog.
    """

    def __init__(self, data_information: list):
        """
        Initializes a DataInformationTableModel object

        :param data_information: The list of items to display on the table
        """
        super().__init__()
        self.data_information = data_information

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        """
        Return the data for the corresponding index and role

        :param index: The index of the cell to display
        :param role: The role to display
        :return: If role is DisplayRole, a string. Else None.
        """
        if index.isValid():
            if role == Qt.DisplayRole:
                return self.data_information[index.row()][index.column()]
            return None
        return None

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        """
        Return the number of rows to display on table

        :param parent:
        :return: The number of rows to display
        """
        return len(self.data_information)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        """
        Return the number of columns to display on table

        :param parent:
        :return: The number of columns to display
        """
        return 2
