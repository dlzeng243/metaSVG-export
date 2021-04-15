import xml.etree.ElementTree as ET
import numpy as np

# create an SVG XML element (see the SVG specification for attribute details)
doc = ET.Element('svg', style="fill:#00ff00;fill-opacity:0.25;stroke:none", viewBox="0 0 360 480", xmlns="http://www.w3.org/2000/svg")

coords_list = [[[np.array([25.99237139,  1.00000054]), np.array([1.00000054, 1.00000054])],
  [np.array([1.00000054, 1.00000054]), np.array([1.00000054, 7.49787978])],
  [np.array([1.00000054, 7.49787978]), np.array([25.99237139,  7.49787978])],
  [np.array([25.99237139,  7.49787978]), np.array([25.99237139,  1.00000054])]],
 [[np.array([51.98474278,  1.00000054]), np.array([26.99237193,  1.00000054])],
  [np.array([26.99237193,  1.00000054]), np.array([26.99237193,  7.22723143])],
  [np.array([26.99237193,  7.22723143]), np.array([51.98474278,  7.22723143])],
  [np.array([51.98474278,  7.22723143]), np.array([51.98474278,  1.00000054])]]]

for i in range(len(coords_list)):
    coords = coords_list[i]
    (a,b) = coords[0][0]
    path = "M " + str(a) + "," + str(b) + " "
    for j in range(1,len(coords) + 1):
        (a,b) = coords[j % len(coords)][0]
        path += "L " + str(a) + "," + str(b) + " "
    path += "z"
    face = "face" + str(i)
    sub = ET.SubElement(doc, "g")
    sub.attrib["data-name"] = face
    sub.attrib["id"] = face
    p = ET.SubElement(sub, "path")
    p.attrib["d"] = path

# add a circle (using the SubElement function)

# ElementTree 1.2 doesn't write the SVG file header errata, so do that manually
f = open('sample.svg', 'w')
f.write('\n')
f.write('\n')
f.write(ET.tostring(doc))
f.close()