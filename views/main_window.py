# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'views/main_window.ui',
# licensing of 'views/main_window.ui' applies.
#
# Created: Thu Oct 31 12:01:09 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 850)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.table_substitutes = QtWidgets.QTableView(self.tab)
        self.table_substitutes.setObjectName("table_substitutes")
        self.table_substitutes.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.table_substitutes, 5, 0, 1, 1)
        self.table_products = QtWidgets.QTableView(self.tab)
        self.table_products.setObjectName("table_products")
        self.gridLayout.addWidget(self.table_products, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.btn_reload_data = QtWidgets.QPushButton(self.tab)
        self.btn_reload_data.setObjectName("btn_reload_data")
        self.gridLayout.addWidget(self.btn_reload_data, 0, 0, 1, 1)
        self.cmb_categories = QtWidgets.QComboBox(self.tab)
        self.cmb_categories.setObjectName("cmb_categories")
        self.gridLayout.addWidget(self.cmb_categories, 1, 0, 1, 1)
        self.btn_save_substitute = QtWidgets.QPushButton(self.tab)
        self.btn_save_substitute.setObjectName("btn_save_substitute")
        self.gridLayout.addWidget(self.btn_save_substitute, 6, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.table_saved_substitutes = QtWidgets.QTableView(self.tab_2)
        self.table_saved_substitutes.setWordWrap(True)
        self.table_saved_substitutes.setObjectName("table_saved_substitutes")
        self.table_saved_substitutes.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.table_saved_substitutes, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menuBar.setObjectName("menuBar")
        self.menuOutils = QtWidgets.QMenu(self.menuBar)
        self.menuOutils.setObjectName("menuOutils")
        MainWindow.setMenuBar(self.menuBar)
        self.action_update = QtWidgets.QAction(MainWindow)
        self.action_update.setObjectName("action_update")
        self.action_about_data = QtWidgets.QAction(MainWindow)
        self.action_about_data.setObjectName("action_about_data")
        self.menuOutils.addAction(self.action_update)
        self.menuOutils.addAction(self.action_about_data)
        self.menuBar.addAction(self.menuOutils.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "NutriChecker by @RoroTiti", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Produits", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "Substituts", None, -1))
        self.btn_reload_data.setText(QtWidgets.QApplication.translate("MainWindow", "Recharger les données", None, -1))
        self.btn_save_substitute.setText(QtWidgets.QApplication.translate("MainWindow", "Enregistrer le substitut", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "Nouvelle recherche", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("MainWindow", "Mes substituts enregistrés", None, -1))
        self.menuOutils.setTitle(QtWidgets.QApplication.translate("MainWindow", "Outils", None, -1))
        self.action_update.setText(QtWidgets.QApplication.translate("MainWindow", "Mise à jour des données...", None, -1))
        self.action_about_data.setText(QtWidgets.QApplication.translate("MainWindow", "À propos de la base de données...", None, -1))

