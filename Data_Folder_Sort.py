# This is a script for creating the directory form we use for DL training
# After downloaded images in GSV, run this script (make some changes accordingly) to form:

"""
/data
    /train
        /cluster
        /non_cluster
    /val
        /cluster
        /non_cluster
    test/
        /cluster
        /non_cluster
"""



import os, sys, shutil

# number of samples
train = 8000
val = 2000
test = 1000
# os.listdir will shuffle samples

cluster_source_folder = "GSVscraper/images/cluster"

if os.path.exists(cluster_source_folder + ".DS_Store"):
    os.remove(cluster_source_folder + ".DS_Store")
else:
    print(".DS_Store does not exist")

non_cluster_source_folder = "GSVscraper/images/no_cluster"

if os.path.exists(non_cluster_source_folder + ".DS_Store"):
    os.remove(non_cluster_source_folder + ".DS_Store")
else:
    print(".DS_Store does not exist")

cluster_image_list = os.listdir(cluster_source_folder)
non_cluster_image_list = os.listdir(non_cluster_source_folder)


counter = 0
train_counter = 0
val_counter = 0
test_counter = 0

for image in cluster_image_list:
    #print(image)
    image_path = os.path.join(cluster_source_folder, image)
    counter = counter + 1
    if counter >= 1 and counter <= train:
        train_counter = train_counter + 1
        train_cluster_des = "DL_Model/adrNet1.0/image_data/data_12.3/train/clusters/" + str(train_counter) + '.jpg'
        shutil.copy(image_path, train_cluster_des)
        #print(train_cluster_des)

    elif counter >= (1 + train) and counter <= (train + val):
        val_counter = val_counter + 1
        val_cluster_des = "DL_Model/adrNet1.0/image_data/data_12.3/val/clusters/" + str(val_counter) + '.jpg'
        shutil.copy(image_path, val_cluster_des)
        #print(val_cluster_des)
        #shutil.copy(image_path, des)
    elif counter >= (1 + train + val) and counter <= (train + val + test):
        test_counter = test_counter + 1
        test_cluster_des = "DL_Model/adrNet1.0/image_data/data_12.3/test/clusters/" + str(test_counter) + '.jpg'
        shutil.copy(image_path, test_cluster_des)
        #print(test_cluster_des)
        #shutil.copy(image_path, des)
    #print(test_counter)


counter = 0
train_counter = 0
val_counter = 0
test_counter = 0

for image in non_cluster_image_list:
    #print(image)
    nc_image_path = os.path.join(non_cluster_source_folder, image)
    counter = counter + 1
    if counter >= 1 and counter <= train:
        train_counter = train_counter + 1
        train_non_cluster_des = "DL_Model/adrNet1.0/image_data/data_12.3/train/no_clusters/" + str(train_counter) + '.jpg'
        shutil.copy(nc_image_path, train_non_cluster_des)
        #print(train_non_cluster_des)

    elif counter >= (1 + train) and counter <= (train + val):
        val_counter = val_counter + 1
        val_non_cluster_des = "DL_Model/adrNet1.0/image_data/data_12.3/val/no_clusters/" + str(val_counter) + '.jpg'
        #print(val_non_cluster_des)
        shutil.copy(nc_image_path, val_non_cluster_des)
    elif counter >= (1 + train + val) and counter <= (train + val + test):
        test_counter = test_counter + 1
        test_non_cluster_des = "DL_Model/adrNet1.0/image_data/data_12.3/test/no_clusters/" + str(test_counter) + '.jpg'
        #print(test_non_cluster_des)
        #print(test_counter)
        shutil.copy(nc_image_path, test_non_cluster_des)
    #print(test_counter)
