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


file_path_list = []
files = glob.glob('./images/test_images_2/*.jpg')
for i in natsort.natsorted(files):
    file_path_list.append(i)

for size in range(40, 250, 10):
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
        results, processing_times = npr.number_plate_recognize(img, img_width=size*2, img_height=size)
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

        pre_time += processing_times['pre_time']
        split_time += processing_times['split_time']
        area_time += processing_times['area_time']
        num1_time += processing_times['num1_time']
        kana_time += processing_times['kana_time']
        num2_time += processing_times['num2_time']
        process_time += processing_times['process_time']
        print("==============")
        print("処理時間｜{} s".format(processing_times['process_time']))
        print("==============\n")

    print("TEST SET DIRECTORY------------------------------")
    print(f"{file_path_list[0].split('/')[-2]}")
    print("ACCURACY------------------------------")
    print("accuracy of all | {:.2f}%".format(correct_all / len(file_path_list) * 100))
    print("accuracy of area| {:.2f}%".format(correct_area / len(file_path_list) * 100))
    print("accuracy of num1| {:.2f}%".format(correct_num1 / len(file_path_list) * 100))
    print("accuracy of kana| {:.2f}%".format(correct_kana / len(file_path_list) * 100))
    print("accuracy of num2| {:.2f}%".format(correct_num2 / len(file_path_list) * 100))

    print("TIME----------------------------------")
    print("average of all process time\t| {:.4f}".format(process_time / len(file_path_list)))
    print("average of preprocessing time\t| {:.4f}".format(pre_time / len(file_path_list)))
    print("average of split time\t\t| {:.4f}".format(split_time / len(file_path_list)))
    print("average of area time\t\t| {:.4f}".format(area_time / len(file_path_list)))
    print("average of num1 time\t\t| {:.4f}".format(num1_time / len(file_path_list)))
    print("average of kana time\t\t| {:.4f}".format(kana_time / len(file_path_list)))
    print("average of num2 time\t\t| {:.4f}".format(num2_time / len(file_path_list)))

    #精度を追記
    with open('./test_size_log_acc.txt', 'a') as f_acc:
        print('{},{:.2f},{:.2f},{:.2f},{:.2f},{:.2f}'.format(
            size,
            correct_all / len(file_path_list) * 100,
            correct_area / len(file_path_list) * 100,
            correct_num1 / len(file_path_list) * 100,
            correct_kana / len(file_path_list) * 100,
            correct_num2 / len(file_path_list) * 100
        ), file=f_acc)

    #処理時間を追記
    with open('./test_size_log_time.txt', 'a') as f_time:
        print('{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}'.format(
            size,
            process_time / len(file_path_list),
            pre_time / len(file_path_list),
            split_time / len(file_path_list),
            area_time / len(file_path_list),
            num1_time / len(file_path_list),
            kana_time / len(file_path_list),
            num2_time / len(file_path_list)
        ), file=f_time)