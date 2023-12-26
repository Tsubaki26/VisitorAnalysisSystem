import cv2
import copy
import glob
import natsort


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

file_path_list = []
files = glob.glob('./../images/test_images_2/*')
for i in natsort.natsorted(files):
    file_path_list.append(i)

count = 0

dirname = 'test_images_2_light'
for image_path in file_path_list:
    image = cv2.imread(image_path)

    # image_dark_all_50 = toDark_all(image, 70)
    
    # image_dark_top = toDark_top(image, 50)
    # image_dark_all_top = toDark_top(image_dark_all, 30)
    image_light = toLight(image, 40)

    # save_img(image)
    # save_img(image_dark_all_50,dirname)
    # save_img(image_dark_top,dirname)
    # save_img(image_dark_all_top)
    save_img(image_light,dirname)
