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
ap.add_argument("-m", "--model", required=True,
                help="path to trained model model")
ap.add_argument("-f", "--folder", required=True,
                help="path to test folder")
args = vars(ap.parse_args())

# makes folder for results
classFolder = r"predicted"
if not os.path.exists(classFolder):
    os.makedirs(classFolder)


folderPaths = sorted(list(paths.list_images(args["folder"])))
counter = 0
count_cluster = 0 # counting the images labeled to "cluster"

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])

# loop over the input images
for imagePath in folderPaths:
    # load the image

    image = cv2.imread(imagePath)
    #image.imshow()
    #cv2.imshow('image', image)
    orig = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (200, 1000))
    image = image.astype("float") / 255.0
    image = Image.img_to_array(image)
    image = np.expand_dims(image, axis=0)


    # classify the input image
    print(model.predict(image))
    a = model.predict(image)[0]
    # print(a, b)
    # build the printed label
    label = "no cluster" if a < 0.5 else "cluster"
    if label == "cluster":
        count_cluster = count_cluster + 1
    proba = 1-a if a < 0.5 else a
    # label = "{}: {:.2f}%".format(label, proba * 100)
    # made a few revision, confused by this format tranfering
    label = label + str(proba * 100) + "%"

    # draw the label on the image
    output = imutils.resize(orig, width=1000 , height = 200)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)
    finalImg = cv2.imwrite("predicted/" + str(counter) +
                           "_" + str(int(proba*100))+".jpg", output)
    counter += 1

print("The test accuracy: " + str(count_cluster/counter))



    #show the output image
    #cv2.imshow("Output", output)
    #cv2.waitKey(0)
