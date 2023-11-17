#標準ライブラリ
import time
import sys

#外部ライブラリ
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#自作ライブラリ
from MyLibrary.preprocessing import preprocessing
import MyLibrary.split_histgram as his
import MyLibrary.split_hough as hough
import MyLibrary.rc_num as rc_num
import MyLibrary.rc_kana as rc_kana
import MyLibrary.rc_area as rc_area
import MyLibrary.denoise as denoise
# import MyLibrary.ocr as ocr
from test_data import test_annotation as ta


#画像ファイルのパスを指定
file_path = "./images/test_kei/test_10.jpg"

img = cv2.imread(file_path)                                             #画像読み込み

def number_plate_recognize(img):
    start_time = time.time()
    results = {
        'area':'',
        'num1':'',
        'kana':'',
        'num2':''
    }

    #正規化の際の画像サイズを設定
    img_width = 240
    img_height = 120
    pre_start_time = time.time()
    original_img, img_th, img_erode = preprocessing(img, img_width=img_width, img_height=img_height)    #前処理
    pre_end_time = time.time()
    # cv2.imshow("",original_img)
    # cv2.waitKey()

    #*ヒストグラム法による画像分割
    split_start_time = time.time()
    r_hist, c_hist, r_top_index, r_index, r_bottom_index, left1_index, left_index, right_index = his.find_split_point(img_erode)                        #分割位置の特定
    print("aaaa", r_bottom_index)
    #ヒストグラムを出力
    his.draw_hist_2(img_th, r_hist, c_hist, r_top_index, r_index, r_bottom_index, left1_index, left_index, right_index)                                #ヒストグラムの表示
    kana_img = his.split(original_img, left1_index, r_index, left_index, r_bottom_index)                        #かなを切り抜く
    num2_img = his.split(original_img, left_index, r_index, img.shape[1], r_bottom_index)          #下数字を切り抜く
    area_num_img = his.split(original_img, left_index, r_top_index, right_index, r_index)                    #地域・上数字を切り抜く
    # cv2.imshow("area&num1",area_num_img)
    # cv2.waitKey()
    # cv2.imshow("",num2_img)
    # cv2.waitKey()
    kernel = np.ones((2,2), np.uint8)
    area_num_img_th = cv2.adaptiveThreshold(area_num_img,
                                        255,
                                        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY,
                                        31, 30)
    area_num_img_erode = cv2.erode(area_num_img_th, kernel, iterations=2)
    c_hist, left_index = his.find_split_point_top(area_num_img_erode, 0.55, 0.65)
    #ヒストグラムを出力
    #! his.draw_hist_1(area_num_img, c_hist, left_index)
    area_img = his.split(area_num_img, 0, 0, left_index, area_num_img.shape[0])
    num1_img = his.split(area_num_img_th, left_index+1, 0, area_num_img.shape[1], area_num_img.shape[0])
    original_num1_img = num1_img
    cv2.imwrite('./images/output_images/num1.jpg', original_num1_img)
    split_end_time = time.time()


    #*地域の処理（未完成）
    area_start_time = time.time()
    kernel = np.ones((2,2), np.uint8)
    area_img = cv2.erode(area_img, kernel, iterations=2)
    area_img = cv2.cvtColor(area_img, cv2.COLOR_GRAY2BGR)
    results['area'] = rc_area.rc_area(area_img)
    area_end_time = time.time()
    print(results['area'])

    #*上数字の処理
    #まだアルファベットには対応していない
    num1_start_time = time.time()
    # cv2.imshow("num1",num1_img)
    # cv2.waitKey()
    sp_img_list = hough.split(num1_img)                      #ハフ変換により数字を分割
    hough.draw_images(sp_img_list, 'num1_split')                              #分割結果の表示
    result_num1 = ""
    acc_result_list = []
    for img in sp_img_list:
        # cv2.imshow("", img)
        # cv2.waitKey()
        # img = cv2.erode(img, kernel, iterations=1)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("num1",img)
        # cv2.waitKey()
        result, acc_result = rc_num.rc_num(img)
        result_num1 += str(result)
        acc_result_list.append(np.max(acc_result))
    results['num1'] = result_num1
    num1_end_time = time.time()
    print(results['num1'])

    #*かなの処理
    kana_start_time = time.time()
    # cv2.imshow("",kana_img)
    # cv2.waitKey()
    # kernel = np.ones((2,2), np.uint8)
    # kana_img = cv2.dilate(kana_img, kernel, iterations=2) #文字を細くする
    # kana_img = denoise.denoise(kana_img, 0.3,0.8,0.2,0.8)
    kana_img = cv2.adaptiveThreshold(kana_img,
                                255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,
                                31, 30)
    #幅10の余白を追加
    padding_side = int((kana_img.shape[0]-kana_img.shape[1])/2)
    kana_img = cv2.copyMakeBorder(kana_img,0,0,padding_side,padding_side,cv2.BORDER_CONSTANT,value=[255,255,255])
    # cv2.imshow("",kana_img)
    # cv2.waitKey()
    # kana_img=cv2.resize(kana_img, (54, 54))
    # cv2.imshow("denoised", kana_img)
    # cv2.waitKey()
    kana_img = cv2.cvtColor(kana_img, cv2.COLOR_GRAY2BGR)
    results['kana'] = rc_kana.rc_kana(kana_img)
    kana_end_time = time.time()
    print(results['kana'])

    #*下数字の処理
    # cv2.imshow("num2",num2_img)
    # cv2.waitKey()
    num2_start_time = time.time()
    original_num2_img = num2_img
    num2_img = cv2.adaptiveThreshold(num2_img,
                                255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,
                                71, 30)
    # kernel = np.ones((2,2), np.uint8)
    # num2_img = cv2.dilate(num2_img, kernel, iterations=2) #文字を細くする
    # his.find_split_point_number(num2_img)
    # cv2.imshow("",num2_img)
    # cv2.waitKey()
    sp_img_list = hough.split(num2_img)                      #ハフ変換により数字を分割
    #! hough.draw_images(sp_img_list, 'num2_split')                              #分割結果の表示
    result_num2 = ""
    acc_result_list = []
    print("list len", len(sp_img_list))
    for img in sp_img_list:
        # result_num2 = result_num2 + str(rc_num.rc_num(img))
        # img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        # cv2.imshow("", img)
        # cv2.waitKey()
        result, acc_result = rc_num.rc_num(img)
        # cv2.imshow("num2",img)
        # cv2.waitKey()
        print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ")
        result_num2 = result_num2 + str(result)
        acc_result_list.append(np.max(acc_result))
    # result_num2 = rc_num.rc_num_list(sp_img_list)
    print("kekkaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",result_num2)
    #出力の修正
    if len(result_num2) == 4:
        temp = ''
        for index, i in enumerate(result_num2):
            temp = temp + i
            if index == 1:
                temp = temp + '-'
        result_num2 = temp
    elif len(result_num2) < 4:
        while len(result_num2) < 4:
            result_num2 = '・' + result_num2
    results['num2'] = result_num2
    num2_end_time = time.time()
    print(results['num2'])
    end_time = time.time()


    #?出力####################################################################
    #画像を出力
    cv2.imwrite('./images/output_images/area&num1.jpg', area_num_img)
    cv2.imwrite('./images/output_images/kana.jpg', kana_img)
    cv2.imwrite('./images/output_images/num2.jpg', num2_img)
    cv2.imwrite('./images/output_images/area.jpg', area_img)
    # cv2.imwrite('./output_images/num1.jpg', original_num1_img)

    pre_time = pre_end_time - pre_start_time
    split_time = split_end_time - split_start_time
    area_time = area_end_time - area_start_time
    num1_time = num1_end_time - num1_start_time
    num2_time = num2_end_time - num2_start_time
    kana_time = kana_end_time - kana_start_time
    process_time = end_time - start_time

    img_index = int(file_path.split('/')[-1].split('_')[1].split('.')[0])
    print(file_path)
    print(img_index)
    ans_area = ta.annotation[img_index][0]
    ans_num1 = ta.annotation[img_index][1]
    ans_kana = ta.annotation[img_index][2]
    ans_num2 = ta.annotation[img_index][3]

    print("\n=================")
    print(f"|result\t|")
    print(f"| {results['area']} {results['num1']}\t|")
    print(f"| {results['kana']} {results['num2']}\t|")
    print("===================")
    print(f"preprocess time\t\t| {pre_time:.4f}s")
    print(f"histgram split time\t| {split_time:.4f}s")
    print(f"area recognition time\t| {area_time:.4f}s")
    print(f"num1 recognition time\t| {num1_time:.4f}s")
    print(f"kana recognition time\t| {kana_time:.4f}s")
    print(f"num2 recognition time\t| {num2_time:.4f}s")
    print("=================================")
    print(f"process time\t\t| {process_time:.4f}s\n")

    return results, pre_time, split_time, area_time, num1_time, kana_time, num2_time, process_time

if __name__ == '__main__':
    number_plate_recognize(img)