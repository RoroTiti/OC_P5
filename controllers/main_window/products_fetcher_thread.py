from PySide2.QtCore import QThread, Signal

from models.database.models import Food, CategoryFood


class ProductsFetcherThread(QThread):
    result = Signal(list)

    def __init__(self):
        super().__init__()
        self.category = None

    def run(self):
        query = Food.select().join(CategoryFood).where(CategoryFood.id_category == self.category.id_category)
        products = list(query)
        products.sort(key=lambda x: x.food_name)
        self.result.emit(products)
