import json
from pprint import pprint
import gmplot

cluster_locations_path = "adr_cluster_locations.json"
api_key = ""
map_html = "adr_cluster_map.html"
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
