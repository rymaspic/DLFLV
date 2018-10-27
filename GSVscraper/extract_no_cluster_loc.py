import json
from pprint import pprint

with open('Sample JSON/20160915_clustering_clusters_R30_P15_simple.json','r') as f:
    data = json.load(f)

#['1473935700']
#pprint(data["C"]["1473907200"]["C86"]["meanCoord"])

total_train_location = 1000
locations = []
total_loc_number = 0
# for index_time in data["UnC"].values():
#     while total_train_location:
#         for index_c in index_time.values():
#             if index_c["coord"] not in locations: #make sure we do not append a replicated coord
#                 locations.append(index_c["coord"])
#                 total_train_location = total_train_location - 1

            #locations.append(index_c["coord"])


for index in data["UnC"]["1473935700"]["coord"]:
    while total_train_location:
        if index not in locations:
            locations.append(index)
            total_loc_number = total_loc_number + 1
            total_train_location = total_train_location - 1
            break
        else:
            break

pprint(total_loc_number)
pprint(locations)
dict = {"train_nocluster":locations}

with open('train_nc_locations.json','w') as w:
    json.dump(dict,w)










