import cv2
import numpy as np
<<<<<<< HEAD
import copy

# for i in range(12):
#     image = cv2.imread(f'./images/gotouchi/test{i+1}.jpg')
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # image_2 = image - 75 #色の数字はループしていた．６０を足すと文字だけ真っ白になる．
#     # threshold_value = 190
#     # _, thresholded_image = cv2.threshold(image_2, threshold_value, 255, cv2.THRESH_BINARY)
#     # image_3 = 255 - thresholded_image

#     _, image_3 = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)
#     # image_3 = 255 - thresholded_image

#     cv2.imshow("original", image)
#     cv2.imshow("image3", image_3)
=======
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

# image = cv2.imread(f'./images/test_images_2/test_6.jpg')
# hsvimage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# h, s, v = cv2.split(hsvimage)
# print(h)

# cv2.imshow("original", image)
# cv2.imshow("hsv", hsvimage)
# cv2.imshow("h", h)


# cv2.waitKey()


for i in range(12):
    # image = cv2.imread(f'./images/gotouchi/test{i+1}.jpg')
    image = cv2.imread(f'./images/test_images_2/test_{i+1}.jpg')
    imagegray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image ?= image.astype(np.uint1?)
    # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    # image_k = clahe.apply(image)

    # image2 = cv2.convertScaleAbs(image, alpha=2, beta=50)

    img_b, img_g, img_r = cv2.split(image)

    # Add required value
    img_b = cv2.add(img_b, img_b)
    img_g = cv2.add(img_g, img_g)
    img_r = cv2.add(img_r, img_r)

    # Merge each cannels
    image2 = cv2.merge([img_b, img_g, img_r])

    image2 = cv2.add(image, 50)

    image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image_3 = cv2.threshold(image2, 70, 255, cv2.THRESH_BINARY)

    # cv2.imshow("k", image_k)
    cv2.imshow("original", imagegray)
    cv2.imshow("aaa", image2)
    cv2.imshow("image3", image_3)
>>>>>>> 2493c5d149d14ad5405f9eb5c1a4bdd5b7aa266e

#     cv2.waitKey()

# image = cv2.imread(f'./images/test_images_2/test_2.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # image_2 = image - 75 #色の数字はループしていた．６０を足すと文字だけ真っ白になる．
# # threshold_value = 190
# # _, thresholded_image = cv2.threshold(image_2, threshold_value, 255, cv2.THRESH_BINARY)
# # image_3 = 255 - thresholded_image

# _, image_3 = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

# cv2.imshow("image3", image_3)

# cv2.waitKey()

def toDark_top(image, a):
    # result = np.zeros(image.shape)
    # print(result.shape)
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
    # result = np.zeros(image.shape)
    # print(result.shape)
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
    # result = np.zeros(image.shape)
    # print(result.shape)
    result = copy.deepcopy(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                if image[i][j][k] + a <= 255:
                    result[i][j][k] = image[i][j][k] + a
                else:
                    result[i][j][k] = 255
    return result

for i in range(20):
    # image = cv2.imread(f'./images/gotouchi/test{i+1}.jpg')
    image = cv2.imread(f'./images/test_images_2/test_{i}.jpg')

    image_2 = toDark_all(image, 50)
    image_2_2 = toDark_top(image_2, 50)
    image_l = toLight(image, 50)


    cv2.imshow("original", image)
    cv2.imshow("image2", image_2)
    cv2.imshow("image2_2", image_2_2)
    cv2.imshow("light", image_l)

    cv2.waitKey()
