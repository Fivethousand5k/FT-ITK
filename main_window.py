# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.openGLWidget_4 = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget_4.setGeometry(QtCore.QRect(430, 300, 351, 271))
        self.openGLWidget_4.setObjectName("openGLWidget_4")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 290, 801, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(390, 0, 20, 561))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.openGLWidget_1 = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget_1.setGeometry(QtCore.QRect(30, 10, 351, 271))
        self.openGLWidget_1.setObjectName("openGLWidget_1")
        self.openGLWidget_2 = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget_2.setGeometry(QtCore.QRect(420, 10, 351, 271))
        self.openGLWidget_2.setObjectName("openGLWidget_2")
        self.openGLWidget_3 = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget_3.setGeometry(QtCore.QRect(30, 300, 351, 271))
        self.openGLWidget_3.setObjectName("openGLWidget_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
