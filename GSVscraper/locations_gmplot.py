import json
from pprint import pprint
import gmplot
import argparse

# # # # # # # # # # # # # # # #
#
# USAGE:
# python3 -k your_google_key -locations path_to_location_JSON_file -map name_of_map_html
#
# # # # # # # # # # # # # # # #
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-k", "--key", required=True,
                help="Google Places key")
ap.add_argument("-filename", "--locations", required=True,
                help="File path of the locations")
ap.add_argument("-mapname", "--map", required=True,
                help="Html name of the map to be saved")
args = vars(ap.parse_args())

cluster_locations_path = args["locations"]
# cluster_locations_path = "adr_cluster_locations.json"
api_key = args["key"]
map_html = args["map"]
#read the saved JSON documents which contain the locations
with open(cluster_locations_path,'r') as f:
    data = json.load(f)

locations = data["train_cluster"]
pprint(locations)

# plot the scatter points
gmapLatList = []
gmapLonList = []
for i in locations:
        lat = i[0]
        lon = i[1]
        gmap = gmplot.GoogleMapPlotter(lat, lon, 30)
        # add first point to map
        gmapLatList.append(lat)
        gmapLonList.append(lon)
        # make heatmap
        gmap.heatmap(gmapLatList, gmapLonList, opacity=1.0)
        gmap.apikey = api_key
        gmap.draw(map_html)
