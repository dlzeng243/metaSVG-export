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
did = "8340450a9fd4cc9837a89656"
wid = "d01511894f7b5682a854cff1"
eid = "7394a48da4001f45b67489f8"
'''
'''
did = "d934491f87de847f2d4bccac"
wid = "2abe57ce0ac3f5cbe20ee001"
eid = "54bf2b3c2414d066af55dcec"
'''
'''
did = "b3ea79d344251df6495836cc"
wid = "37bdc8e4d3b079cb2acffc8d"
eid = "f5ad63f423a46fabd7ae042d"
'''
'''
did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"
'''
'''
did = "e163a13cdcf203350a1a1ce2"
wid = "50030d897bfa683e0da3be9a"
eid = "bd80ff440cc33e6e73cdfc32"
'''

# raspberry pi


did = "939592630e92d28997eb29da"
wid = "3ce34ba3e44b5d34438378b5"
eid = "93d44db90466c59ec8203929"

features = c.get_features(did, wid, eid)
f = features.json()
pprint.pprint(f)
'''
sketch = c.get_sketch(did, wid, eid)
pprint.pprint(sketch.json())
'''

parts = c.get_parts(did, wid)
p = parts.json()


for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    pprint.pprint(body)