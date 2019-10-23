from itertools import zip_longest

import requests
import unidecode
from PySide2.QtCore import QThread, Signal

from models.database.models import CategoryFood, BrandFood, StoreFood, Brand, Store, Food, Category


class ProductsDownloaderThread(QThread):
    progress = Signal(int)

    def __init__(self):
        super().__init__()
        self.current_progress = 0
        self.selected_categories = None

    def run(self):
        CategoryFood.delete().execute()
        BrandFood.delete().execute()
        StoreFood.delete().execute()

        Category.delete().execute()
        Brand.delete().execute()
        Store.delete().execute()

        Food.delete().execute()

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
                "nutrition_grade_fr",
                "brands_tags",
                "brands",
                "stores_tags",
                "stores"
            ]

            expected_nutriments_keys = [
                "nutrition-score-fr",
                "energy_value",
                "energy_unit",
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
                        if bool(product["ingredients_text_fr"].strip()):

                            # Getting the individual brands
                            brands: str = product["brands"]
                            brands_list = brands.split(",")

                            # Getting the individual stores
                            stores: str = product["stores"]
                            stores_list = stores.split(",")

                            # Performing a first clean in data, removing all the extra spaces, accents and case differences
                            for index, (brand_name, store_name) in enumerate(zip_longest(brands_list, stores_list)):
                                if brand_name is not None:
                                    brands_list[index] = unidecode.unidecode(brand_name.upper().lstrip().rstrip())
                                if store_name is not None:
                                    stores_list[index] = unidecode.unidecode(store_name.upper().lstrip().rstrip())

                            # Removing all empty elements from list
                            brands_list = [brand for brand in brands_list if brand]
                            stores_list = [store for store in stores_list if store]

                            # Finally, removing duplicates from list
                            brands_list = set(brands_list)
                            stores_list = set(stores_list)

                            # If nothing is remaining on the lists, skipping the current product
                            if len(brands_list) > 0 and len(stores_list) > 0:
                                # The product has all required characteristics to be integrated into the database
                                print("Product OK")

                                # Inserting the food product into the database
                                food, created = Food.get_or_create(
                                    allergens=product["allergens_from_ingredients"],
                                    carbohydrates_100g=nutriments["carbohydrates_100g"],
                                    energy_100g=nutriments["energy_value"],
                                    energy_unit=nutriments["energy_unit"],
                                    fat_100g=nutriments["fat_100g"],
                                    fiber_100g=nutriments["fiber_100g"],
                                    food_code=product["code"],
                                    food_name=product["product_name"],
                                    ingredients=product["ingredients_text_fr"],
                                    nutriscore=nutriments["nutrition-score-fr"],
                                    nutrition_grade=product["nutrition_grade_fr"],
                                    proteins_100g=nutriments["proteins_100g"],
                                    salt_100g=nutriments["salt_100g"],
                                    saturated_fat_100g=nutriments["saturated-fat_100g"],
                                    sodium_100g=nutriments["sodium_100g"],
                                    sugars_100g=nutriments["sugars_100g"]
                                )

                                force_insert = created

                                CategoryFood.create(id_category=db_category.id_category, id_food=food.id_food)

                                print(food.id_food)
                                print(brands_list)
                                print(stores_list)

                                if force_insert:
                                    for index, (brand_name, store_name) in enumerate(zip_longest(brands_list, stores_list)):
                                        if brand_name is not None:
                                            print("Brand OK")
                                            brand, created = Brand.get_or_create(brand_name=brand_name)
                                            BrandFood.create(id_brand=brand.id_brand, id_food=food.id_food)

                                        if store_name is not None:
                                            print("Store OK")
                                            store, created = Store.get_or_create(store_name=store_name)
                                            StoreFood.create(id_store=store.id_store, id_food=food.id_food)

                                print("Product saved successfully !")

                            else:
                                print("Not OK, brands or stores missing")
                        else:
                            print("Not OK, empty ingredients")
                    else:
                        print("Not OK, nutriments missing")
                else:
                    print("Not OK, product properties missing")

                if self.isInterruptionRequested():
                    return
                else:
                    self.current_progress += 1
                    self.progress.emit(self.current_progress)

    @property
    def max_progress(self):
        return len(self.selected_categories) * 50
