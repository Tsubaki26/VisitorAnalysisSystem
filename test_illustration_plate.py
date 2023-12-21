import cv2
import numpy as np
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
