from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import decode_predictions
import matplotlib.image as mpimg
from keras import backend as K
from keras import models
import matplotlib.pyplot as plt
import numpy as np
from keras import backend as K
import matplotlib.pyplot as plt
from keras.preprocessing import image as Image
import cv2
import os
import argparse
# python3 visualize_cam.py -model The Model for visualizing CAM
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-input", "--input_imgs", required=False, default= "predicted/cam_cluster",
                help="directory name that contains all the images")
ap.add_argument("-output", "--output_imgs", required=False, default= "cam",
                help="directory name that contains all the output CAM images")
ap.add_argument("-model", "--model", required=True,
                help="The model we use for visualizing CAM")

args = vars(ap.parse_args())
imgs_path = args["input_imgs"]
out_path = args["output_imgs"]

def cam(img_path,output_path):
    K.clear_session()
    #config = model.get_config()
    #print(model)
    # model = model.from_config(config)
    #model = models.load_model("adr_model_12.6.h5")
    model = args["model"]
    #model.summary()
    img = cv2.imread(img_path)
    img = cv2.resize(img, (512, 512))
    img = img.astype("float") / 255.0
    #img = img.astype("float") / 255.0
    x = Image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # from keras.applications.vgg16 import preprocess_input
    # img = preprocess_input(img)
    #print(x.shape)
    preds = model.predict(x)[0]
    label = "no cluster" if preds < 0.5 else "cluster"
    print(preds)
    # we could set certain therhold for out put the cam. eg.visualize those who have more than 80%
    #label = "no cluster" if preds < 0.5 else "cluster"
    argmax = np.argmax(preds[0])
    #print(argmax)
    output = model.output[:, argmax]
    #print(output)
    #output = model.output[:, ]
    last_conv_layer = model.get_layer('conv2d_3')
    #print(last_conv_layer)
    grads = K.gradients(output, last_conv_layer.output)[0]
    #print(grads)
    #print(grads)
    pooled_grads = K.mean(grads, axis=(0,1,2))
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
    pooled_grads_value, conv_layer_output_value = iterate([x])
    #print(pooled_grads_value)
    #print(conv_layer_output_value)
    for i in range(pooled_grads_value.shape[0]):
        conv_layer_output_value[:, :, i] *= pooled_grads_value[i]
    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    hif = .8
    superimposed_img = heatmap * hif + img
    output = output_path
    cv2.imwrite(output, superimposed_img)
    img = mpimg.imread(output)
    plt.figure()
    plt.imshow(superimposed_img)
    plt.axis('off')
    plt.title(label)
    #plt.show()
    print("start saving")
    #plt.savefig(output)
    return None


# img_path = 'image_data/data_nopano/test/cluster/test_cluster1.jpg'
# img=mpimg.imread(img_path)
# plt.imshow(img)
# plt.show()
#model = models.load_model()
#makes folder for results
classFolder = args["output"]
if not os.path.exists(classFolder):
    os.makedirs(classFolder)


#model = models.load_model("adr_model_12.6.h5")

for image in os.listdir(imgs_path):
    path = os.path.join(imgs_path,image)
    if cv2.imread(path) is not None:
        print(path)
        print(out_path + '/' + str(image))
        cam(path,out_path + '/' + str(image))
    else:
        pass

