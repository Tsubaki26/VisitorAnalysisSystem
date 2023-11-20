from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import cv2
import numpy as np
from matplotlib import pyplot as plt
# from test_data import test_annotation as ta
from test_data import test_annotation2 as ta
import glob
import natsort
import difflib
import time

#自作ライブラリ
# from recognition.NPrecognition_v3 import number_plate_recognize
# from recognition.NPrecognition_v3 import number_plate_recognize
from recognition import NPrecognition_v3 as npr


file_path_list = []
# files = glob.glob('./images/test_images/*.jpg')
files = glob.glob('./images/test_images_2/*.jpg')
for i in natsort.natsorted(files):
    file_path_list.append(i)

correct_area = 0
correct_num1 = 0
correct_kana = 0
correct_num2 = 0
correct_all  = 0
bad_area = []
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
    # if index != 17:
    #     continue
    print(str(index) + "/" + str(len(file_path_list)))
    # img = cv2.imread(path)
    pil_img = Image.open(path)
    img = np.array(pil_img, dtype=np.uint8)
    img = cv2.resize(img, (500, 200))
    # pil_img = Image.open(path)
    # cv2_img = np.array(pil_img, dtype=np.uint8)
    # results, p_time, s_time, a_time, n1_time, k_time, n2_time, pros_time = number_plate_recognize(cv2_img)
    # cv2.imshow("",img)
    # cv2.waitKey()
    # print(f"SHEPEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE, {img.shape}")
    results, p_time, s_time, a_time, n1_time, k_time, n2_time, pros_time = npr.number_plate_recognize(img)
    area = 0
    num1 = 0
    kana = 0
    num2 = 0

    #areaの正誤判定
    if results['area'] == ta.annotation[index][0]:
        correct_area += 1
        area = 1
        print("good!!!!!!!!!!!!!!!!!!")
    else:
        area = 0
        bad_area.append(index)
        bad_area_pos.append("\n".join(difflib.ndiff(ta.annotation[index][0], results["area"])))
    #num1の正誤判定
    if results['num1'] == ta.annotation[index][1]:
        correct_num1 += 1
        num1 = 1
        print("good!!!!!!!!!!!!!!!!!!")
    else:
        num1 = 0
        bad_num1.append(index)
        bad_num1_pos.append("\n".join(difflib.ndiff(ta.annotation[index][1], results["num1"])))
    #kanaの正誤判定
    if results['kana'] == ta.annotation[index][2]:
        correct_kana += 1
        kana = 1
        print("good!!!!!!!!!!!!!!!!!!")
    else:
        kana = 0
        bad_kana.append(index)
        bad_kana_pos.append("\n".join(difflib.ndiff(ta.annotation[index][2], results["kana"])))
    #num2の正誤判定
    if results['num2'] == ta.annotation[index][3]:
        correct_num2 += 1
        num2 = 1
        print("good!!!!!!!!!!!!!!!!!!")
    else:
        num2 = 0
        bad_num2.append(index)
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',results["num2"])
        bad_num2_pos.append("\n".join(difflib.ndiff(ta.annotation[index][3], results["num2"])))
    if area * num1 * kana * num2:
        correct_all += 1

    pre_time += p_time
    split_time += s_time
    area_time += a_time
    num1_time += n1_time
    kana_time += k_time
    num2_time += n2_time
    process_time += pros_time
    print("==============")
    print("処理時間｜{} s".format(pros_time))
    print("==============")

print("ACCURACY------------------------------")
print("accuracy of all | {}%".format(correct_all / len(file_path_list) * 100))
print("accuracy of area| {}%".format(correct_area / len(file_path_list) * 100))
print("accuracy of num1| {}%".format(correct_num1 / len(file_path_list) * 100))
print("accuracy of kana| {}%".format(correct_kana / len(file_path_list) * 100))
print("accuracy of num2| {}%".format(correct_num2 / len(file_path_list) * 100))

print("TIME----------------------------------")
print("average of all process time\t| {:.4f}".format(process_time / len(file_path_list)))
print("average of preprocessing time\t| {:.4f}".format(pre_time / len(file_path_list)))
print("average of split time\t\t| {:.4f}".format(split_time / len(file_path_list)))
print("average of area time\t\t| {:.4f}".format(area_time / len(file_path_list)))
print("average of num1 time\t\t| {:.4f}".format(num1_time / len(file_path_list)))
print("average of kana time\t\t| {:.4f}".format(kana_time / len(file_path_list)))
print("average of num2 time\t\t| {:.4f}".format(num2_time / len(file_path_list)))


print("BAD RECOGNITION INDEX-----------------")
print("areaを誤認識した画像: {}".format(bad_area))
# for i in bad_area_pos:
#     print("==============")
#     print(i)

print("num1を誤認識した画像: {}".format(bad_num1))


# for i in bad_num1_pos:
#     print("==============")
#     print(i)
print("kanaを誤認識した画像: {}".format(bad_kana))
# for i in bad_kana_pos:
#     print("==============")
#     print(i)

print("num2を誤認識した画像: {}".format(bad_num2))
# for i in bad_num2_pos:
#     print("==============")
#     print(i)
