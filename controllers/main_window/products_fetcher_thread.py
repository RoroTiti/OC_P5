from PySide2.QtCore import QThread, Signal

from models.database.models import Food, CategoryFood, BrandFood, Brand


class ProductsFetcherThread(QThread):
    result = Signal(list)

    def __init__(self):
        super().__init__()
        self.category = None

    def run(self):
        try:
            query = BrandFood.select(
                Food.food_name,
                Brand.brand_name,
                Food.ingredients,
                Food.allergens,
                Food.nutriscore,
                Food.energy_100g,
                Food.carbohydrates_100g,
                Food.sugars_100g,
                Food.fat_100g,
                Food.saturated_fat_100g,
                Food.salt_100g,
                Food.sodium_100g,
                Food.fiber_100g,
                Food.proteins_100g
            ) \
                .join(Food) \
                .switch(BrandFood) \
                .join(Brand) \
                .switch(Food) \
                .join(CategoryFood) \
                .where(CategoryFood.id_category == self.category.id_category) \
                .group_by(Food.id_food) \
                .dicts()

            products = list(query)
            products.sort(key=lambda x: x["food_name"])

            self.result.emit(products)

        except Exception as e:
            print(e)
