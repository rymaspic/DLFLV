# USAGE
# python3 test_model.py --m model.model --f test

# import the necessary packages
from keras.preprocessing import image as Image
from keras.models import load_model
import numpy as np
import argparse
import imutils
from imutils import paths
import cv2
# file handaling
import os

# for stoping
import sys  # sys.exit("Error message")


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", default = 'models/adrnet.h5',
                help="path to trained model")
ap.add_argument("-f1", "--folder1", default = 'image_data/data_12.3/test/clusters',
                help="path to test folder")
ap.add_argument("-f2", "--folder2", default = 'image_data/data_12.3/test/no_cluster',
                help="path to test folder")
args = vars(ap.parse_args())

# makes folder for results
classFolder = r"predicted/nc"
if not os.path.exists(classFolder):
    os.makedirs(classFolder)


folderPaths1 = sorted(list(paths.list_images(args["folder1"])))
folderPaths2 = sorted(list(paths.list_images(args["folder2"])))
counter1 = 0
counter2 = 0
count_right1 = 0
count_right2 = 0
# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])
model.summary()

# loop over the input images
for imagePath in folderPaths1:
    # load the image

    image = cv2.imread(imagePath)
    #image.imshow()
    #cv2.imshow('image', image)
    orig = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (512, 512))
    #image = cv2.resize(image, (200, 1000))
    image = image.astype("float") / 255.0
    image = Image.img_to_array(image)
    image = np.expand_dims(image, axis=0)


    # classify the input image
    print(model.predict(image))
    a = model.predict(image)[0]
    # print(a, b)
    # build the printed label
    label = "no cluster" if a > 0.5 else "cluster"
    flag = "1_" # 0 means predicted right , 1 means wrong
    if label == "cluster":
        count_right1 = count_right1 + 1
        flag = "0_"
    proba = 1-a if a < 0.5 else a
    # label = "{}: {:.2f}%".format(label, proba * 100)
    # made a few revision, confused by this format tranfering
    label = label + str(proba * 100) + "%"

    # draw the label on the image
    # output = imutils.resize(orig, width=1000 , height = 200)
    output = imutils.resize(orig, width=512, height=512)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
    finalImg = cv2.imwrite("predicted/c/" + flag + str(counter1) +
                           "_" + str(int(proba*100))+".jpg", output)
    counter1 += 1
#print("The test accuracy: " + str(count_right1/counter1))

for imagePath in folderPaths2:
    # load the image

    image = cv2.imread(imagePath)
    #image.imshow()
    #cv2.imshow('image', image)
    orig = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (512, 512))
    #image = cv2.resize(image, (200, 1000))
    image = image.astype("float") / 255.0
    image = Image.img_to_array(image)
    image = np.expand_dims(image, axis=0)


    # classify the input image
    print(model.predict(image))
    a = model.predict(image)[0]
    # print(a, b)
    # build the printed label
    flag = "1_"  # 0 means predicted right , 1 means wrong
    label = "no cluster" if a > 0.5 else "cluster"
    if label == "no cluster":
        count_right2 = count_right2 + 1
        flag = "_0"
    proba = 1-a if a < 0.5 else a
    # label = "{}: {:.2f}%".format(label, proba * 100)
    # made a few revision, confused by this format tranfering
    label = label + str(proba * 100) + "%"

    # draw the label on the image
    # output = imutils.resize(orig, width=1000 , height = 200)
    output = imutils.resize(orig, width=512, height=512)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
    finalImg = cv2.imwrite("predicted/nc/" + flag + str(counter2) +
                           "_" + str(int(proba*100))+".jpg", output)
    counter2 += 1

#print("The test accuracy: " + str(count_cluster/counter))

print("The test accuracy: ", (count_right1 + count_right2)/(counter1 + counter2))




    #show the output image
    #cv2.imshow("Output", output)
    #cv2.waitKey(0)
