import PySide2
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt, QObject, Signal, QModelIndex
from PySide2.QtWidgets import QMainWindow, QAbstractItemView, QMessageBox, QTableView

from controllers.about_data_window.about_data_window_controller import DataInformationDialogController
from controllers.main_window.categories_combobox_model import CategoriesComboBoxModel
from controllers.main_window.find_substitutes_thread import FindSubstitutesThread
from controllers.main_window.products_fetcher_thread import ProductsFetcherThread
from controllers.main_window.products_table_model import ProductsTableModel
from controllers.main_window.save_substitute_thread import SaveSubstituteThread
from controllers.main_window.saved_substitutes_fetcher_thread import SavedSubstitutesFetcherThread
from controllers.main_window.saved_substitutes_table_model import SavedSubstitutesTableModel
from controllers.main_window.single_product_fetcher_thread import SingleProductFetcherThread
from controllers.product_details_window.product_details_window_controller import ProductDetailsWindowController
from controllers.updater_dialog.updater_dialog_controller import UpdaterDialogController
from models.database import Category
from views import main_window


class MainWindowController(QMainWindow):
    """
    Controller of the application main window
    """

    def __init__(self):
        """
        Initializes a MainWindowController object
        """
        super(MainWindowController, self).__init__()

        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_update.triggered.connect(self.open_updater_dialog)
        self.ui.action_about_data.triggered.connect(self.open_data_information_dialog)

        self.ui.tabWidget.currentChanged.connect(self.tab_changed)
        self.ui.cmb_categories.currentIndexChanged.connect(self.category_selection_changed)
        self.ui.btn_save_substitute.clicked.connect(self.save_substitute)

        self.fetcher_thread = ProductsFetcherThread()
        self.fetcher_thread.result.connect(self.set_list_products)

        query = Category.select().dicts().execute()
        categories = list(query)
        categories.sort(key=lambda x: x["category_name"])
        model = CategoriesComboBoxModel(categories)
        self.ui.cmb_categories.setModel(model)

        self.find_substitutes_thread = FindSubstitutesThread()
        self.find_substitutes_thread.result.connect(self.set_list_substitutes)

        self.save_substitute_thread = SaveSubstituteThread()
        self.save_substitute_thread.already_saved.connect(self.notify_already_saved)

        self.saved_substitutes_fetcher_thread = SavedSubstitutesFetcherThread()
        self.saved_substitutes_fetcher_thread.result.connect(self.set_table_saved_substitutes_model)

        self.product_fetcher_thread = SingleProductFetcherThread()
        self.product_fetcher_thread.result.connect(self.open_product_details_dialog)

        self.products = []
        self.ui.table_products.setModel(ProductsTableModel(self.products))
        self.ui.table_products.doubleClicked.connect(self.product_details_requested)
        self.ui.table_products.selectionModel().currentChanged.connect(self.load_substitutes)
        self.ui.table_products.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_products.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.table_products.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table_products.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table_products.setFocus()

        self.substitutes = []
        self.ui.table_substitutes.setModel(ProductsTableModel(self.substitutes))
        self.ui.table_substitutes.doubleClicked.connect(self.product_details_requested)
        self.ui.table_substitutes.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.table_substitutes.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.table_substitutes.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.ui.table_substitutes.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        self.saved_substitutes = []
        self.ui.table_saved_substitutes.setModel(SavedSubstitutesTableModel(self.saved_substitutes))
        self.ui.table_saved_substitutes.doubleClicked.connect(self.product_details_requested)
        self.ui.table_saved_substitutes.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.table_saved_substitutes.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.table_saved_substitutes.setStyleSheet("QTableView::item { padding: 5; }")

        event = PressEnterEventFilter(self.ui.table_products)
        self.ui.table_products.installEventFilter(event)
        event.result.connect(self.product_details_requested)

        event = PressEnterEventFilter(self.ui.table_substitutes)
        self.ui.table_substitutes.installEventFilter(event)
        event.result.connect(self.product_details_requested)

        event = PressEnterEventFilter(self.ui.table_saved_substitutes)
        self.ui.table_saved_substitutes.installEventFilter(event)
        event.result.connect(self.product_details_requested)

    def tab_changed(self, index: int) -> None:
        """
        Handle the table changed event between Search and Saved searches tabs

        :param index: The index of the selected tab
        """
        if index == 1:
            self.saved_substitutes_fetcher_thread.run()

    def category_selection_changed(self) -> None:
        """
        Handle the reloading of the products list when the user select a different category
        """
        category = self.ui.cmb_categories.currentData(Qt.UserRole)
        self.fetcher_thread.category = category
        self.fetcher_thread.start()

    def set_list_products(self, products: list) -> None:
        """
        Display the products on the products list

        :param products: The list of the products to display
        """
        self.ui.table_products.model().beginResetModel()
        self.products.clear()
        self.products += products
        self.ui.table_products.model().endResetModel()

        index = self.ui.table_products.model().index(0, 0)

        if index.isValid():
            self.ui.table_products.setCurrentIndex(index)

    def product_details_requested(self, current_index: QModelIndex) -> None:
        """
        Load the product details when the user request the products details, with a double click or a click + enter on an item

        :param current_index: The model index holding the product data
        """
        food = current_index.data(Qt.UserRole)
        self.product_fetcher_thread.food_id = food["id_food"]
        self.product_fetcher_thread.run()

    def open_product_details_dialog(self, product_details: object) -> None:
        """
        Open the product details dialog after the data have been fetched by the thread

        :param product_details: The details of the product to display
        """
        dialog = ProductDetailsWindowController(self, product_details)
        dialog.show()

    def load_substitutes(self) -> None:
        """
        Load the substitutes for the selected product into the selected category
        """
        category = self.ui.cmb_categories.currentData(Qt.UserRole)
        self.find_substitutes_thread.category = category
        food = self.ui.table_products.currentIndex().data(Qt.UserRole)
        self.find_substitutes_thread.product = food
        self.find_substitutes_thread.run()

    def set_list_substitutes(self, substitutes: list) -> None:
        """
        Display the substitutes on the substitutes list

        :param substitutes:
        """
        self.ui.table_substitutes.model().beginResetModel()
        self.substitutes.clear()
        self.substitutes += substitutes
        self.ui.table_substitutes.model().endResetModel()

    def save_substitute(self) -> None:
        """
        Save the selected substitute into the search history on the database
        """
        selected_substitute_index = self.ui.table_substitutes.currentIndex()
        selected_substitute = self.ui.table_substitutes.model().data(selected_substitute_index, Qt.UserRole)

        selected_product_index = self.ui.table_products.currentIndex()
        selected_product = self.ui.table_products.model().data(selected_product_index, Qt.UserRole)

        self.save_substitute_thread.id_food = selected_product["id_food"]
        self.save_substitute_thread.id_food_substitute = selected_substitute["id_food"]
        self.save_substitute_thread.run()

    def set_table_saved_substitutes_model(self, substitutes: list) -> None:
        """
        Display the saved substitutes list on the saved substitutes list

        :param substitutes: The substitutes to display
        """
        self.ui.table_saved_substitutes.model().beginResetModel()
        self.saved_substitutes.clear()
        self.saved_substitutes += substitutes
        self.ui.table_saved_substitutes.model().endResetModel()
        self.ui.table_saved_substitutes.resizeRowsToContents()

    def notify_already_saved(self) -> None:
        """
        Display an error message if the product and its substitute are already saved into the database
        """
        msg = QMessageBox(QMessageBox.Information, "Information", "Ce substitut est déjà enregistré dans la base de données", QMessageBox.Ok, self)
        msg.setWindowModality(Qt.WindowModal)
        msg.exec_()

    def open_updater_dialog(self) -> None:
        """
        Open the database updater tool dialog
        """
        dialog = UpdaterDialogController(self)
        dialog.exec_()

    def open_data_information_dialog(self) -> None:
        """
        Open the data information tool dialog
        """
        dialog = DataInformationDialogController(self)
        dialog.exec_()


class PressEnterEventFilter(QObject):
    """
    Event filter filtering the Enter keypress event
    """
    result = Signal(QModelIndex)

    def eventFilter(self, watched: PySide2.QtCore.QObject, event: PySide2.QtCore.QEvent) -> bool:
        """
        Handle the Enter keypress event

        :param watched: The watched widget
        :param event: The event happened
        """
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
                source: QTableView = watched
                self.result.emit((source.selectionModel().currentIndex()))
                return True
            return super().eventFilter(watched, event)
        return super().eventFilter(watched, event)
