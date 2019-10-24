import os

import markdown
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QImage
from PySide2.QtWidgets import QMainWindow

from controllers.main_window.categories_combobox_model import CategoriesComboBoxModel
from controllers.main_window.find_substitutes_thread import FindSubstitutesThread
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

        query = Category.select().dicts()
        categories = list(query)
        categories.sort(key=lambda x: x["category_name"])
        model = CategoriesComboBoxModel(categories)
        self.ui.cmb_categories.setModel(model)

        self.find_substitutes_thread = FindSubstitutesThread()

        self.ui.btn_find_substitutes.clicked.connect(self.find_substitutes)

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
        food = self.ui.lst_products.model().data(current, Qt.UserRole)
        self.ui.lbl_ingredients.setText(markdown.markdown(food["ingredients"]))
        self.ui.lbl_allergens.setText(markdown.markdown(food["allergens"]) if food["allergens"] else markdown.markdown("_Aucun_"))

        if food["energy_unit"] == "kcal":
            kj = round(food["energy_100g"] * 4.18, 1)
            energy_string = f"{food['energy_100g']} kcal ({kj} kj)"
        else:
            kcal = round(food["energy_100g"] / 4.18, 1)
            energy_string = f"{kcal} kcal ({food['energy_100g']} kj)"

        html_spaces = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

        nutriments = [
            ["<b>Energie</b>", energy_string],
            ["<b>Glucides</b>", f"{food['carbohydrates_100g']} g"],
            [f"{html_spaces}Sucres", f"{food['sugars_100g']} g"],
            ["<b>Matières grasses</b>", f"{food['fat_100g']} g"],
            [f"{html_spaces}Acides gras saturés", f"{food['saturated_fat_100g']} g"],
            ["<b>Sel</b>", f"{food['salt_100g']} g"],
            [f"{html_spaces}Sodium", f"{food['sodium_100g']} g"],
            ["<b>Fibres</b>", f"{food['fiber_100g']} g"],
            ["<b>Protéines</b>", f"{food['proteins_100g']} g"]
        ]

        nutriments_table_content = "<style>td { padding: 3px; }</style>"

        nutriments_table_content += "<table width=100% border=1 cellspacing=0 cellpadding=0>"

        for nutriment in nutriments:
            nutriments_table_content += "<tr>"
            for column in nutriment:
                nutriments_table_content += "<td>"
                nutriments_table_content += str(column)
                nutriments_table_content += "</td>"
            nutriments_table_content += "</tr>"

        nutriments_table_content += "</table>"

        self.ui.lbl_nutriments.setText(nutriments_table_content)

        current_directory = os.path.dirname(__file__)
        filename = os.path.join(current_directory, "..", "..", "assets", f"nutriscore_{food['nutrition_grade']}.png")

        image = QImage(filename)
        pix_map = QPixmap()
        pix_map.convertFromImage(image.scaledToHeight(100, Qt.SmoothTransformation))

        self.ui.lbl_nutriscore.setPixmap(pix_map)

    def open_updater_dialog(self):
        dialog = UpdaterDialogController(self)
        dialog.exec_()

    def find_substitutes(self):
        product_index = self.ui.lst_products.selectionModel().selectedIndexes()[0]
        self.find_substitutes_thread.product = self.ui.lst_products.model().data(product_index, Qt.UserRole)

        category = self.ui.cmb_categories.currentData(Qt.UserRole)
        self.find_substitutes_thread.category = category

        self.find_substitutes_thread.run()
