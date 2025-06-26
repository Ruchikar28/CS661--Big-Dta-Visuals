import vtk
import argparse
import os

def extract_contour_from_vti(source_file, output_file, threshold):
    # Create the output folder if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Read the .vti data
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(source_file)
    reader.Update()
    dataset = reader.GetOutput()

    width, height, _ = dataset.GetDimensions()
    values = dataset.GetPointData().GetScalars()

    # Create VTK objects to store points and line segments
    points = vtk.vtkPoints()
    segments = vtk.vtkCellArray()

    # Loop through the image grid
    for row in range(width - 1):
        for col in range(height - 1):
            # Get flat indices for 4 corner points
            a = row + col * width
            b = (row + 1) + col * width
            c = (row + 1) + (col + 1) * width
            d = row + (col + 1) * width

            # Fetch scalar values at those points
            sa = values.GetValue(a)
            sb = values.GetValue(b)
            sc = values.GetValue(c)
            sd = values.GetValue(d)

            # Direct edge-based interpolation (no marching squares)
            crossings = []

            if (sa < threshold) != (sb < threshold):
                alpha = (threshold - sa) / (sb - sa)
                crossings.append((row + alpha, col))

            if (sb < threshold) != (sc < threshold):
                alpha = (threshold - sb) / (sc - sb)
                crossings.append((row + 1, col + alpha))

            if (sc < threshold) != (sd < threshold):
                alpha = (threshold - sd) / (sc - sd)
                crossings.append((row + alpha, col + 1))

            if (sa < threshold) != (sd < threshold):
                alpha = (threshold - sa) / (sd - sa)
                crossings.append((row, col + alpha))

            # If exactly two intersections, connect with a line
            if len(crossings) == 2:
                idx1 = points.InsertNextPoint(crossings[0][0], crossings[0][1], 0)
                idx2 = points.InsertNextPoint(crossings[1][0], crossings[1][1], 0)

                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, idx1)
                line.GetPointIds().SetId(1, idx2)
                segments.InsertNextCell(line)

    # Create the final polydata object
    polyline = vtk.vtkPolyData()
    polyline.SetPoints(points)
    polyline.SetLines(segments)

    # Save the polydata to file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_file)
    writer.SetInputData(polyline)
    writer.Write()

    print(f"Isocontour written to {output_file} from {source_file} at level {threshold}")

if __name__ == "__main__":
    cli = argparse.ArgumentParser(description="Generate 2D isocontours from VTI data via edge interpolation.")
    cli.add_argument("--input", default="Data/Isabel_2D.vti", help="Input .vti file path")
    cli.add_argument("--output", default="outputs/contour.vtp", help="Output .vtp file path")
    cli.add_argument("--isovalue", type=float, required=True, help="Threshold scalar value for contouring")

    args = cli.parse_args()
    extract_contour_from_vti(args.input, args.output, args.isovalue)
