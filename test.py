
import vtk

# Create a sphere
sphere = vtk.vtkSphereSource()
sphere.SetRadius(1.0)

# Create mapper and actor
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create renderer and window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Add actor and render
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)
render_window.Render()
render_window_interactor.Start()
