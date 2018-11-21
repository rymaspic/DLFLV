# Why People Gather Together in a City?

![image](https://github.com/rymaspic/DLFLV/blob/master/Images/learning_from_lasvegas.jpg)

##Inroduction: What is this project and what the project for?

A combination of telecom data and image data, we could build a accurater data-driven model of certain city behaviors. In this project we focus on the detection of the "people cluster". (...)

## Outlines

1. Learning From Las Vegas
2. When Telecom Dances With Computer Vision: From Location-Based-Service(LBS) Data To Google-Street-View(GSV)
3. Building The Data-driven Model
  <<<<<<< HEAD
4. ...

## Learning From Las Vegas

...

## Dataset Building

Codes in GSVScraper/

###1. The Andorra Data Package

What we have is the data package including one-day's telecom information collected in Andorra, the format is listed in the Sample Json/ :

* "C"  means the cluster information we defined through "Stay Event"
* "UnC" are some random information of places we did not defined to be cluster
* "Timestamp" is the time we collected the data in a format of epoch time
* We also have the information of things like coordinates of the users which is the key part in our project

### 2. Extract the coordinates

Extract the locations we want, codes in extract_cluster.py and extract_no_cluster.py:

* The time that has the largest number of "cluster": 09/15/2016 @ 10:35am (UTC), at that time there exists 31 "clusters" accoding to our telecom data
* We extract the coordinates (the script can avoid the repeated data) with around 1500 "cluster" locations and 5000 "non-cluster" locations, sample Json document is like the testLocations.json
* Call the gmplot library to plot the heat-map of those cluster coordinates so we could visualize the places we collect the GSV images.

### 3. Google Street View Building

In code GSVScraper.py, through the GSV Api we could obtain the street view images of the locations we collected in Step2. The script has automatically detract the "indoor" images and does some basic image preprocessing jobs as soon as we download the GSV images.

Images are labelled into "cluster" or "non-cluster" images and then are used for training a supervised binary classification model.

Through our tests on a very simple Convoultional Neural Network, we found the images in certain angle may not be so accurate for an image may face directly to a wall but the rear area might be a square that easily forms a cluster. So we decide to build a panorama image-dataset instead. 

To change images from different angles of a camera to a single panorama image, we could use some OpenCV script or use some professional software like PtGUI which is good in batch processing. We are still working on this and trying to find the perfect results.




