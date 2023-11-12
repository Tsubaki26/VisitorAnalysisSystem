import tensorflow as tf
import cv2
import numpy as np
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.vgg16 import preprocess_input

model = tf.keras.models.load_model("./myModels/area_model(e)1", compile=False) #compile=Falseをつけないとなぜかエラーになる．
area_list = ['山口', '岡山', '島根', '広島', '鳥取']

def rc_area(img):
    #img = 255 - img
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(img, (100, 50))
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    # probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    # predictions = probability_model.predict(img)
    """
    https://www.tensorflow.org/api_docs/python/tf/keras/Model#predict  ↓
    predictの処理はバッチ処理で行うので大量データの予測もできるけど、入力データが少ない場合はバッチ処理がボトルネックになる。
    predictは時間がかかるから直接 model(x)で予測する．
    """
    predictions = model(img,training=False)
    # print(predictions)
    result = area_list[np.argmax(predictions)]

    print(result)
    return result

if __name__ == '__main__':
    image = cv2.imread('./../images/test_195.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=2)
    cv2.imshow("",image)
    cv2.waitKey()
    rc_area(image)