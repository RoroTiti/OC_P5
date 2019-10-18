from typing import Any

import PySide2
import requests
from PySide2.QtCore import QJsonDocument, QAbstractTableModel, Qt, QUrl, QSortFilterProxyModel, QTimer, QThread, QObject, Signal
from PySide2.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide2.QtWidgets import QDialog, QProgressDialog, QAbstractItemView, QMessageBox

from models.api.category import Category
from models.database.models import Brand, Store, Food
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
        self.operations_done = 0

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
            obj = DownloaderThread(url, category)
            self.objects.append(obj)

            obj.moveToThread(thread)
            obj.finished.connect(thread.quit)

            thread.started.connect(obj.run)
            thread.finished.connect(self.notify_done)
            thread.start()

    def notify_done(self):
        self.operations_done += 1
        print("DONE >>>>> " + str(self.operations_done) + "/" + str(len(self.threads)))


class DownloaderThread(QObject):
    finished = Signal()

    def __init__(self, url, category):
        super().__init__()
        self.url: str = url
        self.category: Category = category

    def run(self):
        request = requests.get(self.url)

        expected_product_keys = [
            "product_name",
            "ingredients_text_fr",
            "allergens_from_ingredients",
            "nutriments",
            "brands_tags",
            "brands",
            "stores_tags",
            "stores"
        ]

        expected_nutriments_keys = [
            "nutrition-score-fr",
            "energy_100g",
            "carbohydrates_100g",
            "sugars_100g",
            "saturated-fat_100g",
            "sodium_100g",
            "salt_100g",
            "fiber_100g",
            "proteins_100g"
        ]

        for product in request.json()["products"]:
            if all(key in product for key in expected_product_keys):
                nutriments = product["nutriments"]
                if all(key in nutriments for key in expected_nutriments_keys):
                    if len(product["brands_tags"]) > 0 and len(product["stores_tags"]) > 0:
                        # The product has all required characteristics to be integrated into the database
                        print("ok")

                        # Getting the individual brands
                        brands: str = product["brands"]
                        brands_list = brands.split(",")

                        for index, brand in enumerate(brands_list):
                            brands_list[index] = brand.upper().lstrip().rstrip()
                            if Brand.select().where(Brand.brand_name == brands_list[index]).count() == 0:
                                Brand.create(company_name=brands_list[index])

                        print(brands_list)

                        # Getting the individual stores
                        stores: str = product["stores"]
                        stores_list = stores.split(",")

                        for index, store in enumerate(stores_list):
                            stores_list[index] = store.upper().lstrip().rstrip()
                            if Store.select().where(Store.store_name == stores_list[index]).count() == 0:
                                Store.create(store_name=stores_list[index])

                        print(stores_list)

                        # Inserting the food product into the database
                        Food.create(
                            allergens=product["allergens_from_ingredients"],
                            carbohydrates_100g=nutriments["carbohydrates_100g"],
                            energy_100g=nutriments["energy_100g"],
                            fat_100g=nutriments["fat_100g"],
                            fiber_100g=nutriments["fiber_100g"],
                            food_name=product["product_name"],
                            ingredients=product["ingredients_text_fr"],
                            name=product["product_name"],
                            nutriscore=nutriments["nutrition-score-fr"],
                            proteins_100g=nutriments["proteins_100g"],
                            salt_100g=nutriments["salt_100g"],
                            saturated_fat_100g=nutriments["saturated-fat_100g"],
                            sodium_100g=nutriments["sodium_100g"],
                            sugars_100g=nutriments["sugars_100g"],
                        )

                    else:
                        print("not ok brands or stores")
                else:
                    print("not ok nutriments")
            else:
                print("not ok product")

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
