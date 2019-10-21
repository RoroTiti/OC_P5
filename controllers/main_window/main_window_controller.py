from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QMainWindow

from controllers.updater_dialog.updater_dialog_controller import UpdaterDialogController
from models.database.models import Category, Food, CategoryFood, BrandFood, Brand
from views import main_window


class MainWindowController(QMainWindow):
    def __init__(self):
        super(MainWindowController, self).__init__()
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_update.triggered.connect(self.open_updater_dialog)

        model = QStandardItemModel()

        liste = ["lol", "lol2"]

        # model.setColumnCount(2)
        model.setHorizontalHeaderLabels(liste)

        categories = Category.select()

        for category in categories:
            item_root = QStandardItem(category.category_name)
            item_root.setEditable(False)
            model.appendRow(item_root)

            products = Food.select(Food.food_name, Food.id_food).join(CategoryFood).join(Category).where(Category.id_category == category.id_category)

            for product in products:
                brands = Brand.select(Brand.brand_name).join(BrandFood).join(Food).where(BrandFood.id_food == product.id_food).limit(1)

                print(brands)

                items_list = []

                item = QStandardItem(product.food_name)
                item.setEditable(False)
                items_list.append(item)

                item_brand = QStandardItem(brands[0].brand_name)
                item_brand.setEditable(False)
                items_list.append(item_brand)

                item_root.appendRow(items_list)

        self.ui.tree_products.setModel(model)
        self.ui.tree_products.resizeColumnToContents(0)

    def open_updater_dialog(self):
        dialog = UpdaterDialogController(self)
        dialog.exec_()
