import tensorflow as tf
import cv2
import numpy as np
from keras.applications.vgg16 import preprocess_input

model = tf.keras.models.load_model("./myModels/kana_model(e)1", compile=False)
# img = cv2.imread('./zero.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kana_list = ["あ","い","う","え","か","き","く","け","こ","さ","す","せ","そ",
             "た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ",
             "ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ",
             "ろ","わ","を"]
def rc_kana(img):
    #img = 255 - img
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(img, (54, 54))
    img = preprocess_input(img)
    img_expand = np.expand_dims(img, axis=0)
    # print(img.shape)
    # probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    # predictions = probability_model.predict(img)
    predictions = model(img_expand, training=False)
    #print(predictions)

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
    print(f'{kana_list[max_index]}, {max}')
    print(f'{kana_list[max_2nd_index]}, {max_2nd}')
    print('=================================')
    EPS = 0.1
    # if max - max_2nd < EPS:
    if max < 0.7:
        # kernel = np.ones((2,2), np.uint8)
        # img = cv2.erode(img, kernel, iterations=1)
        img = cv2.GaussianBlur(img, (3,3),-1)
        #もう一度認識
        return rc_kana(img)
    else:
        return kana_list[np.argmax(predictions)]