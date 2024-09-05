# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appZtPPzu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(821, 494)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rec_button = QPushButton(self.centralwidget)
        self.rec_button.setObjectName(u"rec_button")
        self.rec_button.setGeometry(QRect(20, 40, 181, 51))
        self.run_button = QPushButton(self.centralwidget)
        self.run_button.setObjectName(u"run_button")
        self.run_button.setGeometry(QRect(20, 110, 181, 61))
        self.org_button = QPushButton(self.centralwidget)
        self.org_button.setObjectName(u"org_button")
        self.org_button.setGeometry(QRect(20, 190, 181, 61))
        self.quit_button = QPushButton(self.centralwidget)
        self.quit_button.setObjectName(u"quit_button")
        self.quit_button.setGeometry(QRect(20, 270, 181, 61))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 821, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.rec_button.setText(QCoreApplication.translate("MainWindow", u"Test Recorder", None))
        self.run_button.setText(QCoreApplication.translate("MainWindow", u"Test Runner", None))
        self.org_button.setText(QCoreApplication.translate("MainWindow", u"Test Organizer", None))
        self.quit_button.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
    # retranslateUi

