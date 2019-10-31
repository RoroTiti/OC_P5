# NutriChecker by @RoroTiti

![Screenshots](https://i.imgur.com/jU9H4kz.png)

## User manual

### Getting started

To run the application, it's recommended to setup a virtual environment. We will use virtualenv.

- Move to the source code root directory
```
cd "/the/app/directory"
```

- Initialize a virtualenv
```
pip install virtualenv # install virtualenv if not already installed
virtualenv venv
```

- Enable the virtual environment (Windows)
```
.\venv\Scripts\activate
```

- Enable the virtual environment (macOS)
```
source venv/bin/
```

- Install the app dependencies
```
pip install -r requirements.txt
```

### Database setup

The app requires a MySQL database in order to save its data. 
Follow the steps in order to obtain a working database setup. 

- Execute the ``create_tables.sql`` file on the MySQL database where you want to host the data of the application.

To communicate with the database, the app uses the Peewee ORM.
You have 2 possibilities to configure the app connection to the database.

**Option 1 : regenerate the Peewee model file (recommended and reliable)** 

- From the source root directory, run :
````
python -m pwiz -e mysql -H {database host} -p {database port} -u {database user} -P {database name} > models/database.py
````

**Option 2 : update the model template credentials (may be unreliable according to your database setup)** 

- Modify ``models/database.py`` and update the database connection credentials :
  - ``host`` : the database IP address
  - ``port`` : the database IP address
  - ``user`` : the user who has access to the database created previously
  - ``password`` the password of the user

### Run the app and populate the database

- You can now start the app with the following command
```
python .\main.py
```

In order to populate the data from the OpenFoodFacts API, the app contains an user friendly assistant helping you to download the data.
To access it, go to ``Outils``, ``Mise à jour des données...``

- On the window which will open, click on ``Charger la liste``. It will fetch relevant categories from the OpenFoodFacts API.
- Once the list is fetched, select the categories you want to download and click on ``Ajouter``. The items will be added to the selected categories list.
If you want to remove an item from the selected categories list, simply select it and click on ``Supprimer``.
- Once you are done, click on ``Télécharger les produits``. You can watch the progression and eventual issues on your Python console.
Since the tool only download the products with complete details, if a product is not downloaded, the reason will be displayed on the Python console.

The app is now ready, you can start exploring the data on the application window !

## Working environment
- Windows 10 or macOS Mojave and upper
- Python 3.7.4