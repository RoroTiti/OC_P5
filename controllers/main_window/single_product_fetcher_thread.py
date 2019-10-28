from PySide2.QtCore import QThread, Signal

from models.database.models import Food, BrandFood, Brand, Store, StoreFood


class SingleProductFetcherThread(QThread):
    result = Signal(dict)

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

        stores = []
        brands = []

        for item in food:
            if not any(store["id_store"] == item["id_store"] for store in stores):
                stores.append({"id_store": item["id_store"], "store_name": item["store_name"]})
            if not any(brand["id_brand"] == item["id_brand"] for brand in brands):
                brands.append({"id_brand": item["id_brand"], "brand_name": item["brand_name"]})

        product = food[0]

        product.pop("id_store")
        product.pop("store_name")
        product.pop("id_brand")
        product.pop("brand_name")

        product["stores"] = stores
        product["brands"] = brands

        self.result.emit(product)
