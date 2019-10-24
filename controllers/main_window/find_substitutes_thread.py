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
            Food.food_name,
            Food.nutriscore
        ) \
            .join(CategoryFood) \
            .join(Food) \
            .where(Category.id_category == self.category["id_category"]) \
            .dicts()

        distances = []

        for product in products:
            distances.append(
                {
                    "id_food": product["id_food"],
                    "food_name": product["food_name"],
                    "nutriscore": product["nutriscore"],
                    "similarity": self.round_by_hundred(jellyfish.jaro_distance(self.product["food_name"], product["food_name"]) * 1000)
                }
            )

        distances = filter(lambda x: x["id_food"] != self.product["id_food"], distances)

        distances = filter(lambda x: x["similarity"] > 700, distances)

        distances = sorted(distances, key=lambda x: (x["nutriscore"], -x["similarity"]))

        print(distances)

    @staticmethod
    def round_by_hundred(n):
        return int(round(n / 100)) * 100
