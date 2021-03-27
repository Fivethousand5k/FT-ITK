from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPalette, QFont, QCursor
from PyQt5.QtWidgets import QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget, QFileDialog
from PyQt5 import QtCore
import sys
from Slices_Viewer_Widget import Slice_Viewer_Widget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.Axial_Viewer = Slice_Viewer_Widget()  # axial view,横断位
        self.Sagittal_Viewer = Slice_Viewer_Widget()  # sagittal view，矢状位
        self.Coronal_Viewer = Slice_Viewer_Widget()  # coronal view，冠状位
        self.Others_Viewer = Slice_Viewer_Widget()
        self.main_layout.addWidget(self.Axial_Viewer,0,0)
        self.main_layout.addWidget(self.Sagittal_Viewer,0,1)
        self.main_layout.addWidget(self.Coronal_Viewer,1,0)
        #self.main_layout.addWidget(self.Others_Viewer,1,1)
        self.Axial_Viewer.load_data("medical_files/0001.npy")
        self.Sagittal_Viewer.load_data("medical_files/0001.npy")
        self.Coronal_Viewer.load_data("medical_files/0001.npy")
        self.main_layout.setSpacing(1)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
