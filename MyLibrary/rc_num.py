import tensorflow as tf
import cv2
import numpy as np
from keras.applications.vgg16 import preprocess_input

model = tf.keras.models.load_model("./myModels/num_model(e)1", compile=False)
# img = cv2.imread('./zero.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# @tf.function(reduce_retracing=True)
def rc_num(img):
    print(type(img))
    img = 255 - img
    img = cv2.resize(img, (32,32))
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #cv2.imshow("",img)
    #cv2.waitKey()
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(img)
    print(predictions)

    return np.argmax(predictions), predictions

def rc_num_list(img_list):
    result = ""
    for img in img_list:
        img = 255 - img
        img = cv2.resize(img, (28,28))
        img = np.expand_dims(img, axis=0)
        probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
        predictions = probability_model.predict(img)
        result += str(np.argmax(predictions))
    return result