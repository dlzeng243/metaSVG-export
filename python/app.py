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

# get the body details
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
        for k in range(len(edges)):
            if np.array_equal(order_coords[j][1], edges[k][0]):
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
features = c.get_features(did, wid, eid)
f = features.json()
f["features"][4]["message"]["suppressed"] = True
asdf = []
asdf.append(f["features"][4])
d = dict()
d["features"] = asdf
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)'''


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


questions:
is it safe to assume that the "height" of all the parts will be the same - so when they laser cut, it'll be uniform?
'''