from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import cv2
import numpy as np
from matplotlib import pyplot as plt
from test_data import test_annotation2 as ta

import glob
import natsort
import difflib
import time

#自作ライブラリ
from recognition import NPrecognition_v3 as npr



for dark in range(10, 240, 10):
    file_path_list = []
    files = glob.glob('./images/dark/test_images_2_dark_{}/*.jpg'.format(dark))
    # files = glob.glob('./images/dark_top/test_images_2_dark_top_{}/*.jpg'.format(dark))
    for i in natsort.natsorted(files):
        file_path_list.append(i)

    correct_area = 0
    correct_num1 = 0
    correct_kana = 0
    correct_num2 = 0
    correct_all  = 0
    bad_area = []
    bad_area_p = []
    bad_num1 = []
    bad_kana = []
    bad_num2 = []
    bad_area_pos = []
    bad_num1_pos = []
    bad_kana_pos = []
    bad_num2_pos = []
    process_time    = 0
    pre_time        = 0
    split_time      = 0
    area_time       = 0
    num1_time       = 0
    kana_time       = 0
    num2_time       = 0

    print(file_path_list)
    for index, path in enumerate(file_path_list):
        print(str(index) + "/" + str(len(file_path_list)))
        pil_img = Image.open(path)
        img = np.array(pil_img, dtype=np.uint8)
        # img = cv2.resize(img, (500, 500))
        results, processing_times = npr.number_plate_recognize(img)
        area = 0
        num1 = 0
        kana = 0
        num2 = 0

        #areaの正誤判定
        if results['area'][0] == ta.annotation[index][0]:
            correct_area += 1
            area = 1
        else:
            area = 0
            bad_area.append(index)
            bad_area_p.append(int(results['area'][1]))
            bad_area_pos.append("\n".join(difflib.ndiff(ta.annotation[index][0], results["area"][0])))
        #num1の正誤判定
        if results['num1'] == ta.annotation[index][1]:
            correct_num1 += 1
            num1 = 1
        else:
            num1 = 0
            bad_num1.append(index)
            bad_num1_pos.append("\n".join(difflib.ndiff(ta.annotation[index][1], results["num1"])))
        #kanaの正誤判定
        if results['kana'] == ta.annotation[index][2]:
            correct_kana += 1
            kana = 1
        else:
            kana = 0
            bad_kana.append(index)
            bad_kana_pos.append("\n".join(difflib.ndiff(ta.annotation[index][2], results["kana"])))
        #num2の正誤判定
        if results['num2'] == ta.annotation[index][3]:
            correct_num2 += 1
            num2 = 1
        else:
            num2 = 0
            bad_num2.append(index)
            bad_num2_pos.append("\n".join(difflib.ndiff(ta.annotation[index][3], results["num2"])))
        if area * num1 * kana * num2:
            correct_all += 1

    print("TEST SET DIRECTORY------------------------------")
    print(f"{file_path_list[0].split('/')[-2]}")
    print("ACCURACY------------------------------")
    print("accuracy of all | {:.2f}%".format(correct_all / len(file_path_list) * 100))
    print("accuracy of area| {:.2f}%".format(correct_area / len(file_path_list) * 100))
    print("accuracy of num1| {:.2f}%".format(correct_num1 / len(file_path_list) * 100))
    print("accuracy of kana| {:.2f}%".format(correct_kana / len(file_path_list) * 100))
    print("accuracy of num2| {:.2f}%".format(correct_num2 / len(file_path_list) * 100))

    #精度を追記
    with open('./test_dark_log_acc.txt', 'a') as f_acc:
    # with open('./test_dark_top_log_acc.txt', 'a') as f_acc:
        print('{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}'.format(
            dark,
            correct_all / len(file_path_list) * 100,
            correct_area / len(file_path_list) * 100,
            correct_num1 / len(file_path_list) * 100,
            correct_kana / len(file_path_list) * 100,
            correct_num2 / len(file_path_list) * 100
        ), file=f_acc)