from typing import Any

import PySide2
import requests
from PySide2.QtCore import QJsonDocument, QAbstractTableModel, Qt, QUrl, QSortFilterProxyModel, QTimer, QThread, QObject, Signal
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide2.QtWidgets import QDialog, QProgressDialog, QAbstractItemView, QMessageBox

from models.api.Category import Category
from views import updater_dialog


class UpdaterDialogController(QDialog):
    def __init__(self, parent):
        super(UpdaterDialogController, self).__init__(parent)

        self.categories_progress = QProgressDialog("Récupération des catégories...", "Annuler", 0, 3, self)
        self.categories_progress.reset()
        self.categories_progress.setFixedWidth(300)
        self.categories_progress.canceled.connect(self.handle_cancel_request_list_categories)

        self.products_progress = QProgressDialog("Téléchargement des produits...", "Annuler", 0, 0, self)
        self.products_progress.reset()
        self.products_progress.setFixedWidth(300)
        # self.products_progress.canceled.connect(self.handle_api_reply_category_products)

        self.network_access_manager = QNetworkAccessManager()
        self.man = QNetworkAccessManager()

        self.ui = updater_dialog.Ui_Dialog()

        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModal)

        self.all_categories = []
        self.selected_categories = []

        self.ui.btn_load_list.clicked.connect(self.fetch_categories)
        self.ui.btn_add_category.clicked.connect(self.add_category)
        self.ui.btn_delete_category.clicked.connect(self.delete_category)
        self.ui.btn_download_products.clicked.connect(self.download_products)

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
        self.ui.table_selected_categories.setSortingEnabled(True)
        self.ui.table_selected_categories.sortByColumn(1, Qt.DescendingOrder)

        self.timer = QTimer()
        self.timer.timeout.connect(self.handle_api_timeout_list_categories)
        self.timer.setSingleShot(True)
        self.timer.setInterval(10000)

        self.api_list_categories_reply = None
        self.api_category_products_reply = None
        self.api_products_details_reply = None

        self.threads = []
        self.objects = []

    def fetch_categories(self):
        self.categories_progress.open()
        self.categories_progress.setValue(1)

        request = QNetworkRequest(QUrl("https://fr.openfoodfacts.org/categories.json"))
        self.timer.start()

        self.api_list_categories_reply = self.network_access_manager.get(request)
        self.api_list_categories_reply.finished.connect(self.handle_api_reply_list_categories)

    def handle_api_reply_list_categories(self):
        self.timer.stop()

        self.categories_progress.setValue(2)

        error = self.api_list_categories_reply.error()

        if error == QNetworkReply.NoError:
            bytes_string = self.api_list_categories_reply.readAll()
            json = QJsonDocument.fromJson(bytes_string)
            obj = json.object()["tags"]

            self.all_categories_table_model.beginResetModel()

            self.all_categories.clear()

            for item in obj:
                if item["products"] >= 5000:
                    self.all_categories.append(Category(item["name"], item["products"], item["id"]))

            self.all_categories_table_model.endResetModel()
            self.ui.table_all_categories.resizeColumnsToContents()

            self.categories_progress.setValue(3)

        else:
            print("Error occured: ", error)
            print(self.api_list_categories_reply.errorString())

    def handle_api_timeout_list_categories(self):
        self.api_list_categories_reply.finished.disconnect()
        self.api_list_categories_reply.abort()
        self.categories_progress.cancel()

        dialog = QMessageBox(
            QMessageBox.Critical,
            "Erreur",
            "OpenFoodFacts prend trop de temps pour répondre. Veuillez réessayer plus tard.",
            QMessageBox.Ok,
            self
        )

        dialog.setWindowModality(Qt.WindowModal)
        dialog.show()

    def handle_cancel_request_list_categories(self):
        self.api_list_categories_reply.finished.disconnect()
        self.timer.stop()
        self.api_list_categories_reply.abort()
        self.categories_progress.cancel()

    def add_category(self):
        proxy_model: QSortFilterProxyModel = self.ui.table_all_categories.model()
        source_model: CategoriesTableModel = proxy_model.sourceModel()

        self.selected_categories_table_model.beginResetModel()

        for row in self.ui.table_all_categories.selectionModel().selectedRows():
            model_index = proxy_model.index(row.row(), 0)
            source_index = proxy_model.mapToSource(model_index).row()

            if source_model.items_list[source_index] not in self.selected_categories:
                self.selected_categories.append(source_model.items_list[source_index])

        self.selected_categories_table_model.endResetModel()
        self.ui.table_selected_categories.resizeColumnsToContents()

    def delete_category(self):
        proxy_model: QSortFilterProxyModel = self.ui.table_selected_categories.model()

        self.selected_categories_table_model.beginResetModel()

        for row in self.ui.table_selected_categories.selectionModel().selectedRows():
            model_index = proxy_model.index(row.row(), 0)
            source_index = proxy_model.mapToSource(model_index).row()
            self.selected_categories.pop(source_index)
            self.ui.table_selected_categories.resizeColumnsToContents()

        self.selected_categories_table_model.endResetModel()

    def download_products(self):
        for category in self.selected_categories:
            url = ("https://fr.openfoodfacts.org/cgi/search.pl?"
                   "action=process&"
                   "tagtype_0=categories&"
                   "tag_contains_0=contains&"
                   f"tag_0={category.id}&"
                   "sort_by=unique_scans_n&"
                   "page_size=50&"
                   "json=1")

            thread = QThread()
            self.threads.append(thread)
            obj = DownloaderThread(url)
            self.objects.append(obj)

            obj.moveToThread(thread)
            obj.finished.connect(thread.quit)

            thread.started.connect(obj.run)
            thread.finished.connect(self.notify_done)
            thread.start()

    def notify_done(self):
        print("done")


class DownloaderThread(QObject):
    finished = Signal()

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        request = requests.get(self.url)

        for product in request.json()["products"]:
            print(product)

            if "product_name" in product:
                print("Nom : " + product["product_name"])

            if "ingredients_text_fr" in product:
                print("Ingrédients : " + product["ingredients_text_fr"])

            if "allergens_from_ingredients" in product:
                print("Allergènes : " + product["allergens_from_ingredients"])

            nutriments = product["nutriments"]

            if "nutrition-score-fr" in nutriments:
                print("Nutriscore : " + str(nutriments["nutrition-score-fr"]))

            if "energy_100g" in nutriments:
                print("Energie : " + str(nutriments["energy_100g"]))

            if "carbohydrates_100g" in nutriments:
                print("Glucides : " + str(nutriments["carbohydrates_100g"]))

            if "sugars_100g" in nutriments:
                print("Sucres : " + str(nutriments["sugars_100g"]))

            if "saturated-fat_100g" in nutriments:
                print("Acides gras saturés : " + str(nutriments["saturated-fat_100g"]))

            if "sodium_100g" in nutriments:
                print("Sodium : " + str(nutriments["sodium_100g"]))

            if "salt_100g" in nutriments:
                print("Sel : " + str(nutriments["salt_100g"]))

            if "fiber_100g" in nutriments:
                print("Fibres : " + str(nutriments["fiber_100g"]))

            if "proteins_100g" in nutriments:
                print("Protéines : " + str(nutriments["proteins_100g"]))

            if "brands_tags" in product:
                print("Marques : ")
                print(product["brands_tags"])

            if "stores_tags" in product:
                print("Magasins : ")
                print(product["stores_tags"])

            print("lol")

        self.finished.emit()


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
