import typing

import PySide2
from PySide2.QtCore import QJsonDocument, QAbstractTableModel, Qt, QUrl, QItemSelection, QSortFilterProxyModel
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide2.QtWidgets import QDialog, QProgressDialog, QAbstractItemView, QHeaderView

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

        self.ui.btn_load_list.clicked.connect(self.fetch_categories)

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

            categories_gt_5000 = []

            for item in obj:
                if item["products"] >= 5000:
                    categories_gt_5000.append(Category(item["name"], item["products"], item["id"]))

            categories_gt_5000.sort(key=lambda x: x.name)

            table_model = CategoriesTableModel(self, categories_gt_5000, ["Catégorie", "Nombre de produits"])

            filter_proxy_model = QSortFilterProxyModel()
            filter_proxy_model.setSourceModel(table_model)
            filter_proxy_model.setDynamicSortFilter(False)
            filter_proxy_model.sort(1, Qt.DescendingOrder)

            self.ui.table_all_categories.setModel(filter_proxy_model)
            self.ui.table_all_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.ui.table_all_categories.setSelectionMode(QAbstractItemView.SingleSelection)
            self.ui.table_all_categories.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.ui.table_all_categories.setSortingEnabled(True)
            self.ui.table_all_categories.sortByColumn(1, Qt.DescendingOrder)

            selection_model = self.ui.table_all_categories.selectionModel()
            selection_model.selectionChanged.connect(self.on_category_selected)

        else:
            print("Error occured: ", error)
            print(reply.errorString())

        self.progress.close()

    def on_category_selected(self, selected: QItemSelection, deselected: QItemSelection):
        selected_index = self.ui.table_all_categories.selectionModel().currentIndex().row()
        proxy_model: QSortFilterProxyModel = self.ui.table_all_categories.model()
        model_index = proxy_model.index(selected_index, 0)
        source_model: CategoriesTableModel = proxy_model.sourceModel()
        source_index = proxy_model.mapToSource(model_index)
        print(source_model.items_list[source_index.row()].id)


class CategoriesTableModel(QAbstractTableModel):
    def __init__(self, parent, my_list, my_header):
        QAbstractTableModel.__init__(self, parent)
        self.items_list: [Category] = my_list
        self.header = my_header

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self.items_list)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return 2

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        if index.column() == 0:
            return self.items_list[index.row()].name
        elif index.column() == 1:
            return self.items_list[index.row()].products

    def headerData(self, section: int, orientation: PySide2.QtCore.Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
        return None
