import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QFont, QPixmap, QImage, QWheelEvent, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QSizePolicy, QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import vtk
class VTK_Viewer_widget(QWidget):
    def __init__(self,parent=None):
        super(VTK_Viewer_widget, self).__init__(parent)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)
        self.vtkWidget = QVTKRenderWindowInteractor()
        self.layout.addWidget(self.vtkWidget)
        self.ren=vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create source
        source = vtk.vtkConeSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(0.1)

        source1 = vtk.vtkSphereSource()
        source1.SetCenter(0, 0, 0)
        source1.SetRadius(0.3)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        mapper1 = vtk.vtkPolyDataMapper()
        mapper1.SetInputConnection(source1.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        actor1 = vtk.vtkActor()
        actor1.SetMapper(mapper1)

        self.ren.AddActor(actor)
        self.ren.AddActor(actor1)

        self.ren.ResetCamera()

        self.iren.Initialize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VTK_Viewer_widget()
    window.show()
    sys.exit(app.exec_())