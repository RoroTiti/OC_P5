import markdown
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QHeaderView

from controllers.main_window.categories_combobox_model import CategoriesComboBoxModel
from controllers.main_window.nutriments_table_model import NutrimentsTableModel
from controllers.main_window.products_fetcher_thread import ProductsFetcherThread
from controllers.main_window.products_list_model import ProductsListModel
from controllers.updater_dialog.updater_dialog_controller import UpdaterDialogController
from models.database.models import Category, Food
from views import main_window


class MainWindowController(QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_update.triggered.connect(self.open_updater_dialog)

        self.ui.cmb_categories.currentIndexChanged.connect(self.category_selection_changed)

        self.fetcher_thread = ProductsFetcherThread()
        self.fetcher_thread.result.connect(self.set_list_products_model)

        query = Category.select()
        categories = list(query)
        categories.sort(key=lambda x: x.category_name)
        model = CategoriesComboBoxModel(categories)
        self.ui.cmb_categories.setModel(model)

    def category_selection_changed(self, index):
        category = self.ui.cmb_categories.currentData(Qt.UserRole)
        self.fetcher_thread.category = category
        self.fetcher_thread.start()

    def set_list_products_model(self, products):
        model = ProductsListModel(products)
        self.ui.lst_products.setModel(model)
        self.ui.lst_products.selectionModel().currentChanged.connect(self.product_selection_changed)

        index = model.index(0, 0)

        if index.isValid():
            self.ui.lst_products.setCurrentIndex(index)

    def product_selection_changed(self, current, previous):
        food: Food = self.ui.lst_products.model().data(current, Qt.UserRole)
        self.ui.lbl_ingredients.setText(markdown.markdown(food["ingredients"]))
        self.ui.lbl_allergens.setText(markdown.markdown(food["allergens"]) if food["allergens"] else markdown.markdown("_Aucun_"))

        lst = [
            ["Energie", food["energy_100g"]],
            ["Glucides", food["carbohydrates_100g"]],
            ["Sucres", food["sugars_100g"]],

            ["Energie", food["energy_100g"]],
            ["Glucides", food["carbohydrates_100g"]],
            ["Sucres", food["sugars_100g"]],
            ["Energie", food["energy_100g"]],
            ["Glucides", food["carbohydrates_100g"]],
            ["Sucres", food["sugars_100g"]],
        ]

        model = NutrimentsTableModel(lst)
        self.ui.table_nutriments.setModel(model)
        self.ui.table_nutriments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.vertical_resize_table_view_to_contents(self.ui.table_nutriments)

    def open_updater_dialog(self):
        dialog = UpdaterDialogController(self)
        dialog.exec_()

    @staticmethod
    def vertical_resize_table_view_to_contents(table_view):
        count = table_view.verticalHeader().count()
        scroll_bar_height = table_view.horizontalScrollBar().height()
        horizontal_header_height = table_view.horizontalHeader().height()
        row_total_height = 0

        for i in range(count):
            row_total_height += table_view.verticalHeader().sectionSize(i)

        table_view.setFixedHeight(horizontal_header_height + row_total_height + scroll_bar_height)
