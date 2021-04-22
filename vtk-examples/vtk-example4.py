import vtk
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName('medical_files/pancreas_001.nii.gz')
reader.Update()

mapper = vtk.vtkGPUVolumeRayCastMapper()
mapper.SetInputData(reader.GetOutput())

volume = vtk.vtkVolume()
volume.SetMapper(mapper)

property = vtk.vtkVolumeProperty()

popacity = vtk.vtkPiecewiseFunction()
popacity.AddPoint(1000, 0.0)
popacity.AddPoint(4000, 0.68)
popacity.AddPoint(7000, 0.83)

color = vtk.vtkColorTransferFunction()
color.AddHSVPoint(1000, 0.042, 0.73, 0.55)
color.AddHSVPoint(2500, 0.042, 0.73, 0.55, 0.5, 0.92)
color.AddHSVPoint(4000, 0.088, 0.67, 0.88)
color.AddHSVPoint(5500, 0.088, 0.67, 0.88, 0.33, 0.45)
color.AddHSVPoint(7000, 0.95, 0.063, 1.0)

property.SetColor(color)
property.SetScalarOpacity(popacity)
property.ShadeOn()
property.SetInterpolationTypeToLinear()
property.SetShade(0, 1)
property.SetDiffuse(0.9)
property.SetAmbient(0.1)
property.SetSpecular(0.2)
property.SetSpecularPower(10.0)
property.SetComponentWeight(0, 1)
property.SetDisableGradientOpacity(1)
property.DisableGradientOpacityOn()
property.SetScalarOpacityUnitDistance(0.891927)

volume.SetProperty(property)

ren = vtk.vtkRenderer()
ren.AddActor(volume)
ren.SetBackground(0.1, 0.2, 0.4)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.SetSize(600, 600)
renWin.Render()
iren.Start()

