import cv2
img = cv2.imread('./hiroshima.png')
img_h = img.shape[0]
img_w = img.shape[1]
img_small = cv2.resize(img, (int(img_w / 5), int(img_h / 5)), interpolation=cv2.INTER_NEAREST)
img_2 = cv2.resize(img_small, (img_w, img_h), interpolation=cv2.INTER_NEAREST)
# img_underline = cv2.line(img, (0,img_h), (img_w,img_h), color=(0,0,0), thickness=5)
img_sideline = cv2.line(img, (0,0), (0,img_h), color=(0,0,0), thickness=5)
cv2.imshow("img", img)
cv2.imshow("img_small", img_small)
cv2.imshow("img_2", img_2)
# cv2.imshow("img_line", img_underline)
cv2.imshow("img_line2", img_sideline)

cv2.waitKey()