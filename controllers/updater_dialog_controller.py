from typing import Any

import PySide2
from PySide2.QtCore import QJsonDocument, QAbstractTableModel, Qt, QUrl, QSortFilterProxyModel, QModelIndex
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide2.QtWidgets import QDialog, QProgressDialog, QAbstractItemView, QHeaderView, QAbstractScrollArea

from models.api.Category import Category
from views import updater_dialog


class UpdaterDialogController(QDialog):
    def __init__(self):
        super(UpdaterDialogController, self).__init__()
        self.progress = QProgressDialog("Récupération des catégories...", "", 0, 0, self)
        self.progress.setFixedWidth(300)

        # noinspection PyTypeChecker
        self.progress.setCancelButton(None)

        self.fetch_categories_manager = QNetworkAccessManager()
        self.fetch_categories_manager.finished.connect(self.handle_api_categories)

        self.ui = updater_dialog.Ui_Dialog()

        self.ui.setupUi(self)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.all_categories = []
        self.selected_categories = []

        self.ui.btn_load_list.clicked.connect(self.fetch_categories)
        self.ui.btn_add_category.clicked.connect(self.add_category)

        headers = ["Catégorie", "Nombre de produits"]

        # All categories list initialization
        self.all_categories_table_model = CategoriesTableModel(
            self,
            self.all_categories,
            headers
        )

        all_categories_proxy = QSortFilterProxyModel()
        all_categories_proxy.setSourceModel(self.all_categories_table_model)

        self.ui.table_all_categories.setModel(all_categories_proxy)
        self.ui.table_all_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_all_categories.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.table_all_categories.setSortingEnabled(True)
        self.ui.table_all_categories.sortByColumn(1, Qt.DescendingOrder)

        # Selected categories list initialization
        self.selected_categories_table_model = CategoriesTableModel(
            self,
            self.selected_categories,
            headers
        )

        selected_categories_proxy = QSortFilterProxyModel()
        selected_categories_proxy.setSourceModel(self.selected_categories_table_model)

        self.ui.table_selected_categories.setModel(selected_categories_proxy)
        self.ui.table_selected_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_selected_categories.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.table_selected_categories.setSortingEnabled(True)
        self.ui.table_selected_categories.sortByColumn(1, Qt.DescendingOrder)

    def fetch_categories(self):
        self.progress.open()

        request = QNetworkRequest(QUrl("https://fr.openfoodfacts.org/categories.json"))
        self.fetch_categories_manager.get(request)

    def handle_api_categories(self, reply: QNetworkReply):
        error = reply.error()

        if error == QNetworkReply.NoError:
            bytes_string = reply.readAll()

            json = QJsonDocument.fromJson(bytes_string)
            obj = json.object()["tags"]

            # categories_gt_5000 = []

            self.all_categories_table_model.beginResetModel()

            self.all_categories.clear()

            for item in obj:
                if item["products"] >= 5000:
                    self.all_categories.append(Category(item["name"], item["products"], item["id"]))

            self.all_categories_table_model.endResetModel()
            self.ui.table_all_categories.resizeColumnsToContents()

        else:
            print("Error occured: ", error)
            print(reply.errorString())

        self.progress.close()

    def add_category(self):
        proxy_model: QSortFilterProxyModel = self.ui.table_all_categories.model()
        source_model: CategoriesTableModel = proxy_model.sourceModel()

        new_categories = []

        for row in self.ui.table_all_categories.selectionModel().selectedRows():
            model_index = proxy_model.index(row.row(), 0)
            source_index = proxy_model.mapToSource(model_index)
            new_categories.append(source_model.items_list[source_index.row()])

        self.selected_categories_table_model.beginInsertRows(
            QModelIndex(),
            len(self.selected_categories),
            len(self.selected_categories) + len(new_categories) - 1
        )
        self.selected_categories.extend(new_categories)
        self.selected_categories_table_model.endInsertRows()
        self.ui.table_selected_categories.resizeColumnsToContents()


class CategoriesTableModel(QAbstractTableModel):
    def __init__(self, parent, my_list, my_header):
        QAbstractTableModel.__init__(self, parent)
        self.items_list: [] = my_list
        self.header = my_header

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.items_list)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.header)

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        if index.column() == 0:
            return self.items_list[index.row()].name
        elif index.column() == 1:
            return self.items_list[index.row()].products

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        return None
