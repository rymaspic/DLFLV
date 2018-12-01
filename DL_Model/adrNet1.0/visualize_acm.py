from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import decode_predictions
import matplotlib.image as mpimg
from keras import backend as K
from keras import models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def cam(img_path):
    from keras.applications.vgg16 import VGG16
    from keras import backend as K
    import matplotlib.pyplot as plt
    from keras.preprocessing import image as Image
    import cv2
    K.clear_session()
    model = models.load_model("models/adr_cnn1.h5")
    model.summary()
    img = cv2.imread(img_path)
    img = cv2.resize(img, (256, 256))
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
    #label = "no cluster" if preds < 0.5 else "cluster"
    argmax = np.argmax(preds[0])
    #print(argmax)
    output = model.output[:, argmax]
    print(output)
    #output = model.output[:, ]
    last_conv_layer = model.get_layer('conv2d_3')
    #print(last_conv_layer)
    grads = K.gradients(output, last_conv_layer.output)[0]
    print(grads)
    #print(grads)
    pooled_grads = K.mean(grads, axis=(0,1,2))
    iterate = K.function([model.input], [pooled_grads, last_conv_layer.output[0]])
    pooled_grads_value, conv_layer_output_value = iterate([x])
    print(pooled_grads_value)
    print(conv_layer_output_value)
    for i in range(pooled_grads_value.shape[0]):
        conv_layer_output_value[:, :, i] *= pooled_grads_value[i]
    heatmap = np.mean(conv_layer_output_value, axis=-1)
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)
    import cv2
    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    hif = .8
    superimposed_img = heatmap * hif + img
    output = 'sample.jpg'
    cv2.imwrite(output, superimposed_img)
    img = mpimg.imread(output)
    plt.imshow(img)
    plt.axis('off')
    plt.title(label)
    plt.show()
    return None


# img_path = 'image_data/data_nopano/test/cluster/test_cluster1.jpg'
# img=mpimg.imread(img_path)
# plt.imshow(img)
# plt.show()
cam('image_data/data_nopano/test/cluster/test_cluster1.jpg')
