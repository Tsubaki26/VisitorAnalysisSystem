import cv2
import numpy as np

for i in range(12):
    image = cv2.imread(f'./images/gotouchi/test{i+1}.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # image_2 = image - 75 #色の数字はループしていた．６０を足すと文字だけ真っ白になる．
    # threshold_value = 190
    # _, thresholded_image = cv2.threshold(image_2, threshold_value, 255, cv2.THRESH_BINARY)
    # image_3 = 255 - thresholded_image

    _, image_3 = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)
    # image_3 = 255 - thresholded_image

    cv2.imshow("original", image)
    cv2.imshow("image3", image_3)

    cv2.waitKey()

# image = cv2.imread(f'./images/test_images_2/test_2.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# # image_2 = image - 75 #色の数字はループしていた．６０を足すと文字だけ真っ白になる．
# # threshold_value = 190
# # _, thresholded_image = cv2.threshold(image_2, threshold_value, 255, cv2.THRESH_BINARY)
# # image_3 = 255 - thresholded_image

# _, image_3 = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

# cv2.imshow("image3", image_3)

# cv2.waitKey()