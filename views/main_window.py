# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui',
# licensing of 'main_window.ui' applies.
#
# Created: Tue Oct  8 13:31:49 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.tab)
        self.listWidget.setObjectName("listWidget")
        QtWidgets.QListWidgetItem(self.listWidget)
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar()
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuOutils = QtWidgets.QMenu(self.menuBar)
        self.menuOutils.setObjectName("menuOutils")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action_update = QtWidgets.QAction(MainWindow)
        self.action_update.setObjectName("action_update")
        self.action_preview = QtWidgets.QAction(MainWindow)
        self.action_preview.setObjectName("action_preview")
        self.menuOutils.addAction(self.action_update)
        self.menuOutils.addAction(self.action_preview)
        self.menuBar.addAction(self.menuOutils.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "NutriChecker by @RoroTiti", None, -1))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        self.listWidget.item(0).setText(QtWidgets.QApplication.translate("MainWindow", "lol", None, -1))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "Nouvelle recherche", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("MainWindow", "Mon historique de recherche", None, -1))
        self.menuOutils.setTitle(QtWidgets.QApplication.translate("MainWindow", "Outils", None, -1))
        self.action_update.setText(QtWidgets.QApplication.translate("MainWindow", "Mise à jour des données...", None, -1))
        self.action_preview.setText(QtWidgets.QApplication.translate("MainWindow", "Aperçu des données...", None, -1))

