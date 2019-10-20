from PySide2.QtCore import Qt, QSortFilterProxyModel
from PySide2.QtWidgets import QDialog, QProgressDialog, QAbstractItemView

from controllers.updater_dialog.categories_downloader_thread import CategoriesDownloaderThread
from controllers.updater_dialog.categories_table_model import CategoriesTableModel
from controllers.updater_dialog.products_downloader_thread import ProductsDownloaderThread
from views import updater_dialog


class UpdaterDialogController(QDialog):
    def __init__(self, parent):
        super(UpdaterDialogController, self).__init__(parent)

        self.categories_progress = QProgressDialog("Récupération des catégories...", "Annuler", 0, 0, self)
        self.categories_progress.reset()
        self.categories_progress.setFixedWidth(300)
        self.categories_progress.canceled.connect(self.cancel_categories_downloader)

        self.products_progress = QProgressDialog("Téléchargement des produits...", "Annuler", 0, 0, self)
        self.products_progress.reset()
        self.products_progress.setFixedWidth(300)
        self.products_progress.canceled.connect(self.cancel_products_downloader)

        self.ui = updater_dialog.Ui_Dialog()

        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModal)

        self.all_categories = []
        self.selected_categories = []

        self.ui.btn_load_list.clicked.connect(self.download_categories)
        self.ui.btn_add_category.clicked.connect(self.add_category)
        self.ui.btn_delete_category.clicked.connect(self.delete_category)
        self.ui.btn_download_products.clicked.connect(self.download_products)

        headers = ["Catégorie", "Nombre de produits"]

        # All categories list initialization
        self.all_categories_table_model = CategoriesTableModel(self, self.all_categories, headers)

        all_categories_proxy = QSortFilterProxyModel()
        all_categories_proxy.setSourceModel(self.all_categories_table_model)

        self.ui.table_all_categories.setModel(all_categories_proxy)
        self.ui.table_all_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_all_categories.setSortingEnabled(True)
        self.ui.table_all_categories.sortByColumn(1, Qt.DescendingOrder)

        # Selected categories list initialization
        self.selected_categories_table_model = CategoriesTableModel(self, self.selected_categories, headers)

        selected_categories_proxy = QSortFilterProxyModel()
        selected_categories_proxy.setSourceModel(self.selected_categories_table_model)

        self.ui.table_selected_categories.setModel(selected_categories_proxy)
        self.ui.table_selected_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_selected_categories.setSortingEnabled(True)
        self.ui.table_selected_categories.sortByColumn(1, Qt.DescendingOrder)

        self.categories_downloader = None
        self.products_downloader = None

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

    def download_categories(self):
        self.categories_downloader = CategoriesDownloaderThread()
        self.categories_downloader.result.connect(self.set_all_categories)
        self.categories_downloader.progress.connect(self.set_categories_downloader_progress)
        self.categories_progress.setMaximum(self.categories_downloader.max_progress)
        self.categories_progress.show()
        self.categories_downloader.start()

    def set_categories_downloader_progress(self, current_progress):
        self.categories_progress.setValue(current_progress)

    def cancel_categories_downloader(self):
        self.categories_downloader.quit()

    def set_all_categories(self, all_categories):
        self.all_categories_table_model.beginResetModel()
        self.all_categories.clear()
        self.all_categories += all_categories
        self.all_categories_table_model.endResetModel()
        self.ui.table_all_categories.resizeColumnsToContents()

    def download_products(self):
        self.products_downloader = ProductsDownloaderThread(self.selected_categories)
        self.products_downloader.progress.connect(self.set_products_downloader_progress)
        self.products_progress.setMaximum(self.products_downloader.max_progress)
        self.products_progress.show()
        self.products_downloader.start()

    def set_products_downloader_progress(self, current_progress):
        self.products_progress.setValue(current_progress)

    def cancel_products_downloader(self):
        self.products_downloader.quit()
