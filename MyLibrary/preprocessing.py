import cv2
import numpy as np

#前処理
def preprocessing(img, img_width, img_height):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (img_width, img_height))
    img = cv2.adaptiveThreshold(img,
                                255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,
                                51, 30)
    original_img = img
    kernel = np.ones((2,2), np.uint8)
    img = cv2.erode(img, kernel, iterations=2)

    return img, original_img