# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/updater_dialog.ui',
# licensing of 'views/updater_dialog.ui' applies.
#
# Created: Mon Oct 14 18:03:43 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_download = QtWidgets.QPushButton(Dialog)
        self.btn_download.setObjectName("btn_download")
        self.gridLayout.addWidget(self.btn_download, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_load_list = QtWidgets.QPushButton(self.groupBox)
        self.btn_load_list.setAutoDefault(False)
        self.btn_load_list.setObjectName("btn_load_list")
        self.gridLayout_2.addWidget(self.btn_load_list, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 4, 0, 1, 2)
        self.table_selected_categories = QtWidgets.QTableView(self.groupBox)
        self.table_selected_categories.setObjectName("table_selected_categories")
        self.gridLayout_2.addWidget(self.table_selected_categories, 5, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 2)
        self.table_all_categories = QtWidgets.QTableView(self.groupBox)
        self.table_all_categories.setObjectName("table_all_categories")
        self.gridLayout_2.addWidget(self.table_all_categories, 2, 0, 1, 2)
        self.btn_add_category = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_category.setAutoDefault(False)
        self.btn_add_category.setObjectName("btn_add_category")
        self.gridLayout_2.addWidget(self.btn_add_category, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 2)
        self.btn_delete_category = QtWidgets.QPushButton(self.groupBox)
        self.btn_delete_category.setAutoDefault(False)
        self.btn_delete_category.setObjectName("btn_delete_category")
        self.gridLayout_2.addWidget(self.btn_delete_category, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Mise à jour des données", None, -1))
        self.btn_download.setText(QtWidgets.QApplication.translate("Dialog", "Télécharger les produits", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "Catégories", None, -1))
        self.btn_load_list.setText(QtWidgets.QApplication.translate("Dialog", "Charger la liste", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Catégories sélectionnées", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Dialog", "Lors du téléchargement des données, seuls les 50 produits les plus populaires de chaque catégorie seront récupérés.", None, -1))
        self.btn_add_category.setText(QtWidgets.QApplication.translate("Dialog", "Ajouter", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", "Seules les catégories contenant plus de 5000 produits sont affichées.", None, -1))
        self.btn_delete_category.setText(QtWidgets.QApplication.translate("Dialog", "Supprimer", None, -1))

