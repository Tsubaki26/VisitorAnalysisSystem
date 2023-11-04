import cv2
from PIL import Image
import numpy as np

pil_img = Image.open('./others_folder/testFolder/cell_0.png')
pil_img = pil_img.convert('L')
original_img = np.array(pil_img)
original_img = cv2.resize(original_img, (54,54))
h,w=original_img.shape[:2]
row,col = original_img.shape

pts_x = np.random.randint(0, col-1 , 50)
pts_y = np.random.randint(0, row-1 , 50)
original_img[(pts_y,pts_x)] = 0
cv2.imwrite('./others_folder/timage.png', original_img)