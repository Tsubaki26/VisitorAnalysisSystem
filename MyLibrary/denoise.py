from operator import itemgetter

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def denoise(img,left,right,top,bottom):
    img = split(img,left,right, 0.5)
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = split(img,top,bottom, 0.95)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

def split(img,left,right, judgelength_rate):
    # print("split!!!!!!!!")
    original_img = img
    img_h = img.shape[0]
    img_w = img.shape[1]
    minlength = img_w * 0.1
    lines = []
    sp_img_list = []

    #ハフ変換
    lines = cv2.HoughLinesP(img, rho=1, theta=1, threshold=1, minLineLength=minlength, maxLineGap=0)

    line_list_t = [(0,img_w, 0, 0)]
    k = 3
    judgelength = img_h * judgelength_rate
    isLine_t = False
    split_sizes = []
    #検出した縦線を描画
    for line in lines:
        x1, y1, x2, y2 = line[0]
        #縦線
        if abs(x1 - x2) <= k and abs(y1 - y2) >= judgelength \
            and (x1 < img_w * left or x1 > img_w * right):
            isLine_t = True
            blackline = 1
            lineadd_img_t = cv2.line(img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (50, 50, 0), blackline)
            x1 = line[0][0]
            y1 = line[0][1]
            x2 = line[0][2]
            y2 = line[0][3]
            line = (x1, y1, x2, y2)
            line_list_t.append(line)

    line_list_t.append((img_w, 0, img_w, img_h))
    # cv2.imshow(" ", lineadd_img_t)
    # cv2.waitKey()


    #切り取り（縦）
    if isLine_t:
        line_list_t.sort(key=itemgetter(0, 1, 2, 3))
        line_count = 0
        x1 = line_list_t[0][0]
        for line in line_list_t:
            #line : (x1, y1, x2, y2)
            judge_x1 = line[0]
            judge_x2 = line[2]
            if abs(judge_x1 - x1) != 0:
                if abs(x1-judge_x1) < 4:
                    x1 = judge_x1
                else:
                    print("aaaa, x1:{}".format(x1))
                    split_sizes.append(abs(x1-judge_x1))
                    line_count = line_count + 1
                    x2 = judge_x2
                    print("x1,x2:{},{}".format(x1,x2))
                    sp_img = original_img[1:, x1+1:x2]
                    sp_img_list.append(sp_img)
                    x1 = judge_x1
    # print(split_sizes)
    if split_sizes != []:
        img = sp_img_list[np.argmax(split_sizes)]
    else:
        img = original_img

    return img