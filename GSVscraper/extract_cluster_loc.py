import json
from pprint import pprint
import time
import gmplot

#parameters:
# 1.your Google Api Key!!!!!!!!!!!!!!!!!
api_key = ''
# 2.name of the "cluster information" document
adr_Original_Data = 'Sample JSON/20160915_clustering_clusters_R30_P15_simple.json'
# 3.name of document we saved the extracted (non-cluster) locations
adr_cluster_locations = 'adr_cluster_locations.json'
# 4.name of html document that saves the visulization results of the locations in Google Map
map_html = 'adr_cluster_map_.html'

# Open the Json Document And Load the Datas
with open(adr_Original_Data,'r') as f:
    data = json.load(f)
#Define the sorting function based on the number of clusters each time
sorting_function = lambda time: len(time)
#max of "C" means the cluster that has the largest number of locations
max_cluster = max(data["C"].values(), key = sorting_function)
#pprint(max_cluster)

# A function to extract the key of the dictionary
def get_keys(d, value):
    return [k for k, v in d.items() if v == value]

# Get the time
max_time = get_keys(data["C"], max_cluster)
# In the Json document the time is in the form of epoch time
# we need change it into human-readable time
# max_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch_time))
pprint("The Time That Has The Largest Number of Clusters:")
pprint(max_time)
pprint("At that time, the number of clusters are: " + str(len(max_cluster)))

# def sample_number(cluster,rate = 0.1):
#     total_coord_numbers = len(cluster["coord"])
#     return int(rate*total_coord_numbers)

locations = []
total_sample_numbers = 0

for index_c in max_cluster.values():
    i = 0
    for coord in index_c["coord"]:
        if coord not in locations:
            locations.append(coord)
            i = i + 1
    total_sample_numbers = total_sample_numbers + i


pprint("total number of locations: " + str(total_sample_numbers))
pprint(locations)

# gmplot:https://github.com/vgm64/gmplot
# visualize the locations in Google Map
gmap = gmplot.GoogleMapPlotter(42.5080882978956, 1.5293202323005406, 30)
# Markers
for i in locations:
    hidden_gem_lat, hidden_gem_lon = i[0], i[1]
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')
gmap.apikey = api_key
gmap.draw(map_html)

dict = {"train_cluster":locations}

with open(adr_cluster_locations,'w') as w:
       json.dump(dict,w,indent=4)







