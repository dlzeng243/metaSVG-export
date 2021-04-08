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
All parts will be the same height (because laser cutting the same material)
All parts will be polygonal
Intersection between base and tab will be a "good fit" (meaning the side lengths will match up)
one laser joint feature for now

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
https://forum.onshape.com/discussion/7544/execute-featurescript-using-api-and-python'''



from apikey.client import Client
import pprint
import numpy as np
import svgwrite


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

did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"
'''

did = "a793a3e438b3a8a7859e3244"
wid = "d66b8b4a9bb905cb4090461b"
eid = "bdaa56060d3b9fbbd545f5e7"
'''

features = c.get_features(did, wid, eid)
f = features.json()

# suppress all of the laser joints
features = c.get_features(did, wid, eid)
f = features.json()
lasers = []
for i in range(len(f["features"])):
    if f["features"][i]["message"]["featureType"] == "laserJoint":
        lasers.append(i)
updates = []
for i in range(len(lasers)):
    f["features"][lasers[i]]["message"]["suppressed"] = True
    updates.append(f["features"][lasers[i]])
d = dict()
d["features"] = updates
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)

# get the body details to find length to autolayout
parts = c.get_parts(did, wid)
p = parts.json()
body_list = []
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    body_list.append(body["bodies"])

# Add autolayout feature with specified length
d = dict()
alf = {u'message': {u'featureType': u'autolayout',
        u'hasUserCode': False,
        u'name': u'Auto Layout 1',
        u'namespace': u'df0ea3e290860f984f4075197::vc2e512d1951a9eda143a5a40::e43c995e59341bb62975a36b8::m487f3f81e149ec9cd19f43e7',
        u'parameters': [{u'message': {u'expression': u'0.12 in',
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
val = 0.3
d["feature"] = alf
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["feature"]["message"]["parameters"][0]["message"]["expression"] = unicode(str(val) + " in")

c.add_feature(did, wid, eid, d)


# get the body details after adding in the autolayout feature
parts = c.get_parts(did, wid)
p = parts.json()
body_list = []
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    body_list.append(body["bodies"])

# get a list of edges for each body
edge_list = []
for body in body_list:
    face_list = []
    for face in body[0]["faces"]:
        if face["surface"]["normal"] == [0.0, 0.0, 1.0] or face["surface"]["normal"] == [0.0, 0.0, -1.0]:
            coedges = face["loops"][0]["coedges"]
            for edge in coedges:
                edgeId = edge["edgeId"]
                for e in body[0]["edges"]:
                    if e["id"] == edgeId:
                        if edge["orientation"]:
                            face_list.append([np.array(e["geometry"]["startPoint"][:2]) * 39.3701, np.array(e["geometry"]["endPoint"][:2]) * 39.3701])
                        else:
                            face_list.append([np.array(e["geometry"]["endPoint"][:2]) * 39.3701, np.array(e["geometry"]["startPoint"][:2]) * 39.3701])
            break
    edge_list.append(face_list)

# now we have a list of edges for each body
# need to get coordinates for each 

coords_list = []
for i in range(len(edge_list)):
    body = body_list[i]
    edges = edge_list[i]
    order_coords = [edges[0]]
    for j in range(len(edges)):
        print(order_coords[j])
        for k in range(len(edges)):
            print(edges[k])
            if np.allclose(order_coords[j][1], edges[k][0]):
                order_coords.append(edges[k])
                continue
    coords_list.append(order_coords[:len(order_coords) - 1])
'''
for i in range(len(coords_list)):
    for j in range(len(coords_list[i])):
        print("start " + str(coords_list[i][j][0]) + " end " + str(coords_list[i][j][1]) + "\n")'''

dwg = svgwrite.Drawing('test.svg', profile='tiny')
for i in range(len(coords_list)):
    coords = coords_list[i]
    (a,b) = coords[0][0]
    path = "M " + str(a) + "," + str(b) + " "
    for j in range(1,len(coords) + 1):
        (a,b) = coords[j % len(coords)][0]
        path += "L " + str(a) + "," + str(b) + " "
    path += "z"
    print(path)
    dwg.add(dwg.path(path, stroke="#000", fill="none", stroke_width=0.01))
dwg.save()

# coords = [(np.array([1,2]), np.array([1,4])), (np.array([1,4]), np.array([3,4])), (np.array([3,2]), np.array([1,2])), (np.array([3,4]), np.array([3,2]))]





'''
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

questions:
is it safe to assume that the "height" of all the parts will be the same - so when they laser cut, it'll be uniform?
    will be one of the assumptions im using (might change later)

extract_metadata -> look at the metadata format
'''
