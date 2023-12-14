import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from PIL import Image
from MyLibrary.preprocessing import preprocessing



#ヒストグラム法
def find_split_point(img):
    histgram_row = []
    histgram_col = []
    height = img.shape[0]
    width = img.shape[1]

    #行のヒストグラム
    row_top_min = 100       #最小値の初期化
    row_top_min_index = 0   #最小値のインデックス
    row_min = 100       #最小値の初期化
    row_min_index = 0   #最小値のインデックス
    row_bottom_min = 50       #最小値の初期化
    row_bottom_min_index = height   #最小値のインデックス
    for i in range(height):
        h = width - np.sum(img[i]) / 255
        histgram_row.append(h)
        if i > 0 and i < 15:    #２０から変更
            if h <= row_top_min:
                row_top_min = h
                row_top_min_index = i
        if i > 30 and i < 60:
            if h <= row_min:
                row_min = h
                row_min_index = i
        if i > 100 and i < 115:
            if h < row_bottom_min:
                row_bottom_min = h
                row_bottom_min_index = i
    print("y split position: ", row_min_index)

    #列のヒストグラム
    t_img = img.T
    print(t_img.shape)
    left_min1 = 100       #最小値の初期化
    left_min1_index = 0   #最小値のインデックス
    left_min = 100       #最小値の初期化
    left_min_index = 0   #最小値のインデックス
    right_min = 100       #最小値の初期化
    right_min_index = 0   #最小値のインデックス
    for i in range(width):
        h = height - np.sum(t_img[i]) / 255
        histgram_col.append(h)
        if i > 0 and i < 20:
            if h < left_min1:
                left_min1 = h
                left_min1_index = i
        if i > 40 and i < 70:
            if h < left_min:
                left_min = h
                left_min_index = i
        if i > 170 and i < 200:
            if h < right_min:
                right_min = h
                right_min_index = i
    print("x split position: ", left_min_index)

    return histgram_row, histgram_col, row_top_min_index, row_min_index, row_bottom_min_index,\
        left_min1_index, left_min_index, right_min_index

def find_split_point_top(img, start_ratio, end_ratio):
    histgram_col = []
    height = img.shape[0]
    width = img.shape[1]

    #列のヒストグラム
    t_img = img.T
    print(t_img.shape)
    left_min = 100       #最小値の初期化
    left_min_index = 0   #最小値のインデックス
    for i in range(width):
        h = height - np.sum(t_img[i]) / 255
        histgram_col.append(h)
        if i > width*start_ratio and i < width*end_ratio:
            if h <= left_min:
                left_min = h
                left_min_index = i
    print("x split position: ", left_min_index)

    return histgram_col, left_min_index

def find_split_point_number(img):
    histgram_col = []
    height = img.shape[0]
    width = img.shape[1]

    #列のヒストグラム
    t_img = img.T
    print(t_img.shape)
    for i in range(width):
        h = height - np.sum(t_img[i]) / 255
        histgram_col.append(h)
    draw_hist_1(img, histgram_col, 0)

    return histgram_col

def split(img, x1, y1, x2, y2):
    sp_img = img[y1:y2, x1:x2]
    #cv2.imshow("splited", sp_img)
    #cv2.waitKey()
    """cv2.imwrite("./images/split/" + "split" +
                str(x1)+str(y1)+str(x2)+str(y2) + '.jpg', sp_img)
    """
    return sp_img

def draw_hist_2(img, histgram_row, histgram_col, row_top_min_index, row_min_index, row_bottom_min_index,\
    left1_min_index, left_min_index, right_min_index):
    height = img.shape[0]
    width = img.shape[1]

    cv2.line(img, (0,row_top_min_index),(width,row_top_min_index), color=(0,0,255))
    cv2.line(img, (0,row_min_index),(width,row_min_index), color=(0,0,255))
    cv2.line(img, (0,row_bottom_min_index),(width,row_bottom_min_index), color=(0,0,255))
    cv2.line(img, (left_min_index,0),(left_min_index,height), color=(0,0,255))
    cv2.line(img, (right_min_index,0),(right_min_index,row_min_index), color=(0,0,255))
    cv2.line(img, (left1_min_index,row_min_index),(left1_min_index,height), color=(0,0,255))

    rcParams['axes.xmargin'] = 0
    rcParams['axes.ymargin'] = 0

    fig, ax = plt.subplots(2,2,
                        gridspec_kw={
                            'width_ratios':[2,1],
                            'height_ratios':[1,1]
                        })

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = Image.fromarray(img)
    ax[0][0].imshow(img)

    y = range(height,0,-1)
    ax[0][1].barh(y, histgram_row, color='gray')
    x = range(width)
    ax[1][0].bar(x, histgram_col, color='gray')

    fig.delaxes(ax[1,1])
    plt.savefig('./images/output_images/hist.jpg')
    plt.clf()
    plt.close()
    #plt.show()

def draw_hist_1(img, histgram_col, left_min_index):
    height = img.shape[0]
    width = img.shape[1]

    cv2.line(img, (left_min_index,0),(left_min_index,height), color=(0,0,255))

    rcParams['axes.xmargin'] = 0
    rcParams['axes.ymargin'] = 0

    fig, ax = plt.subplots(2,1)

    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    img = Image.fromarray(img)
    ax[0].imshow(img)
    x = range(width)
    ax[1].bar(x, histgram_col, color='gray')

    plt.savefig('./images/output_images/hist1.jpg')
    plt.clf()
    plt.close()
    #plt.show()

#テスト##############
"""
file_path = "./images/test_kei/test_7.jpg"
img_width = 240
img_height = 120
img = cv2.imread(file_path)
img = preprocessing(img, img_width=img_width, img_height=img_height)
r_hist, c_hist, r_index, c_index = find_split_point(img)
draw_hist(img, r_hist, c_hist)
split(img, 0, r_index, c_index, img.shape[0])
split(img, c_index, r_index, img.shape[1], img.shape[0])
split(img, c_index, 0, img.shape[1], r_index)
"""