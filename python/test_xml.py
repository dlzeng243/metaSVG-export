import xml.etree.ElementTree as ET
import numpy as np

# create an SVG XML element (see the SVG specification for attribute details)
doc = ET.Element('svg', style="fill:#00ff00;fill-opacity:0.25;stroke:none", viewBox="0 0 600 480", xmlns="http://www.w3.org/2000/svg")

coords_list = [[[np.array([249.5248,   9.5999]), np.array([9.5999, 9.5999])], 
[np.array([9.5999, 9.5999]), np.array([ 9.5999, 71.9791])], 
[np.array([ 9.5999, 71.9791]), np.array([249.5248,  71.9791])], 
[np.array([249.5248,  71.9791]), np.array([249.5248,   9.5999])]], 
[[np.array([499.0496,   9.5999]), np.array([259.1247,   9.5999])], 
[np.array([259.1247,   9.5999]), np.array([259.1247,  69.3809])], 
[np.array([259.1247,  69.3809]), np.array([499.0496,  69.3809])], 
[np.array([499.0496,  69.3809]), np.array([499.0496,   9.5999])]]]



d = dict()
d["attrib"] = {"style" : "fill:#00ff00;fill-opacity:0.25;stroke:none", "viewBox" : "0 0 600 400", "xmlns" : "http://www.w3.org/2000/svg"}

counter = 1
edges = []
d["tree"] = dict()
for i in range(len(coords_list)):
    coords = coords_list[i]
    (a,b) = coords[0][0]
    face = "face" + str(i+1)
    d["tree"][face] = dict()
    path = "M " + str(a) + "," + str(b) + " "
    edge = path
    for j in range(1,len(coords) + 1):
        (a,b) = coords[j % len(coords)][0]
        path += "L " + str(a) + "," + str(b) + " "
        ej = edge + "L " + str(a) + "," + str(b)
        edge = "M " + str(a) + "," + str(b) + " "
        edges.append({"d" : ej, "edge" : counter, "face": face})
        counter += 1
    path += "Z"
    d["tree"][face]["Perimeter"] = {"paths": [path]}
    sub = ET.SubElement(doc, "g")
    sub.attrib["data-name"] = face
    sub.attrib["id"] = face
    p = ET.SubElement(sub, "path")
    p.attrib["d"] = path
d["edge_data"] = dict()
d["edge_data"]["edges"] = edges
d["edge_data"]["viewBox"] = "0 0 600 400"
d["joint_index"] = 0


meta = ET.SubElement(doc, "metadata")
laser = ET.SubElement(meta, "laserassistant")
laser.attrib["model"] = str(d)

'''
https://docs.python.org/3/library/xml.etree.elementtree.html
https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths
https://www.geeksforgeeks.org/python-nested-dictionary/
https://www.tutorialspoint.com/the-elementtree-xml-api-in-python
'''

"""
"joint_parameters": {
    "joint_type": "Box",    // ALWAYS BOX FOR NOW
    "fit": "Clearance",     // 
    "tabsize": 10,          // 
    "tabspace": 20,         // 
    "tabnum": 2,            // num pins?
    "boltsize": "M2.5",     // 0?
    "boltspace": 5,         // 0?
    "boltnum": 2,           // 0?
    "boltlength": 10        // 0?
}
"""

# ElementTree 1.2 doesn't write the SVG file header errata, so do that manually
f = open('sample.svg', 'w')
f.write('\n')
f.write('\n')
f.write(ET.tostring(doc))
f.close()