from apikey.client import Client
from collections import Counter
import pprint
import numpy as np
import xml.etree.ElementTree as ET
import json
import sys

epsilon = 0.000001
constant = 3779.5

# stacks to choose from
stacks = {
    'cad': 'https://cad.onshape.com'
}

# create instance of the onshape client; change key to test on another stack
c = Client(stack=stacks['cad'], logging=True)

# document evaluate test
'''
did = "36ad7f2f4e1268bfd6df7618"
wid = "b9622808903e3a2f41542423"
eid = "c93892577d28abd4165cc7f8"
'''

# box
'''
did = "a793a3e438b3a8a7859e3244"
wid = "d66b8b4a9bb905cb4090461b"
eid = "bdaa56060d3b9fbbd545f5e7"
'''
'''
did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"
'''

# harder box
did = "b3ea79d344251df6495836cc"
wid = "37bdc8e4d3b079cb2acffc8d"
eid = "f5ad63f423a46fabd7ae042d"

features = c.get_features(did, wid, eid)
f = features.json()
data = []
geomids = []
updates = []
partquery = []
for i in range(len(f["features"])):
    if f["features"][i]["message"]["featureType"] == "laserJoint":
        updates.append(f["features"][i])
        partquery.append([f["features"][i]["message"]["parameters"][1]["message"]["queries"], 
                          f["features"][i]["message"]["parameters"][2]["message"]["queries"], 
                          f["features"][i]["message"]["parameters"][3]["message"]["queries"]])
        ids = []
        if f["features"][i]["message"]["parameters"][1]["message"]["queries"]:
            ids += f["features"][i]["message"]["parameters"][1]["message"]["queries"][0]["message"]["geometryIds"]
        if f["features"][i]["message"]["parameters"][2]["message"]["queries"]:
            ids += f["features"][i]["message"]["parameters"][2]["message"]["queries"][0]["message"]["geometryIds"]
        if not ids or (len(ids) != 2):
            print("Not proper LaserJoint \n")
            sys.exit()
        geomids.append(ids)
        f["features"][i]["message"]["suppressed"] = True
print(geomids)
print("\n")

d = dict()
d["features"] = updates
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)

'''
ASSUME ONLY TAB AND BASE
'''

parts = c.get_parts(did, wid)
p = parts.json()
map_parts = dict()
partIdDict = dict()
counter = 0
numEdges = 0
offsetx = round(10.0 / constant, 6)
offsety = 0.0
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    area = -1
    # due to how laserjoint is coded, max of 2 faces with same area
    twodicts = [dict(), dict()]
    index = 0
    maxx = 0
    for i in range(len(body["bodies"][0]["faces"])):
        area = max(area, body["bodies"][0]["faces"][i]["area"])
    for i in range(len(body["bodies"][0]["faces"])):
        if abs(area - body["bodies"][0]["faces"][i]["area"]) < epsilon:
            x = round(body["bodies"][0]["faces"][i]["surface"]["normal"][0], 6)
            y = round(body["bodies"][0]["faces"][i]["surface"]["normal"][1], 6)
            z = round(body["bodies"][0]["faces"][i]["surface"]["normal"][2], 6)
            cornerx = round(body["bodies"][0]["faces"][i]["box"]["minCorner"][0], 6)
            cornery = round(body["bodies"][0]["faces"][i]["box"]["minCorner"][1], 6)
            cornerz = round(body["bodies"][0]["faces"][i]["box"]["minCorner"][2], 6)
            minCorner = np.array([cornerx, cornery, cornerz])
            if body["bodies"][0]["faces"][i]["orientation"]:
                twodicts[index]["normal"] = [x, y, z]
            else:
                twodicts[index]["normal"] = [-1 * x, -1 * y, -1 * z]
            twodicts[index]["edges"] = []
            twodicts[index]["2d_edges"] = []
            twodicts[index]["id"] = counter
            axisIndex = np.nonzero(twodicts[index]["normal"])[0]
            minCorner = np.delete(minCorner, axisIndex)
            for j in range(len(body["bodies"][0]["faces"][i]["loops"][0]["coedges"])):
                edgeId = body["bodies"][0]["faces"][i]["loops"][0]["coedges"][j]["edgeId"]
                orientation = body["bodies"][0]["faces"][i]["loops"][0]["coedges"][j]["orientation"]
                for k in range(len(body["bodies"][0]["edges"])):
                    if body["bodies"][0]["edges"][k]["id"] == edgeId:
                        startx = round(body["bodies"][0]["edges"][k]["geometry"]["startPoint"][0], 6)
                        starty = round(body["bodies"][0]["edges"][k]["geometry"]["startPoint"][1], 6)
                        startz = round(body["bodies"][0]["edges"][k]["geometry"]["startPoint"][2], 6)
                        
                        endx = round(body["bodies"][0]["edges"][k]["geometry"]["endPoint"][0], 6)
                        endy = round(body["bodies"][0]["edges"][k]["geometry"]["endPoint"][1], 6)
                        endz = round(body["bodies"][0]["edges"][k]["geometry"]["endPoint"][2], 6)

                        start = np.array([startx,starty,startz])
                        end = np.array([endx,endy,endz])

                        maxx = max(np.delete(start, axisIndex)[0] - minCorner[0], maxx)
                        maxx = max(np.delete(end, axisIndex)[0] - minCorner[0], maxx)
                        offsety = max(np.delete(start, axisIndex)[1] - minCorner[1], offsety)
                        offsety = max(np.delete(end, axisIndex)[1] - minCorner[1], offsety)

                        svgstart = (np.delete(start, axisIndex) - minCorner + np.array([offsetx, round(10.0 / constant, 6)]))
                        svgend =  np.delete(end, axisIndex) - minCorner + np.array([offsetx, round(10.0 / constant, 6)])
                        if orientation:
                            twodicts[index]["edges"].append([start, end])
                            twodicts[index]["2d_edges"].append([svgstart, svgend])
                        else:
                            twodicts[index]["edges"].append([end, start])
                            twodicts[index]["2d_edges"].append([svgend, svgstart])
            twodicts[index]["orientation"] = body["bodies"][0]["faces"][i]["orientation"]
            twodicts[index]["numEdges"] = numEdges
            index += 1
    cross0 = np.cross(twodicts[0]["2d_edges"][0][1]-twodicts[0]["2d_edges"][0][0], twodicts[0]["2d_edges"][1][1]-twodicts[0]["2d_edges"][1][0])
    cross1 = np.cross(twodicts[1]["2d_edges"][0][1]-twodicts[1]["2d_edges"][0][0], twodicts[1]["2d_edges"][1][1]-twodicts[1]["2d_edges"][1][0])
    print(cross0)
    print(cross1)
    if round(cross0, 4) < 0:
        for i in range(len(twodicts[0]["edges"])):
            list.reverse(twodicts[0]["edges"][i])
            list.reverse(twodicts[0]["2d_edges"][i])
        twodicts[0]["2d_edges"][1:] = twodicts[0]["2d_edges"][1:][::-1]
        twodicts[0]["edges"][1:] = twodicts[0]["edges"][1:][::-1]
    if round(cross1, 4) < 0:
        for i in range(len(twodicts[1]["edges"])):
            list.reverse(twodicts[1]["edges"][i])
            list.reverse(twodicts[1]["2d_edges"][i])
        twodicts[1]["2d_edges"][1:] = twodicts[1]["2d_edges"][1:][::-1]
        twodicts[1]["edges"][1:] = twodicts[1]["edges"][1:][::-1]
    offsetx += round(maxx + 50.0 / constant, 6)
    offsety += round(10.0 / constant, 6)
    numEdges += len(twodicts[0]["edges"])
    map_parts[pid] = twodicts
    counter += 1

pprint.pprint(map_parts)

laserEdges = []

for i in range(len(geomids)):
    tabId = geomids[i][0]
    baseId = geomids[i][1]

    tabDict = map_parts[tabId]
    baseDict = map_parts[baseId]
    axis = np.cross(np.array(tabDict[0]["normal"]), np.array(baseDict[0]["normal"]))
    if (abs(axis[0]) < epsilon and abs(axis[1]) < epsilon and abs(axis[2]) < epsilon):
        print("Not proper LaserJoint\n")
        sys.exit()
    # axis is a permutation of [0, 0, 1] if nonzero
    edge = (-1,-1)
    for j in range(2):
        for k in range(len(tabDict[j]["edges"])):
            va = tabDict[j]["edges"][k][0]
            vb = tabDict[j]["edges"][k][1]
            for jb in range(2):
                for kb in range(len(baseDict[jb]["edges"])):
                    checkf1 = va - baseDict[jb]["edges"][kb][0]
                    checkf2 = vb - baseDict[jb]["edges"][kb][1]
                    checkb1 = va - baseDict[jb]["edges"][kb][1]
                    checkb2 = vb - baseDict[jb]["edges"][kb][0]
                    if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                        (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                        ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                        (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                        edge = (j + k * 2, jb + kb * 2)
    if edge[0] < 0 or edge[1] < 0:
        print("Not proper LaserJoint \n")
        sys.exit()
    laserEdges.append(edge)
print(laserEdges)
print("\n")

vb = "0 0 " + str(round(offsetx * constant, 6)) + " " + str(round(offsety * constant, 6)) 
doc = ET.Element('svg', style="fill:none;stroke:#ff0000;stroke-linejoin:round;stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5", viewBox= vb, xmlns="http://www.w3.org/2000/svg")

meta = dict()
meta["attrib"] = {"style" : "fill:none;stroke:#ff0000;stroke-linejoin:round;stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5", "viewBox" : vb, "xmlns" : "http://www.w3.org/2000/svg"}
meta["joints"] = dict()

for i in range(len(laserEdges)):
    a,b = laserEdges[i]
    tabId, baseId = geomids[i]
    partIdDict[tabId] = True
    partIdDict[baseId] = True
    indexT0 = a % 2
    indexT1 = a // 2
    indexB0 = b % 2
    indexB1 = b // 2
    meta["joints"]["Joint" + str(i + 1)] = dict()
    tab = map_parts[tabId][indexT0]["2d_edges"][indexT1]
    base = map_parts[baseId][indexB0]["2d_edges"][indexB1]
    tabEdge = "M " + str(np.around(tab[0][0] * constant, 6)) + "," + str(np.around(tab[0][1] * constant, 6)) + " L " + \
                     str(np.around(tab[1][0] * constant, 6)) + "," + str(np.around(tab[1][1] * constant, 6))
    baseEdge = "M " + str(np.around(base[0][0] * constant, 6)) + "," + str(np.around(base[0][1] * constant, 6)) + " L " + \
                     str(np.around(base[1][0] * constant, 6)) + "," + str(np.around(base[1][1] * constant, 6))
    meta["joints"]["Joint" + str(i + 1)]["edge_a"] = {"d" : tabEdge,
                                                      "edge" : indexT1 + map_parts[tabId][indexT0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[tabId][indexT0]["id"] + 1)}
    meta["joints"]["Joint" + str(i + 1)]["edge_b"] = {"d" : baseEdge,
                                                      "edge" : indexB1 + map_parts[baseId][indexB0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[baseId][indexB0]["id"] + 1)}
    length = max(abs(tab[1][0] - tab[0][0]), abs(tab[1][1] - tab[0][1])) * constant
    tabnum = int((str(updates[i]["message"]["parameters"][4]["message"]["expression"])))
    meta["joints"]["Joint" + str(i + 1)]["joint_parameters"] = {"joint_type": "Box",
                                                "joint_align": "Inside",
                                                "fit": "Clearance",
                                                "tabsize": length / (2 * tabnum - 1),
                                                "tabspace": length / (2 * tabnum - 1),
                                                "tabnum": tabnum - 1,
                                                "boltsize": "M0",
                                                "boltspace": 0,
                                                "boltnum": 0,
                                                "boltlength": 0}



edges = []
meta["tree"] = dict() 
for partkey in map_parts:
    pedges = map_parts[partkey][0]["2d_edges"]
    (a,b) = np.around(pedges[0][0] * constant, 6)
    face = "face" + str(map_parts[partkey][0]["id"]+1)
    meta["tree"][face] = dict()
    path = "M " + str(a) + "," + str(b) + " "
    edge = path
    for j in range(1,len(pedges) + 1):
        (a,b) = np.around(pedges[j % len(pedges)][0] * constant, 6)
        path += "L " + str(a) + "," + str(b) + " "
        ej = edge + "L " + str(a) + "," + str(b)
        edge = "M " + str(a) + "," + str(b) + " "
        edges.append({"d" : ej, "edge" : j + map_parts[partkey][0]["numEdges"], "face": face})
        counter += 1
    meta["tree"][face]["Perimeter"] = {"paths": [path]}
    meta["tree"][face]["Cuts"] = {"paths": []}
    path += "Z"
    sub = ET.SubElement(doc, "g")
    sub.attrib["data-name"] = face
    sub.attrib["id"] = face
    p = ET.SubElement(sub, "path")
    p.attrib["d"] = path

meta["edge_data"] = dict()
meta["edge_data"]["edges"] = edges
meta["edge_data"]["viewBox"] = vb
meta["joint_index"] = 0


pprint.pprint(meta)
metaTree = ET.SubElement(doc, "metadata")
laser = ET.SubElement(metaTree, "laserassistant")
laser.attrib["model"] = str(meta).replace("\'", "\"")

svg = open('try4.svg', 'w')
svg.write(ET.tostring(doc))
svg.close()


# unsupress all laser joints
features = c.get_features(did, wid, eid)
f = features.json()
for i in range(len(updates)):
    # unsuppress the laser joint
    laseri = updates[i]
    laseri["message"]["suppressed"] = False
    laseri["message"]["parameters"][1]["message"]["queries"] = partquery[i][0]
    laseri["message"]["parameters"][2]["message"]["queries"] = partquery[i][1]
    laseri["message"]["parameters"][3]["message"]["queries"] = partquery[i][2]

d = dict()
d["features"] = updates
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)







'''
d = {
  "script" : "function (context is Context, queries is map) { return getVariable(context, \"a\"); }",
  "queries" : [],
  "sourceMicroversion" : f["sourceMicroversion"]
}
a = c.evaluate_feature(did, wid, eid, d) '''