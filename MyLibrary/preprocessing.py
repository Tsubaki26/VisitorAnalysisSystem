import cv2
import numpy as np

#前処理
def preprocessing(img, img_width, img_height):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("gray",img)
    # cv2.waitKey()
    img = cv2.resize(img, (img_width, img_height))
    # img_cont = cv2.convertScaleAbs(img, alpha=1.5, beta=1)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_cont = clahe.apply(img)

    # cv2.imshow("",img_cont)
    # cv2.waitKey()

    kernel = np.ones((2,2), np.uint8)

    original_img = img_cont
    img_th = cv2.adaptiveThreshold(img_cont,
                                255,
                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY,
                                51, 30)
    # cv2.imshow("",img_th)
    # cv2.waitKey()
    # cv2.imshow("",img_erode)
    # cv2.waitKey()

    # 水平方向の黒ピクセル数を計算
    img_erode = cv2.erode(img_th, kernel, iterations=2)
    black_pixel_count_horizontal = np.sum(img_erode == 0, axis=1)
    black_pixel_count_vertical = np.sum(img_erode==0, axis=0)
    # 画像幅の8割以上の行が黒ピクセル数であれば白で染める
    threshold_h = int(0.6 * img_width)
    threshold_v = int(0.8 * img_height)
    for i in range(img_height):
        if black_pixel_count_horizontal[i] >= threshold_h:
            img_th[i, :] = 255
            img_erode[i, :] = 255
    # for i in range(img_height):
    #     if black_pixel_count_vertical[i] >= threshold_v:
    #         img_th[:, i] = 255
    # cv2.imshow("",img_erode)
    # cv2.waitKey()

    return original_img, img_th, img_erode