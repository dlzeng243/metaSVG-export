'''
First time:
add creds.json to python folder:

{
    "https://cad.onshape.com": {
        "access_key": "ACCESS KEY",
        "secret_key": "SECRET KEY"
    }
}
install python2, pip, virtualenv

How to run:
run $ virtualenv -p /Library/Frameworks/Python.framework/Versions/2.7/bin/python2 env && source env/bin/activate 
    in python folder
run $ pip install -r requirements.txt
run python2 app.py
'''

'''
ASSUMPTIONS SO FAR:
Use laser joint featurescript
All parts will have the same height (because laser cutting the same material)
All parts will be polygonal
Intersection between base and tab will be a "good fit" (meaning the side lengths will match up)
no cuts on the inside

'''

'''
IDEA:
Get feature list (have users raw input did, wid, and eid)
// read kerf csv (I don't think we need to do this, we just need to make the metasvg)
Check if they have used the laser joint feature
    If not, then return need to use that feature
If so, then need to figure out how to keep the laser joint information + also lay out the parts
    Can get part details with get_body_details on each part in the parts list
From here, we need to make it an SVG somehow, and then attach all the laser joint information as metadata

idea:
Go through each part
Find the common height
Make a auto layout feature with the common height
Call it on the thing
Get updated body details
Get all faces with a normal of 001 or 00-1
Then we can get the lengths of each edge of the faces
then use svgpathtools to make the svg


ALL MEASUREMENTS IN BODY DETAILS ARE IN METERS
    Find a way to rescale this

'''

'''
functions that might be useful:
PARTS - body details (get information about lengths and stuff)
PARTS - get parts (get parts id)

PARTSTUDIO - get features (get laser cut info)
PARTSTUDIO - update feature (suppress)
PARTSTUDIO - add feature (add the autolayout)
PARTSTUDIO - delete feature

ELEMENTS - get configuration?

DRAWINGS - get translation format?

there's a feature script to autolayout - maybe try using it to get info?
https://www.youtube.com/watch?v=YPoJ484-7tI&t=1s

check if the body details are different with and without the laser cut (they are very different)
'''


'''
https://cad.onshape.com/FsDoc/tutorials/create-a-slot-feature.html
https://forum.onshape.com/discussion/5528/evaluate-featurescript-request-returns-empty-btfsvaluearray-instead-of-face
https://forum.onshape.com/discussion/7544/execute-featurescript-using-api-and-python
'''



from apikey.client import Client
from collections import Counter
import pprint
import numpy as np
import xml.etree.ElementTree as ET
import json

epsilon = 0.000001
constant = 3779.5

# stacks to choose from
stacks = {
    'cad': 'https://cad.onshape.com'
}

# create instance of the onshape client; change key to test on another stack
c = Client(stack=stacks['cad'], logging=True)

'''
did = raw_input('Enter document ID: ')
wid = raw_input('Enter workspace ID: ')
eid = raw_input('Enter element ID: ')
'''

# for convenience sake, will use one of my onshape documents as testing

# document 1

did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"


# document test1
'''
did = "a793a3e438b3a8a7859e3244"
wid = "d66b8b4a9bb905cb4090461b"
eid = "bdaa56060d3b9fbbd545f5e7"
'''

# document hexagon
'''
did = "f64e517b60b7be5b9e096610"
wid = "8819fa3e5a42943b4f6d72b2"
eid = "37cd35df347f894e04bab4c7"
'''


features = c.get_features(did, wid, eid)
f = features.json()

# get the body details to find length to autolayout
parts = c.get_parts(did, wid)
p = parts.json()
body_list = []
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    body_list.append(body["bodies"])

length_list = []
for body in body_list:
    length_set = set()
    for edge in body[0]["edges"]:
        length_set.add(edge["geometry"]["length"])
    length_list.append(length_set)
for i in range(1, len(length_list)):
    length_list[0].intersection_update(length_list[i])
if len(length_list[0]) == 0:
    exit
sort_lengths = sorted(list(length_list[0]))

# Add autolayout feature with specified length
d = dict()
alf = {u'message': {u'featureType': u'autolayout',
        u'hasUserCode': False,
        u'name': u'Auto Layout 1',
        u'namespace': u'df0ea3e290860f984f4075197::vc2e512d1951a9eda143a5a40::e43c995e59341bb62975a36b8::m487f3f81e149ec9cd19f43e7',
        u'parameters': [{u'message': {u'expression': u'0.0 in',
        u'hasUserCode': False,
        u'isInteger': False,
        u'parameterId': u'thickness',
        u'units': u'',
        u'value': 0.0},
        u'type': 147,
        u'typeName': u'BTMParameterQuantity'},
        {u'message': {u'expression': u'60 in',
        u'hasUserCode': False,
        u'isInteger': False,
        u'parameterId': u'width',
        u'units': u'',
        u'value': 0.0},
        u'type': 147,
        u'typeName': u'BTMParameterQuantity'},
        {u'message': {u'expression': u'100 in',
        u'hasUserCode': False,
        u'isInteger': False,
        u'parameterId': u'height',
        u'units': u'',
        u'value': 0.0},
        u'type': 147,
        u'typeName': u'BTMParameterQuantity'},
        {u'message': {u'expression': u'0.1 in',
        u'hasUserCode': False,
        u'isInteger': False,
        u'parameterId': u'spacing',
        u'units': u'',
        u'value': 0.0},
        u'type': 147,
        u'typeName': u'BTMParameterQuantity'},
        {u'message': {u'hasUserCode': False,
        u'parameterId': u'showSheets',
        u'value': False},
        u'type': 144,
        u'typeName': u'BTMParameterBoolean'}],
        u'returnAfterSubfeatures': False,
        u'subFeatures': [],
        u'suppressed': False,
        u'suppressionState': {u'type': 0}},
        u'type': 134,
        u'typeName': u'BTMFeature'}
d["feature"] = alf
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["feature"]["message"]["parameters"][0]["message"]["expression"] = unicode(str(sort_lengths[0]) + " in")

auto = c.add_feature(did, wid, eid, d)
autolayout = auto.json()


# get parts feature of laser joint + auto layout
parts = c.get_parts(did, wid)
p = parts.json()
allLasers = []
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    allLasers.append(body["bodies"])

# suppress all of the laser joints
features = c.get_features(did, wid, eid)
f = features.json()

partquery = []
updates = []
for i in range(len(f["features"])):
    if f["features"][i]["message"]["featureType"] == "laserJoint":
        f["features"][i]["message"]["suppressed"] = True
        partquery.append([f["features"][i]["message"]["parameters"][1]["message"]["queries"], 
                          f["features"][i]["message"]["parameters"][2]["message"]["queries"], 
                          f["features"][i]["message"]["parameters"][3]["message"]["queries"]])
        updates.append(f["features"][i])
d = dict()
d["features"] = updates
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)

# get the body details after adding in the autolayout feature
parts = c.get_parts(did, wid)
p = parts.json()
body_list = []
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    body_list.append(body["bodies"])

#change viewbox if need to
# make the metadata
doc = ET.Element('svg', style="fill:none;stroke:#ff0000;stroke-linejoin:round;stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5", viewBox="0 0 600 480", xmlns="http://www.w3.org/2000/svg")

meta = dict()
meta["attrib"] = {"style" : "fill:none;stroke:#ff0000;stroke-linejoin:round;stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5", "viewBox" : "0 0 600 400", "xmlns" : "http://www.w3.org/2000/svg"}
meta["joints"] = dict()

for laserCounter in range(len(updates)):
    # unsuppress the laser joint
    features = c.get_features(did, wid, eid)
    f = features.json()

    laseri = updates[laserCounter]
    laseri["message"]["suppressed"] = False
    laseri["message"]["parameters"][1]["message"]["queries"] = partquery[laserCounter][0]
    laseri["message"]["parameters"][2]["message"]["queries"] = partquery[laserCounter][1]
    laseri["message"]["parameters"][3]["message"]["queries"] = partquery[laserCounter][2]
    d = dict()
    d["features"] = [laseri]
    d["serializationVersion"] = f["serializationVersion"]
    d["sourceMicroversion"] = f["sourceMicroversion"]
    d["updateSuppressionAttributes"] = True
    c.update_feature(did, wid, eid, d)

    # do everything for one laser joint between two parts
    #
    #
    # get the body details of one laser joint
    parts = c.get_parts(did, wid)
    p = parts.json()
    oneLaser = []
    for part in p:
        pid = part["partId"]
        body = c.get_body_details(did, wid, eid, pid)
        body = body.json()
        oneLaser.append(body["bodies"])

    # supress the laser joint
    features = c.get_features(did, wid, eid)
    f = features.json()

    laseri = updates[laserCounter]
    laseri["message"]["suppressed"] = True
    d = dict()
    d["features"] = [laseri]
    d["serializationVersion"] = f["serializationVersion"]
    d["sourceMicroversion"] = f["sourceMicroversion"]
    d["updateSuppressionAttributes"] = True
    c.update_feature(did, wid, eid, d)

    # get a list of edges for each body
    edge_list = []
    midpoint_list = []
    vertices_list = []
    for body in body_list:
        face_list = []
        midpoints = []
        vertices = []
        for face in body[0]["faces"]:
            if (abs(face["surface"]["normal"][0]) < epsilon and \
                abs(face["surface"]["normal"][1]) < epsilon and \
                abs(face["surface"]["normal"][2] - 1.0) < epsilon) or \
                (abs(face["surface"]["normal"][0]) < epsilon and \
                abs(face["surface"]["normal"][1]) < epsilon and \
                abs(face["surface"]["normal"][2] + 1.0) < epsilon):
                coedges = face["loops"][0]["coedges"]
                for edge in coedges:
                    edgeId = edge["edgeId"]
                    for e in body[0]["edges"]:
                        if e["id"] == edgeId:
                            arr1 = np.around(np.array(e["geometry"]["startPoint"][:2]) * constant, 4)
                            arr2 = np.around(np.array(e["geometry"]["endPoint"][:2]) * constant, 4)
                            if edge["orientation"]:
                                face_list.append([arr1, arr2])
                                vertices.append(np.around(np.array(e["geometry"]["startPoint"][:2]) * constant, 4))
                            else:
                                face_list.append([arr2, arr1])
                                vertices.append(np.around(np.array(e["geometry"]["endPoint"][:2]) * constant, 4))
                            midpoints.append(np.around(np.array(e["geometry"]["midPoint"][:2]) * constant, 4))
                break
        midpoint_list.append(midpoints)
        edge_list.append(face_list)
        vertices_list.append(vertices)

    # now we have a list of edges for each body
    # need to get coordinates for each 

    coords_list = []
    for i in range(len(edge_list)):
        body = body_list[i]
        edges = edge_list[i]
        if len(edges) == 0:
            continue
        order_coords = [edges[0]]
        for j in range(len(edges)):
            for k in range(len(edges)):
                if np.allclose(order_coords[j][1], edges[k][0]):
                    order_coords.append(edges[k])
                    continue
        coords_list.append(order_coords[:len(order_coords) - 1])

    i = 0
    for body in oneLaser:
        for face in body[0]["faces"]:
            if (abs(face["surface"]["normal"][0]) < epsilon and \
                abs(face["surface"]["normal"][1]) < epsilon and \
                abs(face["surface"]["normal"][2] - 1.0) < epsilon) or \
                (abs(face["surface"]["normal"][0]) < epsilon and \
                abs(face["surface"]["normal"][1]) < epsilon and \
                abs(face["surface"]["normal"][2] + 1.0) < epsilon):
                coedges = face["loops"][0]["coedges"]
                for edge in coedges:
                    edgeId = edge["edgeId"]
                    for e in body[0]["edges"]:
                        if e["id"] == edgeId:
                            mid = np.around(np.array(e["geometry"]["midPoint"][:2]) * constant, 4)
                            start = np.around(np.array(e["geometry"]["startPoint"][:2]) * constant, 4)
                            for j in range(len(midpoint_list[i])):
                                mids = midpoint_list[i][j]
                                if abs(mid[0] - mids[0]) < epsilon and abs(mid[1] - mids[1]) < epsilon:
                                    midpoint_list[i].pop(j)
                                    break
                            for j in range(len(vertices_list[i])):
                                vert = vertices_list[i][j]
                                if abs(start[0] - vert[0]) < epsilon and abs(start[1] - vert[1]) < epsilon:
                                    vertices_list[i].pop(j)
                                    break
        i += 1

    counter = 1
    length = 0
    meta["joints"]["Joint" + str(laserCounter + 1)] = dict()
    for i in range(len(coords_list)):
        coords = coords_list[i]
        (a,b) = coords[0][0]
        face = "face" + str(i+1)
        edge = "M " + str(a) + "," + str(b) + " "
        for j in range(1,len(coords) + 1):
            (a,b) = coords[j % len(coords)][0]
            ej = edge + "L " + str(a) + "," + str(b)
            edge = "M " + str(a) + "," + str(b) + " "

            # midpoint check
            mid = np.around((coords[j-1][0] + coords[j-1][1]) / 2, 4)
            if (len(midpoint_list[i]) == 1):
                mids = midpoint_list[i][0]
                if abs(mid[0] - mids[0]) < epsilon and abs(mid[1] - mids[1]) < epsilon:
                    meta["joints"]["Joint" + str(laserCounter + 1)]["edge_" + chr(i + 97)] = {"d" : ej, "edge" : counter, "face" : face}
            elif (len(vertices_list[i]) == 2):
                mids = np.around((vertices_list[i][0] + vertices_list[i][1]) / 2, 4)
                if abs(mid[0] - mids[0]) < epsilon and abs(mid[1] - mids[1]) < epsilon:
                    meta["joints"]["Joint" + str(laserCounter + 1)]["edge_" + chr(i + 97)] = {"d" : ej, "edge" : counter, "face" : face}
                    length = np.linalg.norm(vertices_list[i][1] - coords[i][0])
            counter += 1

    tabnum = int((str(updates[laserCounter]["message"]["parameters"][4]["message"]["expression"])))
    meta["joints"]["Joint" + str(laserCounter + 1)]["joint_parameters"] = {"joint_type": "Box",
                                                "joint_align": "Inside",
                                                "fit": "Clearance",
                                                "tabsize": length / (2 * tabnum - 1),
                                                "tabspace": length / (2 * tabnum - 1),
                                                "tabnum": tabnum - 1,
                                                "boltsize": "M0",
                                                "boltspace": 0,
                                                "boltnum": 0,
                                                "boltlength": 0}


# get a list of edges for each body
edge_list = []
midpoint_list = []
vertices_list = []
for body in body_list:
    face_list = []
    midpoints = []
    vertices = []
    for face in body[0]["faces"]:
        if (abs(face["surface"]["normal"][0]) < epsilon and \
            abs(face["surface"]["normal"][1]) < epsilon and \
            abs(face["surface"]["normal"][2] - 1.0) < epsilon) or \
            (abs(face["surface"]["normal"][0]) < epsilon and \
            abs(face["surface"]["normal"][1]) < epsilon and \
            abs(face["surface"]["normal"][2] + 1.0) < epsilon):
            coedges = face["loops"][0]["coedges"]
            for edge in coedges:
                edgeId = edge["edgeId"]
                for e in body[0]["edges"]:
                    if e["id"] == edgeId:
                        arr1 = np.around(np.array(e["geometry"]["startPoint"][:2]) * constant, 4)
                        arr2 = np.around(np.array(e["geometry"]["endPoint"][:2]) * constant, 4)
                        if edge["orientation"]:
                            face_list.append([arr1, arr2])
                            vertices.append(np.around(np.array(e["geometry"]["startPoint"][:2]) * constant, 4))
                        else:
                            face_list.append([arr2, arr1])
                            vertices.append(np.around(np.array(e["geometry"]["endPoint"][:2]) * constant, 4))
                        midpoints.append(np.around(np.array(e["geometry"]["midPoint"][:2]) * constant, 4))
            break
    midpoint_list.append(midpoints)
    edge_list.append(face_list)
    vertices_list.append(vertices)

# now we have a list of edges for each body
# need to get coordinates for each 

coords_list = []
for i in range(len(edge_list)):
    body = body_list[i]
    edges = edge_list[i]
    if len(edges) == 0:
        continue
    order_coords = [edges[0]]
    for j in range(len(edges)):
        for k in range(len(edges)):
            if np.allclose(order_coords[j][1], edges[k][0]):
                order_coords.append(edges[k])
                continue
    coords_list.append(order_coords[:len(order_coords) - 1])

counter = 1
edges = []
meta["tree"] = dict() 
for i in range(len(coords_list)):
    coords = coords_list[i]
    (a,b) = coords[0][0]
    face = "face" + str(i+1)
    meta["tree"][face] = dict()
    path = "M " + str(a) + "," + str(b) + " "
    edge = path
    for j in range(1,len(coords) + 1):
        (a,b) = coords[j % len(coords)][0]
        path += "L " + str(a) + "," + str(b) + " "
        ej = edge + "L " + str(a) + "," + str(b)
        edge = "M " + str(a) + "," + str(b) + " "
        edges.append({"d" : ej, "edge" : counter, "face": face})
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
meta["edge_data"]["viewBox"] = "0 0 600 400"
meta["joint_index"] = 0




metaTree = ET.SubElement(doc, "metadata")
laser = ET.SubElement(metaTree, "laserassistant")
laser.attrib["model"] = str(meta).replace("\'", "\"")

svg = open('1.svg', 'w')
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

# delete autolayout

fid = autolayout["feature"]["message"]["featureId"]
c.delete_feature(did, wid, eid, fid)



