from operator import itemgetter

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def split(img):
    original_img = img
    minlength = img.shape[0] * 0.1
    lines = []
    sp_img_list = []

    #ハフ変換(縦線)
    lines = cv2.HoughLinesP(img, rho=1, theta=1, threshold=1, minLineLength=minlength, maxLineGap=0)

    line_list = [(0,img.shape[0], 0, 0)]
    k = 3
    judgelength = img.shape[0] * 0.8
    isLine = False
    #検出した縦線を描画
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x1 - x2) <= k and abs(y1 - y2) >= judgelength:
            isLine = True
            blackline = 1
            lineadd_img = cv2.line(img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 0), blackline)
            x1 = line[0][0]
            y1 = line[0][1]
            x2 = line[0][2]
            y2 = line[0][3]
            line = (x1, y1, x2, y2)
            line_list.append(line)
    #line_list.append((img.shape[1],img.shape[0], img.shape[1], 0))
    if isLine:
        line_list.sort(key=itemgetter(0, 1, 2, 3))
        # cv2.imshow(" ", lineadd_img)
        # cv2.waitKey()

        line_count = 0
        x1 = line_list[0][0]
        for line in line_list:
            judge_x1 = line[0]
            judge_x2 = line[2]
            if abs(judge_x1 - x1) != 0:
                if abs(x1-judge_x1) < 4:
                    x1 = judge_x1
                else:
                    line_count = line_count + 1
                    x2 = judge_x2
                    sp_img = original_img[1:, x1+1:x2]
                    sum_sp_img = np.sum(sp_img)
                    #if judge_x1 < img.shape[1] * 0.95:
                        #黒の割合が1割以下のもの（ハイフンとかノイズ）はスキップ
                    if sum_sp_img < sp_img.shape[0] * sp_img.shape[1] * 255 * 0.85:
                        if x1 < img.shape[1] * 0.9:
                            #幅10の余白を追加
                            sp_img = cv2.copyMakeBorder(sp_img,5,5,10,10,cv2.BORDER_CONSTANT,value=[255,255,255])
                            sp_img_list.append(sp_img)
                    #print(sp_img)
                    # cv2.imshow("", sp_img)
                    # cv2.waitKey()
                    x1 = judge_x1
    else:
        print("線が見つかりませんでした．")

    return sp_img_list

def draw_images(sp_img_list, name):
    fig, ax = plt.subplots(1,len(sp_img_list), tight_layout=True)
    for index, i in enumerate(sp_img_list):
        i = cv2.cvtColor(i, cv2.COLOR_GRAY2RGB)
        pil_img = Image.fromarray(i)
        ax[index].imshow(pil_img)
    plt.savefig(f'./{name}.jpg')
    #plt.show()