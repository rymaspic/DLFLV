import json
from pprint import pprint
import gmplot


# After running the extract_cluster_loc.py we now know the time has the largest number of cluster
# ['1473935700']
# pprint(data["C"]["1473907200"]["C86"]["meanCoord"])

#parameters:
# 1.your Google Api Key!!!!!!!!!!!!
api_key = ''
# 2.name of the "cluster information" document
adr_Original_Data = 'Sample JSON/20160915_clustering_clusters_R30_P15_simple.json'
# 3.name of document we saved the extracted (non-cluster) locations
adr_no_cluster_locations = 'adr_no_cluster_locations.json'
# 4.name of document we saved the extracted cluster locations, we use this to avoid repeating
adr_cluster_locations = 'adr_cluster_locations.json'
# 5.name of html document that saves the visualization results of the locations in Google Map
map_html = 'adr_no_cluster_map.html'
map_whole_html = 'adr_whole_map.html'

locations = []
total_loc_number = 0

with open(adr_Original_Data,'r') as f:
    data = json.load(f)

with open('adr_cluster_locations.json','r') as ff:
    data2 = json.load(ff)
cluster_locations = data2["train_cluster"]

# check cluster locations to avoid repeating
# (actually the json original data seperates them pretty well)
for index in data["UnC"]["1473935700"]["coord"]:
        if (index not in locations)and (index not in cluster_locations):
            locations.append(index)
            total_loc_number = total_loc_number + 1

pprint('total number of no-cluster locations:' + str(total_loc_number))
# pprint(locations)
dict = {"train_nocluster":locations}

with open(adr_no_cluster_locations,'w') as w:
     json.dump(dict,w,indent=4)

gmap = gmplot.GoogleMapPlotter(42.5080882978956, 1.5293202323005406, 30)
# Markers
for i in locations:
     hidden_gem_lat, hidden_gem_lon = i[0], i[1]
     gmap.marker(hidden_gem_lat, hidden_gem_lon, 'y')

gmap.apikey = api_key
gmap.draw(map_html)
gmap.draw(map_whole_html)


#gmap2 = gmplot.GoogleMapPlotter(42.5080882978956, 1.5293202323005406, 30)
for j in cluster_locations:
    hidden_gem_lat, hidden_gem_lon = j[0], j[1]
    gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')
gmap.draw(map_whole_html)



