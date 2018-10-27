import json
from pprint import pprint

#parameters:
rate = 0.6 # the percentage of locations we sample at each cluster

# Open the Json Document And Load the Datas
with open('Sample JSON/20160915_clustering_clusters_R30_P15_simple.json','r') as f:
    data = json.load(f)
#Define the sorting function based on the number of clusters each time
sorting_function = lambda time: len(time)
max_cluster = max(data["C"].values(), key = sorting_function)
#pprint(max_cluster)

# A function to extract the key of the dictionary
def get_keys(d, value):
    return [k for k, v in d.items() if v == value]

# Get the time
max_time = get_keys(data["C"], max_cluster)
pprint("The Time That Has The Biggest Number of Clusters:")
pprint(max_time)
pprint("At that time, the number of clusters are:")
pprint(len(max_cluster))

# def sample_number(cluster,rate = 0.1):
#     total_coord_numbers = len(cluster["coord"])
#     return int(rate*total_coord_numbers)

locations = []
total_sample_numbers = 0


# def deleteDuplicatedElementFromLis(one_list):
#     return list(set(one_list))
#
# a = [2,2,6]

#print(deleteDuplicatedElementFromLis(a))

for index_c in max_cluster.values():
    #sample_seed = sample_number(index_c, 0.2)
    #print(index_c['coord'])
    sample_seed  = int(rate * len(index_c["coord"]))
    total_sample_numbers = total_sample_numbers + sample_seed
    i = 0
    while sample_seed:
        #i = len(index_c["coord"]) - 1
        if index_c["coord"][i] not in locations: #make sure we do not append a replicated coord
            locations.append(index_c["coord"][i])
            #locations.append('\n')
            sample_seed = sample_seed - 1
        # else:
        #     print("cfffff")
        i = i + 1

#locations = deleteDuplicatedElementFromList(locations)

pprint(total_sample_numbers)

pprint(locations)
dict = {"train_cluster":locations}

# with open('train_c_locations_new.json','w') as w:
#     json.dump(dict,w)








