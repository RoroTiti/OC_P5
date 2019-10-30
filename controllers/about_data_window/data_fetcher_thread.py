from PySide2.QtCore import QThread, Signal

from models.database import Category, Food, Store, Brand


class DataInformationFetcherThread(QThread):
    """
    Thread to fetch the data information from the database
    """
    result = Signal(list)

    def __init__(self):
        """
        Initializes a DataFetcherThread object
        """
        super().__init__()

    def run(self) -> None:
        """
        Fetch the data information from the database and compute results
        """
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
