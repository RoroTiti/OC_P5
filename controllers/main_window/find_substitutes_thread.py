import operator

import jellyfish
from PySide2.QtCore import QThread, Signal

from models.database.models import Category, CategoryFood, Food


class FindSubstitutesThread(QThread):
    result = Signal()

    def __init__(self):
        super().__init__()
        self.product = None
        self.category = None

    def run(self):
        print(self.product["food_name"])

        products = Category.select(
            Food.id_food,
            Food.food_name
        ) \
            .join(CategoryFood) \
            .join(Food) \
            .where(Category.id_category == self.category["id_category"]) \
            .dicts()

        distances = []

        for product in products:
            distances.append([product["food_name"], jellyfish.jaro_distance(self.product["food_name"], product["food_name"])])

        distances = sorted(distances, key=operator.itemgetter(1), reverse=True)

        print(distances)
