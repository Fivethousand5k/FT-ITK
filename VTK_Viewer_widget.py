import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPalette, QFont, QPixmap, QImage, QWheelEvent, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QWidget, QSizePolicy, QApplication
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.vtkImageImportFromArray import *
import vtk
import SimpleITK as sitk
import numpy as np
import time


def mkVtkIdList(it):
    """
    Makes a vtkIdList from a Python iterable. I'm kinda surprised that
     this is necessary, since I assumed that this kind of thing would
     have been built into the wrapper and happen transparently, but it
     seems not.

    :param it: A python iterable.
    :return: A vtkIdList
    """
    vil = vtk.vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil



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
        self.init_display()


    def init_display(self):

        colors = vtk.vtkNamedColors()

        # x = array of 8 3-tuples of float representing the vertices of a cube:
        x = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
             (0.0, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 1.0, 1.0), (0.0, 1.0, 1.0)]

        # pts = array of 6 4-tuples of vtkIdType (int) representing the faces
        #     of the cube in terms of the above vertices
        pts = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
               (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]

        # We'll create the building blocks of polydata including data attributes.
        cube = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        scalars = vtk.vtkFloatArray()

        # Load the point, cell, and data attributes.
        for i, xi in enumerate(x):
            points.InsertPoint(i, xi)
        for pt in pts:
            polys.InsertNextCell(mkVtkIdList(pt))
        for i, _ in enumerate(x):
            scalars.InsertTuple1(i, i)

        # We now assign the pieces to the vtkPolyData.
        cube.SetPoints(points)
        cube.SetPolys(polys)
        cube.GetPointData().SetScalars(scalars)

        # Now we'll look at it.
        cubeMapper = vtk.vtkPolyDataMapper()
        cubeMapper.SetInputData(cube)
        cubeMapper.SetScalarRange(cube.GetScalarRange())
        cubeActor = vtk.vtkActor()
        cubeActor.SetMapper(cubeMapper)

        # The usual rendering stuff.
        camera = vtk.vtkCamera()
        camera.SetPosition(1, 1, 1)
        camera.SetFocalPoint(0, 0, 0)

        # renderer = vtk.vtkRenderer()
        # renWin = vtk.vtkRenderWindow()
        # renWin.AddRenderer(renderer)
        #
        # iren = vtk.vtkRenderWindowInteractor()
        # iren.SetRenderWindow(renWin)

        self.ren.AddActor(cubeActor)
        self.ren.SetActiveCamera(camera)
        self.ren.ResetCamera()
        self.ren.SetBackground(colors.GetColor3d("Cornsilk"))
        self.iren.Start()


    def load_nii(self,path='F:\programs\FT-ITK\medical_files\pancreas_001.nii.gz'):
        self.ren.ResetCamera()
        self.iren.Initialize()
        ds = sitk.ReadImage(path)  # 读取nii数据的第一个函数sitk.ReadImage
        print('ds: ', ds)
        data = sitk.GetArrayFromImage(ds)  # 把itk.image转为array
        print('data: ', data)
        print('shape_of_data', data.shape)

        spacing = ds.GetSpacing()  # 三维数据的间隔
        print('spacing_of_data', spacing)
        # data = data[50:]
        # data = data[:,:,300:]
        srange = [np.min(data), np.max(data)]
        print('shape_of_data_chenged', data.shape)
        img_arr = vtkImageImportFromArray()  # 创建一个空的vtk类-----vtkImageImportFromArray
        print('img_arr: ', img_arr)
        img_arr.SetArray(data)  # 把array_data塞到vtkImageImportFromArray（array_data）
        img_arr.SetDataSpacing(spacing)  # 设置spacing
        origin = (0, 0, 0)
        img_arr.SetDataOrigin(origin)  # 设置vtk数据的坐标系原点
        img_arr.Update()
        print('spacing: ', spacing)
        print('srange: ', srange)
        self.iren.SetInteractorStyle(KeyPressInteractorStyle(parent=self.iren))  # 在交互操作里面添加这个自定义的操作例如up,down
        min = srange[0]
        max = srange[1]
        diff = max - min  # 体数据极差
        inter = 4200 / diff
        shift = -min
        print(min, max, inter, shift)  # 这几个数据后面有用
        shifter = vtk.vtkImageShiftScale()  # 对偏移和比例参数来对图像数据进行操作 数据转换，之后直接调用shifter
        shifter.SetShift(shift)
        shifter.SetScale(inter)
        shifter.SetOutputScalarTypeToUnsignedShort()
        shifter.SetInputData(img_arr.GetOutput())
        shifter.ReleaseDataFlagOff()
        shifter.Update()

        tfun = vtk.vtkPiecewiseFunction()  # 不透明度传输函数---放在tfun
        tfun.AddPoint(1129, 0)
        tfun.AddPoint(1300.0, 0.1)
        tfun.AddPoint(1600.0, 0.12)
        tfun.AddPoint(2000.0, 0.13)
        tfun.AddPoint(2200.0, 0.14)
        tfun.AddPoint(2500.0, 0.16)
        tfun.AddPoint(2800.0, 0.17)
        tfun.AddPoint(3000.0, 0.18)

        gradtfun = vtk.vtkPiecewiseFunction()  # 梯度不透明度函数---放在gradtfun
        gradtfun.AddPoint(-1000, 9)
        gradtfun.AddPoint(0.5, 9.9)
        gradtfun.AddPoint(1, 10)

        ctfun = vtk.vtkColorTransferFunction()  # 颜色传输函数---放在ctfun
        ctfun.AddRGBPoint(0.0, 0.5, 0.0, 0.0)
        ctfun.AddRGBPoint(600.0, 1.0, 0.5, 0.5)
        ctfun.AddRGBPoint(1280.0, 0.9, 0.2, 0.3)
        ctfun.AddRGBPoint(1960.0, 0.81, 0.27, 0.1)
        ctfun.AddRGBPoint(2200.0, 0.9, 0.2, 0.3)
        ctfun.AddRGBPoint(2500.0, 1, 0.5, 0.5)
        ctfun.AddRGBPoint(3024.0, 0.5, 0.5, 0.5)

        volumeMapper = vtk.vtkGPUVolumeRayCastMapper()  # 映射器volumnMapper使用vtk的管线投影算法
        volumeMapper.SetInputData(shifter.GetOutput())  # 向映射器中输入数据：shifter(预处理之后的数据)
        volumeProperty = vtk.vtkVolumeProperty()  # 创建vtk属性存放器,向属性存放器中存放颜色和透明度
        volumeProperty.SetColor(ctfun)
        volumeProperty.SetScalarOpacity(tfun)
        # volumeProperty.SetGradientOpacity(gradtfun)
        volumeProperty.SetInterpolationTypeToLinear()  # ???
        volumeProperty.ShadeOn()

        newvol = vtk.vtkVolume()  # 演员
        newvol.SetMapper(volumeMapper)
        newvol.SetProperty(volumeProperty)

        outline = vtk.vtkOutlineFilter()
        outline.SetInputConnection(shifter.GetOutputPort())

        outlineMapper = vtk.vtkPolyDataMapper()
        outlineMapper.SetInputConnection(outline.GetOutputPort())

        outlineActor = vtk.vtkActor()
        outlineActor.SetMapper(outlineMapper)

        self.ren.AddActor(outlineActor)
        self.ren.AddVolume(newvol)
        self.ren.SetBackground(0, 0, 0)
        # renWin.SetSize(600, 600)

        planes = vtk.vtkPlanes()

        boxWidget = vtk.vtkBoxWidget()
        boxWidget.SetInteractor(self.iren)
        boxWidget.SetPlaceFactor(1.0)
        boxWidget.PlaceWidget(0, 0, 0, 0, 0, 0)
        boxWidget.InsideOutOn()
        # boxWidget.AddObserver("StartInteractionEvent", StartInteraction)
        # boxWidget.AddObserver("InteractionEvent", ClipVolumeRender)
        # boxWidget.AddObserver("EndInteractionEvent", EndInteraction)

        outlineProperty = boxWidget.GetOutlineProperty()
        outlineProperty.SetRepresentationToWireframe()
        outlineProperty.SetAmbient(1.0)
        outlineProperty.SetAmbientColor(1, 1, 1)
        outlineProperty.SetLineWidth(9)

        selectedOutlineProperty = boxWidget.GetSelectedOutlineProperty()
        selectedOutlineProperty.SetRepresentationToWireframe()
        selectedOutlineProperty.SetAmbient(1.0)
        selectedOutlineProperty.SetAmbientColor(1, 0, 0)
        selectedOutlineProperty.SetLineWidth(3)

        self.ren.ResetCamera()
        self.iren.Initialize()


class KeyPressInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    gradtfun = vtk.vtkPiecewiseFunction()  # 梯度不透明度函数---放在gradtfun
    gradtfun.AddPoint(-1000, 9)
    gradtfun.AddPoint(0.5, 9.9)
    gradtfun.AddPoint(1, 10)

    ctfun = vtk.vtkColorTransferFunction()  # 颜色传输函数---放在ctfun
    ctfun.AddRGBPoint(0.0, 0.5, 0.0, 0.0)
    ctfun.AddRGBPoint(600.0, 1.0, 0.5, 0.5)
    ctfun.AddRGBPoint(1280.0, 0.9, 0.2, 0.3)
    ctfun.AddRGBPoint(1960.0, 0.81, 0.27, 0.1)
    ctfun.AddRGBPoint(2200.0, 0.9, 0.2, 0.3)
    ctfun.AddRGBPoint(2500.0, 1, 0.5, 0.5)
    ctfun.AddRGBPoint(3024.0, 0.5, 0.5, 0.5)

    def __init__(self, parent=None):
        self.parent = vtk.vtkRenderWindowInteractor()
        if (parent is not None):
            self.parent = parent

        self.AddObserver("KeyPressEvent", self.keyPress)

    def keyPress(self, obj, event):
        key = self.parent.GetKeySym()
        if key == 'Up':
            gradtfun.AddPoint(-100, 1.0)
            gradtfun.AddPoint(10, 1.0)
            gradtfun.AddPoint(20, 1.0)

            volumeProperty.SetGradientOpacity(gradtfun)
            # 下面这一行是关键，实现了actor的更新
            renWin.Render()
        if key == 'Down':
            tfun.AddPoint(1129, 0)
            tfun.AddPoint(1300.0, 0.1)
            tfun.AddPoint(1600.0, 0.2)
            tfun.AddPoint(2000.0, 0.1)
            tfun.AddPoint(2200.0, 0.1)
            tfun.AddPoint(2500.0, 0.1)
            tfun.AddPoint(2800.0, 0.1)
            tfun.AddPoint(3000.0, 0.1)
            # 下面这一行是关键，实现了actor的更新
            renWin.Render()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VTK_Viewer_widget()
    window.show()
    # window.init_display()
    #window.load_nii(path="F:\programs\FT-ITK\medical_files\pancreas_001.nii.gz")
    sys.exit(app.exec_())