from itertools import zip_longest

import requests
from PySide2.QtCore import QThread, Signal

from models.database.models import CategoryFood, BrandFood, StoreFood, Brand, Store, Food, Category


class ProductsDownloaderThread(QThread):
    progress = Signal(int)

    def __init__(self, selected_categories):
        super().__init__()
        self.selected_categories = selected_categories
        self.max_progress = len(selected_categories) * 50
        self.current_progress = 0

    def run(self):
        CategoryFood.delete().execute()
        BrandFood.delete().execute()
        StoreFood.delete().execute()

        Category.delete().execute()
        Brand.delete().execute()
        Store.delete().execute()

        Food.delete().execute()

        print(self.selected_categories)

        for category in self.selected_categories:
            db_category = Category(category_name=category.name)
            db_category.save()

            url = ("https://fr.openfoodfacts.org/cgi/search.pl?"
                   "action=process&"
                   "tagtype_0=categories&"
                   "tag_contains_0=contains&"
                   f"tag_0={category.id}&"
                   "sort_by=unique_scans_n&"
                   "page_size=50&"
                   "json=1")

            request = requests.get(url)

            expected_product_keys = [
                "product_name",
                "code",
                "ingredients_text_fr",
                "allergens_from_ingredients",
                "nutriments",
                "brands_tags",
                "brands",
                "stores_tags",
                "stores"
            ]

            expected_nutriments_keys = [
                "nutrition-score-fr",
                "energy_100g",
                "carbohydrates_100g",
                "sugars_100g",
                "saturated-fat_100g",
                "sodium_100g",
                "salt_100g",
                "fiber_100g",
                "proteins_100g"
            ]

            for product in request.json()["products"]:
                if all(key in product for key in expected_product_keys):
                    nutriments = product["nutriments"]
                    if all(key in nutriments for key in expected_nutriments_keys):
                        if len(product["brands_tags"]) > 0 and len(product["stores_tags"]) > 0 and bool(product["ingredients_text_fr"].strip()):
                            # The product has all required characteristics to be integrated into the database
                            print("OK")

                            # Inserting the food product into the database
                            food = Food(
                                allergens=product["allergens_from_ingredients"],
                                carbohydrates_100g=nutriments["carbohydrates_100g"],
                                energy_100g=nutriments["energy_100g"],
                                fat_100g=nutriments["fat_100g"],
                                fiber_100g=nutriments["fiber_100g"],
                                food_code=product["code"],
                                food_name=product["product_name"],
                                ingredients=product["ingredients_text_fr"],
                                nutriscore=nutriments["nutrition-score-fr"],
                                proteins_100g=nutriments["proteins_100g"],
                                salt_100g=nutriments["salt_100g"],
                                saturated_fat_100g=nutriments["saturated-fat_100g"],
                                sodium_100g=nutriments["sodium_100g"],
                                sugars_100g=nutriments["sugars_100g"]
                            )

                            food.save()

                            CategoryFood.create(id_category=db_category.id_category, id_food=food.id_food)

                            # Getting the individual brands
                            brands: str = product["brands"]
                            brands_list = brands.split(",")

                            # Getting the individual stores
                            stores: str = product["stores"]
                            stores_list = stores.split(",")

                            for index, (brand_name, store_name) in enumerate(zip_longest(brands_list, stores_list)):
                                if brand_name is not None:
                                    brand_name = brand_name.upper().lstrip().rstrip()
                                    brand, created = Brand.get_or_create(brand_name=brand_name)
                                    BrandFood.create(id_brand=brand.id_brand, id_food=food.id_food)

                                if store_name is not None:
                                    store_name = store_name.upper().lstrip().rstrip()
                                    store, created = Store.get_or_create(store_name=store_name)
                                    StoreFood.create(id_store=store.id_store, id_food=food.id_food)

                        else:
                            print("not ok brands or stores")

                    else:
                        print("not ok nutriments")
                else:
                    print("not ok product")

                if self.isInterruptionRequested():
                    return
                else:
                    self.current_progress += 1
                    self.progress.emit(self.current_progress)
