import os

import markdown
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QDialog

from views import product_details_dialog


class ProductDetailsDialogController(QDialog):

    def __init__(self, parent, product_details):
        super(ProductDetailsDialogController, self).__init__(parent)
        self.product_details = product_details

        self.setWindowModality(Qt.NonModal)

        self.ui = product_details_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        food = self.product_details

        self.ui.lbl_ingredients.setText(markdown.markdown(food["ingredients"]))

        palm_oil_presence = food["ingredients_from_palm_oil_n"] > 0

        self.ui.lbl_palm_oil.setStyleSheet(
            "* { background-color: red; color: white; padding: 3 px; }"
            if palm_oil_presence else
            "* { background-color: green; color: white; padding: 3 px; }"
        )

        self.ui.lbl_palm_oil.setText(
            "Contient de l'huile de palme"
            if palm_oil_presence else
            "Ne contient pas d'huile de palme"
        )

        self.ui.lbl_allergens.setText(markdown.markdown(food["allergens"]) if food["allergens"] else "<i>Aucun</i>")

        if food["energy_unit"] == "kcal":
            kj = round(food["energy_100g"] * 4.18, 1)
            energy_string = f"{food['energy_100g']} kcal ({kj} kj)"
        else:
            kcal = round(food["energy_100g"] / 4.18, 1)
            energy_string = f"{kcal} kcal ({food['energy_100g']} kj)"

        html_spaces = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"

        nutriments = [
            ["<b>Energie</b>", energy_string],
            ["<b>Glucides</b>", f"{food['carbohydrates_100g']} g"],
            [f"{html_spaces}Sucres", f"{food['sugars_100g']} g"],
            ["<b>Matières grasses</b>", f"{food['fat_100g']} g"],
            [f"{html_spaces}Acides gras saturés", f"{food['saturated_fat_100g']} g"],
            ["<b>Sel</b>", f"{food['salt_100g']} g"],
            [f"{html_spaces}Sodium", f"{food['sodium_100g']} g"],
            ["<b>Fibres</b>", f"{food['fiber_100g']} g"],
            ["<b>Protéines</b>", f"{food['proteins_100g']} g"]
        ]

        nutriments_table_content = "<style>td { padding: 3px; }</style>"

        nutriments_table_content += "<table width=100% border=1 cellspacing=0 cellpadding=0>"

        for nutriment in nutriments:
            nutriments_table_content += "<tr>"
            for column in nutriment:
                nutriments_table_content += "<td>"
                nutriments_table_content += str(column)
                nutriments_table_content += "</td>"
            nutriments_table_content += "</tr>"

        nutriments_table_content += "</table>"

        self.ui.lbl_nutriments.setText(nutriments_table_content)

        current_directory = os.path.dirname(__file__)
        filename = os.path.join(current_directory, "..", "..", "assets", f"nutriscore_{food['nutrition_grade']}.png")

        image = QImage(filename)
        pix_map = QPixmap()
        pix_map.convertFromImage(image.scaledToHeight(100, Qt.SmoothTransformation))

        self.ui.lbl_nutriscore.setPixmap(pix_map)
        self.ui.lbl_nutriscore_number.setText(f"<b>Indice NUTRI-SCORE:</b> {food['nutriscore']}")
