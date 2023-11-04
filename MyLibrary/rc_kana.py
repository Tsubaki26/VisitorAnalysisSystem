import tensorflow as tf
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

model = tf.keras.models.load_model("./myModels/kana_model1", compile=False)
# img = cv2.imread('./zero.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kana_list = ["あ","い","う","え","か","き","く","け","こ","さ","す","せ","そ",
             "た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ",
             "ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ",
             "ろ","わ","を"]
def rc_kana(img):
    #img = 255 - img
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(img)
    #print(predictions)

    return kana_list[np.argmax(predictions)]