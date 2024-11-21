import tensorflow as tf
import cv2
import numpy as np
from keras.applications.vgg16 import preprocess_input   # type: ignore
import time

model = tf.keras.models.load_model("./myModels/num_model(e)3", compile=False)
print("load model")
# img = cv2.imread('./zero.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# @tf.function(reduce_retracing=True)
def rc_num(img):
    # print(type(img))
    # img = 255 - img
    img_width = 32
    img_height = 54
    img = cv2.resize(img, (img_width,img_height))
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    """ノイズを取り除く"""
    histgram_row = []
    histgram_col = []

    #行のヒストグラム
    row_top_min = 100       #最小値の初期化
    row_top_min_index = 0   #最小値のインデックス
    row_min = 100       #最小値の初期化
    row_min_index = 0   #最小値のインデックス
    row_bottom_min = 50       #最小値の初期化
    row_bottom_min_index = img_height   #最小値のインデックス
    for i in range(img_height):
        h = img_width - np.sum(img[i]) / 255
        histgram_row.append(h)
        if i > 0 and i < int(img_height*0.1):    #２０から変更
            if h <= row_top_min:
                row_top_min = h
                row_top_min_index = i
        if i > int(img_height*0.9) and i < img_height:
            if h < row_min:
                row_min = h
                row_min_index = i

    img = img[row_top_min_index:row_min_index, 0:img_width]
    img = cv2.resize(img, (img_width,img_height))
    img = cv2.medianBlur(img, 3)

    img = preprocess_input(img)

    # cv2.imshow("",img)
    # cv2.waitKey()

    img_expand = np.expand_dims(img, axis=0)
    # probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    # predictions = probability_model.predict(img)
    start = time.time()
    predictions = model(img_expand, training=False)
    # print(predictions)
    end = time.time()
    # print(end-start, "s")

    #信頼度について，最大と２番目を調べる．
    max, max_2nd = 0, 0
    max_index, max_2nd_index = 0, 0
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
    print(f'{max_index}, {max}')
    print(f'{max_2nd_index}, {max_2nd}')
    print('=================================')
    EPS = 0.1
    # if max - max_2nd < EPS:
    if max < 0.5:
        kernel = np.ones((2,2), np.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        # img = cv2.GaussianBlur(img, (3,3),-1)
        #もう一度認識
        return rc_num(img)
    else:
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