import tensorflow as tf
import cv2
import numpy as np
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.vgg16 import preprocess_input

model = tf.keras.models.load_model("./myModels/area_model(e)2", compile=False) #compile=Falseをつけないとなぜかエラーになる．
area_list = ['下関', '倉敷', '出雲', '山口', '岡山', '島根', '広島', '福山', '鳥取']

def rc_area(img):
    #img = 255 - img
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(img, (100, 50))
    img = preprocess_input(img)
    img_expand = np.expand_dims(img, axis=0)
    # print(img.shape)
    # probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    # predictions = probability_model.predict(img)
    """
    https://www.tensorflow.org/api_docs/python/tf/keras/Model#predict  ↓
    predictの処理はバッチ処理で行うので大量データの予測もできるけど、入力データが少ない場合はバッチ処理がボトルネックになる。
    predictは時間がかかるから直接 model(x)で予測する．
    """
    predictions = model(img_expand,training=False)
    # print(predictions)
    result = area_list[np.argmax(predictions)]

    #信頼度
    confidence = np.max(predictions) * 100

    #信頼度について，最大と２番目を調べる．
    max, max_2nd = 0, 0
    max_index, max_2nd_index = 0, 0
    '''
    # print(predictions)
    for index, pr in enumerate(predictions[0]): #predictions: (1,42)
        if pr > max:
            max_2nd = max
            max = pr
            max_2nd_index = max_index
            max_index = index
        elif pr > max_2nd:
            max_2nd = pr
            max_2nd_index = index
    print('信頼度============================')
    print(f'{area_list[max_index]}, {max}')
    print(f'{area_list[max_2nd_index]}, {max_2nd}')
    print('=================================')
    '''
    # EPS = 0.1
    # if max - max_2nd < EPS:
    # if max < 0.7:
        # kernel = np.ones((2,2), np.uint8)
        # img = cv2.erode(img, kernel, iterations=1)
        # img = cv2.GaussianBlur(img, (3,3),-1)
        #もう一度認識
        # return rc_area(img)
    # else:
    return result, confidence

if __name__ == '__main__':
    image = cv2.imread('./../images/test_195.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2,2), np.uint8)
    image = cv2.erode(image, kernel, iterations=2)
    cv2.imshow("",image)
    cv2.waitKey()
    rc_area(image)