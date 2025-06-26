import vtk
import argparse

def display_3d_volume(file_path, use_phong):
    # Load the .vti volume dataset
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    dataset = reader.GetOutput()

    # Define color mapping based on scalar values
    color_transfer = vtk.vtkColorTransferFunction()
    color_transfer.AddRGBPoint(-4931.54, 0.0, 1.0, 1.0)
    color_transfer.AddRGBPoint(-2508.95, 0.0, 0.0, 1.0)
    color_transfer.AddRGBPoint(-1873.9,  0.0, 0.0, 0.5)
    color_transfer.AddRGBPoint(-1027.16, 1.0, 0.0, 0.0)
    color_transfer.AddRGBPoint(-298.031, 1.0, 0.4, 0.0)
    color_transfer.AddRGBPoint(2594.97,  1.0, 1.0, 0.0)

    # Define opacity transfer mapping
    opacity_transfer = vtk.vtkPiecewiseFunction()
    opacity_transfer.AddPoint(-4931.54, 1.0)
    opacity_transfer.AddPoint(101.815,  0.002)
    opacity_transfer.AddPoint(2594.97,  0.0)

    # Set up visual properties for rendering
    rendering_properties = vtk.vtkVolumeProperty()
    rendering_properties.SetColor(color_transfer)
    rendering_properties.SetScalarOpacity(opacity_transfer)
    rendering_properties.SetInterpolationTypeToLinear()

    if use_phong:
        rendering_properties.ShadeOn()
        rendering_properties.SetAmbient(0.5)
        rendering_properties.SetDiffuse(0.5)
        rendering_properties.SetSpecular(0.5)
    else:
        rendering_properties.ShadeOff()

    # Prepare volume rendering pipeline
    smart_mapper = vtk.vtkSmartVolumeMapper()
    smart_mapper.SetInputData(dataset)

    volume = vtk.vtkVolume()
    volume.SetMapper(smart_mapper)
    volume.SetProperty(rendering_properties)

    # Create an outline for spatial reference
    boundary = vtk.vtkOutlineFilter()
    boundary.SetInputData(dataset)

    boundary_mapper = vtk.vtkPolyDataMapper()
    boundary_mapper.SetInputConnection(boundary.GetOutputPort())

    boundary_actor = vtk.vtkActor()
    boundary_actor.SetMapper(boundary_mapper)

    # Create the renderer and window
    scene = vtk.vtkRenderer()
    scene.SetBackground(1.0, 1.0, 1.0)
    scene.AddVolume(volume)
    scene.AddActor(boundary_actor)

    window = vtk.vtkRenderWindow()
    window.SetSize(1000, 1000)
    window.AddRenderer(scene)

    controller = vtk.vtkRenderWindowInteractor()
    controller.SetRenderWindow(window)

    # Start the visualization
    window.Render()
    controller.Start()

if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Visualize a 3D VTI volume with optional Phong lighting.")
    cli.add_argument("--input", default="Data/Isabel_3D.vti", help="Path to the .vti volume file")
    cli.add_argument("--phong", action="store_true", help="Enable Phong shading effect")
    options = cli.parse_args()

    display_3d_volume(options.input, options.phong)
