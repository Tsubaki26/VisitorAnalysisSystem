import cv2
import numpy as np
from PIL import Image
import glob
import natsort
import random
import sys


def write(images, name, path):
    for index, img in enumerate(images):
        cv2.imwrite('{}_{}_{}.jpg'.format(path,name,index), img)

def get_file(path):
    file_path_list = []
    files = glob.glob(f'{path}/*.jpg')
    # print(files)
    for i in natsort.natsorted(files):
        file_path_list.append(i)
    return file_path_list


dir_path = '../images/yolo_datasets/license_plate/images'
# file_name = get_file(dir_path)[0]
# area = file_name.split('/')[-1].split('.')[0]   #kanaを取得
# print(area)


"""左右反転"""
file_path_list = get_file(dir_path)
images = []
for i in file_path_list:
    pil_img = Image.open(i)
    # pil_img = pil_img.convert('L')
    original_img = np.array(pil_img)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    # print(original_img.shape)
    images.append(cv2.flip(original_img, 1))
write(images, 'flip', i)
images = []

# """歪み"""
# #透視変換を用いている
# file_path_list = get_file(dir_path)
# images = []
# for i in file_path_list:
#     pil_img = Image.open(i)
#     # pil_img = pil_img.convert('L')
#     original_img = np.array(pil_img)
#     original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
#     img_w = original_img.shape[1]
#     img_h = original_img.shape[0]
#     sumimg = original_img/255.0
#     d_level = 5
#     for j in range(100):
#         pts1 = np.float32([[0,0],[0,img_h],[img_w,img_h],[img_w,0]])
#         pts2 = np.float32([[random.randint(-d_level, d_level),random.randint(-d_level, d_level)],
#                         [random.randint(-d_level,d_level), img_h+random.randint(-d_level,d_level)],
#                         [img_w+random.randint(-d_level,d_level),img_h+random.randint(-d_level,d_level)],
#                         [img_w+random.randint(-d_level,d_level), random.randint(-d_level,d_level)]])
#         M = cv2.getPerspectiveTransform(pts1, pts2)
#         dst = cv2.warpPerspective(original_img, M, (img_w,img_h),borderValue=255)
#         images.append(dst)
# write(images, 'distortion', i)
# images = []


"""回転"""
file_path_list = get_file(dir_path)
images = []
for i in file_path_list:
    pil_img = Image.open(i)
    # pil_img = pil_img.convert('L')
    original_img = np.array(pil_img)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
    height, width = original_img.shape[:2]
    center = (width/2, height/2)
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=-20, scale=1)
    images.append(cv2.warpAffine(src=original_img, M=rotate_matrix, dsize=(width, height), borderValue=0))
    rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=-30, scale=1)
    images.append(cv2.warpAffine(src=original_img, M=rotate_matrix, dsize=(width, height), borderValue=0))
write(images, 'rot', i)
images = []

