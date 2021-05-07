# Onshape python script

(In progress)

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
run $ virtualenv -p /path/to/python2 env && source env/bin/activate 
    in python folder
run $ pip install -r requirements.txt
run python2 app.py



ASSUMPTIONS SO FAR:
Use laser joint featurescript
All parts will have the same height (because laser cutting the same material)
All parts will be rectangular
Intersection between base and tab will be a "good fit" (meaning the side lengths will match up)
Joints are evenly split
No cuts on the inside
All LaserJoints have exactly two parts

Idea:
Go through each part
Find the common height
Make a auto layout feature with the common height
Call it on the thing
Get updated body details
Get all faces with a normal of 001 or 00-1
Then we can get the lengths of each edge of the faces
Then construct the faces

Notes:
ALL MEASUREMENTS IN BODY DETAILS ARE IN METERS
    Find a way to rescale this

Functions that might be useful:
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



Possible useful links:
https://cad.onshape.com/FsDoc/tutorials/create-a-slot-feature.html
https://forum.onshape.com/discussion/5528/evaluate-featurescript-request-returns-empty-btfsvaluearray-instead-of-face
https://forum.onshape.com/discussion/7544/execute-featurescript-using-api-and-python



---

(Cloned from Onshape-public/apikey)

### Local Setup

Install the dependencies:

* Python 2 (2.7.9+)
* pip
* virtualenv

Then, from this folder:

--for Linux:
```sh
$ virtualenv -p /path/to/python2 env && source env/bin/activate
```

--for Windows:
```sh
$ virtualenv -p /path/to/python2.exe env && env/Scripts/activate.bat
```
References:

* https://stackoverflow.com/questions/8921188/issue-with-virtualenv-cannot-activate
* https://virtualenv.pypa.io/en/stable/userguide/#activate-script

You can now install the needed Python packages:

--for Linux:
```sh
$ pip install -r requirements.txt
```

--for Windows:
```sh
$ pip install -r requirements-win.txt
```

The windows-specific requirements file encompasses libraries that work for Win-OS

References:
* https://pypi.python.org/pypi/pyreadline

To exit the virtual environment at any time, simply type `deactivate`.

### Running the App

Create a `creds.json` file in the root project directory, with the following format:

```json
{
    "https://cad.onshape.com": {
        "access_key": "ACCESS KEY",
        "secret_key": "SECRET KEY"
    }
}
```

Just replace "ACCESS KEY" and "SECRET KEY" with the values you got from the
developer portal. To test on other stacks, you'll create another object in the file,
with credentials for that specific stack.

To run the basic application:

```sh
$ python app.py
```

To print an STL representation of a given part studio to the console:

```sh
$ python exportstl.py
```

If you want to specify a different stack to test on, simply go into the file you're running and
change the `stack` parameter on this line:

```py
c = Client(stack='NEW STACK HERE')
```

### Working with API Keys

For general information on our API keys and how they work, read this
[document](https://github.com/onshape/apikey/blob/master/README.md). For general
API support, please reach out to us at
[api-support@onshape.com](mailto:api-support@onshape.com).
