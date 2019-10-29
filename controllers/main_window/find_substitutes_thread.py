import jellyfish
from PySide2.QtCore import QThread, Signal

from models.database import Category, CategoryFood, Food, BrandFood, Brand


class FindSubstitutesThread(QThread):
    result = Signal(list)

    def __init__(self):
        super().__init__()
        self.product = None
        self.category = None

    def run(self):
        products = Category.select(
            Food.id_food,
            Food.food_name,
            Brand.brand_name,
            Food.ingredients,
            Food.ingredients_from_palm_oil_n,
            Food.allergens,
            Food.nutriscore,
            Food.nutrition_grade,
            Food.energy_100g,
            Food.energy_unit,
            Food.carbohydrates_100g,
            Food.sugars_100g,
            Food.fat_100g,
            Food.saturated_fat_100g,
            Food.salt_100g,
            Food.sodium_100g,
            Food.fiber_100g,
            Food.proteins_100g
        ) \
            .join(CategoryFood) \
            .join(Food) \
            .join(BrandFood) \
            .join(Brand) \
            .switch(Food) \
            .where(Category.id_category == self.category["id_category"]) \
            .group_by(Food.id_food) \
            .dicts() \
            .execute()

        for product in products:
            product["similarity"] = self.round_by_hundred(jellyfish.jaro_distance(self.product["food_name"], product["food_name"]) * 1000)

        products = filter(lambda x: x["id_food"] != self.product["id_food"], products)
        products = filter(lambda x: x["similarity"] >= 700, products)
        products = sorted(products, key=lambda x: (x["nutriscore"], -x["similarity"], x["ingredients_from_palm_oil_n"]))

        self.result.emit(products)

    @staticmethod
    def round_by_hundred(n):
        return int(round(n / 100)) * 100
