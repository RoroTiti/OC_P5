create table brand
(
    id_brand   int auto_increment,
    brand_name longtext null,
    constraint company_id_company_uindex
        unique (id_brand)
)
    charset = utf8mb4;

alter table brand
    add primary key (id_brand);

create table category
(
    id_category   int auto_increment,
    category_name longtext null,
    constraint category_id_category_uindex
        unique (id_category)
)
    charset = utf8mb4;

alter table category
    add primary key (id_category);

create table food
(
    id_food                     int auto_increment,
    food_code                   longtext null,
    food_name                   text     null,
    ingredients                 longtext null,
    ingredients_from_palm_oil_n int      null,
    allergens                   longtext null,
    nutriscore                  int      null,
    nutrition_grade             char     null,
    energy_100g                 double   null,
    energy_unit                 tinytext null,
    carbohydrates_100g          double   null,
    sugars_100g                 double   null,
    fat_100g                    double   null,
    saturated_fat_100g          double   null,
    salt_100g                   double   null,
    sodium_100g                 double   null,
    fiber_100g                  double   null,
    proteins_100g               double   null,
    constraint food_id_food_uindex
        unique (id_food)
)
    charset = utf8mb4;

alter table food
    add primary key (id_food);

create table brand_food
(
    id_brand int not null,
    id_food  int not null,
    primary key (id_brand, id_food),
    constraint brand_food_brand_id_brand_fk
        foreign key (id_brand) references brand (id_brand),
    constraint brand_food_food_id_food_fk
        foreign key (id_food) references food (id_food)
)
    charset = utf8mb4;

create table category_food
(
    id_category int not null,
    id_food     int not null,
    primary key (id_category, id_food),
    constraint category_food_category_id_category_fk
        foreign key (id_category) references category (id_category),
    constraint category_food_food_id_food_fk
        foreign key (id_food) references food (id_food)
)
    charset = utf8mb4;

create table store
(
    id_store   int auto_increment,
    store_name longtext null,
    constraint store_id_store_uindex
        unique (id_store)
)
    charset = utf8mb4;

alter table store
    add primary key (id_store);

create table store_food
(
    id_store int not null,
    id_food  int not null,
    primary key (id_food, id_store),
    constraint sell_food_id_food_fk
        foreign key (id_food) references food (id_food),
    constraint sell_store_id_store_fk
        foreign key (id_store) references store (id_store)
)
    charset = utf8mb4;

create table substitute
(
    id_food            int not null,
    id_food_substitute int not null,
    primary key (id_food, id_food_substitute),
    constraint substitutes_food_id_food_fk
        foreign key (id_food) references food (id_food),
    constraint substitutes_food_id_food_fk_2
        foreign key (id_food_substitute) references food (id_food)
)
    charset = utf8mb4;


