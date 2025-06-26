CS661: Assignment 1 – Isocontour & Volume Visualization
Group No : 2

1. Setup Requirements
Before running the code, ensure you have the following installed:

VTK for Python
Install using pip:
pip install vtk
ParaView – recommended for visually verifying outputs and capturing screenshots

2. Project Directory Layout

GROUP_ASSIGNMENT1/
├── Data/
│   ├── Isabel_2D.vti        # 2D scalar field (pressure slice)
│   └── Isabel_3D.vti        # Full 3D volume data
├── outputs/
│   └── contour.vtp          # Output of the isocontour script
├── screenshots/
│   ├── volume_noPhong_front.png
│   ├── volume_noPhong_back.png
│   ├── volume_phong_front.png
│   └── volume_phong_back.png
├── isocontour.py            # Part 1: 2D contour generation script
├── volumeRender.py         # Part 2: 3D volume rendering script
└── README.txt               # This documentation




3. Part 1 – Isocontour Extraction (2D)
Script: isocontour.py

Overview:

This script reads a 2D VTK image (.vti), extracts an isocontour at a specified scalar value, and writes the result to a .vtp (VTK PolyData) file.
The algorithm uses simple edge-based interpolation to locate intersections—no Marching Squares lookup table is used.

How to Run:

python isocontour.py --input Data/Isabel_2D.vti --output outputs/contour.vtp --isovalue <VALUE>
Parameters:

input : Path to input .vti file (default: Data/Isabel_2D.vti)

output : Output .vtp file path (default: outputs/contour.vtp)

isovalue : Scalar value where the contour is extracted (required)

Example:
//To run this file type this command in terminal//
python isocontour.py --isovalue 150
This creates contour.vtp with contours at pressure = 150.

Validation:

Using ParaView:
Load both Isabel_2D.vti and outputs/contour.vtp
Apply the Probe Location filter to sample scalar values onto the contour
Color the contour by the sampled values — they should all match the specified isovalue

From the script:
The script can be modified to print the range of scalar values on the contour to check for correctness.





4. Part 2 – 3D Volume Rendering
Script: volumeRender.py

Overview:

This script reads a 3D VTK volume (.vti), applies custom color and opacity mappings, and renders the volume using vtkSmartVolumeMapper.
Phong shading can be optionally enabled for more realistic lighting.

Basic Usage:
python volumeRender.py --input Data/Isabel_3D.vti [--phong]
Parameters:

input : Path to the 3D .vti file (default: Data/Isabel_3D.vti)

phong : Enables Phong lighting (ambient = 0.5, diffuse = 0.5, specular = 0.5)


Render without lighting:
//To run this file type this command in terminal//
python volumeRender.py
Render with Phong shading:
python volumeRender.py --phong


#Screenshots:

Captured render views are saved under screenshots/:

volumeRender_noPhong_front.png
volumeRender_noPhong_back.png
volumeRender_phong_front.png
volumeRender_phong_back.png

#Screenshot Instructions:

Run the script and wait for the render to display.
Use ParaView to open the .vti file (if needed for clarity).
Use Reset Camera for the front view.
Rotate 180° around Y-axis for the back view.
Go to File → Save Screenshot, and export images at 1000×1000 resolution.