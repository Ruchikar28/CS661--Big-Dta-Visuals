import vtk
import numpy as np
import os

def load_vti_file(file_path):
    """Load and verify VTI file"""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {os.path.abspath(file_path)}")
        print("Available files in directory:", os.listdir(os.path.dirname(file_path)))
        return None

    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(file_path)
    try:
        reader.Update()
        return reader.GetOutput()
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

def print_dataset_info(data):
    """Print basic dataset information"""
    dims = data.GetDimensions()
    print("\n=== Dataset Information ===")
    print(f"Dimensions: {dims}")
    print(f"Number of Points: {data.GetNumberOfPoints()}")
    print(f"Number of Cells: {data.GetNumberOfCells()}")

    pressure_array = data.GetPointData().GetScalars("Pressure")
    if not pressure_array:
        print("Warning: No 'Pressure' array found!")
        available_arrays = [data.GetPointData().GetArrayName(i) 
                          for i in range(data.GetPointData().GetNumberOfArrays())]
        print("Available arrays:", available_arrays)
        return None

    pressure_range = pressure_array.GetRange()
    pressure_values = np.array([pressure_array.GetTuple1(i) 
                              for i in range(pressure_array.GetNumberOfTuples())])
    
    print(f"Pressure Range: {pressure_range}")
    print(f"Average Pressure: {np.mean(pressure_values):.2f}")
    return pressure_array

def analyze_cell(data, cell_id, pressure_array):
    """Analyze specific cell and return its properties"""
    cell = data.GetCell(cell_id)
    print(f"\n=== Cell Analysis (ID: {cell_id}) ===")
    print(f"Number of points in cell: {cell.GetNumberOfPoints()}")

    points_coords = []
    pressures = []
    for i in range(cell.GetNumberOfPoints()):
        pt_id = cell.GetPointId(i)
        coord = data.GetPoint(pt_id)
        pressure = pressure_array.GetTuple1(pt_id)
        points_coords.append(coord)
        pressures.append(pressure)
        print(f"  Vertex {i}:")
        print(f"    Point ID: {pt_id}")
        print(f"    Coordinates: {coord}")
        print(f"    Pressure: {pressure:.2f}")

    center = np.mean(np.array(points_coords), axis=0)
    center[2] = 25  # Maintain original Z-coordinate
    avg_cell_pressure = np.mean(pressures)
    
    print(f"\nCell Center: {tuple(center)}")
    print(f"Average Cell Pressure: {avg_cell_pressure:.2f}")
    return points_coords

def visualize_points(points):
    """Visualize points with different colors"""
    vtk_points = vtk.vtkPoints()
    for pt in points:
        vtk_points.InsertNextPoint(pt)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(vtk_points)

    # Assign colors (Red, Green, Blue, Yellow)
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")
    colors.InsertNextTuple3(255, 0, 0)
    colors.InsertNextTuple3(0, 255, 0)
    colors.InsertNextTuple3(0, 0, 255)
    colors.InsertNextTuple3(255, 255, 0)
    polydata.GetPointData().SetScalars(colors)

    # Visualization pipeline
    glyph_filter = vtk.vtkVertexGlyphFilter()
    glyph_filter.SetInputData(polydata)
    
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph_filter.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(10)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.2, 0.4)  # Dark blue background

    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(800, 600)
    render_window.AddRenderer(renderer)
    render_window.SetWindowName("Cell Vertices Visualization")

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    print("\nRendering visualization...")
    render_window.Render()
    interactor.Start()

def main():
    # Configuration
    data_file = "Data/Isabel_2D.vti"  # Relative path
    cell_id_to_analyze = 0  # Change this to analyze different cells

    # Load data
    data = load_vti_file(data_file)
    if not data:
        return

    # Print dataset info
    pressure_array = print_dataset_info(data)
    if not pressure_array:
        return

    # Analyze specific cell
    points_coords = analyze_cell(data, cell_id_to_analyze, pressure_array)

    # Visualize cell vertices
    visualize_points(points_coords)

if __name__ == "__main__":
    main()