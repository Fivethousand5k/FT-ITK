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
    def __init__(self, parent=None, type="axial"):
        super(Slice_Viewer_Widget, self).__init__(parent)
        self.init_type(type)
        self.init_UI()
        self.init_data()

        # self.data=np.load("0001.npy")
        # self.screen_width,self.screen_height,self.slices_num=self.data.shape
        # init_cover=self.data[:,:,self.slice_index]
        # showImage=array_preprocess(init_cover,-255,255)

    def init_type(self, type):
        assert type in ["axial", "sagittal",
                        "coronal"], "the type of slice viewer must be in [\"axial\",\"sagittal\",\"coronal\"]"
        color_dict = {
            "axial": "red",  # red for axial view
            "sagittal": "green",  # green for sagittal view
            "coronal": "blue"}  # blue for coronal view

        # the color of horizontal_line on the screen, different colors represent slice viewers of different perspectives in accordance with their edges' color
        horizontal_line_color_dict = {
            "axial": Qt.blue,
            "sagittal": Qt.red,
            "coronal": Qt.red
        }

        # the color of vertical_line on the screen, different colors represent slice viewers of different perspectives in accordance with their edges' color
        vertical_line_color_dict = {
            "axial": Qt.green,
            "sagittal": Qt.blue,
            "coronal": Qt.green
        }

        self.edge_color = color_dict[type]  # the color surrounding the label_screen
        self.horizontal_line_color=horizontal_line_color_dict[type]
        self.vertical_line_color=vertical_line_color_dict[type]
        self.type=type

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
        # 设置边框样式 可选样式有Box Panel等
        self.label_screen.setFrameShape(QtWidgets.QFrame.Box)
        # 设置阴影 只有加了这步才能设置边框颜色
        # 可选样式有Raised、Sunken、Plain（这个无法设置颜色）等
        self.label_screen.setFrameShadow(QtWidgets.QFrame.Raised)
        # 设置线条宽度
        self.label_screen.setLineWidth(3)
        # 设置背景颜色，包括边框颜色
        #self.label_screen.setStyleSheet('background-color: rgb{}'.format(self.edge_color))
        self.label_screen.setStyleSheet('background-color:'+self.edge_color)


    def init_data(self):
        self.data = None
        self.screen_width, self.screen_height, self.slices_num = None, None, None
        self.slice_index = 0
        self.current_slice = None
        self.old_line = (0, 0, 0, 0)
        self.mouse_x, self.mouse_y = 0, 0  # record the last coordinates of the mouse

    def load_data_from_path(self, file_path: str):
        """
        the Slice_viewer reads the array from file_path(a str). It currently supports .npy
        :param file_path: file_path should be a string
        :return:
        """
        if ".npy" in file_path:  # numpy_file
            data = np.load(file_path)
        self.data = data
        self.screen_width, self.screen_height, self.slices_num = self.get_screen_width_height_slicenum(data)
        self.slice_index = 0  # initialize the slice index with 0
        self.show_a_slice()

    def load_data_from_father(self, data):
        """
        the Slice_viewer receives data directly from the father widget. By doing this, all the Slice_viewers could share
         a variable with potentially large size(several hundred MB usually), thus help save the consumption of memory.
        :param data:
        :return:
        """
        self.data = data
        self.screen_width, self.screen_height, self.slices_num = self.get_screen_width_height_slicenum(data)
        self.slice_index = 0  # initialize the slice index with 0
        self.show_a_slice()

    def get_screen_width_height_slicenum(self,data):
        """
        self.screen_width, self.screen_height, self.slices_num according to the type of slice_viewer
        :return:
        """
        if self.type == "axial":
            self.screen_height, self.screen_width, self.slices_num = data.shape
        elif self.type =="sagittal":
            self.screen_height,self.slices_num,self.screen_width=data.shape
        elif self.type == "coronal":
            self.slices_num,self.screen_height,self.screen_width=data.shape
        return self.screen_width, self.screen_height, self.slices_num


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
                    self.update_current_slice()
                    self.pixmap = QPixmap(self.current_slice)
                    self.draw_lines(x=self.mouse_x, y=self.mouse_y)
                    self.label_screen.setPixmap(self.pixmap)
            elif mode == "down":
                if self.slice_index - 1 < 0:
                    print("currently already at the bottom of slices")
                else:
                    self.slice_index -= 1
                    self.update_current_slice()
                    self.pixmap = QPixmap(self.current_slice)
                    self.draw_lines(x=self.mouse_x, y=self.mouse_y)
                    self.label_screen.setPixmap(self.pixmap)
            else:  # neither "up" nor "down", this situation would occur when it loads data.

                self.update_current_slice()
                self.pixmap = QPixmap(self.current_slice)
                self.draw_lines(x=self.mouse_x, y=self.mouse_y)
                self.label_screen.setPixmap(self.pixmap)
        else:
            print("No data has been loaded!")
    def update_current_slice(self):
        if self.type is "axial":
            self.current_slice = self.data[:, :, self.slice_index]
        elif self.type is "sagittal":
            self.current_slice =self.data[:,self.slice_index,:]
        elif self.type is "coronal" :
            self.current_slice =self.data[self.slice_index,:,:]
        self.current_slice=array_preprocess(self.current_slice,-255,255,type=self.type)

    def wheelEvent(self, event: QWheelEvent):
        if event.angleDelta().y() > 0:  # mouse scrolling up
            print("up")
            self.show_a_slice(mode="up")
        else:  # mouse scrolling down
            print("down")
            self.show_a_slice(mode="down")
        event.accept()

    def draw_lines(self, x, y, radius=30):

        painter = QPainter(self.pixmap)
        painter.drawPixmap(0, 0, self.pixmap)
        #### draw horizontal line ####
        pen = QPen(self.horizontal_line_color, 3)
        painter.setPen(pen)
        painter.drawLine(0, y, x - radius, y)
        painter.drawLine(x + radius, y, 512, y)
        ############################

        #### draw vertical line ###
        pen = QPen(self.vertical_line_color, 3)
        painter.setPen(pen)
        painter.drawLine(x, 0, x, y - radius)
        painter.drawLine(x, y + radius, x, 512)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:

        self.pixmap = QPixmap(self.current_slice)
        self.draw_lines(x=event.x(), y=event.y())
        self.label_screen.setPixmap(self.pixmap)
        self.mouse_x, self.mouse_y = event.x(), event.y()
        print(event.x(), event.y())
        # print(self.label_screen.width(),self.label_screen.height())

    def paintEvent(self, QPaintEvent):
        # painter = QPainter(self)
        # painter.setPen(QPen(Qt.red, 3))
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Slice_Viewer_Widget(type="coronal")
    gui.load_data_from_path("medical_files/0001.npy")
    gui.show()
    sys.exit(app.exec_())

