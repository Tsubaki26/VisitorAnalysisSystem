import cv2
import numpy as np
from PIL import Image
import glob
import natsort
import random


def write(images, name, path, area):
    for index, img in enumerate(images):
        cv2.imwrite('{}/{}_{}{}.png'.format(path,area,name, str(index)), img)

def get_file(path):
    file_path_list = []
    files = glob.glob('{}/*.png'.format(path))
    # print(files)
    for i in natsort.natsorted(files):
        file_path_list.append(i)
    return file_path_list

img_w = 100
img_h = 50
# dir_list = glob.glob('./training/area_images/鳥取')    #フォルダパスを取得

# for dir_path in dir_list:
    # if len(get_file(dir_path)) > 1:
    #     continue
    # file_name = get_file(dir_path)[0]
    # area = file_name.split('/')[-1].split('.')[0]   #kanaを取得
    # print(area)
dir_path = './training/area_images/鳥取'
file_name = get_file(dir_path)[0]
area = file_name.split('/')[-1].split('.')[0]   #kanaを取得
print(area)

"""歪み"""
#透視変換を用いている
file_path_list = get_file(dir_path)
images = []
for i in file_path_list:
    pil_img = Image.open(i)
    pil_img = pil_img.convert('L')
    original_img = np.array(pil_img)
    original_img = cv2.resize(original_img, (img_w,img_h))
    sumimg = original_img/255.0
    d_level = 5
    for j in range(100):
        pts1 = np.float32([[0,0],[0,img_h],[img_w,img_h],[img_w,0]])
        pts2 = np.float32([[random.randint(-d_level, d_level),random.randint(-d_level, d_level)],
                        [random.randint(-d_level,d_level), img_h+random.randint(-d_level,d_level)],
                        [img_w+random.randint(-d_level,d_level),img_h+random.randint(-d_level,d_level)],
                        [img_w+random.randint(-d_level,d_level), random.randint(-d_level,d_level)]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(original_img, M, (img_w,img_h),borderValue=255)
        images.append(dst)
write(images, 'distortion', dir_path, area)
images = []

"""膨張と縮小"""
file_path_list = get_file(dir_path)
images = []
for i in file_path_list:
    pil_img = Image.open(i)
    pil_img = pil_img.convert('L')
    original_img = np.array(pil_img)
    original_img = cv2.resize(original_img, (img_w,img_h))
    images.append(cv2.dilate(original_img, kernel=(3,3), iterations=2))
    images.append(cv2.erode(original_img, kernel=(3,3), iterations=2))
write(images, 'ed', dir_path, area)
images = []

"""回転"""
# file_path_list = get_file(dir_path)
# images = []
# for i in file_path_list:
#     pil_img = Image.open(i)
#     pil_img = pil_img.convert('L')
#     original_img = np.array(pil_img)
#     original_img = cv2.resize(original_img, (img_w,img_h))
#     height, width = original_img.shape[:2]
#     center = (width/2, height/2)
#     rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=10, scale=1)
#     images.append(cv2.warpAffine(src=original_img, M=rotate_matrix, dsize=(width, height), borderValue=255))
#     rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=-10, scale=1)
#     images.append(cv2.warpAffine(src=original_img, M=rotate_matrix, dsize=(width, height), borderValue=255))
# write(images, 'rot', dir_path, area)
# images = []

"""ぼかし"""
file_path_list = get_file(dir_path)
images = []
for i in file_path_list:
    pil_img = Image.open(i)
    pil_img = pil_img.convert('L')
    original_img = np.array(pil_img)
    original_img = cv2.resize(original_img, (img_w,img_h))
    images.append(cv2.blur(original_img, (3,3)))
    images.append(cv2.blur(original_img, (7,7)))
    images.append(cv2.GaussianBlur(original_img, (7,7), 2))
    images.append(cv2.GaussianBlur(original_img, (9,9), 2))
write(images, 'blur', dir_path, area)
images = []

# """ノイズ"""
# file_path_list = get_file(dir_path)
# images = []
# for i in file_path_list:
#     pil_img = Image.open(i)
#     pil_img = pil_img.convert('L')
#     original_img = np.array(pil_img)
#     original_img = cv2.resize(original_img, (img_w,img_h))
#     noise_level = 50
#     noise_x = np.random.randint(0, img_w-1, noise_level)
#     noise_y = np.random.randint(0, img_h-1, noise_level)
#     original_img[(noise_y, noise_x)] = 100  #グレーのノイズ
#     images.append(original_img)
# write(images, 'noise', dir_path, area)
# images = []

"""欠損"""
# file_path_list = get_file(dir_path)
# images = []
# for i in file_path_list:
#     pil_img = Image.open(i)
#     pil_img = pil_img.convert('L')
#     original_img = np.array(pil_img)
#     original_img = cv2.resize(original_img, (img_w,img_h))
#     noise_level = 1000
#     noise_x = np.random.randint(0, img_w-1, noise_level)
#     noise_y = np.random.randint(0, img_h-1, noise_level)
#     original_img[(noise_y, noise_x)] = 255
#     images.append(original_img)
# write(images, 'loss', dir_path, area)
# images = []
