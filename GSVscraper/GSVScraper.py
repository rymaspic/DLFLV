# # # # # # # # # # # # # # # #
# By Ariel Noyman https://github.com/RELNO/
#
# USAGE:
# python3 0_StViewScraper.py -l __FILE NAME__ -i __ANGLE__
# # # # # # # # # # # # # # # #

# urllib/requests for accessing web content
import urllib.request
import requests
# os for file path creation
import os
# PIL image manipultaion
import PIL
from PIL import Image
# json
import json
# xml parser
import xml.etree.ElementTree as ET
# for command line args
import argparse


# # # # # # # # # # # # # # # #
# Vars
# # # # # # # # # # # # # # # #

# streetview url up to the address
pre = "https://maps.googleapis.com/maps/api/streetview?size=300x300"
head = "&heading="
# the pitch[height] of the camera
pitch = "&pitch=-0.76"
loc = "&location="
# API key
suf = "&amp;key=AIzaSyC8ejNwVI-DZcv8cE-zcES21k0nlQeD5Nk"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--locations", required=True,
                help="filename of locations JSON")
ap.add_argument("-i", "--interval",  type=int, required=True,
                help="camera angle intervals [0 to 360 degrees]")

args = vars(ap.parse_args())

# the addresses in this text file will complete
# the URL needed to return a streetview image and provide
# the filename of each streetview image
locations = json.load(open(args["locations"]+".json"))

# # # # # # # # # # # # # # # #
# Methods
# # # # # # # # # # # # # # # #


def GetGSV(LOCATIONS, INTERVAL):
    "gets photos from GSV for given locations"
    # start a loop through the 'lines' list
    for dl_class in LOCATIONS:
        filenameCounter = 0

        # make the folders for each class if missing
        # this is the directory that will store the streetview images
        classFolder = r"train/" + str(dl_class)
        if not os.path.exists(classFolder):
            os.makedirs(classFolder)

        # go through each location in this class and get its photos
        for location in locations[dl_class]:
            # 0 to 360 in jumps of 30 degrees
            latLon = str(location[0]) + ',' + str(location[1])
            # check if this Google SV URL returns a valid SV images or not
            if (checkSV(latLon) != [False]):

                # get view angles from each point
                for ang in range(0, 360, INTERVAL):
                    filenameCounter += 1
                    # creates the url that will be passed to the url reader,
                    # a google streetview image for each address in the address text file
                    URL = pre + head + str(ang) + pitch + loc + latLon + suf
                    # creates the filename needed
                    # to save each address's streetview image locally

                    filename = os.path.join(
                        classFolder, "00" + str(filenameCounter) + ".jpg")
                    # fetches and saves the streetview image
                    # for each address using the url created in the previous steps
                    img = urllib.request.urlretrieve(URL, filename)

                    # resize to fit DL module if needed
                    # imgSm = Image.open(img[0])
                    # imgSm.resize((227, 227), Image.ANTIALIAS).save(img[0])
                    print("OUTPUT FILENAME:" + filename)
            else:
                print(latLon, " is not a Google StView location")


def checkSV(LATLON):
    "looks for a respone in XML callback from google SV API"
    # return value
    bool = False
    # check GSV URL base
    checkURLstart = "http://maps.google.com/cbk?output=xml&hl=en&ll="
    # 39.47611, -0.3899
    checkURLend = "&radius=50&cb_client=maps_sv&v=4"
    URL = checkURLstart + LATLON + checkURLend
    response = requests.get(URL)
    root = ET.fromstring(response.content)
    if root:
        bool = True
    return [bool]

# # # # # # # # # # # # # # # #
# Caller
# # # # # # # # # # # # # # # #


# call GSV scraper method with locations and camera angle inerval
GetGSV(locations, args["interval"])
