from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPalette, QFont, QCursor
from PyQt5.QtWidgets import QMenu, QTreeWidgetItem, QLabel, QSizePolicy, QTreeWidget, QFileDialog
from PyQt5 import QtCore
import sys
from Slices_Viewer_Widget import Slice_Viewer_Widget
from Signal_Central_Process_Unit import SCPU
from VTK_Viewer_widget import VTK_Viewer_widget
import numpy as np

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_data()
        self.init_SCPU_signal_connection()
    def init_ui(self):
        self.setWindowTitle("FT-ITK")
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.Axial_Viewer = Slice_Viewer_Widget(type="axial")  # axial view,横断位
        self.Sagittal_Viewer = Slice_Viewer_Widget(type="sagittal")  # sagittal view，矢状位
        self.Coronal_Viewer = Slice_Viewer_Widget(type="coronal")  # coronal view，冠状位
        # self.Others_Viewer = Slice_Viewer_Widget()
        self.VTK_Viewer=VTK_Viewer_widget()
        self.main_layout.addWidget(self.Axial_Viewer,0,0)
        self.main_layout.addWidget(self.Sagittal_Viewer,0,1)
        self.main_layout.addWidget(self.Coronal_Viewer,1,0)
        self.main_layout.addWidget(self.VTK_Viewer,1,1)
        self.data=np.load("medical_files/0001.npy")
        self.VTK_Viewer.load_nii()
        #self.main_layout.addWidget(self.Others_Viewer,1,1)
        self.Axial_Viewer.load_data_from_father(self.data)
        self.Sagittal_Viewer.load_data_from_father(self.data)
        self.Coronal_Viewer.load_data_from_father(self.data)
        self.main_layout.setSpacing(2)

    def init_data(self):
        self.SCPU=SCPU()    #Signal_Central_Process_Unit(SCPU)

    def init_SCPU_signal_connection(self):
        self.Axial_Viewer.output_signal.connect(self.SCPU.Process_Core)
        self.Sagittal_Viewer.output_signal.connect(self.SCPU.Process_Core)
        self.Coronal_Viewer.output_signal.connect(self.SCPU.Process_Core)
        self.SCPU.command_to_axial.connect(self.Axial_Viewer.handle_SCPU_command)
        self.SCPU.command_to_sagittal.connect(self.Sagittal_Viewer.handle_SCPU_command)
        self.SCPU.command_to_coronal.connect(self.Coronal_Viewer.handle_SCPU_command)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
