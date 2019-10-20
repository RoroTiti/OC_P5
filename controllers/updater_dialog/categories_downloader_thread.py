import requests
from PySide2.QtCore import Signal, QThread

from models.api.category import Category


class CategoriesDownloaderThread(QThread):
    result = Signal(list)
    progress = Signal(int)

    def __init__(self):
        super().__init__()
        self.max_progress = 3

    def run(self):
        self.progress.emit(1)

        url = "https://fr.openfoodfacts.org/categories.json"
        request = requests.get(url)

        self.progress.emit(2)

        tags = request.json()["tags"]

        all_categories = []

        for tag in tags:
            if tag["products"] >= 5000:
                all_categories.append(Category(tag["name"], tag["products"], tag["id"]))

        self.progress.emit(3)
        self.result.emit(all_categories)
