'''
app
===

Demos basic usage of the Onshape API
'''

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
did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"

# get the document details
# details = c.get_document(did)
# print 'Document name: ' + details.json()['name']
parts = c.get_parts(did, wid)
p = parts.json()
for part in p:
    eid = part["elementId"]
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    pprint.pprint(body.json())


dwg = svgwrite.Drawing('test.svg', profile='tiny')
dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 0.2)))
dwg.save()


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

