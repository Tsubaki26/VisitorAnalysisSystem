import cv2
import copy
import glob
import natsort
import sys


def toDark_top(image, a):
    result = copy.deepcopy(image)
    for i in range(image.shape[0]):
        if i > image.shape[0] * 0.3:
            break
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                if image[i][j][k] - a >= 0:
                    result[i][j][k] = image[i][j][k] - a
                else:
                    result[i][j][k] = 0
    return result

def toDark_all(image, a):
    result = copy.deepcopy(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                if image[i][j][k] - a >= 0:
                    result[i][j][k] = image[i][j][k] - a
                else:
                    result[i][j][k] = 0
    return result

def toLight(image, a):
    result = copy.deepcopy(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                if image[i][j][k] + a <= 255:
                    result[i][j][k] = image[i][j][k] + a
                else:
                    result[i][j][k] = 255
    return result

def save_img(image, dir_name):
    global count
    cv2.imwrite(f"./../images/{dir_name}/test_{count}.jpg", image)
    count += 1

# img = cv2.imread("./../aaa.jpg")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.adaptiveThreshold(img,
#                                 255,
#                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                 cv2.THRESH_BINARY,
#                                 51, 30)
# img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
# img_2 = toDark_all(img, 130)
# img_3 = cv2.adaptiveThreshold(cv2.cvtColor(img_2, cv2.COLOR_RGB2GRAY),
#                                 255,
#                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                 cv2.THRESH_BINARY,
#                                 51, 30)
# cv2.imshow("", img)
# cv2.imshow("2", img_2)
# cv2.imshow("3", img_3)
# cv2.waitKey()
# sys.exit()

file_path_list = []
files = glob.glob('./../images/test_images_2/*')
for i in natsort.natsorted(files):
    file_path_list.append(i)

count = 0

dirname = 'dark/test_images_2_dark'
# dirname = 'dark_top/test_images_2_dark_top'
# dirname = 'light/test_images_2_light'

image_list = []
for image_path in file_path_list:
    image = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(img,
                                    255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY,
                                    51, 30)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    image_list.append(img)

for i in range(10, 240, 10):
    print(i)
    for image in image_list:
    # for image_path in file_path_list:
    #     image = cv2.imread(image_path)
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     image = cv2.adaptiveThreshold(image,
    #                                     255,
    #                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                     cv2.THRESH_BINARY,
    #                                     51, 30)
    #     image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # image_dark_all = toDark_all(image, 230)
        # cv2.imshow("",image_dark_all)
        # cv2.waitKey()
        # sys.exit()
        
        # image_dark_top = toDark_top(image, 50)
        # image_dark_all_top = toDark_top(image_dark_all, 30)
        # image_light = toLight(image, 40)

        # save_img(image)
        # save_img(image_dark_all,dirname)
        # save_img(image_dark_top,dirname)
        # save_img(image_dark_all_top)
        # save_img(image_light,dirname)

        image_dark_all = toDark_all(image, i)
        # image_dark_top = toDark_top(image, i)
        # image_light = toLight(image, i)
        
        # image_dark_top = toDark_top(image, 50)
        # image_dark_all_top = toDark_top(image_dark_all, 30)
        # image_light = toLight(image, 40)

        # save_img(image)
        save_img(image_dark_all,'{}_{}'.format(dirname,i))
        # save_img(image_dark_top,'{}_{}'.format(dirname,i))
        # save_img(image_light,'{}_{}'.format(dirname,i))