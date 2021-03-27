import cv2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QFont, QPixmap, QImage,QWheelEvent
from PyQt5.QtWidgets import QWidget, QSizePolicy

import threading
import  time
import sys
import numpy as np
from  tools import *
class Player(QWidget):
    def __init__(self,parent=None,):
        super(Player, self).__init__(parent)
        self.init_UI()
        self.data=np.load("medical_files/0001.npy")
        self.screen_width,self.screen_height,self.slices_num=self.data.shape
        print(self.data.shape)
        self.slice_index=self.slices_num//2
        init_cover=self.data[:,:,self.slice_index]
        showImage=process(init_cover,-255,255)
        self.label_screen.setPixmap(QPixmap(showImage))

    def init_UI(self):
        self.layout1=QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.label_screen = QtWidgets.QLabel(self)  # 用于展示图片的label
        self.label_screen.setPixmap(QPixmap("GUI/resources/helmet.jpg"))
        self.layout1.addWidget(self.label_screen)
        self.setLayout(self.layout1)  # 设置窗口主部件布局为网格布局

    def show_a_slice(self,mode):
        if mode=="up":
            if self.slice_index+1>=self.slices_num:
                print("currently already at the top of slices")
            else:
                self.slice_index+=1
                array=self.data[:,:,self.slice_index]
                array=process(array,-255,255)
                self.label_screen.setPixmap(QPixmap(array))
        else:
            if self.slice_index-1<0:
                print("currently already at the bottom of slices")
            else:
                self.slice_index -= 1
                array = self.data[:, :, self.slice_index]
                array = process(array, -255, 255)
                self.label_screen.setPixmap(QPixmap(array))

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y()>0:
            print("up")
            self.show_a_slice(mode="up")
        else:
            print("down")
            self.show_a_slice(mode="down")
        event.accept()
def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = Player()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



