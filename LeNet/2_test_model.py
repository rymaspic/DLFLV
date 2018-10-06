# USAGE
# python3 2_test_model.py --m model.model --f test

# import the necessary packages
from keras.preprocessing.image import img_to_array
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
classFolder = r"final"
if not os.path.exists(classFolder):
    os.makedirs(classFolder)


folderPaths = sorted(list(paths.list_images(args["folder"])))
counter = 0

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model(args["model"])

# loop over the input images
for imagePath in folderPaths:
    # load the image

    image = cv2.imread(imagePath)
    orig = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (28, 28))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # classify the input image
    (a, b) = model.predict(image)[0]
    print(a, b)
    # build the printed label
    label = "not" if a > b else "sq"
    proba = a if a > b else b
    label = "{}: {:.2f}%".format(label, proba * 100)

    # draw the label on the image
    output = imutils.resize(orig, width=200)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)
    finalImg = cv2.imwrite("final/" + str(counter) +
                           "_" + str(int(proba*100))+".jpg", output)
    counter += 1

    # show the output image
    # cv2.imshow("Output", output)
    # cv2.waitKey(0)
