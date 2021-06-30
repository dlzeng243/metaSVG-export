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

did = "b3ea79d344251df6495836cc"
wid = "37bdc8e4d3b079cb2acffc8d"
eid = "f5ad63f423a46fabd7ae042d"
'''
did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"
'''
features = c.get_features(did, wid, eid)
f = features.json()
pprint.pprint(f)

print("\n")

parts = c.get_parts(did, wid)
p = parts.json()
pprint.pprint(p)

for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    pprint.pprint(body)