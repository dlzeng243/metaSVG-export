# Onshape LaserJoint Python Script

## Local Setup:
Make sure you have installed the following dependencies:  
* Python 2 (2.7.17)  
* pip  
* virtualenv  

Next, run the following line:  
-- for Linux:  

    $ virtualenv -p /path/to/python2 env && source env/bin/activate

-- for Windows:

    $ virtualenv -p /path/to/python2.exe env && env/Scripts/activate.bat

Now, install the remaining dependencies:  
-- for Linux:  

    $ pip install -r requirements.txt

-- for Windows:

    $ pip install -r requirements-win.txt

To exit the virtual environment at any time, simply type `deactivate`.

## Running the Script

Create a creds.json with the following format:

    {  
        "https://cad.onshape.com": {  
            "access_key": "ACCESS KEY",  
            "secret_key": "SECRET KEY"  
        }  
    }

Replace "ACCESS KEY" and "SECRET KEY" with the values OnShape gives you in the developer portal.


How to run:  

    $ python2 app.py  

## Notes about the script

## ASSUMPTIONS MADE SO FAR:  
User uses the laser joint featurescript (https://cad.onshape.com/documents/578830e4e4b0e65410f9c34e/v/a86eb3c2ef0f3e5e88710cc9/e/7af109b2f1cead90850525ae)  
All parts will have the same height (because we're laser cutting the same material)  
All parts will be rectangular (odd / even parity for computing which edges correspond to each other)
Intersection between base and tab will be a "good fit" (meaning the side lengths will match up)  
Joints are evenly split  
No cuts on the inside (normal box joints for now)  
All LaserJoints have exactly two parts (no solution otherwise for now)  

## General thought process:  
Go through each part in the OnShape document  
Find the common height (with respect to the assumption)  
Make an auto layout feature with the common height    
Get updated body details  
Get all faces with a normal of 001 or 00-1  
Get the lengths of each edge of the faces  
Do some math to compute which sides correspond to each other  
Construct the SVG file

## OnShape API additional functions:  
ALL MEASUREMENTS IN BODY DETAILS ARE IN METERS  
    Find a way to rescale this to pixels  

Functions that might be useful from OnShape API:  
PARTS - body details (get information about lengths and stuff)  
PARTS - get parts (get parts id)  
PARTSTUDIO - get features (get laser cut info)  
PARTSTUDIO - update feature (suppress)  
PARTSTUDIO - add feature (add the autolayout)  
PARTSTUDIO - delete feature  
ELEMENTS - get configuration?  
DRAWINGS - get translation format?  

## Other Onshape Forums stuff:
there's a feature script to autolayout - maybe try using it to get info?  
https://www.youtube.com/watch?v=YPoJ484-7tI&t=1s  

check if the body details are different with and without the laser cut (they are very different)  

Possible useful links:  
https://cad.onshape.com/FsDoc/tutorials/create-a-slot-feature.html  
https://forum.onshape.com/discussion/5528/evaluate-featurescript-request-returns-empty-btfsvaluearray-instead-of-face  
https://forum.onshape.com/discussion/7544/execute-featurescript-using-api-and-python  

## Stuff to be done:
* Finish documentation / clean up code
* Make more OnShape examples
* Find a new way to find which edges correspond to each other in a laser joint (possibly with FeatureScript)
* Learn how to use FeatureScript to modify the LaserJoint feature to do other types of laser joints
* Adjust Matt's thing to take in a spreadsheet for kerfs
* Schedule in zulip

## Credits
Credits to onshape-public/apikey for the general setup on how to use the OnShape API keys.  
Go to https://github.com/onshape-public/apikey for more information.