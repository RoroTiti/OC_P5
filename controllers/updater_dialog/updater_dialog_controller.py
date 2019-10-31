from PySide2 import QtWidgets
from PySide2.QtCore import Qt, QSortFilterProxyModel
from PySide2.QtWidgets import QDialog, QProgressDialog, QAbstractItemView, QMainWindow

from controllers.updater_dialog.categories_downloader_thread import CategoriesDownloaderThread
from controllers.updater_dialog.categories_table_model import CategoriesTableModel
from controllers.updater_dialog.products_downloader_thread import ProductsDownloaderThread
from views import updater_dialog


class UpdaterDialogController(QDialog):
    """
    Controller of the data updater dialog
    """

    def __init__(self, parent: QMainWindow):
        """
        Initialize a UpdaterDialogController object

        :param parent:
        """
        super(UpdaterDialogController, self).__init__(parent)

        self.categories_progress = QProgressDialog("Récupération des catégories...", "Annuler", 0, 0, self)
        self.categories_progress.reset()
        self.categories_progress.setFixedWidth(300)
        self.categories_progress.canceled.connect(self.cancel_categories_downloader)
        self.categories_progress.setWindowModality(Qt.WindowModal)

        self.products_progress = QProgressDialog("Téléchargement des produits...", "Annuler", 0, 0, self)
        self.products_progress.reset()
        self.products_progress.setFixedWidth(300)
        self.products_progress.canceled.connect(self.cancel_products_downloader)
        self.products_progress.setWindowModality(Qt.WindowModal)

        self.ui = updater_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.WindowModal)

        self.all_categories = []
        self.selected_categories = []

        self.ui.btn_load_list.clicked.connect(self.download_categories)
        self.ui.btn_add_category.clicked.connect(self.add_category)
        self.ui.btn_delete_category.clicked.connect(self.delete_category)
        self.ui.btn_download_products.clicked.connect(self.download_products)
        self.ui.btn_close.clicked.connect(self.close_dialog)

        # All categories list initialization
        self.all_categories_table_model = CategoriesTableModel(self, self.all_categories)

        all_categories_proxy = QSortFilterProxyModel()
        all_categories_proxy.setSourceModel(self.all_categories_table_model)

        self.ui.table_all_categories.setModel(all_categories_proxy)
        self.ui.table_all_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_all_categories.setSortingEnabled(True)
        self.ui.table_all_categories.sortByColumn(1, Qt.DescendingOrder)
        self.ui.table_all_categories.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.table_all_categories.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        # Selected categories list initialization
        self.selected_categories_table_model = CategoriesTableModel(self, self.selected_categories)

        selected_categories_proxy = QSortFilterProxyModel()
        selected_categories_proxy.setSourceModel(self.selected_categories_table_model)

        self.ui.table_selected_categories.setModel(selected_categories_proxy)
        self.ui.table_selected_categories.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_selected_categories.setSortingEnabled(True)
        self.ui.table_selected_categories.sortByColumn(1, Qt.DescendingOrder)
        self.ui.table_selected_categories.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.table_selected_categories.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.categories_downloader = CategoriesDownloaderThread()
        self.categories_downloader.progress.connect(self.set_categories_downloader_progress)
        self.categories_downloader.result.connect(self.set_all_categories)
        self.categories_downloader.finished.connect(self.categories_downloader_finished)

        self.products_downloader = ProductsDownloaderThread()
        self.products_downloader.progress.connect(self.set_products_downloader_progress)
        self.products_downloader.finished.connect(self.products_downloader_finished)

    def add_category(self) -> None:
        """
        Add a category highlighted by the user into the whole categories list to the selected categories list
        """
        self.selected_categories_table_model.beginResetModel()

        for index in self.ui.table_all_categories.selectionModel().selectedIndexes():
            if index.data(Qt.UserRole) not in self.selected_categories:
                self.selected_categories.append(index.data(Qt.UserRole))

        self.selected_categories_table_model.endResetModel()

    def delete_category(self) -> None:
        """
        Delete a category highlighted by the user from the selected categories list
        """
        self.selected_categories_table_model.beginResetModel()

        selected_categories_after_filtering = self.selected_categories

        for index in self.ui.table_selected_categories.selectionModel().selectedIndexes():
            selected_categories_after_filtering = list(
                filter(lambda x: x["id"] != index.data(Qt.UserRole)["id"], selected_categories_after_filtering))

        self.selected_categories.clear()
        self.selected_categories += selected_categories_after_filtering

        self.selected_categories_table_model.endResetModel()

    def download_categories(self) -> None:
        """
        Download the categories from the OpenFoodFacts API
        """
        self.categories_progress.setMaximum(self.categories_downloader.max_progress)
        self.categories_progress.show()
        self.categories_downloader.start()

    def set_categories_downloader_progress(self, current_progress: int) -> None:
        """
        Update the categories downloading progress bar

        :param current_progress: The current progress of categories downloading
        """
        self.categories_progress.setValue(current_progress)

    def cancel_categories_downloader(self) -> None:
        """
        Cancel the categories downloading
        """
        self.categories_downloader.requestInterruption()

    def categories_downloader_finished(self) -> None:
        """
        Reset the categories downloader progress bar once the download is finished
        """
        self.categories_progress.reset()

    def set_all_categories(self, all_categories: list) -> None:
        """
        Display the whole categories list into the all categories table

        :param all_categories: The categories to diplay
        """
        self.all_categories_table_model.beginResetModel()
        self.all_categories.clear()
        self.all_categories += all_categories
        self.all_categories_table_model.endResetModel()

    def download_products(self) -> None:
        """
        Downland the products of the selected categories
        """
        self.products_downloader.selected_categories = self.selected_categories
        self.products_progress.setMaximum(self.products_downloader.max_progress)
        self.products_progress.show()
        self.products_downloader.start()

    def set_products_downloader_progress(self, current_progress: int) -> None:
        """
        Update the products downloading progress bar

        :param current_progress: The current progress of products downloading
        """
        self.products_progress.setValue(current_progress)

    def cancel_products_downloader(self) -> None:
        """
        Cancel the products downloading
        """
        self.products_downloader.requestInterruption()

    def products_downloader_finished(self) -> None:
        """
        Reset the predicts downloader progress bar once the download is finished
        """
        self.products_progress.reset()

    def close_dialog(self) -> None:
        """
        Handle click on close button
        """
        self.done(0)

    def reject(self) -> None:
        """
        Handle escape key press
        """
        self.done(0)
