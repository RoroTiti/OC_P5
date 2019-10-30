from PySide2.QtCore import QThread, Signal

from models.database import Substitute


class SaveSubstituteThread(QThread):
    """
    Thread to save a product and one of its corresponding substitutes into the database
    """
    already_saved = Signal()

    def __init__(self):
        """
        Initialize a SaveSubstituteThread object
        """
        super().__init__()
        self.id_food = None
        self.id_food_substitute = None

    def run(self) -> None:
        """
        Save a product and the chosen substitute into the database
        """
        substitute, created = Substitute.get_or_create(id_food=self.id_food, id_food_substitute=self.id_food_substitute)

        if not created:
            self.already_saved.emit()
