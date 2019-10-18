class Product:
    def __init__(self, name, ingredients, allergens, nutriscore, energy_100g, carbohydrates_100g, sugars_100g, fat_100g, saturated_fat_100g,
                 sodium_100g, salt_100g, fiber_100g, proteins_100g):
        self.name: str = name
        self.ingredients: str = ingredients
        self.allergens: str = allergens
        self.nutriscore: int = nutriscore
        self.energy_100g: float = energy_100g
        self.carbohydrates_100g: float = carbohydrates_100g
        self.sugars_100g: float = sugars_100g
        self.fat_100g: float = fat_100g
        self.saturated_fat_100g: float = saturated_fat_100g
        self.sodium_100g: float = sodium_100g
        self.salt_100g: float = salt_100g
        self.fiber_100g: float = fiber_100g
        self.proteins_100g: float = proteins_100g
