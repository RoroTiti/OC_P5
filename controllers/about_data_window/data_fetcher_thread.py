from PySide2.QtCore import QThread, Signal

from models.database import Category, Food, Store, Brand


class DataFetcherThread(QThread):
    result = Signal(list)

    def run(self):
        categories_count = Category.select().count()
        products_count = Food.select().count()
        stores_count = Store.select().count()
        brands_count = Brand.select().count()

        self.result.emit([
            ["Nombre de catégories", categories_count],
            ["Nombre de produits", products_count],
            ["Nombre de magasins", stores_count],
            ["Nombre de marques", brands_count]
        ])
