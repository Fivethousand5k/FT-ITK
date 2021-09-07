#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    @Author Fivethousand
    @Date 2021/4/30 13:53
    @Describe 
    @Version 1.0
"""
import time

from Display_widget import Display_widget
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPalette, QFont, QCursor
from PyQt5.QtWidgets import QMainWindow, QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget, QFileDialog, QWidget, \
    QProgressBar,QRadioButton
from PyQt5 import QtCore
import sys
from Slices_Viewer_Widget import Slice_Viewer_Widget
from Signal_Central_Process_Unit import SCPU
from VTK_Viewer_widget import VTK_Viewer_widget
from Drop_Tree_Widget import Drop_Tree_Widget
import numpy as np
from Switch_Button import SwitchBtn
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.init_widgets()
        self.init_UI()
        self.init_connection()
    def init_widgets(self):
        self.Display_Widget=Display_widget()

    def init_UI(self):
        self.setWindowIcon(QIcon("GUI-resourses/FT-icon.png"))
        self.setWindowTitle("FT-ITK  简易三维医学数据可视化平台")
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        #self.main_widget.setObjectName('main_widget')
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.main_widget.setLayout(self.main_layout)
        #self.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.left_widget= QtWidgets.QWidget()  # 创建窗口左部件
        self.left_layout=QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)
        self.main_layout.addWidget(self.left_widget, 0, 0)
        self.main_layout.addWidget(self.Display_Widget,0,1)

        self.left_treewidget=Drop_Tree_Widget(self.left_widget)
        self.left_layout.addWidget(self.left_treewidget,0,0,20,10)

        self.left_pbar_container_widget=QtWidgets.QWidget(self.left_widget)
        self.pbar = QProgressBar(self.left_widget)
        self.model_btn=QRadioButton(self.left_widget)
        self.model_btn.setText("Seg")
        self.left_layout.addWidget(self.pbar,21,1,1,9)
        self.left_layout.addWidget(self.model_btn,21,0,1,1)
        self.left_layout.setSpacing(20)
        # self.left_layout.addWidget(self.left_pbar_container_widget)
        # self.left_treewidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.model_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #self.left_pbar_container_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.left_pbar_container_layout= QtWidgets.QHBoxLayout()
        # self.left_pbar_container_widget.setLayout(self.left_pbar_container_layout)
        # self.left_pbar_container_layout.addWidget(self.pbar)


       # self.model_btn=SwitchBtn(self.left_pbar_container_widget)
#        self.left_pbar_container_layout.addWidget(self.model_btn)
        #self.pbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_connection(self):
        self.left_treewidget.file_text_signal.connect(self.handle_drop_file)
        self.model_btn.toggled.connect(self.handle_model_btn_clicked)
        self.Display_Widget.pbar_signal.connect(self.progress_bar_effect)



    def handle_drop_file(self,file_path:str):
        """
        activated when a file is dropped into treewidget
        :param file_path: the path of the dropped file
        :return:
        """
        self.Display_Widget.load_data(file_path=file_path)
        if self.model_btn.isChecked() :   #do segmentation
            self.Display_Widget.load_label_data()
            self.Display_Widget.flash()
        else:
            pass


    def handle_model_btn_clicked(self):
        if self.model_btn.isChecked()==True:            #do segmentation
            self.Display_Widget.load_label_data()
            self.Display_Widget.flash()
        else:
            self.pbar.setValue(0)
            self.Display_Widget.clear_label()
            self.Display_Widget.flash()

    def FixSize(self):
        self.setFixedSize(self.width(),self.height())


    def progress_bar_effect(self):              # just for show
        for i in range(100):
            self.pbar.setValue(i+1)
            time.sleep(0.01)


if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        myWin = MainWindow()
        myWin.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        myWin.show()
        myWin.FixSize()
        sys.exit(app.exec_())