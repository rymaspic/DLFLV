# Functions that may be helpful in Deep Learning process
# USAGE: install relevant library in Python
# 1. pip install split-folders
# 2. vis

# 1. split images in a whole folder into train/validation/test set
import split_folders
# Split with a ratio.
# To only split into training and validation (/test) set, set a tuple to `ratio`, i.e, `(.8, .2)`.
split_folders.ratio('input_folder', output="output", seed=1337, ratio=(.8, .1, .1)) # default values


# 2. filter_visualization
# visualize the activation maps of the network so we could tell what exactly it learned
from keras import models
#https://www.analyticsvidhya.com/blog/2018/03/essentials-of-deep-learning-visualizing-convolutional-neural-networks/
model = models.load_model("models/adr_cnn1.h5")
model.summary()

from vis.visualization import visualize_activation
from vis.utils import utils


from matplotlib import pyplot as plt
#matplotlib inline
plt.rcParams['figure.figsize'] = (18, 6)

# Utility to search for layer index by name.
# Alternatively we can specify this as -1 since it corresponds to the last layer.
layer_idx = utils.find_layer_idx(model, 'dense_2')

# This is the output node we want to maximize.
filter_idx = 0
img = visualize_activation(model, layer_idx, filter_indices=filter_idx)
plt.imshow(img[..., 0])
plt.imsave("test.png")

