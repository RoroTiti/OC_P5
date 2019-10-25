from PySide2.QtCore import QThread, Signal

from models.database.models import Substitute


class SaveSubstituteThread(QThread):
    already_saved = Signal()

    def __init__(self):
        super().__init__()
        self.id_food = None
        self.id_food_substitute = None

    def run(self):
        substitute, created = Substitute.get_or_create(id_food=self.id_food, id_food_substitute=self.id_food_substitute)

        if not created:
            self.already_saved.emit()
