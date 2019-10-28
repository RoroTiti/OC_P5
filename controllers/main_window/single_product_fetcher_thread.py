from PySide2.QtCore import QThread, Signal

from models.database.models import Food, BrandFood, Brand, Store, StoreFood


class SingleProductFetcherThread(QThread):
    result = Signal(object)

    def __init__(self):
        super().__init__()
        self.food_id = None

    def run(self):
        food = Food.select(
            Food, Store, Brand
        ) \
            .join(StoreFood) \
            .join(Store) \
            .switch(Food) \
            .join(BrandFood) \
            .join(Brand) \
            .where(Food.id_food == self.food_id) \
            .group_by(Store.id_store, Brand.id_brand) \
            .dicts() \
            .execute()

        stores = set()
        brands = set()

        for item in food:
            stores.add(item["brand_name"])
            brands.add(item["store_name"])

        food[0].pop("brand_name")
        food[0].pop("store_name")

        print(food[0])
        print(stores)
        print(brands)
