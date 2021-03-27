import cv2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QFont, QPixmap, QImage, QWheelEvent, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QSizePolicy

import threading
import time
import sys
import numpy as np
from tools import *


class Slice_Viewer_Widget(QWidget):
    def __init__(self, parent=None, ):
        super(Slice_Viewer_Widget, self).__init__(parent)
        self.init_UI()
        self.init_data()

        # self.data=np.load("0001.npy")
        # self.screen_width,self.screen_height,self.slices_num=self.data.shape
        # init_cover=self.data[:,:,self.slice_index]
        # showImage=array_preprocess(init_cover,-255,255)

    def init_UI(self):
        self.pixmap = QPixmap("GUI-resourses/start-up.PNG")
        self.layout = QtWidgets.QGridLayout()
        self.label_screen = QtWidgets.QLabel(self)  # label used as a screen to display CT slices
        self.label_screen.setPixmap(self.pixmap)  # initialize the label_screen with start-up.PNG
        self.layout.addWidget(self.label_screen)
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.setWindowTitle("Slice_Viewer_example")
        self.setWindowIcon(QIcon("GUI-resourses/FT-icon.png"))

    def init_data(self):
        self.data = None
        self.screen_width, self.screen_height, self.slices_num = None, None, None
        self.slice_index = 0
        self.current_slice = None
        self.old_line = (0, 0, 0, 0)
        self.mouse_x,self.mouse_y=0,0      # record the last coordinates of the mouse

    def load_data(self, file_path):
        if ".npy" in file_path:  # numpy_file
            data = np.load(file_path)
        self.data = data
        self.screen_width, self.screen_height, self.slices_num = data.shape
        self.slice_index = 0  # initialize the slice index with 0
        self.show_a_slice()

    def show_a_slice(self, mode="others"):
        """
        display a slice onto the label screen, this function would be called when the user scrolls the mouse or loads a file
        The slice would be fetched from a self.data (3-dimention array) according to the slice_index.

        :param mode: this parameter has three possibile value:
                    "up" ---- mouse scrolling up, then slice_index+=1
                    "down" ---- mouse scrolling down, then slice_index=-1
                    "others" ---- slice_index stays the same

        :return:
        """
        if self.data is not None:
            if mode == "up":
                if self.slice_index + 1 >= self.slices_num:
                    print("currently already at the top of slices")
                else:
                    self.slice_index += 1
                    self.current_slice = self.data[:, :, self.slice_index]
                    self.current_slice = array_preprocess(self.current_slice, -255, 255)
                    self.pixmap = QPixmap(self.current_slice)
                    self.draw_lines(x=self.mouse_x,y=self.mouse_y)
                    self.label_screen.setPixmap(self.pixmap)
            elif mode == "down":
                if self.slice_index - 1 < 0:
                    print("currently already at the bottom of slices")
                else:
                    self.slice_index -= 1
                    self.current_slice = self.data[:, :, self.slice_index]
                    self.current_slice = array_preprocess(self.current_slice, -255, 255)
                    self.pixmap = QPixmap(self.current_slice)
                    self.draw_lines(x=self.mouse_x, y=self.mouse_y)
                    self.label_screen.setPixmap(self.pixmap)
            else:  # neither "up" nor "down", this situation would occur when it loads data.
                self.current_slice = self.data[:, :, self.slice_index]
                self.current_slice = array_preprocess(self.current_slice, -255, 255)
                self.pixmap = QPixmap(self.current_slice)
                self.draw_lines(x=self.mouse_x, y=self.mouse_y)
                self.label_screen.setPixmap(self.pixmap)
        else:
            print("No data has been loaded!")

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:  # mouse scrolling up
            print("up")
            self.show_a_slice(mode="up")
        else:  # mouse scrolling down
            print("down")
            self.show_a_slice(mode="down")
        event.accept()

    def draw_lines(self, x, y,radius=30):

        painter = QPainter(self.pixmap)
        painter.drawPixmap(0, 0, self.pixmap)
        #### draw vertical line ####
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(0, y, x - radius, y)
        painter.drawLine(x+radius, y, 512, y)
        ############################

        #### draw horizontal line ###
        pen = QPen(Qt.green, 3)
        painter.setPen(pen)
        painter.drawLine(x, 0, x, y-radius)
        painter.drawLine(x, y+radius, x, 512)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:

        self.pixmap = QPixmap(self.current_slice)
        self.draw_lines(x=event.x(), y=event.y())
        self.label_screen.setPixmap(self.pixmap)
        self.mouse_x,self.mouse_y=event.x(),event.y()
        print(event.x(), event.y())
        # print(self.label_screen.width(),self.label_screen.height())

    def paintEvent(self, QPaintEvent):
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.red, 3))
        # painter.begin(self)
        # painter.drawLine(10,10, 200 - 10, 200)
        # painter.end()
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Slice_Viewer_Widget()
    gui.load_data("medical_files/0001.npy")
    gui.show()
    sys.exit(app.exec_())
