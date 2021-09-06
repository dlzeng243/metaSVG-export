from apikey.client import Client
from collections import Counter
import pprint
import numpy as np
import xml.etree.ElementTree as ET
import json
import sys

epsilon = 0.00001
constant = 1000.0

# Jim's perpendicular function
def perpendicular(n):
    p = np.zeros(3)
    # set p to a vector that *definitely isn't parallel* to n:
    if (abs(n[0]) < abs(n[1]) and abs(n[0]) < abs(n[2])):
        p = np.array([1, 0, 0])
    elif (abs(n[1]) < abs(n[2])):
        p = np.array([0, 1, 0])
    else:
        p = np.array([0, 0, 1])
    # make p actually perpendicular (vec is nonzero):
    vec = p - np.dot(p, n) * n
    p = vec / np.linalg.norm(vec)
    return p

def circlePath(cx, cy, r):
    return 'M ' + str(cx) + ' ' + str(cy) + ' m -' + str(r) + ', 0 a ' + str(r) + ',' + str(r) + ' 0 1,0 ' + str(r*2) + ',0 a ' + str(r) + ','+ str(r) + ' 0 1,0 -' + str(2 * r) + ',0'

def toNumpyArray(dic, id, s):
    if s == "start":
        startx = round(dic[id]["geometry"]["startPoint"][0], 8)
        starty = round(dic[id]["geometry"]["startPoint"][1], 8)
        startz = round(dic[id]["geometry"]["startPoint"][2], 8)
        return np.array([startx,starty,startz])

    endx = round(dic[id]["geometry"]["endPoint"][0], 8)
    endy = round(dic[id]["geometry"]["endPoint"][1], 8)
    endz = round(dic[id]["geometry"]["endPoint"][2], 8)
    return np.array([endx,endy,endz])

''' Convert expression to millimeters'''
def readUnits(s):
    string = s.split()
    units = string[len(string) - 1]
    if units == "in" or units == "inches":
        return float(string[0]) * 25.4 / 1000.0
    elif units == "mm" or units == "millimeter":
        return float(string[0])
    elif units == "m" or units == "meter":
        return float(string[0]) / 1000.0
    elif units == "cm" or units == "centimeter":
        return float(string[0]) / 10.0
    return -1.0

def unsuppress(box, tslot, tas, slotted, part_box, part_tslot, part_tas, part_slotted):
    features = c.get_features(did, wid, eid)
    f = features.json()

    for i in range(len(box)):
        # unsuppress the laser joint
        laseri = box[i]
        laseri["message"]["suppressed"] = False
        laseri["message"]["parameters"][1]["message"]["queries"] = part_box[i][0]
        laseri["message"]["parameters"][2]["message"]["queries"] = part_box[i][1]
        laseri["message"]["parameters"][3]["message"]["queries"] = part_box[i][2]

    for i in range(len(tslot)):
        # unsuppress the laser joint
        laseri = tslot[i]
        laseri["message"]["suppressed"] = False
        laseri["message"]["parameters"][0]["message"]["queries"] = part_tslot[i][0]
        laseri["message"]["parameters"][1]["message"]["queries"] = part_tslot[i][1]
        laseri["message"]["parameters"][2]["message"]["queries"] = part_tslot[i][2]
        laseri["message"]["parameters"][3]["message"]["queries"] = part_tslot[i][3]
        laseri["message"]["parameters"][4]["message"]["queries"] = part_tslot[i][4]

    for i in range(len(tas)):
        laseri = tas[i]
        laseri["message"]["suppressed"] = False
        laseri["message"]["parameters"][0]["message"]["queries"] = part_tas[i][0]
        laseri["message"]["parameters"][1]["message"]["queries"] = part_tas[i][1]
        laseri["message"]["parameters"][2]["message"]["queries"] = part_tas[i][2]

    for i in range(len(slotted)):
        laseri = slotted[i]
        laseri["message"]["suppressed"] = False
        laseri["message"]["parameters"][0]["message"]["queries"] = part_slotted[i][0]
        laseri["message"]["parameters"][1]["message"]["queries"] = part_slotted[i][1]
        laseri["message"]["parameters"][2]["message"]["queries"] = part_slotted[i][2]
        laseri["message"]["parameters"][3]["message"]["queries"] = part_slotted[i][3]
        laseri["message"]["parameters"][4]["message"]["queries"] = part_slotted[i][4]
        laseri["message"]["parameters"][5]["message"]["queries"] = part_slotted[i][5]


    d = dict()
    d["features"] = box + tslot + tas + slotted
    d["serializationVersion"] = f["serializationVersion"]
    d["sourceMicroversion"] = f["sourceMicroversion"]
    d["updateSuppressionAttributes"] = True
    c.update_feature(did, wid, eid, d)

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
# 1
did = "342cee7fe5c2effe369c8dc3"
wid = "1362f0d767136d7d96f8c33a"
eid = "7d2020bde3f6f951e141da13"
'''

# harder box
'''
did = "b3ea79d344251df6495836cc"
wid = "37bdc8e4d3b079cb2acffc8d"
eid = "f5ad63f423a46fabd7ae042d"
'''

# tilt
'''
did = "34f358b08844ead297ba74f6"
wid = "275579ddc140dfe00b49da5e"
eid = "745d66adff6ff8d563831f69"
'''

# tab and slot
'''
did = "8340450a9fd4cc9837a89656"
wid = "d01511894f7b5682a854cff1"
eid = "7394a48da4001f45b67489f8"
'''

# slotted
'''
did = "d934491f87de847f2d4bccac"
wid = "2abe57ce0ac3f5cbe20ee001"
eid = "54bf2b3c2414d066af55dcec"
'''
# nur box
'''
did = "b9e234f251a607d0d9ce0e9a"
wid = "c45c28f23e25a36988322572"
eid = "960e4e2c57080fe58395912f"
'''
# nur tslot box
'''
did = "e163a13cdcf203350a1a1ce2"
wid = "50030d897bfa683e0da3be9a"
eid = "bd80ff440cc33e6e73cdfc32"
'''

# bird house
'''
did = "939592630e92d28997eb29da"
wid = "3ce34ba3e44b5d34438378b5"
eid = "93d44db90466c59ec8203929"
'''

# chair
'''
did = "3b2c4abe65815a81dc709aa8"
wid = "97f88956c7d4edca883aa894"
eid = "56e319b635b4794492166d23"
'''

# raspberry pi

'''
did = "2583e97f0a333a38d03fc29e"
wid = "eb85696d78b9ca148a08977d"
eid = "2a7422c47555a3ece3c994f1"
'''
# printer
'''
did = "a7c63a8b20c4b911aa9ee0dd"
wid = "0ff2f9dda8a0ccfbf9ba7679"
eid = "b01cb8d18f450ea6f16185b8"
'''
# octogonal candle holder
'''
did = "da1045b9fbea9a5b3b6516c8"
wid = "33af49ef094546773e9a5e40"
eid = "a87ebba31cd6f918db244ce9"
'''
# house
'''
did = "cb694ed0b30f8354559273f1"
wid = "733bb59e3d32dfa30a2e47c9"
eid = "3616eb0cf82bed75c4f40e6e"
'''

# arcade
'''
did = "0ada0244726dbd2eccf605c4"
wid = "74af87e822132b87fad407ce"
eid = "4a428daee5c62a5644aef745"
'''

# laptop
'''
did = "4553f9339af206c9dbac6b64"
wid = "597b7587765e8d04f6a1b00e"
eid = "197ab26790f10eddbd774050"
'''
# windmill
'''
did = "029851f598e19e5b49784a9b"
wid = "a902a5bd9d5432b35d9b372c"
eid = "2a77759f7830e9bad303a87b"

'''
# dice
'''
did = "0fc385d7050f56bc9a1adae3"
wid = "63eddd978595af3059316e76"
eid = "c3a9b1ec7ac169d26c478ced"
'''

# tray
'''
did = "b50e40745ce6ce567e69c657"
wid = "85237d35c764cbc9b835ef62"
eid = "6868d15c5e6449716872430e"
'''


# tests
did = "175191ecf6dfd33fc82e76eb"
wid = "4b3b42dc77a0a6698a0372c5"
eid = "843560ba2c50135fa96a61ec"

features = c.get_features(did, wid, eid)
f = features.json()
pprint.pprint(f)

# box joint info
boxIDS = []
updatesBox = []
partQueryBox = []

# t slot joint info
tSlotIDS = []
updatesTSlot = []
partQueryT = []

# tab and slot joint info
tabAndSlotIDS = []
updatesTAS = []
partQueryTAS = []

# slotted joint info
slotIDS = []
updatesSlot = []
partQuerySlot = []

for i in range(len(f["features"])):
    if f["features"][i]["message"]["suppressed"] == False:
        if f["features"][i]["message"]["featureType"] == "laserJoint":
            updatesBox.append(f["features"][i])
            partQueryBox.append([f["features"][i]["message"]["parameters"][1]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][2]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][3]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][4]["message"]["queries"]])
            ids = []
            if f["features"][i]["message"]["parameters"][1]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][1]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][2]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][2]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][3]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][3]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][4]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][4]["message"]["queries"][0]["message"]["geometryIds"]
            if not ids or len(ids) != 4:
                print(ids)
                pprint.pprint(f["features"][i])
                print("Not proper LaserJoint1 \n")
                sys.exit()
            boxIDS.append(ids)
            f["features"][i]["message"]["suppressed"] = True
        elif f["features"][i]["message"]["featureType"] == "tSlotJoint":
            updatesTSlot.append(f["features"][i])
            partQueryT.append([f["features"][i]["message"]["parameters"][0]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][1]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][2]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][3]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][4]["message"]["queries"]])
            ids = []
            if f["features"][i]["message"]["parameters"][0]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][0]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][1]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][1]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][2]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][2]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][3]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][3]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][4]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][4]["message"]["queries"][0]["message"]["geometryIds"]
            if not ids or len(ids) != 5:
                print("Not proper tSlotJoint1 \n")
                sys.exit()
            tSlotIDS.append(ids)
            f["features"][i]["message"]["suppressed"] = True
        elif f["features"][i]["message"]["featureType"] == "tabAndSlot":
            updatesTAS.append(f["features"][i])
            partQueryTAS.append([f["features"][i]["message"]["parameters"][0]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][1]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][2]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][3]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][4]["message"]["queries"]])
            ids = []
            if f["features"][i]["message"]["parameters"][0]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][0]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][1]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][1]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][2]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][2]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][3]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][3]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][4]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][4]["message"]["queries"][0]["message"]["geometryIds"]
            if not ids or len(ids) != 5:
                print("Not proper TabAndSlotJoint1 \n")
                sys.exit()
            tabAndSlotIDS.append(ids)
            f["features"][i]["message"]["suppressed"] = True

d = dict()
d["features"] = updatesBox + updatesTSlot + updatesTAS
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)

# slotted joint info
slotIDS = []
updatesSlot = []
partQuerySlot = []

# slots only
features = c.get_features(did, wid, eid)
f = features.json()

for i in range(len(f["features"])):
    if f["features"][i]["message"]["suppressed"] == False:
        if f["features"][i]["message"]["featureType"] == "slot":
            updatesSlot.append(f["features"][i])
            partQuerySlot.append([f["features"][i]["message"]["parameters"][0]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][1]["message"]["queries"], 
                            f["features"][i]["message"]["parameters"][2]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][3]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][4]["message"]["queries"],
                            f["features"][i]["message"]["parameters"][5]["message"]["queries"]])
            ids = []
            if f["features"][i]["message"]["parameters"][0]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][0]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][1]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][1]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][2]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][2]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][3]["message"]["queries"]:
                ids += f["features"][i]["message"]["parameters"][3]["message"]["queries"][0]["message"]["geometryIds"]
            if f["features"][i]["message"]["parameters"][4]["message"]["queries"]:
                ids.append([f["features"][i]["message"]["parameters"][4]["message"]["queries"][0]["message"]["geometryIds"][0],
                            f["features"][i]["message"]["parameters"][4]["message"]["queries"][1]["message"]["geometryIds"][0]])
            if f["features"][i]["message"]["parameters"][5]["message"]["queries"]:
                ids.append([f["features"][i]["message"]["parameters"][5]["message"]["queries"][0]["message"]["geometryIds"][0],
                            f["features"][i]["message"]["parameters"][5]["message"]["queries"][1]["message"]["geometryIds"][0]])
            if not ids or len(ids) != 6:
                print("Not proper Slotted1 \n")
                print(ids)
                unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])
                sys.exit()
            slotIDS.append(ids)
            f["features"][i]["message"]["suppressed"] = True
print(slotIDS)
d = dict()
d["features"] = updatesSlot
d["serializationVersion"] = f["serializationVersion"]
d["sourceMicroversion"] = f["sourceMicroversion"]
d["updateSuppressionAttributes"] = True
c.update_feature(did, wid, eid, d)


'''
ASSUME ONLY TAB AND BASE FOR LASERJOINT
ONlY ONE FACE FOR TSLOTJOINT
'''

parts = c.get_parts(did, wid)
p = parts.json()
map_parts = dict()
map_edges = dict()
counter = 0
numEdges = 0
offsetx = round(10.0 / constant, 8)
offsety = 0.0
faceDict = dict()

# sets up data structures
for part in p:
    pid = part["partId"]
    body = c.get_body_details(did, wid, eid, pid)
    body = body.json()
    area = -1
    # due to how laserjoint is coded, max of 2 faces with same area
    twodicts = [dict(), dict()]
    index = 0
    maxx = 0

    edgedict = dict()
    for i in range(len(body["bodies"][0]["edges"])):
        edgedict[body["bodies"][0]["edges"][i]["id"]] = body["bodies"][0]["edges"][i]
    for i in range(len(body["bodies"][0]["faces"])):
        faceDict[body["bodies"][0]["faces"][i]["id"]] = dict()
        faceDict[body["bodies"][0]["faces"][i]["id"]]["pid"] = pid
        faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"] = []
        faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"] = []
        if body["bodies"][0]["faces"][i]["surface"]["type"] == "plane":
            x = round(body["bodies"][0]["faces"][i]["surface"]["normal"][0], 8)
            y = round(body["bodies"][0]["faces"][i]["surface"]["normal"][1], 8)
            z = round(body["bodies"][0]["faces"][i]["surface"]["normal"][2], 8)
            perp = perpendicular(np.array([x, y, z]))
            perp2 = np.cross(perp, np.array([x, y, z]))
            perp2 = perp2 / np.linalg.norm(perp2)
            for k in range(len(body["bodies"][0]["faces"][i]["loops"])):
                curve = body["bodies"][0]["faces"][i]["loops"][k]
                # boundary
                if curve["type"] == "outer":
                    for j in range(len(curve["coedges"])):
                        edgeId = curve["coedges"][j]["edgeId"]
                        orientation = curve["coedges"][j]["orientation"]
                        
                        start = toNumpyArray(edgedict, edgeId, "start")
                        svgstart = np.array([np.dot(start, perp2), np.dot(start, perp)])
                        end = toNumpyArray(edgedict, edgeId, "end")
                        svgend = np.array([np.dot(end, perp2), np.dot(end, perp)])
                        if orientation:
                            faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"].append([start, end])
                            faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"].append([svgstart, svgend])
                        else:
                            faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"].append([end, start])
                            faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"].append([svgend, svgstart])
            sum0 = 0
            for j in range(len(faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"])):
                sum0 += (faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][j][1][0] - faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][j][0][0]) * (faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][j][1][1] + faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][j][0][1])
            if sum0 > 0:
                for j in range(len(faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"])):
                    list.reverse(faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"][j])
                    list.reverse(faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][j])
                faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][1:] = faceDict[body["bodies"][0]["faces"][i]["id"]]["2d_edges"][1:][::-1]
                faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"][1:] = faceDict[body["bodies"][0]["faces"][i]["id"]]["edges"][1:][::-1]
        area = max(area, body["bodies"][0]["faces"][i]["area"])
    for i in range(len(body["bodies"][0]["faces"])):
        if abs(area - body["bodies"][0]["faces"][i]["area"]) < epsilon:
            x = round(body["bodies"][0]["faces"][i]["surface"]["normal"][0], 8)
            y = round(body["bodies"][0]["faces"][i]["surface"]["normal"][1], 8)
            z = round(body["bodies"][0]["faces"][i]["surface"]["normal"][2], 8)

            n = np.array([x, y, z])
            if body["bodies"][0]["faces"][i]["orientation"]:
                twodicts[index]["normal"] = n / np.linalg.norm(n)
            else:
                twodicts[index]["normal"] = -1 * (n / np.linalg.norm(n))
            perp = perpendicular(np.array([x, y, z]))
            perp2 = np.cross(perp, np.array([x, y, z]))
            perp2 = perp2 / np.linalg.norm(perp2)
            twodicts[index]["edges"] = []
            twodicts[index]["2d_edges"] = []
            twodicts[index]["id"] = counter
            cuts = []
            for k in range(len(body["bodies"][0]["faces"][i]["loops"])):
                curve = body["bodies"][0]["faces"][i]["loops"][k]
                coordscut = []
                svgpath = ""
                cutdict = dict()
                # boundary
                if curve["type"] == "outer":
                    for j in range(len(curve["coedges"])):
                        edgeId = curve["coedges"][j]["edgeId"]
                        orientation = curve["coedges"][j]["orientation"]

                        start = toNumpyArray(edgedict, edgeId, "start")
                        svgstart = np.array([np.dot(start, perp2), np.dot(start, perp)])
                        end = toNumpyArray(edgedict, edgeId, "end")
                        svgend = np.array([np.dot(end, perp2), np.dot(end, perp)])
                        
                        if orientation:
                            twodicts[index]["edges"].append([start, end])
                            twodicts[index]["2d_edges"].append([svgstart, svgend])
                        else:
                            twodicts[index]["edges"].append([end, start])
                            twodicts[index]["2d_edges"].append([svgend, svgstart])
                # circle/ellipse cut
                elif len(curve["coedges"]) == 1:
                    edgeId = curve["coedges"][0]["edgeId"]
                    arc = edgedict[edgeId]
                    if arc["curve"]["type"] == "circle":
                        radius = round(arc["curve"]["radius"] * constant, 8)
                        svgpath = ""
                        cutdict["radius"] = radius
                        cutdict["name"] = "circle"
                    '''
                    else:
                        major = str(round(arc["curve"]["majorRadius"] * constant, 8))
                        minor = str(round(arc["curve"]["minorRadius"] * constant, 8))
                        angle = np.array(arc["curve"]["majorAxis"])
                        angle /= np.linalg.norm(angle)
                        angle = np.arccos(np.dot(angle, perp2))
                        cutdict["major"] = major
                        cutdict["minor"] = minor
                        cutdict["angle"] = angle
                        svgpath = ""
                        cutdict["name"] = "ellipse"
                    '''
                    centerx = round(arc["curve"]["origin"][0], 8)
                    centery = round(arc["curve"]["origin"][1], 8)
                    centerz = round(arc["curve"]["origin"][2], 8)
                    center = np.array([centerx,centery,centerz])
                    center = np.array([np.dot(center, perp2), np.dot(center, perp)])
                    coordscut.append([center, center])
                    cutdict["path"] = svgpath
                    cutdict["coords"] = coordscut
                # polygonal cut
                else:
                    svgpath = "M "
                    for j in range(len(curve["coedges"])):
                        edgeId = curve["coedges"][j]["edgeId"]
                        orientation = curve["coedges"][j]["orientation"]

                        start = toNumpyArray(edgedict, edgeId, "start")
                        svgstart = np.array([np.dot(start, perp2), np.dot(start, perp)])
                        end = toNumpyArray(edgedict, edgeId, "end")
                        svgend = np.array([np.dot(end, perp2), np.dot(end, perp)])
                        
                        if orientation:
                            coordscut.append([svgstart, svgend])
                        else:
                            coordscut.append([svgend, svgstart])
                        cutdict["name"] = "polygon"
                        cutdict["path"] = svgpath
                        cutdict["coords"] = coordscut
                if cutdict:
                    cuts.append(cutdict)
            boxx = float("inf")
            boxy = float("inf")
            for i in range(len(twodicts[index]["2d_edges"])):
                boxx = min(boxx, twodicts[index]["2d_edges"][i][0][0])
                boxy = min(boxy, twodicts[index]["2d_edges"][i][0][1])
            for i in range(len(twodicts[index]["2d_edges"])):
                twodicts[index]["2d_edges"][i][0] -= np.array([boxx, boxy])
                twodicts[index]["2d_edges"][i][1] -= np.array([boxx, boxy])
                maxx = max(maxx, twodicts[index]["2d_edges"][i][0][0])
                offsety = max(offsety, twodicts[index]["2d_edges"][i][0][1])
                twodicts[index]["2d_edges"][i][0] += np.array([offsetx, round(10.0 / constant, 8)])
                twodicts[index]["2d_edges"][i][1] += np.array([offsetx, round(10.0 / constant, 8)])
            for i in range(len(cuts)):
                cutdict = cuts[i]
                coordscut = cutdict["coords"]
                if cutdict["name"] == "circle" or cutdict["name"] == "ellipse":
                    coordscut[0][0] += np.array([offsetx - boxx, round(10.0 / constant, 8) - boxy])
                    cutdict["path"] = circlePath(round(coordscut[0][0][0] * constant, 8), round(coordscut[0][0][1] * constant, 8), cutdict["radius"])
                else:
                    for j in range(len(coordscut)):
                        coordscut[j] += np.array([offsetx - boxx, round(10.0 / constant, 8) - boxy])
                        cutdict["path"] += str(round(coordscut[j][0][0] * constant, 8)) + " " + str(round(coordscut[j][0][1] * constant, 8)) + " L "
                    cutdict["path"] += str(round(coordscut[0][0][0] * constant, 8)) + " " + str(round(coordscut[0][0][1] * constant, 8)) + " "
                cuts[i] = cutdict
            twodicts[index]["orientation"] = body["bodies"][0]["faces"][i]["orientation"]
            twodicts[index]["numEdges"] = numEdges
            twodicts[index]["cuts"] = cuts
            index += 1
    if not twodicts[0] or not twodicts[1]:
        continue
    sum0 = 0

    for i in range(len(twodicts[0]["2d_edges"])):
        sum0 += (twodicts[0]["2d_edges"][i][1][0] - twodicts[0]["2d_edges"][i][0][0]) * (twodicts[0]["2d_edges"][i][1][1] + twodicts[0]["2d_edges"][i][0][1])
    sum1 = 0
    for i in range(len(twodicts[1]["2d_edges"])):
        sum1 += (twodicts[1]["2d_edges"][i][1][0] - twodicts[1]["2d_edges"][i][0][0]) * (twodicts[1]["2d_edges"][i][1][1] + twodicts[1]["2d_edges"][i][0][1])
    print(sum0)
    print(sum1)
    if sum0 > 0:
        for i in range(len(twodicts[0]["edges"])):
            list.reverse(twodicts[0]["edges"][i])
            list.reverse(twodicts[0]["2d_edges"][i])
        twodicts[0]["2d_edges"][1:] = twodicts[0]["2d_edges"][1:][::-1]
        twodicts[0]["edges"][1:] = twodicts[0]["edges"][1:][::-1]

    if sum1 > 0:
        for i in range(len(twodicts[1]["edges"])):
            list.reverse(twodicts[1]["edges"][i])
            list.reverse(twodicts[1]["2d_edges"][i])
        twodicts[1]["2d_edges"][1:] = twodicts[1]["2d_edges"][1:][::-1]
        twodicts[1]["edges"][1:] = twodicts[1]["edges"][1:][::-1]

    offsetx += round(maxx + 50.0 / constant, 8)
    offsety += round(10.0 / constant, 8)
    numEdges += len(twodicts[0]["edges"])
    map_parts[pid] = twodicts
    map_edges[pid] = edgedict
    counter += 1

slotdata = []
for i in range(len(slotIDS)):
    slotdata.append(dict())
    slotdata[i]["baseDist1"] = 0
    slotdata[i]["baseDist2"] = 0 
    slotdata[i]["tabDist1"] = 0 
    slotdata[i]["tabDist2"] = 0
    """ unsuppress slot"""
    features = c.get_features(did, wid, eid)
    f = features.json()
    laseri = updatesSlot[i]
    laseri["message"]["suppressed"] = False
    laseri["message"]["parameters"][0]["message"]["queries"] = partQuerySlot[i][0]
    laseri["message"]["parameters"][1]["message"]["queries"] = partQuerySlot[i][1]
    laseri["message"]["parameters"][2]["message"]["queries"] = partQuerySlot[i][2]
    laseri["message"]["parameters"][3]["message"]["queries"] = partQuerySlot[i][3]
    laseri["message"]["parameters"][4]["message"]["queries"] = partQuerySlot[i][4]
    laseri["message"]["parameters"][5]["message"]["queries"] = partQuerySlot[i][5]

    d = dict()
    d["features"] = updatesSlot
    d["updateSuppressionAttributes"] = True
    c.update_feature(did, wid, eid, d)

    """Get part details"""
    parts = c.get_parts(did, wid)
    p = parts.json()
    tabs = dict()
    bases = dict()
    tabId = slotIDS[i][0]
    tabDict = map_parts[tabId]
    tabNormal = tabDict[0]["normal"]
    baseId = slotIDS[i][1]
    baseDict = map_parts[baseId]
    baseNormal = baseDict[0]["normal"]
    cross = np.cross(tabNormal, baseNormal)
    cross = cross / np.linalg.norm(cross)
    for part in p:
        pid = part["partId"]
        if pid == slotIDS[i][0]:
            body = c.get_body_details(did, wid, eid, pid)
            body = body.json()
            for k in range(2):
                tabEdge = [toNumpyArray(map_edges[tabId], slotIDS[i][4][k], "start"), toNumpyArray(map_edges[tabId], slotIDS[i][4][k], "end")]
                tabSlope = tabEdge[1] - tabEdge[0]
                tabSlope = tabSlope / np.linalg.norm(tabSlope)
                print(tabEdge)
                print(tabSlope)
                print("\n")
                for j in range(len(body["bodies"][0]["edges"])):
                    start = toNumpyArray(body["bodies"][0]["edges"], j, "start")
                    end = toNumpyArray(body["bodies"][0]["edges"], j, "end")
                    slope = end - start
                    slope = slope / np.linalg.norm(slope)
                    print(start)
                    print(end)
                    print(slope)
                    print("\n")

                    if (np.allclose(start, tabEdge[0], epsilon, epsilon) and np.allclose(slope, tabSlope, epsilon, epsilon)):
                        slotdata[i]["tabDist1"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        tabs[2*k + 0] = toNumpyArray(body["bodies"][0]["edges"], j, "end")
                    elif (np.allclose(end, tabEdge[0], epsilon, epsilon) and np.allclose(slope, -tabSlope, epsilon, epsilon)):
                        slotdata[i]["tabDist1"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        tabs[2*k + 0] = toNumpyArray(body["bodies"][0]["edges"], j, "start")
                    if (np.allclose(start, tabEdge[1], epsilon, epsilon) and np.allclose(slope, -tabSlope, epsilon, epsilon)):
                        slotdata[i]["tabDist2"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        tabs[2*k + 1] = toNumpyArray(body["bodies"][0]["edges"], j, "end")
                    elif (np.allclose(end, tabEdge[1], epsilon, epsilon) and np.allclose(slope, tabSlope, epsilon, epsilon)):
                        slotdata[i]["tabDist2"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        tabs[2*k + 1] = toNumpyArray(body["bodies"][0]["edges"], j, "start")

        elif pid == slotIDS[i][1]:
            body = c.get_body_details(did, wid, eid, pid)
            body = body.json()
            for k in range(2):
                baseEdge = [toNumpyArray(map_edges[baseId], slotIDS[i][5][k], "start"), toNumpyArray(map_edges[baseId], slotIDS[i][5][k], "end")]
                baseSlope = baseEdge[1] - baseEdge[0]
                baseSlope = baseSlope / np.linalg.norm(baseSlope)
                for j in range(len(body["bodies"][0]["edges"])):
                    start = toNumpyArray(body["bodies"][0]["edges"], j, "start")
                    end = toNumpyArray(body["bodies"][0]["edges"], j, "end")
                    slope = end - start
                    slope = slope / np.linalg.norm(slope)
                    if (np.allclose(start, baseEdge[0], epsilon, epsilon) and np.allclose(slope, baseSlope, epsilon, epsilon)):
                        slotdata[i]["baseDist1"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        bases[2*k + 0] = toNumpyArray(body["bodies"][0]["edges"], j, "end")
                    elif (np.allclose(end, baseEdge[0], epsilon, epsilon) and np.allclose(slope, -baseSlope, epsilon, epsilon)):
                        slotdata[i]["baseDist1"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        bases[2*k + 0] = toNumpyArray(body["bodies"][0]["edges"], j, "start")
                    if (np.allclose(start, baseEdge[1], epsilon, epsilon) and np.allclose(slope, -baseSlope, epsilon, epsilon)):
                        slotdata[i]["baseDist2"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        bases[2*k + 1] = toNumpyArray(body["bodies"][0]["edges"], j, "end")
                    elif (np.allclose(end, baseEdge[1], epsilon, epsilon) and np.allclose(slope, baseSlope, epsilon, epsilon)):
                        slotdata[i]["baseDist2"] = body["bodies"][0]["edges"][j]["geometry"]["length"] * constant
                        bases[2*k + 1] = toNumpyArray(body["bodies"][0]["edges"], j, "start")

        else:
            continue
    length = -1
    print(cross)
    print("\n")
    print(tabs)
    print(bases)
    for j in tabs:
        tabsPoint = tabs[j]
        for k in bases:
            basesPoint = bases[k]
            slope = tabsPoint - basesPoint
            slope = slope / np.linalg.norm(slope)
            print(slope)
            if np.allclose(slope, cross) or np.allclose(slope, -cross):
                length = max(length, np.linalg.norm(basesPoint - tabsPoint))
    if length < 0:
        print("Not proper Slotted2 \n")
        print(tabs)
        print(bases)
        unsuppress(updatesBox, updatesTSlot, updatesTAS, updatesSlot partQueryBox, partQueryT, partQueryTAS, partQuerySlot)
        sys.exit()
    slotdata[i]["intersection"] = length * constant
    

pprint.pprint(slotdata)
pprint.pprint(map_parts)
pprint.pprint(map_edges)
offsetx += round(50.0 / constant, 8)
offsety += round(10.0 / constant, 8)


# Box joint
boxEdges = []
for i in range(len(boxIDS)):
    print(boxIDS[i])
    tabId, baseId, tabedgeId, baseedgeId = boxIDS[i]
    tabDict = map_parts[tabId]
    baseDict = map_parts[baseId]
    edge = (-1,-1)

    if map_edges[tabId].has_key(tabedgeId) and map_edges[baseId].has_key(baseedgeId):
        tabEdge = [toNumpyArray(map_edges[tabId], boxIDS[i][2], "start"), toNumpyArray(map_edges[tabId], boxIDS[i][2], "end")]
        baseEdge = [toNumpyArray(map_edges[baseId], boxIDS[i][3], "start"), toNumpyArray(map_edges[baseId], boxIDS[i][3], "end")]
        for j in range(2):
            for k in range(len(tabDict[j]["edges"])):
                va = tabDict[j]["edges"][k][0]
                vb = tabDict[j]["edges"][k][1]
                checkf1 = va - tabEdge[0]
                checkf2 = vb - tabEdge[1]
                checkb1 = va - tabEdge[1]
                checkb2 = vb - tabEdge[0]
                if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                    (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                    ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                    (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                    edge = (j + k * 2, edge[1])
        for jb in range(2):
            for kb in range(len(baseDict[jb]["edges"])):
                va = baseDict[jb]["edges"][kb][0]
                vb = baseDict[jb]["edges"][kb][1]
                checkf1 = va - baseEdge[0]
                checkf2 = vb - baseEdge[1]
                checkb1 = va - baseEdge[1]
                checkb2 = vb - baseEdge[0]
                if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                    (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                    ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                    (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                    edge = (edge[0], jb + kb * 2)
    else:
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
    print("box \n")
    print(edge)
    if edge[0] < 0 or edge[1] < 0:
        print("Not proper LaserJoint3 \n")
        print(edge)
        print(i)
        pprint.pprint(tabDict)
        pprint.pprint(baseDict)
        unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])
        sys.exit()
    boxEdges.append(edge)




# t slot joints
tEdges = []
for i in range(len(tSlotIDS)):
    print("\n")
    print(i)
    print("\n")
    faceId, tabId, baseId, tabedgeId, baseedgeId = tSlotIDS[i]
    tDict = map_parts[faceDict[faceId]["pid"]]
    edges = []
    tabDict = map_parts[tabId]
    baseDict = map_parts[baseId]
    edge = (-1,-1)
    if map_edges[tabId].has_key(tabedgeId) and map_edges[baseId].has_key(baseedgeId):
        tabEdge = [toNumpyArray(map_edges[tabId], tabedgeId, "start"), toNumpyArray(map_edges[tabId], tabedgeId, "end")]
        baseEdge = [toNumpyArray(map_edges[baseId], baseedgeId, "start"), toNumpyArray(map_edges[baseId], baseedgeId, "end")]
        for j in range(2):
            for k in range(len(tabDict[j]["edges"])):
                va = tabDict[j]["edges"][k][0]
                vb = tabDict[j]["edges"][k][1]
                checkf1 = va - tabEdge[0]
                checkf2 = vb - tabEdge[1]
                checkb1 = va - tabEdge[1]
                checkb2 = vb - tabEdge[0]
                if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                    (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                    ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                    (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                    edge = (j + k * 2, edge[1])
        for jb in range(2):
            for kb in range(len(baseDict[jb]["edges"])):
                va = baseDict[jb]["edges"][kb][0]
                vb = baseDict[jb]["edges"][kb][1]
                checkf1 = va - baseEdge[0]
                checkf2 = vb - baseEdge[1]
                checkb1 = va - baseEdge[1]
                checkb2 = vb - baseEdge[0]
                if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                    (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                    ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                    (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                    edge = (edge[0], jb + kb * 2)
    else:
        for j in range(len(faceDict[faceId]["edges"])):
            fa = faceDict[faceId]["edges"][j][0]
            fb = faceDict[faceId]["edges"][j][1]
            for k in range(2):
                for l in range(len(tDict[k]["edges"])):
                    va = tDict[k]["edges"][l][0]
                    vb = tDict[k]["edges"][l][1]
                    checkf1 = va - fa
                    checkf2 = vb - fb
                    checkb1 = va - fb
                    checkb2 = vb - fa
                    if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                        (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                        ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                        (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                        edges.append((tDict[k]["edges"][l], k + 2 * l))
        print("tslot \n")
        partid = ""
        for j in range(len(edges)):
            fa = edges[j][0][0]
            fb = edges[j][0][1]
            fid = edges[j][1]
            for part in map_parts:
                if map_parts[part][0]["id"] == tDict[0]["id"] or map_parts[part][0]["id"] == tDict[1]["id"]:
                    continue
                for jb in range(2):
                    for kb in range(len(map_parts[part][jb]["edges"])):
                        checkf1 = fa - map_parts[part][jb]["edges"][kb][0]
                        checkf2 = fb - map_parts[part][jb]["edges"][kb][1]
                        checkb1 = fa - map_parts[part][jb]["edges"][kb][1]
                        checkb2 = fb - map_parts[part][jb]["edges"][kb][0]
                        if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                            (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                            ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                            (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                            edge = (jb + kb * 2, edges[j][1])
                            partid = part
        if edge[0] < 0 or edge[1] < 0 or edge[0] == edge[1]:
            print("Not proper TSlotJoint3 \n")
            print(edge)
            unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])
            sys.exit()
    tEdges.append((edge, tabId, baseId))

# Tab and Slot joint

tasEdges = []
for i in range(len(tabAndSlotIDS)):
    tabId, baseId, baseFaceId, tabedgeId, baseedgeId = tabAndSlotIDS[i]
    tabDict = map_parts[tabId]
    baseDict = map_parts[baseId]
    edge = (-1,-1)

    if map_edges[tabId].has_key(tabedgeId) and map_edges[baseId].has_key(baseedgeId):
        tabEdge = [toNumpyArray(map_edges[tabId], tabedgeId, "start"), toNumpyArray(map_edges[tabId], tabedgeId, "end")]
        baseEdge = [toNumpyArray(map_edges[baseId], baseedgeId, "start"), toNumpyArray(map_edges[baseId], baseedgeId, "end")]
        for j in range(2):
            for k in range(len(tabDict[j]["edges"])):
                va = tabDict[j]["edges"][k][0]
                vb = tabDict[j]["edges"][k][1]
                checkf1 = va - tabEdge[0]
                checkf2 = vb - tabEdge[1]
                checkb1 = va - tabEdge[1]
                checkb2 = vb - tabEdge[0]
                if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                    (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                    ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                    (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                    edge = (j + k * 2, edge[1])
        for jb in range(2):
            for kb in range(len(baseDict[jb]["edges"])):
                va = baseDict[jb]["edges"][kb][0]
                vb = baseDict[jb]["edges"][kb][1]
                checkf1 = va - baseEdge[0]
                checkf2 = vb - baseEdge[1]
                checkb1 = va - baseEdge[1]
                checkb2 = vb - baseEdge[0]
                if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                    (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                    ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                    (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                    edge = (edge[0], jb + kb * 2)
    else:
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
    print("tas \n")
    print(edge)
    if edge[0] < 0 or edge[1] < 0:
        print("Not proper TabAndBase \n")
        unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])
        sys.exit()
    tasEdges.append(edge)


# Slotted joint
slotEdges = []
for i in range(len(slotIDS)):
    tabId, baseId, tabFace, baseFace, tabEdges, baseEdges = slotIDS[i]
    tabDict = map_parts[tabId]
    baseDict = map_parts[baseId]
    tabEdge = [toNumpyArray(map_edges[tabId], slotIDS[i][4][0], "start"), toNumpyArray(map_edges[tabId], slotIDS[i][4][0], "end")]
    baseEdge = [toNumpyArray(map_edges[baseId], slotIDS[i][5][0], "start"), toNumpyArray(map_edges[baseId], slotIDS[i][5][0], "end")]
    edge = (-1,-1)
    for j in range(2):
        for k in range(len(tabDict[j]["edges"])):
            va = tabDict[j]["edges"][k][0]
            vb = tabDict[j]["edges"][k][1]
            checkf1 = va - tabEdge[0]
            checkf2 = vb - tabEdge[1]
            checkb1 = va - tabEdge[1]
            checkb2 = vb - tabEdge[0]
            if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                edge = (j + k * 2, edge[1])
    for jb in range(2):
        for kb in range(len(baseDict[jb]["edges"])):
            va = baseDict[jb]["edges"][kb][0]
            vb = baseDict[jb]["edges"][kb][1]
            checkf1 = va - baseEdge[0]
            checkf2 = vb - baseEdge[1]
            checkb1 = va - baseEdge[1]
            checkb2 = vb - baseEdge[0]
            if ((abs(checkf1[0]) < epsilon and abs(checkf1[1]) < epsilon and abs(checkf1[2]) < epsilon) and \
                (abs(checkf2[0]) < epsilon and abs(checkf2[1]) < epsilon and abs(checkf2[2]) < epsilon)) or \
                ((abs(checkb1[0]) < epsilon and abs(checkb1[1]) < epsilon and abs(checkb1[2]) < epsilon) and \
                (abs(checkb2[0]) < epsilon and abs(checkb2[1]) < epsilon and abs(checkb2[2]) < epsilon)):
                edge = (edge[0], jb + kb * 2)
    if edge[0] < 0 or edge[1] < 0:
        print("Not proper slotted \n")
        print(edge)
        unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])
        sys.exit()
    slotEdges.append(edge)

print(boxEdges)
print(tEdges)
print(tasEdges)
print(slotEdges)
print("\n")

vb = "0 0 " + str(round(offsetx * constant, 8)) + " " + str(round(offsety * constant, 8)) 
doc = ET.Element('svg', style="fill:none;stroke:#ff0000;stroke-linejoin:round;stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5", viewBox= vb, xmlns="http://www.w3.org/2000/svg")

meta = dict()
meta["attrib"] = {"style" : "fill:none;stroke:#ff0000;stroke-linejoin:round;stroke-width:0.1px;stroke-linecap:round;stroke-opacity:0.5", "viewBox" : vb, "xmlns" : "http://www.w3.org/2000/svg"}
meta["joints"] = dict()

counter = 0
for i in range(len(boxEdges)):
    a,b = boxEdges[i]
    tabId, baseId, tabedgeId, baseedgeId = boxIDS[i]
    indexT0 = a % 2
    indexT1 = a // 2
    indexB0 = b % 2
    indexB1 = b // 2
    meta["joints"]["Joint" + str(i + 1)] = dict()
    tab = map_parts[tabId][indexT0]["2d_edges"][indexT1]
    base = map_parts[baseId][indexB0]["2d_edges"][indexB1]
    tabEdge = "M " + str(np.around(tab[0][0] * constant, 8)) + "," + str(np.around(tab[0][1] * constant, 8)) + " L " + \
                     str(np.around(tab[1][0] * constant, 8)) + "," + str(np.around(tab[1][1] * constant, 8))
    baseEdge = "M " + str(np.around(base[0][0] * constant, 8)) + "," + str(np.around(base[0][1] * constant, 8)) + " L " + \
                     str(np.around(base[1][0] * constant, 8)) + "," + str(np.around(base[1][1] * constant, 8))
    meta["joints"]["Joint" + str(i + 1)]["edge_a"] = {"d" : tabEdge,
                                                      "edge" : indexT1 + map_parts[tabId][indexT0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[tabId][indexT0]["id"] + 1)}
    meta["joints"]["Joint" + str(i + 1)]["edge_b"] = {"d" : baseEdge,
                                                      "edge" : indexB1 + map_parts[baseId][indexB0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[baseId][indexB0]["id"] + 1)}
    length = max(abs(tab[1][0] - tab[0][0]), abs(tab[1][1] - tab[0][1])) * constant
    tabnum = int((str(updatesBox[i]["message"]["parameters"][7]["message"]["expression"])))
    fit = (str(updatesBox[i]["message"]["parameters"][5]["message"]["value"]).lower()).capitalize()
    tabnormal = map_parts[tabId][indexT0]["normal"]
    basenormal = map_parts[baseId][indexB0]["normal"]
    angle = np.arccos(np.dot(tabnormal, basenormal))
    meta["joints"]["Joint" + str(i + 1)]["joint_parameters"] = {"joint_type": "Box",
                                                "joint_align": "Inside",
                                                "fit": fit,
                                                "tabsize": length / (2 * tabnum - 1),
                                                "tabspace": length / (2 * tabnum - 1),
                                                "tabnum": tabnum - 1,
                                                "boltsize": "M0",
                                                "boltspace": 0,
                                                "boltnum": 0,
                                                "boltlength": 0,
                                                "angle": angle}
counter += len(boxEdges)
for i in range(len(tEdges)):
    a,b = tEdges[i][0]
    tabId = tEdges[i][1]
    baseId = tEdges[i][2]
    if tabId != tSlotIDS[i][1] or baseId != tSlotIDS[i][2]:
        print("Wrong ids for tslot")
        unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])
        sys.exit()
    indexT0 = a % 2
    indexT1 = a // 2
    indexB0 = b % 2
    indexB1 = b // 2
    meta["joints"]["Joint" + str(counter + i + 1)] = dict()
    tab = map_parts[tabId][indexT0]["2d_edges"][indexT1]
    base = map_parts[baseId][indexB0]["2d_edges"][indexB1]
    tabEdge = "M " + str(np.around(tab[0][0] * constant, 8)) + "," + str(np.around(tab[0][1] * constant, 8)) + " L " + \
                     str(np.around(tab[1][0] * constant, 8)) + "," + str(np.around(tab[1][1] * constant, 8))
    baseEdge = "M " + str(np.around(base[0][0] * constant, 8)) + "," + str(np.around(base[0][1] * constant, 8)) + " L " + \
                     str(np.around(base[1][0] * constant, 8)) + "," + str(np.around(base[1][1] * constant, 8))
    meta["joints"]["Joint" + str(counter + i + 1)]["edge_a"] = {"d" : tabEdge,
                                                      "edge" : indexT1 + map_parts[tabId][indexT0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[tabId][indexT0]["id"] + 1)}
    meta["joints"]["Joint" + str(counter + i + 1)]["edge_b"] = {"d" : baseEdge,
                                                      "edge" : indexB1 + map_parts[baseId][indexB0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[baseId][indexB0]["id"] + 1)}
    length = max(abs(tab[1][0] - tab[0][0]), abs(tab[1][1] - tab[0][1])) * constant
    boltnum = int(str(updatesTSlot[i]["message"]["parameters"][15]["message"]["expression"]))
    boltsize = str(updatesTSlot[i]["message"]["parameters"][5]["message"]["value"][3]["value"])
    boltlength = readUnits(str(updatesTSlot[i]["message"]["parameters"][11]["message"]["expression"]))
    edgeSpace = readUnits(str(updatesTSlot[i]["message"]["parameters"][14]["message"]["expression"]))
    tabnormal = map_parts[tabId][indexT0]["normal"]
    basenormal = map_parts[baseId][indexB0]["normal"]
    angle = np.arccos(np.dot(tabnormal, basenormal))
    boltspace = length / 2
    if boltnum > 1:
        boltspace = (length - 2 * edgeSpace) / (boltnum - 1)
    meta["joints"]["Joint" + str(counter + i + 1)]["joint_parameters"] = {"joint_type": "TSlot",
                                                "joint_align": "Inside",
                                                "fit": "Clearance",
                                                "tabsize": 0,
                                                "tabspace": 0,
                                                "tabnum": 0,
                                                "boltsize": boltsize,
                                                "boltspace": boltspace,
                                                "boltnum": boltnum,
                                                "boltlength": boltlength,
                                                "angle": angle,
                                                "edgeSpace": edgeSpace}
counter += len(tEdges)
for i in range(len(tasEdges)):
    a,b = tasEdges[i]
    tabId, baseId, baseFaceId, tabedgeId, baseedgeId = tabAndSlotIDS[i]
    indexT0 = a % 2
    indexT1 = a // 2
    indexB0 = b % 2
    indexB1 = b // 2
    meta["joints"]["Joint" + str(counter + i + 1)] = dict()
    tab = map_parts[tabId][indexT0]["2d_edges"][indexT1]
    base = map_parts[baseId][indexB0]["2d_edges"][indexB1]
    tabEdge = "M " + str(np.around(tab[0][0] * constant, 8)) + "," + str(np.around(tab[0][1] * constant, 8)) + " L " + \
                     str(np.around(tab[1][0] * constant, 8)) + "," + str(np.around(tab[1][1] * constant, 8))
    baseEdge = "M " + str(np.around(base[0][0] * constant, 8)) + "," + str(np.around(base[0][1] * constant, 8)) + " L " + \
                     str(np.around(base[1][0] * constant, 8)) + "," + str(np.around(base[1][1] * constant, 8))
    meta["joints"]["Joint" + str(counter + i + 1)]["edge_a"] = {"d" : tabEdge,
                                                      "edge" : indexT1 + map_parts[tabId][indexT0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[tabId][indexT0]["id"] + 1)}
    meta["joints"]["Joint" + str(counter + i + 1)]["edge_b"] = {"d" : baseEdge,
                                                      "edge" : indexB1 + map_parts[baseId][indexB0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[baseId][indexB0]["id"] + 1)}
    length = max(abs(tab[1][0] - tab[0][0]), abs(tab[1][1] - tab[0][1])) * constant
    tabnum = int((str(updatesTAS[i]["message"]["parameters"][7]["message"]["expression"])))
    tabnormal = map_parts[tabId][indexT0]["normal"]
    basenormal = map_parts[baseId][indexB0]["normal"]
    angle = np.arccos(np.dot(tabnormal, basenormal))
    fit = (str(updatesTAS[i]["message"]["parameters"][5]["message"]["value"]).lower()).capitalize()
    edgeOffset = 0.0
    if updatesTAS[i]["message"]["parameters"][15]["message"]["value"]:
        edgeOffset = readUnits(updatesTAS[i]["message"]["parameters"][16]["message"]["expression"])
    tabsize = (length - 2 * edgeOffset) / (2 * tabnum - 1)
    tabspace = (length - 2 * edgeOffset) / (2 * tabnum - 1)
    if updatesTAS[i]["message"]["parameters"][9]["message"]["value"]:
        tabsize = readUnits(updatesTAS[i]["message"]["parameters"][10]["message"]["expression"])
        tabspace = (length - 2 * edgeOffset - tabsize * tabnum) / (tabnum - 1)
    meta["joints"]["Joint" + str(counter + i + 1)]["joint_parameters"] = {"joint_type": "Tab-and-Slot",
                                                "joint_align": "Inside",
                                                "fit": fit,
                                                "tabsize": tabsize,
                                                "tabspace": tabspace,
                                                "tabnum": tabnum,
                                                "boltsize": "M0",
                                                "boltspace": 0,
                                                "boltnum": 0,
                                                "boltlength": 0,
                                                "angle": angle,
                                                "thickness": readUnits(str(updatesTAS[i]["message"]["parameters"][6]["message"]["expression"])),
                                                "edgeOffset": edgeOffset}
counter += len(tasEdges)
for i in range(len(slotEdges)):
    a,b = slotEdges[i]
    tabId, baseId, tabface, baseface, tabedgeId, baseedgeId = slotIDS[i]
    indexT0 = a % 2
    indexT1 = a // 2
    indexB0 = b % 2
    indexB1 = b // 2
    meta["joints"]["Joint" + str(counter + i + 1)] = dict()
    tab = map_parts[tabId][indexT0]["2d_edges"][indexT1]
    base = map_parts[baseId][indexB0]["2d_edges"][indexB1]
    tabEdge = "M " + str(np.around(tab[0][0] * constant, 8)) + "," + str(np.around(tab[0][1] * constant, 8)) + " L " + \
                     str(np.around(tab[1][0] * constant, 8)) + "," + str(np.around(tab[1][1] * constant, 8))
    baseEdge = "M " + str(np.around(base[0][0] * constant, 8)) + "," + str(np.around(base[0][1] * constant, 8)) + " L " + \
                     str(np.around(base[1][0] * constant, 8)) + "," + str(np.around(base[1][1] * constant, 8))
    meta["joints"]["Joint" + str(counter + i + 1)]["edge_a"] = {"d" : tabEdge,
                                                      "edge" : indexT1 + map_parts[tabId][indexT0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[tabId][indexT0]["id"] + 1)}
    meta["joints"]["Joint" + str(counter + i + 1)]["edge_b"] = {"d" : baseEdge,
                                                      "edge" : indexB1 + map_parts[baseId][indexB0]["numEdges"] + 1, 
                                                      "face" : "face" + str(map_parts[baseId][indexB0]["id"] + 1)}
    length = max(abs(tab[1][0] - tab[0][0]), abs(tab[1][1] - tab[0][1])) * constant
    tabnormal = map_parts[tabId][indexT0]["normal"]
    basenormal = map_parts[baseId][indexB0]["normal"]
    slope = np.cross(tabnormal, basenormal)
    slope = slope / np.linalg.norm(slope)
    perptab = perpendicular(tabnormal)
    perp2tab = np.cross(perptab, tabnormal)
    perp2tab = perp2tab / np.linalg.norm(perp2tab)
    tabslope = np.array([np.dot(slope, perp2tab), np.dot(slope, perptab)])
    perpbase = perpendicular(basenormal)
    perp2base = np.cross(perpbase, basenormal)
    perp2base = perp2base / np.linalg.norm(perp2base)
    baseslope = np.array([np.dot(slope, perp2base), np.dot(slope, perpbase)])
    fit = (str(updatesSlot[i]["message"]["parameters"][7]["message"]["value"]).lower()).capitalize()
    meta["joints"]["Joint" + str(counter + i + 1)]["joint_parameters"] = {"joint_type": "Slotted",
                                                "tabSlope": list(tabslope),
                                                "baseSlope": list(baseslope),
                                                "percentage": float((str(updatesSlot[i]["message"]["parameters"][6]["message"]["expression"]))),
                                                "tabDist1": slotdata[i]["tabDist1"],
                                                "tabDist2": slotdata[i]["tabDist2"],
                                                "baseDist1": slotdata[i]["baseDist1"],
                                                "baseDist2": slotdata[i]["baseDist2"],
                                                "intersection": slotdata[i]["intersection"],
                                                "joint_align": "Inside",
                                                "fit": "Clearance",
                                                "tabsize": 0,
                                                "tabspace": 0,
                                                "tabnum": 0,
                                                "boltsize": "M2",
                                                "boltspace": 0,
                                                "boltnum": 0,
                                                "boltlength": 0,
                                                "angle": 0,}

edges = []
meta["tree"] = dict() 
for partkey in map_parts:
    pedges = map_parts[partkey][0]["2d_edges"]
    (a,b) = np.around(pedges[0][0] * constant, 8)
    face = "face" + str(map_parts[partkey][0]["id"]+1)
    meta["tree"][face] = dict()
    path = "M " + str(a) + "," + str(b) + " "
    edge = path
    for j in range(1,len(pedges) + 1):
        (a,b) = np.around(pedges[j % len(pedges)][0] * constant, 8)
        path += "L " + str(a) + "," + str(b) + " "
        ej = edge + "L " + str(a) + "," + str(b)
        edge = "M " + str(a) + "," + str(b) + " "
        edges.append({"d" : ej, "edge" : j + map_parts[partkey][0]["numEdges"], "face": face})
        counter += 1
    meta["tree"][face]["Perimeter"] = {"paths": [path]}
    cuts = map_parts[partkey][0]["cuts"]
    cutpath = []
    for i in range(len(cuts)):
        cutpath.append(cuts[i]["path"])
        path += cuts[i]["path"]
    meta["tree"][face]["Cuts"] = {"paths": cutpath}
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

svg = open('joints.svg', 'w')
svg.write(ET.tostring(doc))
svg.close()



unsuppress(updatesBox, updatesTSlot, updatesTAS, [], partQueryBox, partQueryT, partQueryTAS, [])


# NEED TO ADJUST THICKNESS TO BE METERS
# ADD FIT TO EACH JOINT
# tab and slot dont worry about ordering
# joints need to be the last thing made