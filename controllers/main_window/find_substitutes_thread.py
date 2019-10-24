import jellyfish
from PySide2.QtCore import QThread, Signal

from models.database.models import Category, CategoryFood, Food, BrandFood, Brand


class FindSubstitutesThread(QThread):
    result = Signal(list)

    def __init__(self):
        super().__init__()
        self.product = None
        self.category = None

    def run(self):
        print(self.product["food_name"])

        products = Category.select(
            Food.id_food,
            Food.food_name,
            Food.nutriscore,
            Food.ingredients_from_palm_oil_n,
            Brand.brand_name
        ) \
            .join(CategoryFood) \
            .join(Food) \
            .join(BrandFood) \
            .join(Brand) \
            .switch(Food) \
            .where(Category.id_category == self.category["id_category"]) \
            .group_by(Food.id_food) \
            .dicts()

        distances = []

        for product in products:
            distances.append(
                {
                    "id_food": product["id_food"],
                    "food_name": product["food_name"],
                    "nutriscore": product["nutriscore"],
                    "ingredients_from_palm_oil_n": product["ingredients_from_palm_oil_n"],
                    "brand_name": product["brand_name"],
                    "similarity": self.round_by_hundred(jellyfish.jaro_distance(self.product["food_name"], product["food_name"]) * 1000)
                }
            )

        distances = filter(lambda x: x["id_food"] != self.product["id_food"], distances)

        distances = filter(lambda x: x["similarity"] >= 700, distances)

        distances = sorted(distances, key=lambda x: (x["nutriscore"], -x["similarity"]))

        print(distances)

        self.result.emit(distances)

    @staticmethod
    def round_by_hundred(n):
        return int(round(n / 100)) * 100
