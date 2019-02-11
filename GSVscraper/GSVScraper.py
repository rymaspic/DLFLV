# # # # # # # # # # # # # # # #

# {{ DLFLV }}
# Copyright (C) {{ 2017 }}  {{ Ariel Noyman }}
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# # # # # # # # # # # # # # # # #

# "@context": "https://github.com/RELNO/", "@type": "Person", "address": {
# "@type": "75 Amherst St, Cambridge, MA 02139", "addressLocality":
# "Cambridge", "addressRegion": "MA",},
# "jobTitle": "Research Scientist", "name": "Ariel Noyman",
# "alumniOf": "MIT", "url": "http://arielnoyman.com",
# "https://www.linkedin.com/", "http://twitter.com/relno",
# https://github.com/RELNO]

# # # # # # # # # # # # # # # #
#
# USAGE:
# python3 GSVScraper.py -l __FILE NAME__ -i __ANGLE__ -k __KEY__
#
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
import random


# # # # # # # # # # # # # # # #
# Vars
# # # # # # # # # # # # # # # #

# streetview url up to the address
pre = "https://maps.googleapis.com/maps/api/streetview?"
pre_meta = "https://maps.googleapis.com/maps/api/streetview/metadata?"
head = "&heading="
# the pitch[height] of the camera
pitch = "&pitch=0"
loc = "location="
# Files need to defined:
img_meta_locations_file = "Json_Files/meta_locations.json" #json file name to save the meta information of GSV images

#title = "cluster" # "nocluster"


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--locations", required=True,
                help="filename of locations JSON")
ap.add_argument("-i", "--interval",  type=int, required=True,
                help="camera angle intervals [0 to 360 degrees]")
ap.add_argument("-k", "--key", required=True,
                help="Google Places key")

args = vars(ap.parse_args())

# API key
suf = "&key=" + args["key"]

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
    f = open(img_meta_locations_file, "w")  # opens file
    meta_locations = []
    for dl_class in LOCATIONS:
        filenameCounter = 0
        # make the folders for each class if missing
        # this is the directory that will store the streetview images
        classFolder = r"images/" + str(dl_class)
        if not os.path.exists(classFolder):
            os.makedirs(classFolder)

        # go through each location in this class and get its photos
        for location in locations[dl_class]:
            # 0 to 360 in jumps of 30 degrees
            filenameCounter += 1
            latLon = str(location[0]) + ',' + str(location[1])
            # check if this Google SV URL returns a valid SV images or not
            if (checkSV(latLon) != [False]):

                # get view angles from each point
                init_ang = random.randint(0,359)
                # for every location, randomly generate a initial angle to avoid
                # unexpected bias when some parts of a city have a north-south street network
                # while other parts have a diagonal-direction street network
                for ang in range(0, 360, INTERVAL):
                    #filenameCounter += 1

                    # creates the url that will be passed to the url reader,
                    # a google streetview image for each address in the address text file
                    URL = pre + loc + latLon + '&size=600x600' + \
                        head + str(init_ang + ang) + pitch + '&source=outdoor' + suf  #only get the indoor images

                    Meta_URL = pre_meta + loc + latLon + '&size=300x300' + \
                        head + str(init_ang + ang) + pitch + '&source=outdoor' + suf  #only get the indoor images

                    print('\n', URL, '\n')
                    print('\n', Meta_URL, '\n')
                    # creates the filename needed
                    # to save each address's streetview image locally

                    filename = os.path.join(
                        classFolder,  str(filenameCounter) + "_ang" + str(ang) + ".jpg")
                    # fetches and saves the streetview image
                    # for each address using the url created in the previous steps
                    img = urllib.request.urlretrieve(URL, filename)

                    # the GSV API returns the nearest image given a GPS location, but we need call the meta_image API
                    # to get the exact GPS information the image were toke
                    img_meta = urllib.request.urlopen(Meta_URL).read()
                    encoding = urllib.request.urlopen(Meta_URL).info().get_content_charset('utf-8')
                    img_meta = json.loads(img_meta.decode(encoding))
                    # print("metadata: ", img_meta["location"])
                    # eg.metadata:  {'lat': 42.50349875571963, 'lng': 1.516247674376121}
                    meta_loc = [img_meta["location"]['lat'], img_meta["location"]['lng']]
                    print(meta_loc)
                    meta_locations.append(meta_loc)

                    img = Image.open(filename)
                    area = (44, 44, 556, 556) # modify the area if the size of image is changed,
                    # current size is 600*600 which is the maxmium size of "free" GSV API
                    cropped_img = img.crop(area)
                    cropped_img.save(filename)

                    f.write(filename + " " + latLon + "\n")

                    # resize to fit DL module if needed
                    # imgSm = Image.open(img[0])
                    # imgSm.resize((227, 227), Image.ANTIALIAS).save(img[0])
                    print("OUTPUT FILENAME:" + filename)
            else:
                print(latLon, " is not a Google StView location")
    f.close()
    meta_dict = {"meta_locations": meta_locations}
    with open(img_meta_locations_file, 'w') as w:
        json.dump(meta_dict, w, indent=4)


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
