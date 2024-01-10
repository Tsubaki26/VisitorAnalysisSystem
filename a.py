import glob
import cv2

files = glob.glob('./images/test_images_2/*.jpg')
size_list = []
for i in files:
    img = cv2.imread(i)
    if img.shape[0] > img.shape[1]:
        size_list.append(img.shape[1])
    else:
        size_list.append(img.shape[0])

print(size_list)
print(sum(size_list) / len(files))