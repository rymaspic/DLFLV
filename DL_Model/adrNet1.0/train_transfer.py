from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,Model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import applications
from keras import backend as K
import matplotlib.pyplot as plt
import argparse
from keras.utils.vis_utils import plot_model

# USAGE
# python3 train_transfer.py options: -bc batch_size -ep epoch -t train_image_folder_name -v validation_image_folder_name


############################ Parameter Defining ##############################
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-bc", "--batch_size", default = 10,
                help="batch size for training")
ap.add_argument("-ep", "--epoch", default = 25,
                help="training epochs")
ap.add_argument("-t", "--train_images", default = 'image_data/data_pano/train',
                help="train images folder name")
ap.add_argument("-v", "--validation_images", default = 'image_data/data_pano/validation',
                help="validation images folder name")
# ap.add_argument("-m", "--model_name_to_save", default = 'adr_pano_1.0',
#                 help="model_name_to_save")
args = vars(ap.parse_args())

# dimensions of our images.
img_width, img_height = 1000, 200
# paths of train data and validation
train_data_dir = args["train_images"]
validation_data_dir = args["validation_images"]

nb_train_samples = 560
    #len(os.listdir(args["train_images"]))
nb_validation_samples = 140
    #len(os.listdir(args["validation_images"]))

epochs = args["epoch"] # training times, I found after around 10 the increase of accuracy is very limited
batch_size = args["batch_size"] # number of samples for training per time

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)


############################ Data Loader #####################################
# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    vertical_flip=True,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')


############################ Model Building #####################################
model = applications.VGG19(weights = "imagenet", include_top=False, input_shape = input_shape)
# Freeze the layers which you don't want to train. Here I am freezing the first 5 layers.
for layer in model.layers[:5]:
    layer.trainable = False
# Output layers, flatten and dropout to avoid the regulation
x = model.output
x = Flatten()(x)
x = Dense(64,activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(64,activation="relu")(x)
prediction = Dense(1,activation='sigmoid')(x)
model = Model(input = model.input, output = prediction)
# print the whole model
model.summary()
plot_model(model, to_file='model.png')
# stimulate the loss,optimal funcs
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

#  option: if you want to start from the training result last time, load the past weights
#model.load_weights('adr_simple.h5')

history = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

# list all data in history
print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# save_weights only save the weights
# model.save_weights('adr_panocnn2.h5')
# save will save the whole net and weights
# I also wrote a weights2model script if you forget save the model while saved the weights
model.save('adr_pano_vgg19.h5')