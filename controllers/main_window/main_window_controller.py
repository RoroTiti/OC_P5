import markdown
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow

from controllers.main_window.categories_combobox_model import CategoriesComboBoxModel
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

        if food["energy_unit"] == "kcal":
            kj = round(food["energy_100g"] * 4.18, 1)
            energy_string = f"{food['energy_100g']} kcal ({kj} kj)"
        else:
            kcal = round(food["energy_100g"] / 4.18, 1)
            energy_string = f"{kcal} kcal ({food['energy_100g']} kj)"

        lst = [
            ["Energie", energy_string],
            ["Glucides", f"{food['carbohydrates_100g']} g"],
            ["Sucres", f"{food['sugars_100g']} g"],
            ["Matières grasses", f"{food['fat_100g']} g"],
            ["Acides gras saturés", f"{food['saturated_fat_100g']} g"],
            ["Sel", f"{food['salt_100g']} g"],
            ["Sodium", f"{food['sodium_100g']} g"],
            ["Fibres", f"{food['fiber_100g']} g"],
            ["Protéines", f"{food['proteins_100g']} g"]
        ]

        tbl = "<table width=100% border=1 cellspacing=0 cellpadding=0>"

        for item in lst:
            tbl += "<tr>"
            for sub_item in item:
                tbl += "<td>"
                tbl += str(sub_item)
                tbl += "</td>"
            tbl += "</tr>"

        tbl += "</table>"

        self.ui.lbl_nutriments.setText(tbl)

    def open_updater_dialog(self):
        dialog = UpdaterDialogController(self)
        dialog.exec_()
