import jellyfish
from PySide2.QtCore import QThread, Signal

from models.database import Category, CategoryFood, Food, BrandFood, Brand


class FindSubstitutesThread(QThread):
    """
    Thread to fetch the substitutes from the database and compute the results to find relevant results
    """
    result = Signal(list)

    def __init__(self):
        """
        Initializes a FindSubstitutesThread object
        """
        super().__init__()
        self.product = None
        self.category = None

    def run(self) -> None:
        """
        Fetch the data information from the database and compute results
        """
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

        # Adding the similarity property to the product object
        for product in products:
            product["similarity"] = self.round_by_hundred(jellyfish.jaro_distance(self.product["food_name"], product["food_name"]) * 1000)

        # Removing the product we are searching a substitute for from the list
        products = list(filter(lambda x: x["id_food"] != self.product["id_food"], products))

        # Finding the best similarity level to obtain at least 1 good substitute
        current_similarity_threshold = 1000
        good_substitutes = []

        while True:
            if current_similarity_threshold == 0:
                break

            possible_substitutes = list(filter(lambda x: x["similarity"] >= current_similarity_threshold, products))

            good_substitutes = list(
                filter(lambda x:
                       x["nutriscore"] < self.product["nutriscore"] and
                       x["ingredients_from_palm_oil_n"] <= self.product["ingredients_from_palm_oil_n"],
                       possible_substitutes)
            )

            if len(good_substitutes) > 0:
                good_substitutes = sorted(good_substitutes, key=lambda x: (x["nutriscore"], -x["similarity"], x["ingredients_from_palm_oil_n"]))
                break
            else:
                current_similarity_threshold -= 100

        self.result.emit(good_substitutes)

    @staticmethod
    def round_by_hundred(n: float) -> int:
        """
        Round a number by 100

        :param n: The number to be rounded
        :return: The rounded value
        """
        return int(round(n / 100)) * 100
