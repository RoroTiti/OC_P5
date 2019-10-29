from PySide2.QtCore import QThread, Signal

from models.database import Food, CategoryFood, BrandFood, Brand


class ProductsFetcherThread(QThread):
    result = Signal(list)

    def __init__(self):
        super().__init__()
        self.category = None

    def run(self):
        try:
            query = BrandFood.select(
                Food.id_food,
                Food.food_name,
                Food.nutriscore,
                Food.ingredients_from_palm_oil_n,
                Brand.brand_name
            ) \
                .join(Food) \
                .switch(BrandFood) \
                .join(Brand) \
                .switch(Food) \
                .join(CategoryFood) \
                .where(CategoryFood.id_category == self.category["id_category"]) \
                .group_by(Food.id_food) \
                .dicts() \
                .execute()

            products = list(query)
            products.sort(key=lambda x: x["food_name"])

            self.result.emit(products)

        except Exception as e:
            print(e)
