import requests
from PySide2.QtCore import Signal, QThread


class CategoriesDownloaderThread(QThread):
    """
    Thread to download the categories available from the OpenFoodFacts API
    """
    result = Signal(list)
    progress = Signal(int)

    def __init__(self):
        """
        Initialize a CategoriesDownloaderThread object
        """
        super().__init__()
        self.max_progress = 3

    def run(self) -> None:
        """
        Download the categories available from the OpenFoodFacts API
        """
        if self.isInterruptionRequested():
            return
        else:
            self.progress.emit(1)

        url = "https://fr.openfoodfacts.org/categories.json"
        request = requests.get(url)

        if self.isInterruptionRequested():
            return
        else:
            self.progress.emit(2)

        tags = request.json()["tags"]

        all_categories = []

        for tag in tags:
            if tag["products"] >= 5000:
                all_categories.append({
                    "id": tag["id"],
                    "name": tag["name"],
                    "products": tag["products"]
                })

        if self.isInterruptionRequested():
            return
        else:
            self.progress.emit(3)
            self.result.emit(all_categories)
