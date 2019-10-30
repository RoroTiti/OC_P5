# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/about_data_dialog.ui',
# licensing of 'views/about_data_dialog.ui' applies.
#
# Created: Wed Oct 30 08:14:40 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table_informations = QtWidgets.QTableView(self.groupBox)
        self.table_informations.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_informations.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_informations.setObjectName("table_informations")
        self.table_informations.horizontalHeader().setVisible(False)
        self.table_informations.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.table_informations, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "Informations sur les données", None, -1))

