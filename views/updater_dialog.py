# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'updater_dialog.ui',
# licensing of 'updater_dialog.ui' applies.
#
# Created: Tue Oct  8 13:31:54 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.list_categories = QtWidgets.QListWidget(self.groupBox)
        self.list_categories.setObjectName("list_categories")
        self.gridLayout_2.addWidget(self.list_categories, 0, 0, 1, 2)
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_2.addWidget(self.listWidget, 3, 0, 1, 2)
        self.btn_load_list = QtWidgets.QPushButton(self.groupBox)
        self.btn_load_list.setAutoDefault(False)
        self.btn_load_list.setObjectName("btn_load_list")
        self.gridLayout_2.addWidget(self.btn_load_list, 1, 0, 1, 1)
        self.btn_add_category = QtWidgets.QPushButton(self.groupBox)
        self.btn_add_category.setAutoDefault(False)
        self.btn_add_category.setObjectName("btn_add_category")
        self.gridLayout_2.addWidget(self.btn_add_category, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Mise à jour des données", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Dialog", "Télécharger les produits", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "Catégories", None, -1))
        self.btn_load_list.setText(QtWidgets.QApplication.translate("Dialog", "Charger la liste", None, -1))
        self.btn_add_category.setText(QtWidgets.QApplication.translate("Dialog", "Ajouter", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "Catégories sélectionnées", None, -1))

