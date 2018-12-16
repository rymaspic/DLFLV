# Why People Gather Together in a City?

![image][image-1]

## Introduction: What is this project and what the project for?

With a combination of telecom data and image data, we could build an more accurate data-driven model of certain city behaviors. In this project we focus on the detection of the "people cluster". 

a simple framework of the project:

![image][image-2]
## Outlines

1. Learning From Las Vegas
2. From Location-Based-Service(LBS) Data To Google-Street-View(GSV)
3. Building The Data-driven Model
4. ...

## Learning From Las Vegas

A book written by Robert Venturi, Denise Scott Brown and Steven Izenour.



## Dataset Building

Codes in GSVScraper/

### 1. The Andorra Data Package

What we have is the data package including one-day's telecom information collected in Andorra, the format is listed in the Sample Json/ :

* "C"  means the cluster information we defined through "Stay Event"
* "UnC" are some random information of places we did not defined to be cluster
* "Timestamp" is the time we collected the data in a format of epoch time
* We also have the information of things like coordinates of the users which is the key part in our project

### 2. Extract the coordinates

Extract the locations we want, codes in extract\_cluster.py and extract\_no\_cluster.py:

* The time that has the largest number of "cluster": 09/15/2016 @ 10:35am (UTC), at that time there exists 31 "clusters" accoding to our telecom data
* We extract the coordinates (the script can avoid the repeated data) with around 1500 "cluster" locations and 5000 "non-cluster" locations, sample Json document is like the testLocations.json
* Call the gmplot library to plot the heat-map of those cluster coordinates so we could visualize the places we collect the GSV images.

(1)cluster-heatmap of Andorra

![image\_heat][image-3]


(2)detailed map: blue markers are cluster locations while yellow are non-clusters

![image\_marker][image-4]


### 3. Google Street View Building

In code GSVScraper.py, through the GSV API we could obtain the street view images of the locations we collected in Step2. The script has automatically detract the "indoor" images and does some basic image preprocessing jobs as soon as we download the GSV images.

**Usage**: 
python3 GSVScraper.py -l __FILE NAME__ -i __ANGLE__ -k __KEY__

Images are labelled into "cluster" or "non-cluster" images and then are used for training a supervised binary classification model.

Through our tests on a very simple Convolutional Neural Network, we found the images in certain angle may not be so accurate for an image may face directly to a wall but the rear area might be a square that easily forms a cluster. So we decide to build a panorama image-dataset instead. 

Sample Prediction Results: the right one is reason for us to use the panorama images:

![image\_marker][image-5]

Panorama image stitching:

![image\_marker][image-6]

Sample Panorama image:
![][image-7]

## Data-driven Model Building

Codes in DL\_Model/

### Train & Test
**Train Usage:**
python3 train.py options: -bc batch_size -ep epoch -t train_image_folder_name -v validation_image_folder_name_
**Test Usage**
python3 test_model.py --m model.model --f test_

Predicted results: (from left to right, probability to be “cluster” increases)

![][image-8]



[image-1]:	https://github.com/rymaspic/DLFLV/blob/master/Images/learning_from_lasvegas.jpg
[image-2]:	https://github.com/rymaspic/DLFLV/blob/master/Images/a%20simple%20framework.png
[image-3]:	https://github.com/rymaspic/DLFLV/blob/master/Images/heatmap.jpg
[image-4]:	https://github.com/rymaspic/DLFLV/blob/master/Images/markermap.png
[image-5]:	https://github.com/rymaspic/DLFLV/blob/master/Images/prediction.png
[image-6]:	https://github.com/rymaspic/DLFLV/blob/master/Images/pano.png
[image-7]:	https://github.com/rymaspic/DLFLV/blob/master/Images/sample_pano.jpg
[image-8]:	https://github.com/rymaspic/DLFLV/blob/master/Images/prediected%20results.png