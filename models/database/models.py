from peewee import *

database = MySQLDatabase('pur_beurre', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '192.168.1.230', 'user': 'root', 'password': 'Phe8AguW!a'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Brand(BaseModel):
    brand_name = TextField(null=True)
    id_brand = AutoField()

    class Meta:
        table_name = 'brand'

class Food(BaseModel):
    allergens = TextField(null=True)
    carbohydrates_100g = FloatField(null=True)
    energy_100g = FloatField(null=True)
    energy_unit = TextField(null=True)
    fat_100g = FloatField(null=True)
    fiber_100g = FloatField(null=True)
    food_code = TextField(null=True)
    food_name = TextField(null=True)
    id_food = AutoField()
    ingredients = TextField(null=True)
    ingredients_from_palm_oil_n = IntegerField(null=True)
    nutriscore = IntegerField(null=True)
    nutrition_grade = CharField(null=True)
    proteins_100g = FloatField(null=True)
    salt_100g = FloatField(null=True)
    saturated_fat_100g = FloatField(null=True)
    sodium_100g = FloatField(null=True)
    sugars_100g = FloatField(null=True)

    class Meta:
        table_name = 'food'

class BrandFood(BaseModel):
    id_brand = ForeignKeyField(column_name='id_brand', field='id_brand', model=Brand)
    id_food = ForeignKeyField(column_name='id_food', field='id_food', model=Food)

    class Meta:
        table_name = 'brand_food'
        indexes = (
            (('id_brand', 'id_food'), True),
        )
        primary_key = CompositeKey('id_brand', 'id_food')

class Category(BaseModel):
    category_name = TextField(null=True)
    id_category = AutoField()

    class Meta:
        table_name = 'category'

class CategoryFood(BaseModel):
    id_category = ForeignKeyField(column_name='id_category', field='id_category', model=Category)
    id_food = ForeignKeyField(column_name='id_food', field='id_food', model=Food)

    class Meta:
        table_name = 'category_food'
        indexes = (
            (('id_category', 'id_food'), True),
        )
        primary_key = CompositeKey('id_category', 'id_food')

class Store(BaseModel):
    id_store = AutoField()
    store_name = TextField(null=True)

    class Meta:
        table_name = 'store'

class StoreFood(BaseModel):
    id_food = ForeignKeyField(column_name='id_food', field='id_food', model=Food)
    id_store = ForeignKeyField(column_name='id_store', field='id_store', model=Store)

    class Meta:
        table_name = 'store_food'
        indexes = (
            (('id_food', 'id_store'), True),
        )
        primary_key = CompositeKey('id_food', 'id_store')

